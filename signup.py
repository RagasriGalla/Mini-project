<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Signup | Task Agent</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="main-container">
    <div class="chat-card">
        <h2 class="title">Create Account</h2>
        <div class="form-center">
            <input 
                class="input-box"
                id="signupUser"
                type="text"
                placeholder="Username"
            >
            <input 
                class="input-box"
                id="signupPass"
                type="password"
                placeholder="Password"
            >
            <button class="primary-btn" onclick="signupUser()">
                Signup
            </button>
            <p>
                Already have an account?
                <a href="login.html" style="color:#c4b5fd">
                    Login
                </a>
            </p>
        </div>
    </div>
</div>
<script src="js/script.js"></script>
</body>
</html>
