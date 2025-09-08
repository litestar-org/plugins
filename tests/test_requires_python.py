from src.utils import parse_requires_python


def test_parse_requires_python():
    # Test with a valid requires_python string
    result = parse_requires_python(">=3.7, <4")
    assert result.raw == ">=3.7, <4"
    assert result.specifier_set == "<4,>=3.7"
    assert "3.7" in result.compatible
    assert "3.8" in result.compatible
    assert "3.9" in result.compatible
    assert "3.10" in result.compatible
    assert "3.11" in result.compatible
    assert "3.12" in result.compatible
    assert "3.13" in result.compatible
    assert "3.14" in result.compatible
    assert "3.15" in result.compatible

    # Test with an empty string
    result = parse_requires_python("")
    assert result.raw == ""
    assert result.specifier_set == ""
    assert result.compatible == []

    # Test with None input (should handle gracefully)
    result = parse_requires_python("")
    assert result.raw == ""
    assert result.specifier_set == ""
    assert result.compatible == []

    # Test with a complex specifier
    result = parse_requires_python(">=3.7, !=3.8.*, <4")
    assert result.raw == ">=3.7, !=3.8.*, <4"
    assert result.specifier_set == "!=3.8.*,<4,>=3.7"
    assert "3.7" in result.compatible
    assert "3.9" in result.compatible
    assert "3.10" in result.compatible
    assert "3.11" in result.compatible
    assert "3.12" in result.compatible
    assert "3.13" in result.compatible
    assert "3.14" in result.compatible
    assert "3.15" in result.compatible
    assert "3.8" not in result.compatible
