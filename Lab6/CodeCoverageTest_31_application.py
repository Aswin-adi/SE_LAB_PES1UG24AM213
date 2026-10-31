import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_welcome10_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome10_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_empty_cart():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_weekend20_saturday_high_cart():
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120


def test_weekend20_sunday_high_cart():
    assert coupon_discount("WEEKEND20", 600, False, "sun") == 120


def test_weekend20_low_cart():
    assert coupon_discount("WEEKEND20", 400, False, "sat") == 50


def test_weekend20_weekday():
    assert coupon_discount("WEEKEND20", 600, False, "mon") == 0


def test_flat100_eligible():
    assert coupon_discount("FLAT100", 500, False, "mon") == 100


def test_flat100_not_eligible():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_invalid_coupon():
    assert coupon_discount("INVALID", 500, True, "sat") == 0


def test_best_discount_empty_list():
    assert best_discount([], 500, True, "sat") == 0


def test_best_discount_selects_highest():
    result = best_discount(
        ["WELCOME10", "WEEKEND20", "FLAT100"],
        600, True, "sat"
    )
    assert result == 120


def test_best_discount_applies_cap():
    result = best_discount(["WEEKEND20"], 100, False, "sat")
    assert result == 40


def test_best_discount_without_cap():
    result = best_discount(["WELCOME10"], 200, True, "mon")
    assert result == 20


def test_expired_zero_validity():
    assert is_expired(10, 5, 0) is True


def test_expired_after_validity():
    assert is_expired(20, 5, 10) is True


def test_not_expired_within_validity():
    assert is_expired(10, 5, 10) is False


def test_not_expired_at_validity_boundary():
    assert is_expired(15, 5, 10) is False
