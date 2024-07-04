from utils import extract_name_from_whisper


def test_extract_name_from_whisper():
    assert extract_name_from_whisper("From SomeName:") == "SomeName"
    assert extract_name_from_whisper("From SomeName: Hello sir") == "SomeName"
    assert (
        extract_name_from_whisper(
            "From SomeName: Hello, I would like to buy something ..."
        )
        == "SomeName"
    )
    assert (
        extract_name_from_whisper("From <©HOM> 相も変わらずお人好:")
        == "相も変わらずお人好"
    )
    assert (
        extract_name_from_whisper(
            "From <©HOM> 相も変わらずお人好: Hello, I would like to buy something ..."
        )
        == "相も変わらずお人好"
    )
    assert (
        extract_name_from_whisper(
            "From 相も変わらずお人好: Hello, I would like to buy something ..."
        )
        == "相も変わらずお人好"
    )
    assert extract_name_from_whisper("From 相も変わらずお人好") == "相も変わらずお人好"
    assert (
        extract_name_from_whisper("From 相も変わらずお人好: Hello")
        == "相も変わらずお人好"
    )
