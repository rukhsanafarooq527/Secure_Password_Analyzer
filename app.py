
import streamlit as st
import re
import string
import random
import pandas as pd
import plotly.express as px

st.set_page_config("ShieldPass: Secure Password Analyzer", page_icon="🛡️", layout="wide")


# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🛡️ ShieldPass: Secure Password Analyzer")

st.markdown(
    """
    <img src="https://static.vecteezy.com/system/resources/thumbnails/021/312/714/small_2x/shield-protection-icon-security-data-concept-png.png"
         class="logo-icon">
    """,
    unsafe_allow_html=True
)


st.subheader(
    "Shield Your Digital Life: Analyze, Optimize, and Strengthen Your Passwords for Smarter Security. 🔐✨"
)

# Sidebar Tips
st.sidebar.title("⚡ Craft an Unbreakable Password!")
st.sidebar.subheader("Boost your digital security with these power-packed tips:")
st.sidebar.markdown(
    """  
🟢 *Make it Long:* Use at least *8+ characters*  
🔠 *Mix Upper & Lowercase Letters*  
🔢 *Include Numbers*  
💢 *Use Special Characters*  
🚫 *Avoid Predictability*
"""
)
st.sidebar.markdown("---")


# Generate strong password
def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(characters) for _ in range(12))


# Session state for password
if "password" not in st.session_state:
    st.session_state.password = ""

if st.sidebar.button("🔄 Auto-Generate Password"):
    st.session_state.password = generate_strong_password()
    st.sidebar.success(f"✅ Generated: {st.session_state.password}")

# Input field
password = st.text_input("🔑 Enter your password:", type="password", value=st.session_state.password)

# Common passwords
common_passwords = [
    "password", "123456", "qwerty", "admin", "user", "test",
    "password123", "12345678", "123456789", "1234567890", "welcome", "hello"
]

# Check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if password in common_passwords:
        feedback.append("❌ Too common! Choose a unique password.")

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ At least 8 characters needed.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both UPPER and lower case letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one digit.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Use special characters like !@#")

    return score, feedback

# Progress color
def get_progress_color(score):
    return ["red", "orange", "yellow", "gold", "green"][score]

# Button to check
if st.button("🔍 Check Password Strength"):
    if password:
        score, feedback = check_password_strength(password)
        strength_percentage = (score / 4) * 100
        color = get_progress_color(score)

        # Layout: Two columns
        col1, col2 = st.columns([2, 1])

        with col1:
            st.header("🔒 Password Strength")

            # Animated Progress
            st.markdown(
                f"""
                <div style='background: lightgray; border-radius: 8px; height: 12px;'>
                    <div style='width: {strength_percentage}%; background-color: {color}; height: 100%; border-radius: 8px; transition: width 1s;'></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if score == 4:
                st.success("✅ Strong Password!")
            elif score >= 3:
                st.warning("⚠ Moderate - Improve further.")
            else:
                st.error("❌ Weak - Follow tips below.")

            if feedback:
                st.subheader("💡 Suggestions")
                for msg in feedback:
                    st.markdown(f"- {msg}")

        with col2:
            df = pd.DataFrame({
                "Criteria": ["Length", "Upper/Lower", "Digit", "Special Char"],
                "Score": [1 if len(password) >= 8 else 0,
                          1 if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) else 0,
                          1 if re.search(r"\d", password) else 0,
                          1 if re.search(r"[!@#$%^&*]", password) else 0]
            })
            fig = px.bar(df, x="Criteria", y="Score", color="Score",
                         color_continuous_scale=["red", "orange", "green"],
                         title="📊 Criteria-wise Strength")
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠ Please enter a password first!")

# Footer
st.markdown('<div class="footer">Made with ⋆❤️⋆ by Rukhsana Shaheen | rukhsanafsarooq527@gmail.com ⋆.˚🦋༘⋆</div>', unsafe_allow_html=True)
