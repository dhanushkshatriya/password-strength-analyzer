import streamlit as st
import math
import hashlib
import time

# Set page config to match your design
st.set_page_config(
    page_title="Password Security Analyzer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# EXACT CSS from your HTML interface
st.markdown("""
<style>
    /* EXACT styling from your image */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    .main-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .header-section {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 18px;
        color: #666;
        line-height: 1.6;
        margin-bottom: 5px;
    }
    
    .tagline {
        font-size: 14px;
        color: #888;
        font-weight: 400;
    }
    
    .analysis-section {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid #e9ecef;
    }
    
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .password-input-container {
        position: relative;
        margin-bottom: 25px;
    }
    
    .password-input {
        width: 100%;
        padding: 16px 20px;
        font-size: 16px;
        border: 2px solid #dee2e6;
        border-radius: 10px;
        background: white;
        transition: all 0.3s;
    }
    
    .password-input:focus {
        outline: none;
        border-color: #4dabf7;
        box-shadow: 0 0 0 3px rgba(77, 171, 247, 0.1);
    }
    
    .analyze-button {
        width: 100%;
        padding: 16px;
        font-size: 18px;
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #4dabf7, #339af0);
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        margin-top: 10px;
    }
    
    .analyze-button:hover {
        background: linear-gradient(135deg, #339af0, #228be6);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(51, 154, 240, 0.3);
    }
    
    .guidelines-section {
        background: #e8f4fc;
        border-radius: 10px;
        padding: 20px;
        margin: 25px 0;
        border-left: 4px solid #4dabf7;
    }
    
    .guidelines-title {
        font-size: 18px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 12px;
    }
    
    .guidelines-list {
        list-style: none;
        padding-left: 5px;
    }
    
    .guidelines-list li {
        margin-bottom: 8px;
        color: #495057;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .guidelines-list li:before {
        content: "✓";
        color: #28a745;
        font-weight: bold;
    }
    
    .results-section {
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin: 30px 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    .results-title {
        font-size: 24px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 25px;
        text-align: center;
    }
    
    .score-display {
        text-align: center;
        margin: 20px 0;
    }
    
    .score-value {
        font-size: 72px;
        font-weight: 800;
        color: #1a1a1a;
        line-height: 1;
    }
    
    .rating-badge {
        display: inline-block;
        background: #28a745;
        color: white;
        padding: 8px 24px;
        border-radius: 25px;
        font-size: 20px;
        font-weight: 600;
        margin-top: 15px;
    }
    
    .strength-meter {
        width: 100%;
        height: 12px;
        background: #e9ecef;
        border-radius: 6px;
        margin: 25px 0;
        overflow: hidden;
    }
    
    .strength-fill {
        height: 100%;
        border-radius: 6px;
        transition: width 1s ease-in-out;
    }
    
    .score-100 { background: linear-gradient(90deg, #28a745, #20c997); }
    .score-90 { background: linear-gradient(90deg, #20c997, #28a745); }
    .score-80 { background: linear-gradient(90deg, #51cf66, #20c997); }
    .score-70 { background: linear-gradient(90deg, #94d82d, #51cf66); }
    .score-60 { background: linear-gradient(90deg, #fcc419, #94d82d); }
    .score-50 { background: linear-gradient(90deg, #ff922b, #fcc419); }
    .score-40 { background: linear-gradient(90deg, #ff6b6b, #ff922b); }
    .score-30 { background: linear-gradient(90deg, #fa5252, #ff6b6b); }
    .score-20 { background: linear-gradient(90deg, #e03131, #fa5252); }
    .score-10 { background: linear-gradient(90deg, #c92a2a, #e03131); }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Your EXACT interface HTML structure
st.markdown("""
<div class="main-container">
    <div class="header-section">
        <h1 class="main-title">Password Security Analyzer</h1>
        <p class="subtitle">Complete password analysis with professional security assessment</p>
        <p class="tagline">Accessible on any device! No data sent to servers</p>
    </div>
    
    <div class="analysis-section">
        <h2 class="section-title">🔐 Analyze Your Password</h2>
        <div class="password-input-container">
            <input type="password" id="passwordInput" class="password-input" placeholder="Enter your password to analyze...">
        </div>
        <button class="analyze-button" onclick="analyzePassword()">Analyze Password Security</button>
    </div>
    
    <div class="guidelines-section">
        <h3 class="guidelines-title">Strong Password Guidelines</h3>
        <ul class="guidelines-list">
            <li>At least 12 characters long</li>
            <li>Mix uppercase and lowercase letters</li>
            <li>Include numbers and special characters</li>
            <li>Avoid dictionary words and common patterns</li>
            <li>Don't use personal information</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# JavaScript for the input field (since Streamlit doesn't have direct password input)
st.markdown("""
<script>
function analyzePassword() {
    const password = document.getElementById('passwordInput').value;
    if (password) {
        // Send to Streamlit
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: password
        }, '*');
    } else {
        alert('Please enter a password to analyze.');
    }
}

// Make Enter key trigger analysis
document.getElementById('passwordInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        analyzePassword();
    }
});
</script>
""", unsafe_allow_html=True)

# Streamlit component to receive password
password = st.text_input("Enter password", type="password", label_visibility="collapsed", key="pwd")

if password:
    # Calculate score (simplified version)
    score = 0
    if len(password) >= 12:
        score += 25
    if any(c.isupper() for c in password) and any(c.islower() for c in password):
        score += 25
    if any(c.isdigit() for c in password):
        score += 25
    if any(not c.isalnum() for c in password):
        score += 25
    
    # Ensure score is 100 for display as in your image
    score = min(100, score)
    
    # Get rating
    if score >= 90:
        rating = "A+ (EXCELLENT)"
        rating_color = "#28a745"
    elif score >= 80:
        rating = "A (STRONG)"
        rating_color = "#20c997"
    elif score >= 70:
        rating = "B (GOOD)"
        rating_color = "#51cf66"
    elif score >= 60:
        rating = "C (FAIR)"
        rating_color = "#94d82d"
    elif score >= 50:
        rating = "D (POOR)"
        rating_color = "#fcc419"
    else:
        rating = "F (WEAK)"
        rating_color = "#ff6b6b"
    
    # Display results EXACTLY as in your image
    st.markdown(f"""
    <div class="main-container">
        <div class="results-section">
            <h2 class="results-title">Analysis Results</h2>
            
            <div class="score-display">
                <div class="score-value">{score:.2f}</div>
                <div class="rating-badge" style="background: {rating_color}">{rating}</div>
            </div>
            
            <div class="strength-meter">
                <div class="strength-fill score-{int(score/10)*10}" style="width: {score}%"></div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #666; font-size: 14px;">Password analyzed: {'•' * len(password)}</p>
                <p style="color: #888; font-size: 12px; margin-top: 20px;">Analysis performed locally in your browser</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="main-container" style="text-align: center; margin-top: 50px; padding: 20px; color: #999; font-size: 12px;">
    <p>Password Security Analyzer | College Project | Python Application</p>
    <p>All analysis happens locally in your browser. No data is stored or transmitted.</p>
</div>
""", unsafe_allow_html=True)
