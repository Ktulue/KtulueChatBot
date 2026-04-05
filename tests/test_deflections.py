from deflections import (
    HUMOR_DEFLECTIONS,
    REDIRECT_DEFLECTIONS,
    WATER_FATHER_DEFLECTIONS,
    get_random_deflection,
)


def test_humor_deflections_has_at_least_five():
    assert len(HUMOR_DEFLECTIONS) >= 5


def test_redirect_deflections_has_at_least_five():
    assert len(REDIRECT_DEFLECTIONS) >= 5


def test_water_father_deflections_has_at_least_five():
    assert len(WATER_FATHER_DEFLECTIONS) >= 5


def test_all_deflections_are_nonempty_strings():
    for pool in [HUMOR_DEFLECTIONS, REDIRECT_DEFLECTIONS, WATER_FATHER_DEFLECTIONS]:
        for entry in pool:
            assert isinstance(entry, str)
            assert len(entry.strip()) > 0


def test_no_duplicate_deflections_within_pools():
    for pool in [HUMOR_DEFLECTIONS, REDIRECT_DEFLECTIONS, WATER_FATHER_DEFLECTIONS]:
        assert len(pool) == len(set(pool))


def test_get_random_deflection_returns_string():
    result = get_random_deflection("humor")
    assert isinstance(result, str)
    assert result in HUMOR_DEFLECTIONS


def test_get_random_deflection_all_categories():
    for category in ["humor", "redirect", "water_father"]:
        result = get_random_deflection(category)
        assert isinstance(result, str)
        assert len(result.strip()) > 0


def test_get_random_deflection_invalid_category():
    result = get_random_deflection("nonexistent")
    assert isinstance(result, str)
    assert len(result.strip()) > 0
