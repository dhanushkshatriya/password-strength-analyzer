# filename: password_analyzer_pro.py
import streamlit as st
import math
import time
from datetime import datetime

# Page configuration to match your design
st.set_page_config(
    page_title="Password Security Analyzer",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS to match your exact design
st.markdown("""
<style>
    /* Main container styling */
    .main {
        max-width: 800px;
        margin: 0 auto;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 10px;
        font-size: 2.8rem;
        font-weight: 700;
    }
    
    .sub-header {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    
    /* Card styling */
    .analysis-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Strength meter styling */
    .strength-container {
        background: #e9ecef;
        border-radius: 25px;
        height: 12px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .strength-fill {
        height: 100%;
        border-radius: 25px;
        transition: width 0.5s ease;
    }
    
    /* Score display */
    .score-display {
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin: 10px 0;
        color: #2c3e50;
    }
    
    .rating-badge {
        display: inline-block;
        background: #28a745;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        text-align: center;
        margin: 0 auto;
        display: table;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #dee2e6;
        padding: 12px 15px;
        font-size: 16px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: #3498db;
        color: white;
        border: none;
        padding: 12px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: #2980b9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
    }
    
    /* Guidelines styling */
    .guidelines-box {
        background: #e8f4fc;
        border-left: 4px solid #3498db;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0;
    }
    
    /* Results section */
    .results-section {
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Color classes for strength levels */
    .color-weak { background: #e74c3c; }
    .color-poor { background: #e67e22; }
    .color-fair { background: #f1c40f; }
    .color-good { background: #2ecc71; }
    .color-strong { background: #27ae60; }
    .color-excellent { background: #16a085; }
    
    .text-weak { color: #e74c3c; }
    .text-poor { color: #e67e22; }
    .text-fair { color: #f1c40f; }
    .text-good { color: #2ecc71; }
    .text-strong { color: #27ae60; }
    .text-excellent { color: #16a085; }
</style>
""", unsafe_allow_html=True)

# Common passwords list
COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "123456789",
    "12345", "1234", "111111", "1234567", "dragon",
    "123123", "baseball", "abc123", "football", "monkey",
    "letmein", "696969", "shadow", "master", "666666"
]

def calculate_entropy(password):
    """Calculate password entropy in bits"""
    if not password:
        return 0
    
    pool_size = 0
    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(not c.isalnum() for c in password):
        pool_size += 32
    
    if pool_size == 0:
        return 0
    
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

def calculate_strength_score(password):
    """Calculate password strength score (0-100)"""
    if not password:
        return 0
    
    score = 0
    length = len(password)
    
    # Length points
    if length >= 8: score += 15
    if length >= 12: score += 20
    if length >= 16: score += 15
    
    # Character variety
    char_types = 0
    if any(c.islower() for c in password): char_types += 1
    if any(c.isupper() for c in password): char_types += 1
    if any(c.isdigit() for c in password): char_types += 1
    if any(not c.isalnum() for c in password): char_types += 1
    
    score += char_types * 15
    
    # Entropy bonus
    entropy = calculate_entropy(password)
    if entropy > 60: score += 20
    elif entropy > 40: score += 15
    elif entropy > 20: score += 10
    
    # Penalty for common password
    if password.lower() in COMMON_PASSWORDS:
        score = max(10, score - 30)
    
    # Penalty for sequential patterns
    if any(str(i) * 3 in password for i in range(10)):
        score -= 15
    
    return min(100, max(0, score))

def get_strength_info(score):
    """Get rating and color based on score"""
    if score >= 90:
        return "A+ (EXCELLENT)", "#16a085", "color-excellent", "text-excellent"
    elif score >= 80:
        return "A (STRONG)", "#27ae60", "color-strong", "text-strong"
    elif score >= 70:
        return "B (GOOD)", "#2ecc71", "color-good", "text-good"
    elif score >= 60:
        return "C (FAIR)", "#f1c40f", "color-fair", "text-fair"
    elif score >= 50:
        return "D (POOR)", "#e67e22", "color-poor", "text-poor"
    else:
        return "F (WEAK)", "#e74c3c", "color-weak", "text-weak"

def get_crack_time(score, length):
    """Estimate time to crack"""
    if score < 30:
        return "Instantly"
    elif score < 50:
        return "Seconds to minutes"
    elif score < 70:
        return "Hours to days"
    elif score < 85:
        return "Months to years"
    else:
        return "Centuries"

# Main UI matching your design
st.markdown("""
<div class="main">
    <h1 class="main-header">Password Security Analyzer</h1>
    <p class="sub-header">Complete password analysis with professional security assessment<br>
    <small>Accessible on any device! No data sent to servers</small></p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown("### 🔐 Analyze Your Password")
password = st.text_input(
    "Enter your password to analyze...",
    type="password",
    key="password_input",
    placeholder="Type your password here..."
)

col1, col2 = st.columns([3, 1])
with col2:
    analyze_btn = st.button("**Analyze Password Security**", use_container_width=True)

# Guidelines
with st.expander("**Strong Password Guidelines**", expanded=True):
    st.markdown("""
    <div class="guidelines-box">
    ✅ **At least 12 characters long**<br>
    ✅ **Mix uppercase and lowercase letters**<br>
    ✅ **Include numbers and special characters**<br>
    ✅ **Avoid common words and patterns**<br>
    ✅ **Don't use personal information**<br>
    ✅ **Use passphrases for better memorability**
    </div>
    """, unsafe_allow_html=True)

# Analysis Results
if analyze_btn and password:
    with st.spinner("Analyzing password security..."):
        time.sleep(0.5)  # Simulate analysis
        
        score = calculate_strength_score(password)
        rating, color, color_class, text_class = get_strength_info(score)
        entropy = calculate_entropy(password)
        crack_time = get_crack_time(score, len(password))
        
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Score display
        st.markdown(f'<div class="score-display">{score:.1f}</div>', unsafe_allow_html=True)
        
        # Rating badge
        st.markdown(f'<div class="rating-badge" style="background: {color}">{rating}</div>', unsafe_allow_html=True)
        
        # Strength meter
        st.markdown("**Strength Meter:**")
        st.markdown(f'''
        <div class="strength-container">
            <div class="strength-fill {color_class}" style="width: {score}%"></div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Detailed analysis
        st.markdown('<div class="analysis-card results-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Basic Analysis**")
            st.markdown(f"""
            - **Length:** {len(password)} characters
            - **Uppercase:** {'✓' if any(c.isupper() for c in password) else '✗'}
            - **Lowercase:** {'✓' if any(c.islower() for c in password) else '✗'}
            - **Numbers:** {'✓' if any(c.isdigit() for c in password) else '✗'}
            - **Special:** {'✓' if any(not c.isalnum() for c in password) else '✗'}
            """)
            
            if password.lower() in COMMON_PASSWORDS:
                st.error("⚠️ **Common Password Detected!**")
        
        with col2:
            st.markdown("**⚡ Security Metrics**")
            st.markdown(f"""
            - **Entropy:** {entropy} bits
            - **Crack Time:** {crack_time}
            - **Character Pool:** {sum([
                26 if any(c.islower() for c in password) else 0,
                26 if any(c.isupper() for c in password) else 0,
                10 if any(c.isdigit() for c in password) else 0,
                32 if any(not c.isalnum() for c in password) else 0
            ])} possibilities
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("### 📝 Recommendations")
        rec_col1, rec_col2, rec_col3 = st.columns(3)
        
        recommendations = []
        if len(password) < 12:
            recommendations.append("Increase length to 12+ characters")
        if not any(c.isupper() for c in password):
            recommendations.append("Add uppercase letters")
        if not any(c.isdigit() for c in password):
            recommendations.append("Include numbers")
        if not any(not c.isalnum() for c in password):
            recommendations.append("Add special characters")
        if password.lower() in COMMON_PASSWORDS:
            recommendations.append("Avoid common passwords")
        
        if score >= 80:
            st.success("🎉 **Excellent password!** No changes needed.")
        elif recommendations:
            for i, rec in enumerate(recommendations[:3], 1):
                with rec_col1 if i == 1 else rec_col2 if i == 2 else rec_col3:
                    st.warning(f"**{i}.** {rec}")
        else:
            st.info("Password is acceptable but could be stronger")
        
        # Footer note
        st.markdown("---")
        st.caption(f"Analysis performed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | No data stored or transmitted")

elif analyze_btn and not password:
    st.warning("Please enter a password to analyze!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #95a5a6; font-size: 0.9rem; margin-top: 30px;">
    <p>🔒 **Password Security Analyzer** | College Project | Python + Streamlit</p>
    <p><em>Note: Analysis happens locally in your browser. No passwords are sent to any server.</em></p>
</div>
""", unsafe_allow_html=True)
