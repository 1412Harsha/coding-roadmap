import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Coding Roadmap Tracker", layout="centered")

st.title("🚀 Coding Roadmap Tracker")

# -------------------------------
# SKILLS INPUT
# -------------------------------
st.header("🧠 Your Skills")

skills = st.text_input(
    "Enter skills you already have (comma separated)",
    key="skills_input"
)

if skills:
    skills_list = [s.strip() for s in skills.split(",")]
    st.write("Your Skills:", skills_list)

# -------------------------------
# COURSE SELECTION
# -------------------------------
st.header("📚 Select Your Course")

course = st.selectbox(
    "Choose a domain",
    ["Frontend", "Backend", "DSA", "Full Stack"],
    key="course_select"
)

# -------------------------------
# TOTAL PROBLEMS SETUP
# -------------------------------
st.header("⚙️ Setup Your Target")

total_problems = st.number_input(
    "Enter total problems you want to solve",
    min_value=1,
    value=50,
    key="total_input"
)

# -------------------------------
# PROGRESS INPUT
# -------------------------------
st.header("📊 Update Your Progress")

solved = st.number_input(
    "How many problems you solved?",
    min_value=0,
    max_value=total_problems,
    value=0,
    key="solved_input"
)

# -------------------------------
# PROGRESS CALCULATION
# -------------------------------
progress = solved / total_problems if total_problems > 0 else 0

st.progress(progress)
st.write(f"### Progress: {int(progress * 100)}%")

# -------------------------------
# MOTIVATION MESSAGE
# -------------------------------
if progress == 1:
    st.success("🔥 Amazing! You completed everything!")
elif progress > 0.5:
    st.info("💪 Great progress, keep going!")
else:
    st.warning("🚀 Start solving problems!")

# -------------------------------
# DAILY GOAL
# -------------------------------
st.header("🎯 Daily Goal")

goal = st.text_input("Enter today's goal", key="goal_input")

if goal:
    st.write(f"Your Goal: {goal}")

# -------------------------------
# SUMMARY
# -------------------------------
st.header("📈 Summary")

st.write(f"Course: **{course}**")
st.write(f"Solved: **{solved} / {total_problems}**")

# -------------------------------
# PROGRESS GRAPH
# -------------------------------
st.header("📊 Progress Graph")

if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append(solved)

df = pd.DataFrame({
    "Attempt": list(range(1, len(st.session_state.history) + 1)),
    "Solved": st.session_state.history
})

st.line_chart(df.set_index("Attempt"))

# -------------------------------
# LINEAR REGRESSION
# -------------------------------
st.header("📉 Progress Prediction (Linear Regression)")

if len(df) > 1:
    X = df["Attempt"].values.reshape(-1, 1)
    y = df["Solved"].values

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 5 attempts
    future_attempts = np.array(range(len(df)+1, len(df)+6)).reshape(-1, 1)
    predictions = model.predict(future_attempts)

    future_df = pd.DataFrame({
        "Attempt": range(1, len(df)+6),
        "Solved": list(df["Solved"]) + list(predictions)
    })

    st.line_chart(future_df.set_index("Attempt"))

    st.info("📌 Graph includes predicted future progress")
else:
    st.warning("Add more data to see prediction")