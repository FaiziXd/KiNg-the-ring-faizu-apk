from flask import Flask, request, jsonify, render_template
import json
import os
import random

app = Flask(__name__)

# Function to generate a unique key
def generate_unique_key():
    return str(random.randint(100000, 999999))  # Generate a random 6-digit key

# Route for sending approval
@app.route('/send_approval', methods=['POST'])
def send_approval():
    data = request.json
    unique_key = data.get('key', generate_unique_key())  # Generate a key if not provided

    # Append the approval request to approvals.json
    try:
        # Check if the file exists and has valid JSON
        try:
            with open('approvals.json', 'r+') as f:
                try:
                    approvals = json.load(f)
                except json.JSONDecodeError:  # Handle empty or invalid JSON
                    approvals = []

                approvals.append({'key': unique_key, 'status': 'pending'})  # Add new approval
                f.seek(0)  # Move to the start of the file to overwrite
                json.dump(approvals, f, indent=4)  # Save changes with pretty formatting
                f.truncate()  # Remove any leftover data
        except FileNotFoundError:
            # If file does not exist, create it with an empty list
            with open('approvals.json', 'w') as f:
                approvals = [{'key': unique_key, 'status': 'pending'}]
                json.dump(approvals, f, indent=4)

        return jsonify({'success': True, 'key': unique_key})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
