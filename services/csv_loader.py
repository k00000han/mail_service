import csv


async def get_emails(file) -> list:
    """
    This function will return a list of customer emails after upload file

    :param file: CSV with emails
    :return: list of customer emails
    """
    email_list = []

    content = await file.read()
    decoded_content = content.decode('utf-8')
    csv_reader = csv.reader(decoded_content.splitlines(), delimiter=',')

    for row in csv_reader:
        email_list.append(row[0])

    return email_list
