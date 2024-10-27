from flask import Flask, render_template, request, redirect
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Load approval requests from JSON file
def load_requests():
    if os.path.exists('approvals.json'):
        with open('approvals.json', 'r') as f:
            return json.load(f)
    return []

# Save approval requests to JSON file
def save_requests(requests):
    with open('approvals.json', 'w') as f:
        json.dump(requests, f, indent=4)

# Get current timestamp
def get_current_time():
    return int(datetime.now().timestamp())

# Check if approval is needed
def is_approval_needed(user_id, requests):
    for req in requests:
        if req['user_id'] == user_id:
            if req['approved']:
                return False
            # Check if 3 months have passed
            last_request_time = req['last_request_time']
            if get_current_time() - last_request_time >= 3 * 30 * 24 * 60 * 60:  # 3 months in seconds
                return True
            return False
    return True  # No request found, approval needed

@app.route('/')
def home():
    user_id = request.args.get('user_id', 'default_user')
    requests = load_requests()
    
    if is_approval_needed(user_id, requests):
        return render_template('approval.html', user_id=user_id)
    return "Access Granted!"

@app.route('/send_request', methods=['POST'])
def send_request():
    user_id = request.form['user_id']
    requests = load_requests()
    requests.append({
        'request_id': len(requests) + 1,
        'user_id': user_id,
        'approved': False,
        'last_request_time': get_current_time()
    })
    save_requests(requests)
    return redirect('/')

@app.route('/approve/<int:request_id>')
def approve(request_id):
    requests = load_requests()
    for req in requests:
        if req['request_id'] == request_id:
            req['approved'] = True
            save_requests(requests)
            break
    return redirect('/')

@app.route('/reject/<int:request_id>')
def reject(request_id):
    requests = load_requests()
    requests = [req for req in requests if req['request_id'] != request_id]
    save_requests(requests)
    return redirect('/')

@app.route('/contact')
def contact():
    return '''
    <h1>Contact Us</h1>
    <p>If you have any questions, please reach out on Facebook: 
    <a href="https://www.facebook.com/The.drugs.ft.chadwick.67">Contact Link</a></p>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
          
