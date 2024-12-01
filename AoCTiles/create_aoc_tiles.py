"""
Author: LiquidFun
Source: https://github.com/LiquidFun/adventofcode

To use this script, you need to have a file named
"session.cookie" in the same folder as this script.

It should contain a single line, the "session" cookie
when logged in to https://adventofcode.com. Just
paste it in there.

Then install the requirements as listed in the requirements.txt:
    pip install -r requirements.txt

Then run the script:
    python create_aoc_tiles.py
"""
import functools
import itertools
import os
import re
from collections import namedtuple
from datetime import datetime, timedelta
from functools import cache
from pathlib import Path

import requests
import yaml
from PIL import Image, ImageColor
from PIL import ImageFont
from PIL.ImageDraw import ImageDraw

# The year and day pattern to detect directories. For example, if your day folders are
# called "day1" to "day25" then set the pattern to r"day\d{1,2}". The script extracts
# a number from the folder and tries to guess its day that way.
YEAR_PATTERN = r"ibidem/advent_of_code/y\d{4}$"
DAY_PATTERN = r"/dec\d{2}.py$"

# This results in the parent directory of the script directory, the year directories should be here
AOC_DIR = Path(__file__).absolute().parent.parent

# The directory where the image files for the tiles are stored. This should be committed to git.
# Year directories are created in this directory, then each day is saved as 01.png, 02.png, etc.
IMAGE_DIR = AOC_DIR / "Media"

# Path to the README file where the tiles should be added
README_PATH = AOC_DIR / "README.rst"

# Path to the README file where the tiles should be added
SESSION_COOKIE_PATH = AOC_DIR / "session.cookie"

# Whether the graphic should be created for days that have not been completed yet. Note that missing days between
# completed days will still be created.
CREATE_ALL_DAYS = False

# Instead of showing the time and rank you achieved this just shows whether
# it was completed with a checkmark
SHOW_CHECKMARK_INSTEAD_OF_TIME_RANK = False

# ======================================================
# === The following likely do not need to be changed ===
# ======================================================

# Color if a part is not completed
NOT_COMPLETED_COLOR = ImageColor.getrgb("#333333")

# Width of each tile in the README.md.
# 161px is a rather specific number, with it exactly 5 tiles fit into a row. It is possible to go
# to 162px, however then 1080p displays show 4 tiles in a row, and phone displays show 1 tile
# instead of 2 in a row. Therefore, 161px is used here.
TILE_WIDTH_PX = "161px"

# This results in the parent folder of the script file
AOC_TILES_SCRIPT_DIR = Path(__file__).absolute().parent

# Cache path is a subfolder of the AOC folder, it includes the personal leaderboards for each year
CACHE_DIR = AOC_TILES_SCRIPT_DIR / ".aoc_tiles_cache"

# Overrides day 24 part 2 and day 25 both parts to be unsolved
DEBUG = False

# URL for the personal leaderboard (same for everyone)
PERSONAL_LEADERBOARD_URL = "https://adventofcode.com/{year}/leaderboard/self"

# Location of yaml file where file extensions are mapped to colors
GITHUB_LANGUAGES_PATH = AOC_TILES_SCRIPT_DIR / "github_languages.yml"

# Image link in reStructuredText syntax, with placeholders
IMAGE_LINK = """
.. image:: {image_path}
   :width: {width}
   :target: {link}
"""


class InvalidLeaderboardFileException(Exception):
    pass


class MissingLeaderboardException(InvalidLeaderboardFileException):
    pass


class TooManyLeaderboardsException(InvalidLeaderboardFileException):
    pass


class InvalidNumberOfScoresException(InvalidLeaderboardFileException):
    pass


@cache
def get_font(size: int, path: str):
    return ImageFont.truetype(str(AOC_DIR / path), size)


# Fonts, note that the fonts sizes are specifically adjusted to the following fonts, if you change the fonts
# you might need to adjust the font sizes and text locations in the rest of the script.
main_font = functools.partial(get_font, path=AOC_TILES_SCRIPT_DIR / "fonts/PaytoneOne.ttf")
secondary_font = functools.partial(get_font, path=AOC_TILES_SCRIPT_DIR / "fonts/SourceCodePro-Regular.otf")

DayScores = namedtuple("DayScores", ["time1", "rank1", "score1", "time2", "rank2", "score2"], defaults=[None] * 3)


def get_extension_to_colors():
    extension_to_color = {}
    with open(GITHUB_LANGUAGES_PATH) as file:
        github_languages = yaml.load(file, Loader=yaml.FullLoader)
        for language, data in github_languages.items():
            if "color" in data and "extensions" in data and data["type"] == "programming":
                for extension in data["extensions"]:
                    extension_to_color[extension.lower()] = data["color"]
    return extension_to_color


extension_to_color: dict[str, str] = get_extension_to_colors()


def get_paths_matching_regex(path: Path, pattern: str):
    for dirpath, dirnames, filenames in os.walk(path):
        if "advent_of_code/." in dirpath: continue
        if re.search(pattern, str(dirpath)):
            yield Path(dirpath)
            continue
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if re.search(pattern, str(fpath)):
                yield fpath


def parse_leaderboard(leaderboard_path: Path) -> dict[str, DayScores]:
    no_stars = "You haven't collected any stars... yet."
    start = '<span class="leaderboard-daydesc-both"> *Time *Rank *Score</span>\n'
    end = "</pre>"
    with open(leaderboard_path) as file:
        html = file.read()
        if no_stars in html:
            return {}
        matches = re.findall(rf"{start}(.*?){end}", html, re.DOTALL | re.MULTILINE)
        if len(matches) == 0:
            raise MissingLeaderboardException(f"Expected 1 leaderboard, got {len(matches)}")
        if len(matches) > 1:
            raise TooManyLeaderboardsException(f"Expected 1 leaderboard, got {len(matches)}")
        table_rows = matches[0].strip().split("\n")
        leaderboard = {}
        for line in table_rows:
            day, *scores = re.split(r"\s+", line.strip())
            if not len(scores) in (3, 6):
                raise InvalidNumberOfScoresException(f"Number scores for {day=} ({scores}) are not 3 or 6.")
            leaderboard[day] = DayScores(*scores)
        return leaderboard


def request_leaderboard(year: int) -> dict[str, DayScores]:
    leaderboard_path = CACHE_DIR / f"leaderboard{year}.html"
    if leaderboard_path.exists():
        now = datetime.now()
        leaderboard_age = now - datetime.fromtimestamp(leaderboard_path.stat().st_mtime)
        if leaderboard_age < timedelta(minutes=10) or year < now.year:
            try:
                leaderboard = parse_leaderboard(leaderboard_path)
                has_no_none_values = all(itertools.chain(map(list, leaderboard.values())))
                if has_no_none_values:
                    return leaderboard
            except InvalidLeaderboardFileException:
                pass
    with open(SESSION_COOKIE_PATH) as cookie_file:
        session_cookie = cookie_file.read().strip()
        data = requests.get(PERSONAL_LEADERBOARD_URL.format(year=year), cookies={"session": session_cookie}).text
        leaderboard_path.parent.mkdir(exist_ok=True, parents=True)
        with open(leaderboard_path, "w") as file:
            file.write(data)
    return parse_leaderboard(leaderboard_path)


def darker_color(c: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return c[0] - 10, c[1] - 10, c[2] - 10, 255


def get_alternating_background(languages, both_parts_completed=True, *, stripe_width=20):
    colors = [ImageColor.getrgb(extension_to_color[language]) for language in languages]
    if len(colors) == 1:
        colors.append(darker_color(colors[0]))
    image = Image.new("RGB", (200, 100), NOT_COMPLETED_COLOR)

    def fill_with_colors(colors, fill_only_half):
        for x in range(image.width):
            for y in range(image.height):
                if fill_only_half and x / image.width + y / image.height > 1:
                    continue
                image.load()[x, y] = colors[((x + y) // stripe_width) % len(colors)]

    fill_with_colors([NOT_COMPLETED_COLOR, darker_color(NOT_COMPLETED_COLOR)], False)
    if colors:
        fill_with_colors(colors, not both_parts_completed)
    return image


def format_time(time: str) -> str:
    """Formats time as mm:ss if the time is below 1 hour, otherwise it returns >1h to a max of >24h"""
    time = time.replace("&gt;", ">")
    if ">" in time:
        formatted = time
    elif "-" in time:
        formatted = "---"
    else:
        h, m, s = time.split(":")
        formatted = f">{h}h" if int(h) >= 1 else f"{m:02}:{s:02}"
    return f"{formatted:>5}"


def generate_day_tile_image(day: str, year: str, languages: list[str], day_scores: DayScores | None) -> Path:
    """Saves a graphic for a given day and year. Returns the path to it."""
    image = get_alternating_background(languages, not (day_scores is None or day_scores.time2 is None))
    drawer = ImageDraw(image)
    font_color = "white"

    # === Left side ===
    drawer.text((3, -5), "Day", fill=font_color, align="left", font=main_font(20))
    drawer.text((1, -10), str(day), fill=font_color, align="center", font=main_font(75))
    # Calculate font size based on number of characters, because it might overflow
    lang_as_str = " ".join(languages)
    lang_font_size = max(6, int(18 - max(0, len(lang_as_str) - 8) * 1.3))
    drawer.text((0, 74), lang_as_str, fill=font_color, align="left", font=secondary_font(lang_font_size))

    # === Right side (P1 & P2) ===
    for part in (1, 2):
        y = 50 if part == 2 else 0
        time, rank = getattr(day_scores, f"time{part}", None), getattr(day_scores, f"rank{part}", None)
        if day_scores is not None and time is not None:
            drawer.text((104, -5 + y), f"P{part} ", fill=font_color, align="left", font=main_font(25))
            if SHOW_CHECKMARK_INSTEAD_OF_TIME_RANK:
                drawer.line((160, 35 + y, 150, 25 + y), fill=font_color, width=2)
                drawer.line((160, 35 + y, 180, 15 + y), fill=font_color, width=2)
                continue
            drawer.text((105, 25 + y), "time", fill=font_color, align="right", font=secondary_font(10))
            drawer.text((105, 35 + y), "rank", fill=font_color, align="right", font=secondary_font(10))
            drawer.text((143, 3 + y), format_time(time), fill=font_color, align="right", font=secondary_font(18))
            drawer.text((133, 23 + y), f"{rank:>6}", fill=font_color, align="right", font=secondary_font(18))
        else:
            drawer.line((140, 15 + y, 160, 35 + y), fill=font_color, width=2)
            drawer.line((140, 35 + y, 160, 15 + y), fill=font_color, width=2)

    if day_scores is None:
        drawer.line((15, 85, 85, 85), fill=font_color, width=2)

    # === Divider lines ===
    drawer.line((100, 5, 100, 95), fill=font_color, width=1)
    drawer.line((105, 50, 195, 50), fill=font_color, width=1)

    path = IMAGE_DIR / f"{year}/{day}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)
    return path


def handle_day(day: int, year: int, day_path: Path, content: list[str], day_scores: DayScores | None):
    languages = []
    solution_file_path = None
    if day_path is not None:
        if day_path.is_file():
            if day_path.suffix.lower() in extension_to_color:
                if solution_file_path is None:
                    solution_file_path = day_path.relative_to(AOC_DIR)
                languages.append(day_path.suffix.lower())
    languages = sorted(set(languages))
    if DEBUG:
        if day == 25:
            languages = []
    day_graphic_path = generate_day_tile_image(f"{day:02}", f"{year:04}", languages, day_scores)
    day_graphic_path = day_graphic_path.relative_to(AOC_DIR)

    day_content = IMAGE_LINK.format(link=str(solution_file_path), image_path=str(day_graphic_path), width=TILE_WIDTH_PX)
    content.append(day_content)


def find_first_number(string: str) -> int:
    return int(re.findall(r"\d+", string)[0])


def handle_year(year_path: Path, year: int):
    leaderboard = request_leaderboard(year)
    if DEBUG:
        leaderboard["25"] = None
        leaderboard["24"] = DayScores("22:22:22", "12313", "0")
    content = []

    # Add year header
    stars = sum((ds.time1 is not None) + (ds.time2 is not None) for ds in leaderboard.values() if ds is not None)
    title = f"{year} - {stars} ⭐"
    content.extend(("", title, "." * len(title.encode("utf-8"))))

    days_with_filled_gaps = {find_first_number(p.name): p for p in
                             sorted(get_paths_matching_regex(year_path, DAY_PATTERN))}
    if not CREATE_ALL_DAYS and len(days_with_filled_gaps) == 0:
        print(f"Year {year} is empty!")
        return
    max_day = 25 if CREATE_ALL_DAYS else max(*days_with_filled_gaps, *map(int, leaderboard))
    for day in range(1, max_day + 1):
        if day not in days_with_filled_gaps:
            days_with_filled_gaps[day] = None
    for day, day_path in days_with_filled_gaps.items():
        handle_day(day, year, day_path, content, leaderboard.get(str(day), None))

    rendered = "\n".join(content)
    with open(README_PATH, "r") as file:
        text = file.read()
        begin = f".. AOC TILES BEGIN - {year}"
        end = f".. AOC TILES END - {year}"
        pattern = re.compile(rf"{begin}.*{end}", re.DOTALL | re.MULTILINE)
        new_text = pattern.sub(f"{begin}\n{rendered}\n{end}", text)

    with open(README_PATH, "w") as file:
        file.write(str(new_text))


def main():
    for year_path in sorted(get_paths_matching_regex(AOC_DIR, YEAR_PATTERN), reverse=True):
        year = find_first_number(year_path.name)
        print(f"=== Generating table for year {year} ===")
        handle_year(year_path, year)


if __name__ == "__main__":
    main()
