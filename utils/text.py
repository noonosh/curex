import yaml


def open_locale_file() -> None:
    global contents

    text_file = open('locale.yaml')
    contents = yaml.load(text_file, Loader=yaml.FullLoader)


def text(key: str):
    """
    Reads texts from locale.yaml file. Return the string of the given key.
    """
    return contents['texts'][key]


def button(key: str):
    """
    Reads texts from locale.yaml file. Return the string of the given key.
    """
    return contents['texts']['buttons'][key]


def custom(key: str):
    return contents[key]
