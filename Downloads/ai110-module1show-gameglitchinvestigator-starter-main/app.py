import random
import streamlit as st

# FIX: Refactored logic into logic_utils.py using Copilot Agent mode
# Collaboration: User requested separation of concerns; Copilot Agent autonomously moved functions
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

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
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

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
        st.session_state.history.append(guess_int)

        # FIX: Removed string conversion bug that broke even-attempt comparisons
        # Challenge 1: Lines 106-108 converted secret to string on even attempts,
        # causing lexicographic instead of numeric comparison ("60" > "100" = True)
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)
        
        # Challenge 4: Hot/Cold Temperature Feedback
        if outcome != "Win":
            distance = abs(guess_int - st.session_state.secret)
            if distance <= 5:
                st.error(f"🔥 BURNING! You're extremely close (distance: {distance})")
            elif distance <= 20:
                st.warning(f"🟡 WARM! Getting closer (distance: {distance})")
            else:
                st.info(f"❄️ COLD! You're far away (distance: {distance})")

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
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )


# Challenge 4: Session Summary Table (appears when game ends)
if st.session_state.status in ["won", "lost"]:
    st.divider()
    st.subheader("📋 Game Session Summary")
    
    # Calculate statistics
    numeric_guesses = [g for g in st.session_state.history if isinstance(g, int)]
    if numeric_guesses:
        distances = [abs(g - st.session_state.secret) for g in numeric_guesses]
        closest_guess = min(numeric_guesses, key=lambda x: abs(x - st.session_state.secret))
        avg_distance = sum(distances) / len(distances)
    else:
        closest_guess = "N/A"
        avg_distance = "N/A"
    
    # Create summary rows
    summary_data = {
        "Metric": [
            "Outcome",
            "Total Attempts",
            "Final Score",
            "Closest Guess",
            "Average Distance",
            "Secret Number"
        ],
        "Value": [
            "🏆 Win!" if st.session_state.status == "won" else "❌ Loss",
            str(st.session_state.attempts),
            str(st.session_state.score),
            str(closest_guess),
            f"{avg_distance:.1f}" if isinstance(avg_distance, float) else avg_distance,
            str(st.session_state.secret)
        ]
    }
    
    import pandas as pd
    st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

# Challenge 2A: Guess History Visualizer
if len(st.session_state.history) > 0:
    st.divider()
    st.subheader("📊 Guess History & Analytics")
    
    # Filter numeric guesses from history (skip invalid entries)
    numeric_guesses = [g for g in st.session_state.history if isinstance(g, int)]
    
    if numeric_guesses:
        import pandas as pd
        
        # Create attempt numbers (1, 2, 3, ...)
        attempt_numbers = list(range(1, len(numeric_guesses) + 1))
        
        # Calculate distance from secret
        distances = [abs(g - st.session_state.secret) for g in numeric_guesses]
        
        # Challenge 4: Create Hot/Cold Status for each guess
        hot_cold_status = []
        for distance in distances:
            if distance <= 5:
                hot_cold_status.append("🔥 BURNING!")
            elif distance <= 20:
                hot_cold_status.append("🟡 WARM")
            else:
                hot_cold_status.append("❄️ COLD")
        
        # Create enhanced dataframe with all metrics
        history_df = pd.DataFrame({
            "Attempt": attempt_numbers,
            "Guess": numeric_guesses,
            "Distance": distances,
            "Status": hot_cold_status
        })
        
        # Display enhanced table
        st.subheader("Attempt Details")
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        # Create visualization columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Guess Progression")
            st.line_chart({
                "Guess Value": numeric_guesses,
                "Secret": [st.session_state.secret] * len(numeric_guesses)
            })
        
        with col2:
            st.subheader("Distance from Secret")
            st.bar_chart({
                "Distance": distances
            })
        
        # Summary stats
        st.subheader("Session Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Distance", f"{sum(distances) / len(distances):.1f}")
        with col2:
            st.metric("Closest Guess", f"{min(numeric_guesses, key=lambda x: abs(x - st.session_state.secret))}")
        with col3:
            closest_distance = min(distances)
            st.metric("Best Attempt", f"{closest_distance} away")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
