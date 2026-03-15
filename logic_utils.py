import random


def get_range_for_difficulty(difficulty: str):
    """Retrieve the inclusive range for the secret number.

    Args:
        difficulty (str): The difficulty level.
            Supported values are 'Easy', 'Normal', 'Hard'.
            Defaults to 'Normal' if an unsupported value is provided.

    Returns:
        tuple[int, int]: A tuple containing the low and high bounds
            (inclusive) for the secret number.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse the raw user input string into a valid integer guess.

    This function validates the input to ensure it represents a positive whole number
    within reasonable bounds to prevent parsing issues or overflow.

    Args:
        raw (str): The raw input string from the user.

    Returns:
        tuple[bool, int | None, str | None]: A tuple containing:
            - ok (bool): True if parsing was successful, False otherwise.
            - guess_int (int | None): The parsed integer guess, or None on failure.
            - error_message (str | None): An error message if parsing failed.
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
    """Compare the user's guess against the secret number and determine the outcome.

    Args:
        guess (int): The user's guessed number.
        secret (int | str): The secret number to guess.
            Can be int or str, but will be converted to int.

    Returns:
        tuple[str, str]: A tuple containing:
            - outcome (str): The result of the guess. Possible values: 'Win',
              'Too High', 'Too Low'.
            - message (str): A user-friendly message describing the outcome.
    """
    # Ensure secret is always an int so we compare numerically rather than
    # lexicographically (e.g., '10' > '2').
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"

    # Correct the hint messages to guide the player properly.
    # Previously, "Too High" said "Go HIGHER!" (should be "Go LOWER!") and
    # "Too Low" said "Go LOWER!" (should be "Go HIGHER!").
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


# Added update_score in logic_utils.py (refactored from app.py) so game rules live together.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update the player's score based on the guess outcome and attempt number.

    Args:
        current_score (int): The player's current score before the update.
        outcome (str): The outcome of the guess.
            Possible values: 'Win', 'Too High', 'Too Low'.
        attempt_number (int): The number of attempts made so far (0-based).

    Returns:
        int: The updated score after applying the scoring rules.
    """
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
    """Resets the game state to its initial values for a new game.

    Args:
        low (int): The lower bound (inclusive) for the secret number range.
        high (int): The upper bound (inclusive) for the secret number range.

    Returns:
        dict: A dictionary representing the initial game state with the
            following keys:
            - 'secret' (int): The randomly generated secret number.
            - 'attempts' (int): Number of attempts made (initially 0).
            - 'score' (int): Current score (initially 0).
            - 'status' (str): Game status (initially 'playing').
            - 'history' (list): List of previous guesses (initially empty).
            - 'reset_counter' (int): Counter for game resets (initially 0).
    """
    return {
        "secret": random.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
        "reset_counter": 0,
    }


# Note: get_attempt_limit was factored out from app.py to keep game logic
# separate from UI concerns.
def get_attempt_limit(difficulty: str) -> int:
    """Retrieve the maximum number of attempts allowed for a given difficulty.

    Args:
        difficulty (str): The difficulty level.
            Supported values are 'Easy', 'Normal', 'Hard'.

    Returns:
        int: The maximum number of attempts allowed for the given difficulty.
            Defaults to 8 if an unsupported difficulty is provided.
    """
    limits = {
        "Easy": 6,
        "Normal": 8,
        "Hard": 5,
    }
    return limits.get(difficulty, 8)
