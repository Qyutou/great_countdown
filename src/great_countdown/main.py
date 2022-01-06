import click
import time
import threading
import re


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


def parse_time_in_seconds(time_in_seconds):
    minutes, seconds = divmod(time_in_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    time_string = "%02d:%02d:%02d" % (hours, minutes, seconds)
    return time_string


def countdown_thread_method(countdown_total_time):

    countdown_total_time_parsed_into_groups = parse_input_time(countdown_total_time)
    countdown_total_time_in_seconds = parse_time_parsed_into_groups(countdown_total_time_parsed_into_groups)

    countdown_time_in_seconds = countdown_total_time_in_seconds
    is_time_passed = False

    while not is_time_passed:
        time_string = parse_time_in_seconds(countdown_time_in_seconds)
        click.clear()
        click.echo(time_string)
        countdown_time_in_seconds -= 1
        time.sleep(1)
        if countdown_time_in_seconds <= 0:
            is_time_passed = True


@click.command()
@click.argument("countdown_time")
def great_countdown(countdown_time):
    """Countdown"""
    countdown_thread = threading.Thread(target=countdown_thread_method(countdown_time))
    countdown_thread.start()


if __name__ == "__main__":
    main()
