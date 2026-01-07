# filename: password_analyzer_app.py
import streamlit as st
import math
import hashlib
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Password Security Analyzer",
    page_icon="🔒",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 30px;
    }
    .report-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin: 10px 0;
    }
    .risk-critical { color: #d32f2f; font-weight: bold; }
    .risk-high { color: #f57c00; }
    .risk-medium { color: #fbc02d; }
    .risk-low { color: #388e3c; }
    .strength-meter {
        height: 25px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🔒 Password Security Analyzer</h1>', unsafe_allow_html=True)
st.markdown("---")

# Common passwords list
COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "123456789",
    "12345", "1234", "111111", "1234567", "dragon",
    "123123", "baseball", "abc123", "football", "monkey",
    "letmein", "696969", "shadow", "master", "666666",
    "qwertyuiop", "123321", "mustang", "1234567890",
    "michael", "654321", "superman", "1qaz2wsx", "7777777",
    "fuckyou", "121212", "000000", "qazwsx", "123qwe",
    "killer", "trustno1", "jordan", "jennifer", "zxcvbnm",
    "asdfgh", "hunter", "buster", "soccer", "harley",
    "batman", "andrew", "tigger", "sunshine", "iloveyou",
    "fuckme", "2000", "charlie", "robert", "thomas",
    "hockey", "ranger", "daniel", "starwars", "klaster",
    "112233", "george", "asshole", "computer", "michelle",
    "jessica", "pepper", "1111", "zxcvbn", "555555",
    "11111111", "131313", "freedom", "777777", "pass",
    "fuck", "maggie", "159753", "aaaaaa", "ginger",
    "princess", "joshua", "cheese", "amanda", "summer",
    "love", "ashley", "6969", "nicole", "chelsea",
    "biteme", "matthew", "access", "yankees", "987654321",
    "dallas", "austin", "thunder", "taylor", "matrix"
]


def calculate_entropy(password):
    """Calculate password entropy in bits"""
    if not password:
        return 0

    # Character pool size
    pool_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 32  # Common special characters

    if pool_size == 0:
        return 0

    # Entropy calculation
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


def calculate_strength_score(password):
    """Calculate password strength score (0-100)"""
    if not password:
        return 0

    score = 0

    # Length points (max 40)
    length = len(password)
    if length >= 8:
        score += 10
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    if length >= 20:
        score += 10

    # Character variety points (max 40)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    char_types = sum([has_lower, has_upper, has_digit, has_special])
    score += char_types * 10

    # Entropy points (max 20)
    entropy = calculate_entropy(password)
    if entropy > 50:
        score += 20
    elif entropy > 30:
        score += 15
    elif entropy > 20:
        score += 10
    elif entropy > 10:
        score += 5

    # Penalty for common password
    if password.lower() in COMMON_PASSWORDS:
        score = max(10, score - 30)

    return min(100, score)


def get_strength_rating(score):
    """Get rating based on score"""
    if score >= 90:
        return "A+ (EXCELLENT)", "#4CAF50"
    elif score >= 80:
        return "A (VERY GOOD)", "#8BC34A"
    elif score >= 70:
        return "B (GOOD)", "#CDDC39"
    elif score >= 60:
        return "C (FAIR)", "#FFEB3B"
    elif score >= 50:
        return "D (WEAK)", "#FFC107"
    elif score >= 40:
        return "E (POOR)", "#FF9800"
    else:
        return "F (VERY POOR)", "#F44336"


def estimate_crack_time(entropy):
    """Estimate crack time based on entropy"""
    # Assumptions: 10^9 guesses per second
    guesses_per_second = 1e9
    possible_combinations = 2 ** entropy
    seconds = possible_combinations / guesses_per_second

    # Convert to readable time
    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} days"
    elif seconds < 3153600000:
        return f"{int(seconds / 31536000)} years"
    else:
        return f"{int(seconds / 31536000):,} years"


def get_recommendations(password, score):
    """Get security recommendations"""
    recommendations = []

    if score < 60:
        recommendations.append("🔴 **CRITICAL:** Consider changing this password")

    if len(password) < 8:
        recommendations.append("🔴 Increase password length to at least 8 characters")
    elif len(password) < 12:
        recommendations.append("🟡 Increase password length to 12+ characters for better security")

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if not has_lower:
        recommendations.append("🟡 Add lowercase letters (a-z)")
    if not has_upper:
        recommendations.append("🟡 Add uppercase letters (A-Z)")
    if not has_digit:
        recommendations.append("🟡 Add numbers (0-9)")
    if not has_special:
        recommendations.append("🟡 Add special characters (!@#$%^&*)")

    if password.lower() in COMMON_PASSWORDS:
        recommendations.append("🔴 **WARNING:** This is a very common password!")

    if score >= 80:
        recommendations.append("✅ Your password is strong! Keep it up!")

    return recommendations


# Main UI
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 🔑 Enter Password")
    password = st.text_input("Password:", type="password", placeholder="Type your password here...")

    analyze_button = st.button("🔍 Analyze Password", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("### 💡 Tips for Strong Passwords")
    st.markdown("""
    1. Use **12+ characters**
    2. Mix **uppercase + lowercase**
    3. Include **numbers & symbols**
    4. Avoid **common words**
    5. Don't use **personal info**
    6. Use **passphrases**: `Coffee@Morning#2024!`
    """)

if analyze_button and password:
    with col2:
        # Calculate metrics
        entropy = calculate_entropy(password)
        score = calculate_strength_score(password)
        rating, rating_color = get_strength_rating(score)
        crack_time = estimate_crack_time(entropy)
        recommendations = get_recommendations(password, score)

        # Display strength meter
        st.markdown(f"### 📊 Strength Score: **{score}/100**")
        st.progress(score / 100)
        st.markdown(f'### 🏆 Rating: <span style="color:{rating_color}">{rating}</span>', unsafe_allow_html=True)

        # Analysis results in columns
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown("#### 📋 Basic Analysis")
            st.markdown(f"**Length:** {len(password)} characters")

            char_types = []
            if any(c.islower() for c in password):
                char_types.append("Lowercase ✓")
            if any(c.isupper() for c in password):
                char_types.append("Uppercase ✓")
            if any(c.isdigit() for c in password):
                char_types.append("Numbers ✓")
            if any(not c.isalnum() for c in password):
                char_types.append("Special ✓")

            st.markdown("**Contains:** " + ", ".join(char_types))
            st.markdown(f"**Entropy:** {entropy} bits")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown("#### ⏱️ Time to Crack")
            st.markdown(f"**Estimated:** {crack_time}")
            st.markdown("*Based on 1 billion guesses/second*")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Security Check")

            if password.lower() in COMMON_PASSWORDS:
                st.error("❌ **COMMON PASSWORD** - Found in hacked databases!")
            else:
                st.success("✅ Not in common password list")

            if len(password) < 8:
                st.error("❌ **TOO SHORT** - Less than 8 characters")
            else:
                st.success(f"✅ Length OK ({len(password)} chars)")

            if entropy < 40:
                st.warning(f"⚠️ **LOW ENTROPY** ({entropy} bits)")
            else:
                st.success(f"✅ Good entropy ({entropy} bits)")
            st.markdown("</div>", unsafe_allow_html=True)

        # Recommendations
        st.markdown("---")
        st.markdown("### 📝 Recommendations")

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
        else:
            st.success("🎉 No recommendations needed! Your password is strong!")

        # Generate sample strong password
        st.markdown("---")
        st.markdown("### 🔐 Need a Strong Password?")
        if st.button("Generate Strong Password"):
            import random
            import string

            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            strong_pass = ''.join(random.choice(chars) for _ in range(16))
            st.code(strong_pass, language="text")
            st.info("💡 Copy this password and save it in a secure place!")

elif analyze_button and not password:
    st.warning("⚠️ Please enter a password to analyze!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🔒 <strong>Password Security Analyzer</strong> | College Project | Made with Python & Streamlit</p>
    <p>💡 Remember: Never share your passwords with anyone!</p>
</div>
""", unsafe_allow_html=True)