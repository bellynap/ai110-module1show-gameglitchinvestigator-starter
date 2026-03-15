from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"

def test_guess_with_string_secret_bug():
    # This test ensures the fix for the glitch where secret was converted to str on even attempts.
    # Even if secret is passed as str, it should be converted to int and compared numerically.
    # When secret is "9" (str) and guess is 10 (int), it should correctly be "Too High" with the right message
    result = check_guess(10, "9")
    assert result == ("Too High", "📉 Go LOWER!")  # Now passes with the fix


def test_hint_direction_correct():
    # When guess is lower than the secret, hint should point higher.
    # E.g., secret=84, guess=32 should say "Go HIGHER!" (still outcome "Too Low").
    result = check_guess(32, 84)
    assert result == ("Too Low", "📈 Go HIGHER!")
