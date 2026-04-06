from web.errors import FRIENDLY_ERRORS, pick_friendly_error


def test_friendly_errors_pool_has_at_least_five_entries():
    assert len(FRIENDLY_ERRORS) >= 5


def test_all_friendly_errors_are_non_empty_strings():
    for msg in FRIENDLY_ERRORS:
        assert isinstance(msg, str)
        assert len(msg.strip()) > 0


def test_friendly_errors_have_no_duplicates():
    assert len(FRIENDLY_ERRORS) == len(set(FRIENDLY_ERRORS))


def test_pick_friendly_error_returns_pool_entry():
    result = pick_friendly_error()
    assert result in FRIENDLY_ERRORS


def test_pick_friendly_error_returns_string():
    assert isinstance(pick_friendly_error(), str)
