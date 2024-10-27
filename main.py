from flask import Flask, request, jsonify

# Other imports and app initialization...

@app.route('/send_approval', methods=['POST'])
def send_approval():
    data = request.json
    unique_key = data.get('key')

    # Here, you can add logic to save the key in approvals.json
    # Example:
    with open('approvals.json', 'r+') as f:
        approvals = json.load(f)
        approvals.append({'key': unique_key, 'status': 'pending'})
        f.seek(0)
        json.dump(approvals, f)

    return jsonify({'success': True})
