import os
import random


def choose_random_file():
    """
    This function random choose template for letter

    :return: HTML markup
    """
    directory = "/Users/air/PycharmProjects/mail_service/api/templates"
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    random_file = random.choice(files)

    html_path = os.path.join(directory, random_file)

    with open(html_path, "r", encoding="utf-8") as file:
        html_file = file.read()

    return html_file
