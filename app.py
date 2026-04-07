from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

MAGIC_URL = "https://ai-api.magicstudio.com/api/ai-art-generator"
MAGIC_HEADERS = {
    "user-agent": "Mozilla/5.0",
    "accept": "application/json, text/plain, */*",
    "origin": "https://magicstudio.com",
    "referer": "https://magicstudio.com/ai-art-generator/"
}

@app.route("/")
def home():
    return jsonify({"message": "Use /generate?prompt=abbas+name+heart"})

@app.route("/generate")
def generate():
    prompt = request.args.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing 'prompt' parameter"}), 400

    magic_data = {
        "prompt": prompt,
        "output_format": "bytes",
        "user_profile_id": "null",
        "anonymous_user_id": "8c8fe58b-f1dd-40b8-86ac-a91ea7d7b4c2",
        "user_is_subscribed": "false",
        "client_id": "pSgX7WgjukXCBoYwDM8G8GLnRRkvAoJlqa5eAVvj95o"
    }

    try:
        magic_response = requests.post(MAGIC_URL, data=magic_data, headers=MAGIC_HEADERS)
    except Exception as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500

    if magic_response.status_code != 200:
        return jsonify({"error": "API failed", "status": magic_response.status_code}), magic_response.status_code

    # Return the image directly
    return Response(magic_response.content, mimetype="image/png")


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True, use_debugger=False, use_reloader=False)