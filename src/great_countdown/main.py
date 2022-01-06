import click
import time
import threading
import re
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def generate_color(color, foreground=True, background=True):
    text = ""

    if foreground:
        text += "\u001b[38;5;%dm" % color
    if background:
        text += "\u001b[48;5;%dm" % color

    return text


def print_text_to_graphics(text):
    click.echo(convert_text_to_graphics(text))


def convert_text_to_graphics(text):
    font = ImageFont.load_default()
    size = font.getsize(text)
    image = Image.new("1", size, "black")
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, "white", font=font)
    pixels = np.array(image, dtype=np.uint8)
    characters = np.array([' ', "0"])[pixels]
    strings = characters.view('U' + str(characters.shape[1])).flatten()
    result = "\n".join(strings)
    result = result.replace("0", "\033[47m\033[37m0\033[0m")
    return result


def parse_input_time(countdown_time):
    regex_pattern = r'([0-9]+[a-z])'
    parsed_into_groups = re.findall(regex_pattern, countdown_time)
    return parsed_into_groups


def parse_time_parsed_into_groups(time_parsed_into_groups):
    total_time_in_seconds = 0

    for group in time_parsed_into_groups:
        regex_pattern = r'([0-9]+)([a-z])'
        match = re.match(regex_pattern, group)
        if match is not None:
            value = int(match.group(1))
            modifier = str(match.group(2))
            if modifier == "s":
                total_time_in_seconds += value
            elif modifier == "m":
                total_time_in_seconds += value * 60
            elif modifier == "h":
                total_time_in_seconds += value * 60 * 60

    return total_time_in_seconds


def parse_time_in_seconds(time_in_seconds, with_separator=True):
    minutes, seconds = divmod(time_in_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if with_separator:
        time_string = "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        time_string = "%02d %02d %02d" % (hours, minutes, seconds)
    return time_string


def countdown_thread_method(countdown_total_time):

    countdown_total_time_parsed_into_groups = parse_input_time(countdown_total_time)
    countdown_total_time_in_seconds = parse_time_parsed_into_groups(countdown_total_time_parsed_into_groups)

    countdown_time_in_seconds = countdown_total_time_in_seconds
    is_time_passed = False

    while not is_time_passed:
        if countdown_time_in_seconds % 2 == 0:
            time_string = parse_time_in_seconds(countdown_time_in_seconds, with_separator=True)
        else:
            time_string = parse_time_in_seconds(countdown_time_in_seconds, with_separator=False)
        click.clear()
        print_text_to_graphics(time_string)
        countdown_time_in_seconds -= 1
        time.sleep(1)
        if countdown_time_in_seconds < 0:
            is_time_passed = True


@click.command()
@click.argument("countdown_time")
def great_countdown(countdown_time):
    """Countdown"""
    countdown_thread = threading.Thread(target=countdown_thread_method(countdown_time))
    countdown_thread.start()


if __name__ == "__main__":
    great_countdown()
