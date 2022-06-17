import re


def extract_int_from_string(string):
    """
    Utlity function to extract an integer from a string 
    in order they appear in the string

    string: str – Input string

    Returns: List – array of all integers in the string
    """
    # Solution taken from
    # https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python

    pattern = '[\d]+[., \d]+|[\d]*[.][\d]+|[\d]+'
    array = []

    if re.search(pattern, string) is not None:
        for catch in re.finditer(pattern, string):
            array.append(int(catch[0]))  # catch is a match object

    return array


def format_currency(currency: int) -> str:
    return "{:,}".format(currency)
