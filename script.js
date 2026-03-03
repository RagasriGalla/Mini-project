// Navigation Functions
function goToSignup(){
    window.location.href="signup.html";
}
function signupUser(){
    alert("Signup successful");
    window.location.href="login.html";
}
function loginUser(){
    alert("Login successful");
    window.location.href="mode.html";
}
function autonomousMode(){
    localStorage.setItem("mode","autonomous");
    window.location.href="chat.html";
}
function humanMode(){
    localStorage.setItem("mode","human");
    window.location.href="chat.html";
}
async function sendMessage(){
    let input = document.getElementById("userInput");
    let chatBox = document.getElementById("chatBox");
    let userText = input.value.trim();
    if(userText === "") return;

    // Show user message
    chatBox.innerHTML += `<div class="user-msg">You: ${userText}</div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        let mode = localStorage.getItem("mode") || "autonomous";
        let response = await fetch("http://127.0.0.1:8000/agent/process", {  // note port 8000, your FastAPI default
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                task: userText,
                mode: mode
            })
        });
        if(!response.ok){
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }
        let data = await response.json();

        // The backend returns an object in `response`, show JSON prettified or stringified
        chatBox.innerHTML += `<div class="ai-msg">Agent: <pre>${JSON.stringify(data.response, null, 2)}</pre></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch(error) {
        console.error(error);
        chatBox.innerHTML += `<div class="ai-msg">⚠️ Error connecting to server: ${error.message}</div>`;
    }
}
