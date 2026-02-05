def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Swapped ranges so Normal is 1-50 (easier) and Hard is 1-100 (harder)
    # Collaboration: Identified by user review; Copilot suggested refactoring to logic_utils.py
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str, min_val: int = None, max_val: int = None):
    """
    Parse user input into an int guess.

    Args:
        raw: User input string
        min_val: Optional minimum allowed value (inclusive)
        max_val: Optional maximum allowed value (inclusive)

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: Added range validation for Challenge 1 edge-case testing
    # Collaboration: User challenge to handle out-of-range guesses
    if min_val is not None and value < min_val:
        return False, None, f"Guess must be at least {min_val}."
    if max_val is not None and value > max_val:
        return False, None, f"Guess must be at most {max_val}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Corrected reversed feedback messages - "Too High" now returns "Go LOWER!" not "Go HIGHER!"
    # Collaboration: User identified reversed hints; Copilot Agent refactored logic into this module
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
