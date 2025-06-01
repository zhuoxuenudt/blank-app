# 在check_password函数中替换以下内容
def check_password():
    """返回是否通过密码验证"""
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    # 创建更加炫酷的赛博朋克背景
    st.markdown("""
    <style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .cyberpunk-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            #0d0221 0%, 
            #ff2a6d 25%, 
            #05d9e8 50%, 
            #d300c5 75%, 
            #0d0221 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        z-index: -2;
    }
    
    .grid-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(5, 217, 232, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(5, 217, 232, 0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        z-index: -1;
    }
    
    .cyberpunk-circle {
        position: fixed;
        border-radius: 50%;
        filter: blur(60px);
        opacity: 0.5;
        z-index: -1;
    }
    
    .circle-1 {
        width: 300px;
        height: 300px;
        background: #ff2a6d;
        top: 20%;
        left: 10%;
        animation: float 8s ease-in-out infinite;
    }
    
    .circle-2 {
        width: 400px;
        height: 400px;
        background: #05d9e8;
        bottom: 15%;
        right: 10%;
        animation: float 10s ease-in-out infinite;
    }
    
    .circle-3 {
        width: 200px;
        height: 200px;
        background: #d300c5;
        top: 60%;
        left: 30%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) translateX(0); }
        50% { transform: translateY(-20px) translateX(20px); }
    }
    
    .password-lock {
        position: relative;
        width: 300px;
        height: 400px;
        margin: 0 auto;
        perspective: 1000px;
    }
    
    .lock-body {
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: all 0.5s ease;
    }
    
    .lock-front, .lock-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        background: rgba(13, 2, 33, 0.8);
        border: 2px solid #ff2a6d;
        border-radius: 10px;
        box-shadow: 0 0 20px #ff2a6d, 
                    0 0 40px #05d9e8,
                    inset 0 0 10px rgba(5, 217, 232, 0.3);
        padding: 30px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .lock-back {
        transform: rotateY(180deg);
        background: rgba(255, 42, 109, 0.8);
    }
    
    .lock-title {
        color: #05d9e8;
        text-shadow: 0 0 10px #05d9e8;
        font-size: 24px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .lock-input {
        background: transparent;
        border: 1px solid #05d9e8;
        color: #ff2a6d;
        padding: 15px;
        width: 100%;
        margin-bottom: 20px;
        font-size: 18px;
        text-align: center;
        outline: none;
        box-shadow: 0 0 10px rgba(5, 217, 232, 0.3);
        transition: all 0.3s;
    }
    
    .lock-input:focus {
        border-color: #ff2a6d;
        box-shadow: 0 0 15px #ff2a6d;
    }
    
    .lock-button {
        background: linear-gradient(45deg, #ff2a6d, #d300c5);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.3s;
        box-shadow: 0 0 10px rgba(255, 42, 109, 0.5);
        margin-top: 20px;
    }
    
    .lock-button:hover {
        background: linear-gradient(45deg, #d300c5, #ff2a6d);
        box-shadow: 0 0 20px #ff2a6d;
    }
    
    .lock-indicator {
        width: 100%;
        height: 10px;
        background: rgba(5, 217, 232, 0.2);
        border-radius: 5px;
        margin-bottom: 20px;
        overflow: hidden;
        position: relative;
    }
    
    .lock-progress {
        height: 100%;
        width: 0%;
        background: linear-gradient(90deg, #05d9e8, #ff2a6d);
        transition: width 0.3s;
    }
    
    .lock-hologram {
        position: absolute;
        width: 80%;
        height: 150px;
        background: linear-gradient(135deg, rgba(5, 217, 232, 0.1), rgba(255, 42, 109, 0.1));
        border: 1px solid #05d9e8;
        border-radius: 10px;
        top: -170px;
        left: 10%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(5, 217, 232, 0.3);
    }
    
    .hologram-text {
        color: #05d9e8;
        font-size: 14px;
        text-align: center;
        text-shadow: 0 0 5px #05d9e8;
        animation: hologram-flicker 2s infinite alternate;
    }
    
    @keyframes hologram-flicker {
        0%, 100% { opacity: 0.8; }
        50% { opacity: 0.3; }
    }
    
    .lock-digits {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
    }
    
    .digit {
        width: 30px;
        height: 40px;
        background: rgba(5, 217, 232, 0.1);
        border: 1px solid #05d9e8;
        color: #ff2a6d;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        position: relative;
    }
    
    .digit::after {
        content: "";
        position: absolute;
        bottom: 5px;
        width: 10px;
        height: 2px;
        background: #05d9e8;
    }
    
    .lock-keypad {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        width: 100%;
    }
    
    .key {
        background: rgba(13, 2, 33, 0.5);
        border: 1px solid #05d9e8;
        color: #05d9e8;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.2s;
        border-radius: 5px;
    }
    
    .key:hover {
        background: rgba(255, 42, 109, 0.3);
        box-shadow: 0 0 10px #ff2a6d;
    }
    
    .key:active {
        transform: scale(0.95);
    }
    
    .key-clear {
        grid-column: span 3;
        background: rgba(255, 42, 109, 0.3);
    }
    
    .access-granted {
        color: #05d9e8;
        font-size: 24px;
        text-align: center;
        margin-top: 20px;
        text-shadow: 0 0 10px #05d9e8;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .access-denied {
        color: #ff2a6d;
        font-size: 24px;
        text-align: center;
        margin-top: 20px;
        text-shadow: 0 0 10px #ff2a6d;
        animation: shake 0.5s;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    </style>
    
    <div class="cyberpunk-bg"></div>
    <div class="grid-overlay"></div>
    <div class="cyberpunk-circle circle-1"></div>
    <div class="cyberpunk-circle circle-2"></div>
    <div class="cyberpunk-circle circle-3"></div>
    
    <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
        <div class="password-lock">
            <div class="lock-body" id="lockBody">
                <div class="lock-front">
                    <div class="lock-hologram">
                        <div class="hologram-text">
                            NEURAL INTERFACE TERMINAL<br>
                            VERIFICATION REQUIRED<br>
                            UNAUTHORIZED ACCESS WILL BE<br>
                            REPORTED TO CYBERSECURITY
                        </div>
                    </div>
                    
                    <h2 class="lock-title">NEON-CHAT 2119</h2>
                    
                    <div class="lock-indicator">
                        <div class="lock-progress" id="lockProgress"></div>
                    </div>
                    
                    <div class="lock-digits" id="lockDigits">
                        <div class="digit"></div>
                        <div class="digit"></div>
                        <div class="digit"></div>
                        <div class="digit"></div>
                        <div class="digit"></div>
                    </div>
                    
                    <div class="lock-keypad">
                        <div class="key" onclick="appendDigit('1')">1</div>
                        <div class="key" onclick="appendDigit('2')">2</div>
                        <div class="key" onclick="appendDigit('3')">3</div>
                        <div class="key" onclick="appendDigit('4')">4</div>
                        <div class="key" onclick="appendDigit('5')">5</div>
                        <div class="key" onclick="appendDigit('6')">6</div>
                        <div class="key" onclick="appendDigit('7')">7</div>
                        <div class="key" onclick="appendDigit('8')">8</div>
                        <div class="key" onclick="appendDigit('9')">9</div>
                        <div class="key" onclick="appendDigit('*')">*</div>
                        <div class="key" onclick="appendDigit('0')">0</div>
                        <div class="key" onclick="appendDigit('#')">#</div>
                        <div class="key key-clear" onclick="clearDigits()">CLEAR</div>
                    </div>
                    
                    <button class="lock-button" onclick="submitPassword()">AUTHENTICATE</button>
                    
                    <div id="accessMessage"></div>
                </div>
                
                <div class="lock-back">
                    <h2 class="lock-title">SYSTEM SCAN</h2>
                    <div style="color: white; text-align: center; margin-bottom: 30px;">
                        BIOMETRIC VERIFICATION IN PROGRESS...
                    </div>
                    <div style="width: 100%; height: 150px; background: rgba(0,0,0,0.3); border: 1px solid #05d9e8; margin-bottom: 30px; padding: 10px;">
                        <div style="color: #05d9e8; font-family: monospace; line-height: 1.5;">
                            > INITIATING NEURAL LINK...<br>
                            > SCANNING RETINA PATTERN...<br>
                            > VERIFYING VOICE PRINT...<br>
                            > CHECKING CYBERNEURAL IMPLANTS...
                        </div>
                    </div>
                    <div style="width: 100%; height: 10px; background: rgba(5, 217, 232, 0.2); border-radius: 5px; overflow: hidden;">
                        <div id="scanProgress" style="height: 100%; width: 0%; background: linear-gradient(90deg, #05d9e8, #ff2a6d);"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
    let currentPassword = "";
    const maxLength = 5;
    
    function appendDigit(digit) {
        if (currentPassword.length < maxLength) {
            currentPassword += digit;
            updateDigitsDisplay();
            updateProgressBar();
        }
    }
    
    function clearDigits() {
        currentPassword = "";
        updateDigitsDisplay();
        updateProgressBar();
        document.getElementById("accessMessage").innerHTML = "";
    }
    
    function updateDigitsDisplay() {
        const digits = document.querySelectorAll(".digit");
        for (let i = 0; i < digits.length; i++) {
            if (i < currentPassword.length) {
                digits[i].textContent = currentPassword[i];
                digits[i].style.color = "#ff2a6d";
                digits[i].style.textShadow = "0 0 5px #ff2a6d";
            } else {
                digits[i].textContent = "";
            }
        }
    }
    
    function updateProgressBar() {
        const progress = (currentPassword.length / maxLength) * 100;
        document.getElementById("lockProgress").style.width = progress + "%";
    }
    
    function submitPassword() {
        if (currentPassword.length === 0) {
            document.getElementById("accessMessage").innerHTML = '<div class="access-denied">ENTER PASSCODE</div>';
            return;
        }
        
        // Flip the lock to show scanning
        document.getElementById("lockBody").style.transform = "rotateY(180deg)";
        
        // Simulate scanning progress
        let progress = 0;
        const scanInterval = setInterval(() => {
            progress += 10;
            document.getElementById("scanProgress").style.width = progress + "%";
            
            if (progress >= 100) {
                clearInterval(scanInterval);
                
                // Send the password to Streamlit
                const data = { password: currentPassword };
                
                fetch("/submit_password", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById("scanProgress").style.background = "linear-gradient(90deg, #05d9e8, #00ff00)";
                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    } else {
                        document.getElementById("lockBody").style.transform = "rotateY(0deg)";
                        document.getElementById("scanProgress").style.width = "0%";
                        document.getElementById("accessMessage").innerHTML = '<div class="access-denied">ACCESS DENIED</div>';
                        currentPassword = "";
                        updateDigitsDisplay();
                        updateProgressBar();
                    }
                });
            }
        }, 200);
    }
    
    // Add keyboard support
    document.addEventListener('keydown', function(event) {
        if (event.key >= '0' && event.key <= '9') {
            appendDigit(event.key);
        } else if (event.key === '*' || event.key === '#') {
            appendDigit(event.key);
        } else if (event.key === 'Backspace') {
            clearDigits();
        } else if (event.key === 'Enter') {
            submitPassword();
        }
    });
    </script>
    """, unsafe_allow_html=True)
    
    # 添加一个端点来处理密码提交
    @st.routes.add_route("/submit_password", methods=["POST"])
    def handle_password_submit():
        data = st.routes.request.get_json()
        if data["password"] == CORRECT_PASSWORD:
            st.session_state.password_correct = True
            return {"success": True}
        else:
            return {"success": False}
    
    return False
