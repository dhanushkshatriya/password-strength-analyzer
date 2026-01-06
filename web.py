import http.server
import socketserver
import webbrowser
import socket
import threading
import os
import sys
from datetime import datetime


# Get local IP address for network access
def get_local_ip():
    """Get the local IP address of the computer"""
    try:
        # Create a socket connection to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_public_ip():
    """Try to get public IP (for informational purposes)"""
    try:
        import urllib.request
        return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    except:
        return "Not available"


# Complete HTML, CSS, and JavaScript
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Security Analyzer</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 25px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(0, 180, 219, 0.3);
        }

        h1 {
            font-size: 2.8rem;
            margin-bottom: 10px;
            background: linear-gradient(to right, #00b4db, #0083b0);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .tagline {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 15px;
        }

        .access-info {
            background: rgba(0, 180, 219, 0.1);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.9rem;
            margin-top: 15px;
            border-left: 4px solid #00b4db;
        }

        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        @media (max-width: 900px) {
            .main-content {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 2.2rem;
            }
        }

        .input-section, .results-section {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .input-section h2, .results-section h2 {
            margin-bottom: 20px;
            color: #00b4db;
            border-bottom: 2px solid #00b4db;
            padding-bottom: 10px;
            font-size: 1.8rem;
        }

        .password-input-container {
            position: relative;
            margin-bottom: 25px;
        }

        #passwordInput {
            width: 100%;
            padding: 18px 60px 18px 20px;
            border-radius: 12px;
            border: 2px solid #0083b0;
            background: rgba(255, 255, 255, 0.08);
            color: white;
            font-size: 1.1rem;
            transition: all 0.3s;
        }

        #passwordInput:focus {
            outline: none;
            border-color: #00b4db;
            box-shadow: 0 0 15px rgba(0, 180, 219, 0.4);
            background: rgba(255, 255, 255, 0.12);
        }

        .toggle-password {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #00b4db;
            cursor: pointer;
            font-size: 1.3rem;
            padding: 5px;
            border-radius: 5px;
            transition: all 0.3s;
        }

        .toggle-password:hover {
            background: rgba(0, 180, 219, 0.1);
        }

        .analyze-btn {
            background: linear-gradient(to right, #00b4db, #0083b0);
            color: white;
            border: none;
            padding: 18px 30px;
            border-radius: 12px;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .analyze-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
        }

        .analyze-btn:active {
            transform: translateY(0);
        }

        .analyze-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .password-rules {
            background: rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 25px;
            margin-top: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .password-rules h3 {
            margin-bottom: 20px;
            color: #00b4db;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .rules-list {
            list-style: none;
        }

        .rules-list li {
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .rules-list li:last-child {
            border-bottom: none;
        }

        .rules-list i {
            margin-right: 15px;
            width: 20px;
            font-size: 1.1rem;
        }

        .results-section {
            display: none;
        }

        .strength-meter {
            height: 22px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 11px;
            overflow: hidden;
            margin: 25px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .strength-fill {
            height: 100%;
            width: 0%;
            border-radius: 11px;
            transition: width 1s ease, background 1s ease;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
        }

        .score-display {
            text-align: center;
            margin: 25px 0;
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
        }

        .score-value {
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .score-rating {
            font-size: 1.6rem;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .details-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 25px 0;
        }

        .detail-box {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            transition: all 0.3s;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .detail-box:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }

        .detail-box i {
            font-size: 2rem;
            margin-bottom: 15px;
            color: #00b4db;
        }

        .detail-box div:first-of-type {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 8px;
        }

        .detail-value {
            font-size: 1.4rem;
            font-weight: bold;
            margin-top: 5px;
        }

        .risk-box {
            padding: 25px;
            border-radius: 12px;
            margin: 25px 0;
            text-align: center;
            border: 2px solid transparent;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .risk-box h3 {
            margin-bottom: 15px;
            font-size: 1.4rem;
        }

        .risk-box p {
            font-size: 1.1rem;
            line-height: 1.5;
        }

        .recommendations {
            background: rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 25px;
            margin-top: 25px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .recommendations h3 {
            margin-bottom: 20px;
            color: #00b4db;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .recommendations ul {
            list-style: none;
        }

        .recommendations li {
            margin-bottom: 15px;
            padding: 12px 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border-left: 4px solid #00b4db;
            transition: all 0.3s;
        }

        .recommendations li:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(5px);
        }

        .charts-section {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            margin-top: 40px;
        }

        @media (max-width: 900px) {
            .charts-section {
                grid-template-columns: 1fr;
            }

            .details-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        @media (max-width: 600px) {
            .details-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            h1 {
                font-size: 1.8rem;
            }

            .input-section, .results-section {
                padding: 20px;
            }
        }

        .chart-container {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .chart-container h3 {
            margin-bottom: 20px;
            color: #00b4db;
            text-align: center;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        canvas {
            width: 100% !important;
            height: 320px !important;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            padding: 25px;
            opacity: 0.8;
            font-size: 0.9rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .loading {
            display: none;
            text-align: center;
            margin: 25px 0;
        }

        .loading-spinner {
            border: 5px solid rgba(255, 255, 255, 0.1);
            border-top: 5px solid #00b4db;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .section-title {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
        }

        .section-title i {
            margin-right: 15px;
            font-size: 1.8rem;
            color: #00b4db;
        }

        .policy-compliance {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .policy-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .policy-name {
            font-weight: bold;
            margin-bottom: 10px;
            color: #00b4db;
        }

        .policy-bar {
            height: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .policy-fill {
            height: 100%;
            border-radius: 5px;
            transition: width 1.5s ease;
        }

        .policy-status {
            font-size: 0.9rem;
            font-weight: bold;
        }

        .color-red { color: #e74c3c; }
        .color-orange { color: #f39c12; }
        .color-yellow { color: #f1c40f; }
        .color-green { color: #2ecc71; }
        .color-blue { color: #3498db; }
        .color-dark-green { color: #27ae60; }

        .risk-critical { background: linear-gradient(135deg, #c0392b, #e74c3c); }
        .risk-high { background: linear-gradient(135deg, #e74c3c, #f39c12); }
        .risk-medium { background: linear-gradient(135deg, #f39c12, #f1c40f); }
        .risk-low { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .risk-very-low { background: linear-gradient(135deg, #27ae60, #16a085); }

        .crack-time-box {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 18px;
            margin-bottom: 15px;
            border-left: 4px solid;
            transition: all 0.3s;
        }

        .crack-time-box:hover {
            transform: translateX(5px);
            background: rgba(255, 255, 255, 0.08);
        }

        .crack-time-title {
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 1rem;
        }

        .crack-time-value {
            font-size: 1.2rem;
            font-weight: bold;
        }

        .fa-check-circle { color: #2ecc71; }
        .fa-times-circle { color: #e74c3c; }
        .fa-exclamation-triangle { color: #f39c12; }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-left: 10px;
        }

        .badge-critical { background: #c0392b; }
        .badge-high { background: #e74c3c; }
        .badge-medium { background: #f39c12; }
        .badge-low { background: #2ecc71; }

        .qr-container {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
        }

        .qr-info {
            font-size: 0.8rem;
            margin-top: 10px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-shield-alt"></i> Password Security Analyzer</h1>
            <p class="tagline">Complete password analysis with professional security assessment</p>
            <div class="access-info">
                <i class="fas fa-mobile-alt"></i> Accessible on any device | <i class="fas fa-lock"></i> No data sent to servers
            </div>
        </header>

        <div class="main-content">
            <div class="input-section">
                <div class="section-title">
                    <i class="fas fa-key"></i>
                    <h2>Analyze Your Password</h2>
                </div>

                <div class="password-input-container">
                    <input type="password" id="passwordInput" placeholder="Enter your password to analyze...">
                    <button class="toggle-password" id="togglePassword" type="button" aria-label="Toggle password visibility">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>

                <button class="analyze-btn" id="analyzeBtn">
                    <i class="fas fa-search"></i> Analyze Password Security
                </button>

                <div class="loading" id="loading">
                    <div class="loading-spinner"></div>
                    <p>Analyzing password security...</p>
                </div>

                <div class="password-rules">
                    <h3><i class="fas fa-clipboard-check"></i> Strong Password Guidelines</h3>
                    <ul class="rules-list">
                        <li><i class="fas fa-check-circle color-green"></i> At least 12 characters long</li>
                        <li><i class="fas fa-check-circle color-green"></i> Mix of uppercase and lowercase letters</li>
                        <li><i class="fas fa-check-circle color-green"></i> Includes numbers (0-9)</li>
                        <li><i class="fas fa-check-circle color-green"></i> Includes special characters (!@#$%^&*)</li>
                        <li><i class="fas fa-times-circle color-red"></i> Not a common password</li>
                    </ul>
                </div>
            </div>

            <div class="results-section" id="resultsSection">
                <div class="section-title">
                    <i class="fas fa-chart-bar"></i>
                    <h2>Analysis Results</h2>
                </div>

                <div class="score-display">
                    <div class="score-value" id="scoreValue">0</div>
                    <div class="score-rating" id="scoreRating">VERY POOR</div>
                </div>

                <div class="strength-meter">
                    <div class="strength-fill" id="strengthFill"></div>
                </div>

                <div class="details-grid">
                    <div class="detail-box">
                        <i class="fas fa-ruler"></i>
                        <div>Length</div>
                        <div class="detail-value" id="lengthValue">0</div>
                    </div>
                    <div class="detail-box">
                        <i class="fas fa-font"></i>
                        <div>Uppercase</div>
                        <div class="detail-value" id="uppercaseValue">No</div>
                    </div>
                    <div class="detail-box">
                        <i class="fas fa-text-height"></i>
                        <div>Lowercase</div>
                        <div class="detail-value" id="lowercaseValue">No</div>
                    </div>
                    <div class="detail-box">
                        <i class="fas fa-hashtag"></i>
                        <div>Numbers</div>
                        <div class="detail-value" id="numbersValue">No</div>
                    </div>
                    <div class="detail-box">
                        <i class="fas fa-asterisk"></i>
                        <div>Special</div>
                        <div class="detail-value" id="specialValue">No</div>
                    </div>
                    <div class="detail-box">
                        <i class="fas fa-brain"></i>
                        <div>Entropy</div>
                        <div class="detail-value" id="entropyValue">0 bits</div>
                    </div>
                </div>

                <div class="risk-box" id="riskBox">
                    <h3>Risk Assessment</h3>
                    <p id="riskText">Enter a password to analyze</p>
                </div>

                <div class="recommendations" id="recommendations">
                    <h3><i class="fas fa-lightbulb"></i> Security Recommendations</h3>
                    <ul id="recommendationsList">
                        <li>Enter a password to get recommendations</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="charts-section" id="chartsSection">
            <div class="chart-container">
                <h3><i class="fas fa-gauge-high"></i> Strength Gauge</h3>
                <canvas id="strengthGauge"></canvas>
            </div>

            <div class="chart-container">
                <h3><i class="fas fa-clock"></i> Crack Time Comparison</h3>
                <canvas id="crackTimeChart"></canvas>
            </div>

            <div class="chart-container">
                <h3><i class="fas fa-puzzle-piece"></i> Security Components</h3>
                <canvas id="componentsChart"></canvas>
            </div>

            <div class="chart-container">
                <h3><i class="fas fa-shield-check"></i> Policy Compliance</h3>
                <div class="policy-compliance" id="policyCompliance">
                    <div class="policy-item">
                        <div class="policy-name">Basic</div>
                        <div class="policy-bar">
                            <div class="policy-fill" style="width: 0%; background: #3498db;"></div>
                        </div>
                        <div class="policy-status">0%</div>
                    </div>
                    <div class="policy-item">
                        <div class="policy-name">Standard</div>
                        <div class="policy-bar">
                            <div class="policy-fill" style="width: 0%; background: #2ecc71;"></div>
                        </div>
                        <div class="policy-status">0%</div>
                    </div>
                    <div class="policy-item">
                        <div class="policy-name">Strong</div>
                        <div class="policy-bar">
                            <div class="policy-fill" style="width: 0%; background: #f1c40f;"></div>
                        </div>
                        <div class="policy-status">0%</div>
                    </div>
                    <div class="policy-item">
                        <div class="policy-name">Military</div>
                        <div class="policy-bar">
                            <div class="policy-fill" style="width: 0%; background: #e74c3c;"></div>
                        </div>
                        <div class="policy-status">0%</div>
                    </div>
                </div>

                <div id="crackTimeDetails" style="margin-top: 20px;">
                    <h4>Estimated Crack Times</h4>
                    <div class="crack-time-box" style="border-left-color: #e74c3c;">
                        <div class="crack-time-title">Basic Computer</div>
                        <div class="crack-time-value color-red" id="crackTimeBasic">Instantly</div>
                    </div>
                    <div class="crack-time-box" style="border-left-color: #f39c12;">
                        <div class="crack-time-title">Hacker (GPU)</div>
                        <div class="crack-time-value color-orange" id="crackTimeHacker">Instantly</div>
                    </div>
                    <div class="crack-time-box" style="border-left-color: #f1c40f;">
                        <div class="crack-time-title">Botnet</div>
                        <div class="crack-time-value color-yellow" id="crackTimeBotnet">Instantly</div>
                    </div>
                    <div class="crack-time-box" style="border-left-color: #2ecc71;">
                        <div class="crack-time-title">Supercomputer</div>
                        <div class="crack-time-value color-green" id="crackTimeSuper">Instantly</div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            <p><i class="fas fa-laptop"></i> Password Security Analyzer &copy; 2023 | All calculations performed locally - no data is sent to servers</p>
            <p><i class="fas fa-info-circle"></i> This tool provides estimates based on standard password cracking techniques</p>
        </footer>
    </div>

    <script>
        // DOM Elements
        const passwordInput = document.getElementById('passwordInput');
        const togglePassword = document.getElementById('togglePassword');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const loading = document.getElementById('loading');
        const resultsSection = document.getElementById('resultsSection');
        const chartsSection = document.getElementById('chartsSection');
        const scoreValue = document.getElementById('scoreValue');
        const scoreRating = document.getElementById('scoreRating');
        const strengthFill = document.getElementById('strengthFill');
        const lengthValue = document.getElementById('lengthValue');
        const uppercaseValue = document.getElementById('uppercaseValue');
        const lowercaseValue = document.getElementById('lowercaseValue');
        const numbersValue = document.getElementById('numbersValue');
        const specialValue = document.getElementById('specialValue');
        const entropyValue = document.getElementById('entropyValue');
        const riskBox = document.getElementById('riskBox');
        const riskText = document.getElementById('riskText');
        const recommendationsList = document.getElementById('recommendationsList');
        const policyCompliance = document.getElementById('policyCompliance');
        const crackTimeBasic = document.getElementById('crackTimeBasic');
        const crackTimeHacker = document.getElementById('crackTimeHacker');
        const crackTimeBotnet = document.getElementById('crackTimeBotnet');
        const crackTimeSuper = document.getElementById('crackTimeSuper');

        // Common passwords list
        const commonPasswords = [
            "123456", "password", "12345678", "qwerty", "123456789",
            "12345", "admin", "welcome", "monkey", "dragon", "letmein",
            "football", "iloveyou", "123123", "sunshine", "password1",
            "princess", "abc123", "111111", "000000", "1234", "superman",
            "trustno1", "master", "hello", "charlie", "secret", "123qwe",
            "password123", "admin123", "login", "welcome123", "passw0rd",
            "1234567", "1234567890", "qwerty123", "1q2w3e4r", "qwertyuiop",
            "asdfgh", "zxcvbnm", "password1234", "12345678910"
        ];

        // Chart instances
        let strengthGaugeChart = null;
        let crackTimeChart = null;
        let componentsChart = null;

        // Toggle password visibility
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            const icon = this.querySelector('i');
            icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
            this.setAttribute('aria-label', type === 'password' ? 'Show password' : 'Hide password');
        });

        // Analyze button click handler
        analyzeBtn.addEventListener('click', function() {
            const password = passwordInput.value.trim();

            if (!password) {
                showAlert("Please enter a password to analyze.");
                passwordInput.focus();
                return;
            }

            if (password.length > 100) {
                showAlert("Password is too long. Please enter a password with 100 characters or less.");
                passwordInput.focus();
                return;
            }

            // Show loading state
            loading.style.display = 'block';
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

            // Simulate analysis delay for better UX
            setTimeout(() => {
                try {
                    analyzePassword(password);
                } catch (error) {
                    console.error("Analysis error:", error);
                    showAlert("An error occurred during analysis. Please try again.");
                } finally {
                    // Hide loading state
                    loading.style.display = 'none';
                    analyzeBtn.disabled = false;
                    analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Password Security';
                }
            }, 800);
        });

        // Show alert function
        function showAlert(message) {
            alert(message);
        }

        // Analyze on Enter key press
        passwordInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                analyzeBtn.click();
            }
        });

        // Main analysis function
        function analyzePassword(password) {
            // Show results and charts
            resultsSection.style.display = 'block';
            chartsSection.style.display = 'grid';

            // Scroll to results smoothly
            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);

            // Basic character analysis
            const length = password.length;
            const hasUpper = /[A-Z]/.test(password);
            const hasLower = /[a-z]/.test(password);
            const hasDigit = /\d/.test(password);
            const hasSpecial = /[^A-Za-z0-9]/.test(password);
            const isCommon = commonPasswords.includes(password.toLowerCase());

            // Calculate entropy (rounded to 2 decimal places)
            const entropy = calculateEntropy(password);

            // Calculate strength score
            const scoreResult = calculateScore(password, length, hasUpper, hasLower, hasDigit, hasSpecial, entropy, isCommon);
            const score = scoreResult.score;
            const breakdown = scoreResult.breakdown;

            // Get rating
            const ratingResult = getRating(score);
            const rating = ratingResult.rating;
            const color = ratingResult.color;

            // Estimate crack times
            const crackTimes = estimateCrackTime(entropy);

            // Get recommendations
            const recommendations = getRecommendations(length, hasUpper, hasLower, hasDigit, hasSpecial, score, isCommon);

            // Check policy compliance
            const policies = checkPolicyCompliance(length, hasUpper, hasLower, hasDigit, hasSpecial);

            // Assess risk
            const risk = assessRisk(score, isCommon);

            // Update UI with results
            updateUI(password, length, hasUpper, hasLower, hasDigit, hasSpecial, 
                    entropy, score, rating, color, crackTimes, recommendations, 
                    policies, risk, breakdown);

            // Create visual charts
            createCharts(score, rating, color, crackTimes, breakdown);
        }

        // Calculate password entropy in bits (rounded to 2 decimal places)
        function calculateEntropy(password) {
            if (!password || password.length === 0) return 0;

            let poolSize = 0;
            if (/[a-z]/.test(password)) poolSize += 26;
            if (/[A-Z]/.test(password)) poolSize += 26;
            if (/\d/.test(password)) poolSize += 10;
            if (/[^A-Za-z0-9]/.test(password)) poolSize += 32;

            if (poolSize === 0) return 0;

            // Calculate and round to 2 decimal places
            const entropy = Math.log2(Math.pow(poolSize, password.length));
            return Math.round(entropy * 100) / 100;
        }

        // Calculate strength score (0-100)
        function calculateScore(password, length, hasUpper, hasLower, hasDigit, hasSpecial, entropy, isCommon) {
            let score = 0;
            const breakdown = {};

            // Length score (max 30)
            const lengthScore = Math.min(30, length * 3);
            score += lengthScore;
            breakdown.length = Math.round(lengthScore * 100) / 100;

            // Character variety (max 40)
            let varietyScore = 0;
            if (hasUpper) varietyScore += 10;
            if (hasLower) varietyScore += 10;
            if (hasDigit) varietyScore += 10;
            if (hasSpecial) varietyScore += 10;
            score += varietyScore;
            breakdown.variety = varietyScore;

            // Bonus for mixed case (10)
            if (hasUpper && hasLower) {
                score += 10;
                breakdown.mixedCase = 10;
            }

            // Entropy bonus (max 20)
            const entropyScore = Math.min(20, entropy / 5);
            score += entropyScore;
            breakdown.entropy = Math.round(entropyScore * 100) / 100;

            // Penalty for common password
            if (isCommon) {
                score = Math.max(10, score - 30);
                breakdown.commonPenalty = -30;
            }

            // Ensure score is between 0-100 and round to 2 decimal places
            score = Math.max(0, Math.min(100, Math.round(score * 100) / 100));

            return { score, breakdown };
        }

        // Get rating based on score
        function getRating(score) {
            if (score >= 80) {
                return { rating: "A+ (EXCELLENT)", color: "#27ae60" };
            } else if (score >= 70) {
                return { rating: "A (VERY GOOD)", color: "#2ecc71" };
            } else if (score >= 60) {
                return { rating: "B (GOOD)", color: "#f1c40f" };
            } else if (score >= 50) {
                return { rating: "C (FAIR)", color: "#f39c12" };
            } else if (score >= 40) {
                return { rating: "D (POOR)", color: "#e67e22" };
            } else {
                return { rating: "F (VERY POOR)", color: "#e74c3c" };
            }
        }

        // Estimate crack time for different attackers
        function estimateCrackTime(entropy) {
            const attackers = {
                "Basic Computer": { speed: 1000 },
                "Hacker (GPU)": { speed: 1000000 },
                "Botnet": { speed: 1000000000 },
                "Supercomputer": { speed: 1000000000000 }
            };

            const results = {};
            const totalCombinations = Math.pow(2, entropy);

            Object.entries(attackers).forEach(([name, att]) => {
                let seconds = totalCombinations / att.speed;

                let timeStr, color;

                if (seconds < 1) {
                    timeStr = "Instantly";
                    color = "#e74c3c";
                } else if (seconds < 60) {
                    timeStr = `${seconds.toFixed(1)} seconds`;
                    color = "#e74c3c";
                } else if (seconds < 3600) {
                    const minutes = seconds / 60;
                    timeStr = minutes < 2 ? `${minutes.toFixed(1)} minute` : `${minutes.toFixed(1)} minutes`;
                    color = "#f39c12";
                } else if (seconds < 86400) {
                    const hours = seconds / 3600;
                    timeStr = hours < 2 ? `${hours.toFixed(1)} hour` : `${hours.toFixed(1)} hours`;
                    color = "#f1c40f";
                } else if (seconds < 31536000) {
                    const days = seconds / 86400;
                    timeStr = days < 2 ? `${days.toFixed(1)} day` : `${days.toFixed(1)} days`;
                    color = "#2ecc71";
                } else {
                    const years = seconds / 31536000;
                    timeStr = years < 2 ? `${years.toFixed(1)} year` : `${years.toFixed(1)} years`;
                    color = years < 100 ? "#27ae60" : "#3498db";
                }

                results[name] = { time: timeStr, color };
            });

            return results;
        }

        // Generate security recommendations
        function getRecommendations(length, hasUpper, hasLower, hasDigit, hasSpecial, score, isCommon) {
            const recs = [];

            if (isCommon) {
                recs.push({ priority: "CRITICAL", text: "CHANGE PASSWORD - It's in common password lists" });
            }

            if (length < 8) {
                recs.push({ priority: "HIGH", text: `Increase length from ${length} to at least 8 characters` });
            } else if (length < 12) {
                recs.push({ priority: "MEDIUM", text: `Increase length from ${length} to 12+ characters` });
            }

            if (!hasUpper) {
                recs.push({ priority: "MEDIUM", text: "Add uppercase letters (A-Z)" });
            }

            if (!hasLower) {
                recs.push({ priority: "MEDIUM", text: "Add lowercase letters (a-z)" });
            }

            if (!hasDigit) {
                recs.push({ priority: "MEDIUM", text: "Add numbers (0-9)" });
            }

            if (!hasSpecial) {
                recs.push({ priority: "HIGH", text: "Add special characters (!@#$%^&*)" });
            }

            if (score < 60) {
                recs.push({ priority: "LOW", text: "Consider using a passphrase (e.g., 'CorrectHorseBatteryStaple')" });
            }

            // If no recommendations and password is weak, add generic one
            if (recs.length === 0 && score < 70) {
                recs.push({ priority: "LOW", text: "Your password is decent but could be improved with more length" });
            }

            // Sort by priority
            const priorityOrder = { "CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3 };
            recs.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);

            return recs.slice(0, 6);
        }

        // Check policy compliance
        function checkPolicyCompliance(length, hasUpper, hasLower, hasDigit, hasSpecial) {
            const policies = {
                "Basic": { minLength: 6, requires: [] },
                "Standard": { minLength: 8, requires: ["upper", "lower", "digit"] },
                "Strong": { minLength: 12, requires: ["upper", "lower", "digit", "special"] },
                "Military": { minLength: 16, requires: ["upper", "lower", "digit", "special"] }
            };

            const compliance = {};

            Object.entries(policies).forEach(([name, policy]) => {
                let passed = 0;
                let total = 0;

                // Length check
                total++;
                if (length >= policy.minLength) passed++;

                // Character requirements
                policy.requires.forEach(req => {
                    total++;
                    if (req === "upper" && hasUpper) passed++;
                    if (req === "lower" && hasLower) passed++;
                    if (req === "digit" && hasDigit) passed++;
                    if (req === "special" && hasSpecial) passed++;
                });

                const percentage = total > 0 ? (passed / total) * 100 : 0;
                compliance[name] = {
                    passed,
                    total,
                    percentage: Math.round(percentage),
                    compliant: percentage === 100
                };
            });

            return compliance;
        }

        // Assess risk level
        function assessRisk(score, isCommon) {
            if (isCommon) {
                return {
                    level: "CRITICAL",
                    description: "This password is in common password lists and can be cracked instantly",
                    color: "#c0392b",
                    action: "CHANGE PASSWORD IMMEDIATELY"
                };
            }

            if (score >= 80) {
                return {
                    level: "VERY LOW",
                    description: "Excellent password security - very difficult to crack",
                    color: "#27ae60",
                    action: "Password is secure"
                };
            } else if (score >= 70) {
                return {
                    level: "LOW",
                    description: "Good password security - adequate for most purposes",
                    color: "#2ecc71",
                    action: "Password is acceptable"
                };
            } else if (score >= 60) {
                return {
                    level: "MODERATE",
                    description: "Moderate security risk - could be improved",
                    color: "#f1c40f",
                    action: "Consider improving password"
                };
            } else if (score >= 50) {
                return {
                    level: "MEDIUM",
                    description: "Medium security risk - vulnerable to determined attackers",
                    color: "#f39c12",
                    action: "Improve password soon"
                };
            } else if (score >= 40) {
                return {
                    level: "HIGH",
                    description: "High security risk - vulnerable to basic attacks",
                    color: "#e67e22",
                    action: "Change password as soon as possible"
                };
            } else {
                return {
                    level: "VERY HIGH",
                    description: "Very high security risk - can be cracked quickly",
                    color: "#e74c3c",
                    action: "CHANGE PASSWORD IMMEDIATELY"
                };
            }
        }

        // Update UI with results
        function updateUI(password, length, hasUpper, hasLower, hasDigit, hasSpecial, 
                         entropy, score, rating, color, crackTimes, recommendations, 
                         policies, risk, breakdown) {
            // Update score and rating
            scoreValue.textContent = score.toFixed(2);
            scoreRating.textContent = rating;
            scoreRating.style.color = color;

            // Update strength meter
            strengthFill.style.width = `${score}%`;
            strengthFill.style.background = color;

            // Update basic details
            lengthValue.textContent = length;
            uppercaseValue.textContent = hasUpper ? "Yes" : "No";
            uppercaseValue.style.color = hasUpper ? "#2ecc71" : "#e74c3c";
            lowercaseValue.textContent = hasLower ? "Yes" : "No";
            lowercaseValue.style.color = hasLower ? "#2ecc71" : "#e74c3c";
            numbersValue.textContent = hasDigit ? "Yes" : "No";
            numbersValue.style.color = hasDigit ? "#2ecc71" : "#e74c3c";
            specialValue.textContent = hasSpecial ? "Yes" : "No";
            specialValue.style.color = hasSpecial ? "#2ecc71" : "#e74c3c";
            entropyValue.textContent = `${entropy.toFixed(2)} bits`;

            // Update risk assessment
            riskBox.style.background = risk.color;
            riskText.innerHTML = `<strong style="font-size: 1.2em;">${risk.level}</strong><br>${risk.description}<br><br><em style="font-weight: bold;">${risk.action}</em>`;

            // Update recommendations
            recommendationsList.innerHTML = '';
            if (recommendations.length > 0) {
                recommendations.forEach(rec => {
                    const li = document.createElement('li');
                    const badgeClass = rec.priority.toLowerCase();
                    li.innerHTML = `<strong>[${rec.priority}]</strong> ${rec.text}`;
                    recommendationsList.appendChild(li);
                });
            } else {
                recommendationsList.innerHTML = '<li style="color: #2ecc71;"><i class="fas fa-check-circle"></i> Your password meets all security guidelines!</li>';
            }

            // Update policy compliance
            const policyItems = policyCompliance.querySelectorAll('.policy-item');
            let i = 0;
            for (const [name, data] of Object.entries(policies)) {
                const item = policyItems[i];
                const fill = item.querySelector('.policy-fill');
                const status = item.querySelector('.policy-status');

                fill.style.width = `${data.percentage}%`;
                status.textContent = `${data.percentage}%`;
                status.style.color = data.compliant ? '#2ecc71' : '#e74c3c';

                i++;
            }

            // Update crack time details
            crackTimeBasic.textContent = crackTimes["Basic Computer"].time;
            crackTimeBasic.style.color = crackTimes["Basic Computer"].color;

            crackTimeHacker.textContent = crackTimes["Hacker (GPU)"].time;
            crackTimeHacker.style.color = crackTimes["Hacker (GPU)"].color;

            crackTimeBotnet.textContent = crackTimes["Botnet"].time;
            crackTimeBotnet.style.color = crackTimes["Botnet"].color;

            crackTimeSuper.textContent = crackTimes["Supercomputer"].time;
            crackTimeSuper.style.color = crackTimes["Supercomputer"].color;
        }

        // Create charts
        function createCharts(score, rating, color, crackTimes, breakdown) {
            // Destroy existing charts if they exist
            if (strengthGaugeChart) strengthGaugeChart.destroy();
            if (crackTimeChart) crackTimeChart.destroy();
            if (componentsChart) componentsChart.destroy();

            // 1. Strength Gauge Chart
            const gaugeCtx = document.getElementById('strengthGauge').getContext('2d');
            strengthGaugeChart = new Chart(gaugeCtx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [score, 100 - score],
                        backgroundColor: [color, 'rgba(255, 255, 255, 0.1)'],
                        borderWidth: 0
                    }]
                },
                options: {
                    circumference: 180,
                    rotation: -90,
                    cutout: '75%',
                    plugins: {
                        legend: { display: false },
                        tooltip: { 
                            enabled: true,
                            callbacks: {
                                label: function(context) {
                                    return `Score: ${score.toFixed(2)}/100`;
                                }
                            }
                        }
                    },
                    animation: { animateRotate: true, animateScale: true }
                },
                plugins: [{
                    id: 'centerText',
                    afterDraw: (chart) => {
                        const { ctx, chartArea: { left, right, top, bottom, width, height } } = chart;
                        const centerX = (left + right) / 2;
                        const centerY = (top + bottom) / 2 + 20;

                        ctx.save();
                        ctx.font = 'bold 24px Arial';
                        ctx.fillStyle = color;
                        ctx.textAlign = 'center';
                        ctx.fillText(`${score.toFixed(2)}/100`, centerX, centerY);

                        ctx.font = '16px Arial';
                        ctx.fillStyle = '#fff';
                        ctx.fillText('SCORE', centerX, centerY + 30);
                        ctx.restore();
                    }
                }]
            });

            // 2. Crack Time Chart
            const crackTimeCtx = document.getElementById('crackTimeChart').getContext('2d');
            const attackers = Object.keys(crackTimes);
            const times = attackers.map(a => {
                const time = crackTimes[a].time;
                if (time === "Instantly") return 0.1;
                if (time.includes("seconds")) return parseFloat(time) / 10;
                if (time.includes("minutes")) return parseFloat(time) * 6;
                if (time.includes("hours")) return parseFloat(time) * 360;
                if (time.includes("days")) return parseFloat(time) * 8640;
                if (time.includes("years")) return parseFloat(time) * 31536000;
                return 1;
            });
            const colors = attackers.map(a => crackTimes[a].color);

            crackTimeChart = new Chart(crackTimeCtx, {
                type: 'bar',
                data: {
                    labels: attackers,
                    datasets: [{
                        label: 'Crack Time (log scale)',
                        data: times,
                        backgroundColor: colors,
                        borderColor: colors.map(c => c.replace('0.7', '1')),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            type: 'logarithmic',
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#fff', callback: value => {
                                if (value <= 1) return "Instantly";
                                if (value < 60) return `${value}s`;
                                if (value < 3600) return `${Math.round(value/60)}m`;
                                if (value < 86400) return `${Math.round(value/3600)}h`;
                                if (value < 31536000) return `${Math.round(value/86400)}d`;
                                return `${Math.round(value/31536000)}y`;
                            }}
                        },
                        x: {
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            ticks: { color: '#fff', font: { size: 11 } }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: (context) => {
                                    const label = context.dataset.label || '';
                                    const attacker = context.label;
                                    return `${attacker}: ${crackTimes[attacker].time}`;
                                }
                            }
                        }
                    }
                }
            });

            // 3. Security Components Chart
            const componentsCtx = document.getElementById('componentsChart').getContext('2d');
            const componentLabels = Object.keys(breakdown).map(key => 
                key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
            );
            const componentData = Object.values(breakdown);
            const componentColors = ['#3498db', '#2ecc71', '#9b59b6', '#f1c40f', '#e74c3c', '#1abc9c'];

            // Filter out zero or negative values for the pie chart
            const filteredLabels = [];
            const filteredData = [];
            const filteredColors = [];

            componentData.forEach((value, index) => {
                if (value > 0) {
                    filteredLabels.push(componentLabels[index]);
                    filteredData.push(Math.abs(value));
                    filteredColors.push(componentColors[index]);
                }
            });

            componentsChart = new Chart(componentsCtx, {
                type: 'pie',
                data: {
                    labels: filteredLabels,
                    datasets: [{
                        data: filteredData,
                        backgroundColor: filteredColors,
                        borderColor: 'rgba(0, 0, 0, 0.3)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#fff', padding: 20, font: { size: 12 } }
                        },
                        tooltip: {
                            callbacks: {
                                label: (context) => {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    return `${label}: ${value.toFixed(2)} points`;
                                }
                            }
                        }
                    }
                }
            });
        }

        // Initialize with a sample password for demonstration
        window.addEventListener('DOMContentLoaded', () => {
            // Set a sample password
            passwordInput.value = "MySecureP@ssw0rd!";

            // Trigger analysis after a short delay
            setTimeout(() => {
                analyzeBtn.click();
            }, 1000);
        });
    </script>
</body>
</html>"""


class PasswordAnalyzerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the password analyzer"""

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            # Serve files if they exist
            super().do_GET()

    def log_message(self, format, *args):
        # Suppress default logging
        pass


def check_port_available(port):
    """Check if port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except socket.error:
            return False


def find_available_port(start_port=8080):
    """Find an available port starting from start_port"""
    port = start_port
    while port < start_port + 100:
        if check_port_available(port):
            return port
        port += 1
    return start_port  # Fallback


def print_qr_code(ip, port):
    """Print QR code for easy mobile access"""
    try:
        import qrcode
        from io import StringIO
        import sys

        url = f"http://{ip}:{port}"
        qr = qrcode.QRCode()
        qr.add_data(url)

        # Create QR code in terminal
        f = StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        qr_code = f.read()

        print("\n📱 QR Code for Mobile Access:")
        print("┌" + "─" * 38 + "┐")
        for line in qr_code.split('\n'):
            if line.strip():
                print("│ " + line.ljust(36) + " │")
        print("└" + "─" * 38 + "┘")
        print(f"Scan to open: {url}")

    except ImportError:
        print("\n📱 Mobile Access:")
        print(f"Open browser on your phone and go to:")
        print(f"http://{ip}:{port}")
        print("\n💡 Tip: Install 'qrcode' library for QR code generation:")
        print("pip install qrcode[pil]")


def run_server():
    """Run the password analyzer web server"""
    PORT = find_available_port(8080)
    local_ip = get_local_ip()

    print("═" * 60)
    print("🔐 PASSWORD SECURITY ANALYZER - WEB SERVER")
    print("═" * 60)
    print(f"\n📊 Application Features:")
    print("   • Complete password strength analysis")
    print("   • Interactive charts and visualizations")
    print("   • Mobile-responsive design")
    print("   • Real-time crack time estimation")
    print("   • Security recommendations")
    print("   • Policy compliance checking")

    print(f"\n🌐 Server Information:")
    print(f"   • Local access: http://localhost:{PORT}")
    print(f"   • Network IP: http://{local_ip}:{PORT}")

    # Try to get public IP
    try:
        public_ip = get_public_ip()
        if public_ip != "Not available":
            print(f"   • Public IP: {public_ip} (if port forwarded)")
    except:
        pass

    print("\n📱 Mobile Access Instructions:")
    print("   1. Ensure phone is on same Wi-Fi network")
    print("   2. Open browser on phone")
    print("   3. Enter: http://" + local_ip + f":{PORT}")

    print("\n🚀 Starting server...")

    # Allow external connections by using "0.0.0.0"
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), PasswordAnalyzerHandler) as httpd:
            print(f"✅ Server started successfully on port {PORT}")

            # Print QR code for easy access
            print_qr_code(local_ip, PORT)

            print("\n📝 Sample passwords to try:")
            print("   • Weak: 'password123'")
            print("   • Good: 'MySecureP@ssw0rd!'")
            print("   • Strong: 'C0rrectHorseB@tteryStaple!'")

            print("\n⚠  Security Note:")
            print("   • All calculations happen in your browser")
            print("   • No passwords are sent to any server")
            print("   • Analysis is 100% private and secure")

            print("\n🛑 Press Ctrl+C to stop the server")
            print("═" * 60)

            # Try to open browser automatically
            try:
                webbrowser.open(f"http://localhost:{PORT}")
            except:
                pass

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n\n🛑 Server stopped by user.")
                print("Thank you for using Password Security Analyzer!")

    except PermissionError:
        print(f"\n❌ ERROR: Port {PORT} is already in use or blocked!")
        print("   Try one of these solutions:")
        print("   1. Close other applications using port {PORT}")
        print("   2. Run as administrator (Windows)")
        print("   3. The script will try a different port automatically")

        # Try next port
        PORT = find_available_port(PORT + 1)
        print(f"   Trying port {PORT} instead...")

        # Restart with new port
        os.execv(sys.executable, ['python'] + sys.argv)

    except OSError as e:
        print(f"\n❌ ERROR: {e}")
        print("   Possible solutions:")
        print("   1. Check your firewall settings")
        print("   2. Try running on a different port")
        print("   3. Ensure you have network permissions")


if __name__ == "__main__":
    print("🚀 Starting Password Security Analyzer Web Application...")
    print("📡 Making website accessible from any device on your network...")

    # Check for required libraries
    try:
        import http.server
        import socketserver
    except ImportError:
        print("❌ ERROR: Required libraries not found!")
        print("   This requires Python's standard libraries.")
        sys.exit(1)

    run_server()