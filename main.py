from flask import Flask, request, jsonify
from g4f.client import Client
import os

app = Flask(__name__)
client = Client()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data:
        return jsonify({"error": "Request body kosong"}), 400

    system = data.get('system', '')
    messages = data.get('messages', [])

    if not messages:
        return jsonify({"error": "messages tidak boleh kosong"}), 400

    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)

    models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    last_error = None

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=full_messages,
            )
            reply = response.choices[0].message.content
            if reply:
                return jsonify({"reply": reply, "model": model})
        except Exception as e:
            last_error = str(e)
            continue

    return jsonify({"error": f"Semua model gagal: {last_error}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Default 8080 sesuai Railway
    app.run(host='0.0.0.0', port=port)
