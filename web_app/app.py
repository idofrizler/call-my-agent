"""Flask server for viewing agent conversations."""

import json
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

# Conversations directory relative to this file
CONV_DIR = Path(__file__).parent.parent / "conversations"

@app.route('/')
def index():
    """Serve the main chat UI."""
    return render_template('index.html')

@app.route('/api/conversations')
def list_conversations():
    """List available conversation sessions."""
    if not CONV_DIR.exists():
        return jsonify([])
    
    sessions = []
    for session_dir in CONV_DIR.iterdir():
        if not session_dir.is_dir():
            continue
            
        log_file = session_dir / "log.json"
        if not log_file.exists():
            continue
            
        try:
            with open(log_file) as f:
                data = json.load(f)
                # Get first user message as title
                title = next((msg["content"] for msg in data["messages"] 
                            if msg["role"] == "User"), "Untitled")
                sessions.append({
                    "id": session_dir.name,
                    "title": title,
                    "timestamp": datetime.strptime(
                        session_dir.name, "%Y-%m-%d_%H-%M-%S"
                    ).isoformat()
                })
        except (json.JSONDecodeError, KeyError):
            continue
            
    # Sort newest first
    sessions.sort(key=lambda s: s["timestamp"], reverse=True)
    return jsonify(sessions)

@app.route('/api/conversation/<session_id>')
def get_conversation(session_id):
    """Get messages for a specific conversation."""
    log_file = CONV_DIR / session_id / "log.json"
    if not log_file.exists():
        return jsonify({"error": "Conversation not found"}), 404
        
    try:
        with open(log_file) as f:
            return jsonify(json.load(f))
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid conversation data"}), 500
        
@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files."""
    return send_from_directory('static', path)

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve generated images."""
    image_dir = Path(__file__).parent.parent / "images"
    return send_from_directory(image_dir, filename)

@app.route('/output/<path:filename>')
def serve_output(filename):
    """Serve generated output files (PDFs etc)."""
    output_dir = Path(__file__).parent.parent / "output"
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
