from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load existing approvals from JSON file
def load_approvals():
    if os.path.exists('approvals.json'):
        with open('approvals.json', 'r') as f:
            return json.load(f)
    return {}

# Save approvals to JSON file
def save_approvals(approvals):
    with open('approvals.json', 'w') as f:
        json.dump(approvals, f)

@app.route('/')
def home():
    approvals = load_approvals()
    return render_template('index.html', approvals=approvals)

@app.route('/send_approval', methods=['POST'])
def send_approval():
    approval_key = request.form.get('approval_key')
    approvals = load_approvals()
    
    # Check if the approval key exists and is approved
    if approval_key in approvals and approvals[approval_key]["approved"]:
        return redirect("https://herf-2-faizu-apk.onrender.com/")  # Redirect to HERF link if approved
    
    # If not approved, redirect back to home
    return redirect(url_for('home'))

@app.route('/approval_success')
def approval_success():
    return '''
    <html>
        <head>
            <title>Approval Granted</title>
            <style>
                body {
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: green;
                }
            </style>
        </head>
        <body>
            <h1>Approval Granted!</h1>
            <p>Your access has been granted for 3 months.</p>
            <p>You can now use the app: <a href="https://herf-2-faizu-apk.onrender.com/">HERF Link</a></p>
            <p><a href="/">Go Back</a></p>
        </body>
    </html>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
  
