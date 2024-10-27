from flask import Flask, request, jsonify, render_template
import json
import os
import random

app = Flask(__name__)

# Unique key generate karne ka function
def generate_unique_key():
    return str(random.randint(100000, 999999))  # 6-digit random key generate karo

# Approvals ko load karne ka function
def load_approvals():
    if not os.path.exists('approvals.json'):
        return []  # Agar file nahi hai to khali list return karo

    with open('approvals.json', 'r') as f:
        try:
            return json.load(f)  # JSON data load karne ki koshish karo
        except json.JSONDecodeError:  # Agar error aaye to handle karo
            return []  # Agar error aaye to khali list return karo

# Approval send karne ka route
@app.route('/send_approval', methods=['POST'])
def send_approval():
    data = request.json
    unique_key = data.get('key', generate_unique_key())  # Agar key nahi hai to generate karo

    # Approval request ko approvals.json mein daalna
    approvals = load_approvals()  # Existing approvals load karo
    approvals.append({'key': unique_key, 'status': 'pending'})  # Nayi approval add karo

    # Approvals ko wapas file mein save karo
    with open('approvals.json', 'w') as f:
        json.dump(approvals, f, indent=4)  # Changes ko save karo with pretty formatting

    return jsonify({'success': True, 'key': unique_key})

# Main page ka route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    
