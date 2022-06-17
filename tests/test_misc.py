from utils.misc import extract_int_from_string, format_currency


def test_extract_int_from_string():
    test_strings = ['$1000', 'UZS 560000']
    expected_results = [1000, 560000]
    for i in range(len(test_strings)):
        assert extract_int_from_string(
            test_strings[i])[0] == expected_results[i]


def test_format_currency():
    assert format_currency(12300) == '12,300'
