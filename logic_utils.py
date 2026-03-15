import random

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # Reject decimals (must be whole numbers)
    if "." in raw:
        return False, None, "Enter a whole number."

    try:
        # Very large integers can be unreasonably slow to parse; reject them.
        # This also avoids overflow-like behaviors in some environments.
        if len(raw) > 9:
            return False, None, "Enter a reasonable number."

        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < 0:
        return False, None, "Enter a positive number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # Fix #2: Ensure secret is always an int to prevent string comparison bugs on even attempts
    # The original code sometimes passes secret as str, causing lexicographical comparisons instead of numerical
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"

    # Fix #7: Correct the hint messages to guide the player properly
    # Previously, "Too High" incorrectly said "Go HIGHER!" (should be "Go LOWER!"), and "Too Low" said "Go LOWER!" (should be "Go HIGHER!")
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


# FIX: Added update_score in logic_utils.py (refactored from app.py) so all game rules live together.
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


def reset_game(low: int, high: int) -> dict:
    """Return initial game state."""
    return {
        "secret": random.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "reset_counter": 0,
    }


# FIX: Added get_attempt_limit function refactored from app.py using Copilot Agent mode for better separation of logic and UI.
def get_attempt_limit(difficulty: str) -> int:
    """Return the attempt limit for a given difficulty."""
    limits = {
        "Easy": 6,
        "Normal": 8,
        "Hard": 5,
    }
    return limits.get(difficulty, 8)
