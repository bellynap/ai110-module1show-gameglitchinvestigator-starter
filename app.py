import random
import streamlit as st
# FIX: Refactored logic into logic_utils.py using Copilot Agent mode. Moved get_range_for_difficulty, parse_guess, check_guess, update_score, get_attempt_limit, reset_game to separate file for better separation of concerns.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score, get_attempt_limit, reset_game
import os

# Agent: Added high score persistence functions to save/load best score from file.
def load_high_score():
    """Load high score from file, default to 0 if not found."""
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    """Save high score to file."""
    with open("high_score.txt", "w") as f:
        f.write(str(score))

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# FIX: Refactored attempt limit logic into get_attempt_limit function in logic_utils.py for cleaner code.
attempt_limit = get_attempt_limit(difficulty)

low, high = get_range_for_difficulty(difficulty)

# Fix #3: Reset secret when difficulty changes to respect the new range
# Previously, changing difficulty didn't update the secret, keeping it in the old range
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty
if st.session_state.current_difficulty != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.current_difficulty = difficulty

# Agent: Added high score tracking to session state, loaded from file.
if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score()

# Agent: Added guess history to track all guesses for visualization.
if "guess_history" not in st.session_state:
    st.session_state.guess_history = []

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Agent: Added high score display in sidebar.
st.sidebar.subheader("🏆 High Score")
st.sidebar.write(f"Best Score: {st.session_state.high_score}")

# Agent: Added guess history visualization in sidebar.
st.sidebar.subheader("📊 Guess History")
if st.session_state.guess_history:
    for i, entry in enumerate(st.session_state.guess_history, 1):
        guess = entry["guess"]
        distance = entry["distance"]
        # Visualize closeness with a progress bar (closer = more filled).
        max_distance = high - low  # Approximate max possible distance.
        closeness = 1 - (distance / max_distance) if max_distance > 0 else 1
        st.sidebar.write(f"Guess {i}: {guess} (Distance: {distance})")
        st.sidebar.progress(min(closeness, 1.0))
else:
    st.sidebar.write("No guesses yet.")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# Fix #5: Fix off-by-one error in attempts counter
# Previously, attempts started at 1, causing "attempts left" to show 7 instead of 8 initially for Normal mode
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# Agent: Added high score tracking to session state, loaded from file.
if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score()

# Agent: Added guess history to track all guesses for visualization.
if "guess_history" not in st.session_state:
    st.session_state.guess_history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.reset_counter}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: Refactored new game reset logic into reset_game function in logic_utils.py to encapsulate state initialization.
if new_game:
    # Use reset_game to get initial state
    initial_state = reset_game(low, high)
    for key, value in initial_state.items():
        st.session_state[key] = value
    # increment reset counter to clear the input widget
    st.session_state.reset_counter += 1

    st.success("New game started.")
    # No st.rerun() needed now

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        # Fix #4: Validate that guess is within the current difficulty range
        # Previously, users could enter numbers outside the range (e.g., 150 in Easy mode), getting misleading hints
        if not (low <= guess_int <= high):
            st.session_state.history.append(guess_int)
            st.error(f"Guess must be between {low} and {high}.")
        else:
            st.session_state.history.append(guess_int)
            # Agent: Record guess with distance from secret for history visualization.
            distance = abs(guess_int - st.session_state.secret)
            st.session_state.guess_history.append({"guess": guess_int, "distance": distance})

            # Fix #6: Always compare numerically so hints are correct.
            # Previously, secret could be passed as a string on even attempts, causing lexicographical comparisons.
            secret = int(st.session_state.secret)

            outcome, message = check_guess(guess_int, secret)

            if show_hint:
                st.warning(message)

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
                # Agent: Update high score if current score is better.
                if st.session_state.score > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.score
                    save_high_score(st.session_state.score)
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )
                    # Agent: Update high score even on loss if score is positive.
                    if st.session_state.score > st.session_state.high_score:
                        st.session_state.high_score = st.session_state.score
                        save_high_score(st.session_state.score)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
