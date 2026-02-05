"""Edge-case tests for Game Glitch Investigator.

Tests for boundary conditions, invalid inputs, and hidden bugs.
Challenge 1: Advanced Edge-Case Testing
"""

import pytest
from logic_utils import parse_guess, check_guess, update_score


class TestParseGuessEdgeCases:
    """Test parse_guess() with edge case inputs."""

    def test_negative_number(self):
        """Negative numbers should be parsed correctly (but range check needed)."""
        ok, value, err = parse_guess("-50")
        assert ok is True
        assert value == -50
        assert err is None

    def test_very_large_number(self):
        """Very large numbers should parse but exceed game range."""
        ok, value, err = parse_guess("999999")
        assert ok is True
        assert value == 999999
        assert err is None

    def test_decimal_truncation(self):
        """Decimals should truncate to int, but user gets no feedback."""
        ok, value, err = parse_guess("50.9")
        assert ok is True
        assert value == 50  # Truncated, not rounded
        assert err is None

    def test_decimal_rounding_edge(self):
        """50.1 should also truncate to 50, not round to 50."""
        ok, value, err = parse_guess("50.1")
        assert ok is True
        assert value == 50
        assert err is None

    def test_leading_trailing_whitespace(self):
        """Leading/trailing spaces - relies on Streamlit sanitization."""
        ok, value, err = parse_guess("  50  ")
        # Note: This may fail if Streamlit doesn't auto-strip.
        # Current behavior depends on Streamlit's input handling.
        if ok:
            assert value == 50
        else:
            assert err is not None

    def test_zero(self):
        """Zero is a valid int, but outside typical game range."""
        ok, value, err = parse_guess("0")
        assert ok is True
        assert value == 0
        assert err is None

    def test_float_with_scientific_notation(self):
        """Scientific notation without decimal - should fail (not parsed as float)."""
        ok, value, err = parse_guess("1e10")
        # "1e10" has no ".", so it tries int() which fails
        assert ok is False
        assert err is not None


class TestStringComparisonGlitch:
    """Test the hidden bug: string comparison on even attempts.
    
    Lines 77-81 of app.py convert secret to string on even attempts,
    causing lexicographic instead of numeric comparison.
    """

    def test_numeric_vs_string_comparison_basic(self):
        """60 > 100 (numeric) but "60" > "100" (string)."""
        # Numeric comparison
        assert (60 > 100) is False
        # String comparison (the bug)
        assert ("60" > "100") is True

    def test_even_attempt_string_glitch_basic(self):
        """On even attempts, secret becomes string, breaking comparisons."""
        guess = 60
        secret_str = "100"  # Simulates line 80: secret = str(st.session_state.secret)
        
        # String comparison: "60" > "100" is True (lexicographic)
        # So check_guess would return "Too High" when numerically 60 < 100
        # This is wrong!
        outcome, message = check_guess(guess, secret_str)
        
        # Current broken behavior: string comparison
        assert outcome == "Too High"  # THIS IS WRONG! 60 < 100
        assert "LOWER" in message

    def test_string_comparison_single_digit_vs_double(self):
        """String "9" > "100" because '9' > '1'."""
        # Numeric: 9 < 100
        assert 9 < 100
        
        # String: "9" > "100"
        assert "9" > "100"
        
        # Game would erroneously say guess 9 is "Too High"
        outcome, _ = check_guess(9, "100")
        assert outcome == "Too High"  # WRONG! 9 < 100

    def test_odd_attempt_correct_then_even_attempt_breaks(self):
        """Odd attempts work (numeric), even attempts fail (string)."""
        # Odd attempt: numeric comparison (correct)
        outcome_odd, msg_odd = check_guess(60, 50)
        assert outcome_odd == "Too High"
        assert "LOWER" in msg_odd
        
        # Even attempt: string comparison (broken)
        # On even attempts, app.py converts secret to str
        outcome_even, msg_even = check_guess(60, "50")
        # String: "60" > "50" is True, so "Too High" is correct by accident
        # But with secret "100": "60" > "100" is True, so "Too High" is WRONG
        assert outcome_even == "Too High"


class TestCheckGuessEdgeCases:
    """Test check_guess() with boundary values."""

    def test_guess_equals_secret(self):
        """Standard win condition."""
        outcome, msg = check_guess(50, 50)
        assert outcome == "Win"
        assert "Correct" in msg

    def test_guess_boundary_one_below(self):
        """Guess is exactly one below secret."""
        outcome, msg = check_guess(49, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in msg

    def test_guess_boundary_one_above(self):
        """Guess is exactly one above secret."""
        outcome, msg = check_guess(51, 50)
        assert outcome == "Too High"
        assert "LOWER" in msg

    def test_negative_guess_vs_positive_secret(self):
        """Negative guess compared to positive secret."""
        outcome, msg = check_guess(-10, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in msg

    def test_both_negative(self):
        """Both guess and secret are negative."""
        outcome, msg = check_guess(-10, -50)
        assert outcome == "Too High"
        assert "LOWER" in msg

    def test_large_difference(self):
        """Huge difference between guess and secret."""
        outcome, msg = check_guess(1, 1000000)
        assert outcome == "Too Low"
        assert "HIGHER" in msg


class TestUpdateScoreEdgeCases:
    """Test score updates with edge case outcomes."""

    def test_win_on_first_attempt(self):
        """Winning immediately gives maximum points."""
        score = update_score(current_score=0, outcome="Win", attempt_number=1)
        # 100 - 10 * (1 + 1) = 100 - 20 = 80
        assert score == 80

    def test_win_on_last_attempt(self):
        """Winning on last attempt gives minimum points (10)."""
        score = update_score(current_score=0, outcome="Win", attempt_number=8)
        # 100 - 10 * (8 + 1) = 100 - 90 = 10
        assert score == 10

    def test_win_on_many_attempts_caps_at_10(self):
        """Winning after many attempts still caps at 10."""
        score = update_score(current_score=0, outcome="Win", attempt_number=20)
        # 100 - 10 * (20 + 1) = 100 - 210 = -110, but capped at 10
        assert score == 10

    def test_too_high_even_attempt_bonus(self):
        """Even attempts on 'Too High' get +5 bonus (oddly)."""
        score = update_score(current_score=0, outcome="Too High", attempt_number=2)
        # attempt 2 is even: +5
        assert score == 5

    def test_too_high_odd_attempt_penalty(self):
        """Odd attempts on 'Too High' get -5 penalty."""
        score = update_score(current_score=0, outcome="Too High", attempt_number=1)
        # attempt 1 is odd: -5
        assert score == -5

    def test_too_low_always_penalty(self):
        """'Too Low' always penalizes -5 regardless of attempt parity."""
        score1 = update_score(current_score=0, outcome="Too Low", attempt_number=1)
        score2 = update_score(current_score=0, outcome="Too Low", attempt_number=2)
        assert score1 == -5
        assert score2 == -5


class TestOutOfRangeDetection:
    """Test that out-of-range guesses can be rejected with range validation."""

    def test_guess_below_minimum_with_range(self):
        """Guess below 1 on Normal difficulty should be rejected when min_val set."""
        ok, value, err = parse_guess("0", min_val=1, max_val=100)
        assert ok is False
        assert err is not None
        assert "at least" in err.lower()

    def test_guess_above_maximum_with_range(self):
        """Guess above 100 on Normal difficulty should be rejected when max_val set."""
        ok, value, err = parse_guess("101", min_val=1, max_val=100)
        assert ok is False
        assert err is not None
        assert "at most" in err.lower()

    def test_guess_in_valid_range(self):
        """Guess within range should be accepted."""
        ok, value, err = parse_guess("50", min_val=1, max_val=100)
        assert ok is True
        assert value == 50
        assert err is None

    def test_parse_guess_backwards_compatible(self):
        """parse_guess() without range params should still work."""
        ok, value, err = parse_guess("999")
        assert ok is True
        assert value == 999
        assert err is None
