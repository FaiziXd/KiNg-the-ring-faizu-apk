from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Endpoint to send approval
@app.route('/send_approval', methods=['POST'])
def send_approval():
    data = request.json
    unique_key = data.get('key')

    # Append the approval request to approvals.json
    try:
        with open('approvals.json', 'r+') as f:
            approvals = json.load(f)
            approvals.append({'key': unique_key, 'status': 'pending'})  # Add new approval
            f.seek(0)  # Move to the start of the file to overwrite
            json.dump(approvals, f, indent=4)  # Save changes with pretty formatting
            f.truncate()  # Remove any leftover data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
