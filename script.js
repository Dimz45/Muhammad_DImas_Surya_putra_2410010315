const sessionId = Date.now().toString();

const chatBox = document.getElementById("chat-box");

function addMessage(text, sender){

    const div = document.createElement("div");

    div.classList.add("message");
    div.classList.add(sender);

    div.textContent = text;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(){

    const input = document.getElementById("user-input");

    const message = input.value.trim();

    if(message === "")
        return;

    addMessage(message, "user");

    input.value = "";

    showTyping();

    const response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            session_id:sessionId,
            message:message
        })
    });

    const data = await response.json();

    removeTyping();

    addMessage(data.reply, "bot");
}

window.onload = async ()=>{

    const response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            session_id:sessionId,
            message:"start"
        })
    });

    const data = await response.json();

    addMessage(data.reply, "bot");
};

document
.getElementById("user-input")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){
        sendMessage();
    }

});

function showTyping(){

    const div = document.createElement("div");

    div.classList.add("message");
    div.classList.add("bot");

    div.id = "typing";

    div.textContent = "FitBot sedang mengetik...";

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping(){

    const typing =
        document.getElementById("typing");

    if(typing){
        typing.remove();
    }
}