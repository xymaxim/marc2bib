from marc2bib import remove_punctuation


def test_terminal_space_and_punctuation():
    assert "Test" == remove_punctuation("Test .")
    assert "Test" == remove_punctuation("Test ,")
    assert "Test" == remove_punctuation("Test :")
    assert "Test" == remove_punctuation("Test ;")
    assert "Test" == remove_punctuation("Test +")
    assert "Test" == remove_punctuation("Test /")
    assert "Test" == remove_punctuation("Test =")


def test_punctuation_without_space():
    assert "Test" == remove_punctuation("Test.")


def test_year():
    assert "2022" == remove_punctuation("2022.")


def test_initials():
    assert "A.B." == remove_punctuation("A.B.")


def test_name_suffixes():
    assert "Jane Doe, Sr." == remove_punctuation("Jane Doe, Sr.")
    assert "John Doe, Jr." == remove_punctuation("John Doe, Jr.")


def test_ellipsis():
    assert "Test..." == remove_punctuation("Test...")


def test_ordinal_numbers():
    assert "1st." == remove_punctuation("1st.")
    assert "2nd." == remove_punctuation("2nd.")
    assert "3rd." == remove_punctuation("3rd.")
    assert "4th." == remove_punctuation("4th.")
