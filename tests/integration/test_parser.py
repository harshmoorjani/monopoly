from pathlib import Path

from pydantic import SecretStr
from pytest import raises

from monopoly.pdf import (
    BadPasswordFormatError,
    MissingPasswordError,
    PdfParser,
    WrongPasswordError,
)

fixture_directory = Path(__file__).parent / "fixtures"


def test_can_open_file_stream(parser: PdfParser):
    with open(fixture_directory / "4_pages_blank.pdf", "rb") as file:
        parser.file_bytes = file.read()
        document = parser.open()
        assert len(document) == 4


def test_can_open_protected(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"
    parser._passwords = [SecretStr("foobar123")]

    parser.open()


def test_wrong_password_raises_error(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"
    parser._passwords = [SecretStr("wrong_pw")]

    with raises(WrongPasswordError, match="Could not open"):
        parser.open()


def test_get_pages(parser: PdfParser):
    parser.file_path = fixture_directory / "4_pages_blank.pdf"
    parser.page_range = slice(0, -1)

    pages = parser.get_pages()
    assert len(pages) == 3


def test_get_pages_invalid_returns_error(parser: PdfParser):
    parser.file_path = fixture_directory / "4_pages_blank.pdf"
    parser.page_range = slice(99, -99)

    with raises(ValueError, match="bad page number"):
        parser.get_pages()


def test_override_password(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"
    parser._passwords = [SecretStr("foobar123")]
    document = parser.open()
    assert not document.is_encrypted


def test_error_raised_if_override_is_wrong(parser: PdfParser):
    with raises(WrongPasswordError, match="Could not open"):
        parser.file_path = fixture_directory / "protected.pdf"
        parser._passwords = [SecretStr("wrongpw")]
        parser.open()


def test_missing_password_raises_error(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"

    with raises(MissingPasswordError, match="No password found in PDF configuration"):
        parser.open()


def test_null_password_raises_error(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"
    parser._passwords = [SecretStr("")]

    with raises(MissingPasswordError, match="is empty"):
        parser.open()


def test_invalid_password_type_raises_error(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"
    parser._passwords = "not a list"

    with raises(BadPasswordFormatError, match="should be stored in a list"):
        parser.open()


def test_plain_text_passwords_raises_error(parser: PdfParser):
    parser.file_path = fixture_directory / "protected.pdf"
    parser._passwords = ["password"]

    with raises(BadPasswordFormatError, match="should be stored as SecretStr"):
        parser.open()
