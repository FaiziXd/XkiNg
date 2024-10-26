from flask import Flask, render_template_string, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# HTML Template
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Approval System</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #222;
            color: white;
            font-family: Arial, sans-serif;
        }

        .button {
            padding: 10px 20px;
            margin: 10px;
            background-color: red;
            color: white;
            border: none;
            font-size: 1.2em;
            cursor: pointer;
            font-weight: bold;
            border-radius: 5px;
            transition: 0.3s ease;
        }

        .button:hover {
            box-shadow: 0 0 10px 3px red, 0 0 15px 5px #ff4d4d;
        }

        .highlighted-button {
            background-color: green;
            color: white;
            font-size: 1em;
            width: 150px;
            transition: all 0.2s ease;
        }

        .highlighted-button:hover {
            box-shadow: 0 0 10px 3px green, 0 0 15px 5px lime;
        }

        .hidden {
            display: none;
        }

        #approvalForm, #passwordPrompt, #showApproval {
            margin-top: 20px;
            text-align: center;
        }

        #noteSection {
            background-color: #333;
            color: #ffeb3b;
            padding: 10px;
            margin-top: 20px;
            border-radius: 5px;
            width: 80%;
            text-align: center;
            font-size: 1.1em;
            box-shadow: 0 0 10px 3px yellow;
        }
    </style>
</head>
<body>
    <img src="https://raw.githubusercontent.com/FaiziXd/XkiNg/main/be0315df5e257b8eb23978b0cca85604.jpg" alt="Approval Image" width="300">
    <button class="button" id="sendApprovalBtn" onclick="toggleApprovalForm()">Send Approval</button>
    <button class="button" id="showApprovalBtn" onclick="showPasswordPrompt()">Show Approval</button>

    <div id="approvalForm" class="hidden">
        <h3>Enter Your Name</h3>
        <input type="text" id="userName" placeholder="Name">
        <button class="highlighted-button" onclick="sendApproval()">OK</button>
    </div>

    <div id="passwordPrompt" class="hidden">
        <h3>Enter Password</h3>
        <input type="password" id="password" placeholder="Password">
        <button class="highlighted-button" onclick="checkPassword()">Submit</button>
    </div>

    <div id="showApproval" class="hidden">
        <h3>Approval Requests</h3>
        <p id="approvalDetails"></p>
        <button class="highlighted-button" onclick="acceptApproval()">Accept</button>
        <button class="highlighted-button" onclick="rejectApproval()">Reject</button>
    </div>

    <div id="noteSection" class="hidden">
        <h4>Note Your Key</h4>
        <p id="keyInfo"></p>
        <a id="contactLink" href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank">
            <button class="highlighted-button">Send Key on Facebook</button>
        </a>
    </div>

    <script>
        let approvalSent = {{ approval_sent|tojson }};
        let userKey = "{{ user_key }}";
        let userName = "{{ user_name }}";
        let approvalAccepted = {{ approval_accepted|tojson }};

        function toggleApprovalForm() {
            if (!approvalSent) {
                document.getElementById("approvalForm").classList.toggle("hidden");
            } else {
                alert("PLEASE WAIT! This is your first key: " + userKey);
            }
        }

        function sendApproval() {
            userName = document.getElementById("userName").value;
            if (userName) {
                userKey = "KEY-" + Math.floor(Math.random() * 10000);
                approvalSent = true;
                document.getElementById("approvalForm").classList.add("hidden");
                document.getElementById("noteSection").classList.remove("hidden");
                document.getElementById("keyInfo").innerText = "Your Key: " + userKey;
                document.getElementById("showApproval").classList.remove("hidden");
            } else {
                alert("Please enter your name!");
            }
        }

        function showPasswordPrompt() {
            if (!approvalAccepted) { // Show prompt only if approval not accepted
                document.getElementById("passwordPrompt").classList.remove("hidden");
            } else {
                alert("Approval has already been accepted. No further actions available.");
            }
        }

        function checkPassword() {
            const password = document.getElementById("password").value;
            if (password === "THE FAIZAN") {
                document.getElementById("passwordPrompt").classList.add("hidden");
                document.getElementById("showApproval").classList.remove("hidden");
                document.getElementById("approvalDetails").innerText = `Name: ${userName}, Key: ${userKey}`;
            } else {
                alert("Wrong password!");
            }
        }

        function acceptApproval() {
            alert("Approval Accepted for " + userName);
            approvalAccepted = true; // Update approval status
            window.location.href = "https://herf-2-faizu-apk.onrender.com/"; // Redirect to the specified URL
        }

        function rejectApproval() {
            alert("Approval Rejected for " + userName);
            approvalAccepted = true; // Update approval status
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize session variables
    if 'approval_sent' not in session:
        session['approval_sent'] = False
        session['approval_accepted'] = False
        session['user_name'] = ''
        session['user_key'] = ''

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:
            session['user_name'] = user_name
            session['user_key'] = "KEY-" + str(random.randint(1000, 9999))  # Generate a random key
            session['approval_sent'] = True
            return redirect('/')

    return render_template_string(
        html_template,
        approval_sent=session['approval_sent'],
        approval_accepted=session['approval_accepted'],
        user_name=session['user_name'],
        user_key=session['user_key'],
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
