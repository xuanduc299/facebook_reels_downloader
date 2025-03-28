from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Cho phép extension truy cập API

# Hàm tải video Facebook
def get_facebook_video(fb_url):
    response = requests.get(f"https://facebook-reels-downloader.onrender.com/get_video?url={fb_url}")
    return response.json().get("video_url", "")

# Hàm tải video TikTok
def get_tiktok_video(tt_url):
    response = requests.get(f"https://www.tikwm.com/api/?url={tt_url}")
    data = response.json()
    return data.get("data", {}).get("play", "")

# Hàm tải video Instagram
def get_instagram_video(ig_url):
    response = requests.get(f"https://saveig.app/api?url={ig_url}")
    data = response.json()
    return data.get("url", "")

@app.route("/get_video", methods=["GET"])
def get_video():
    url = request.args.get("url")
    platform = request.args.get("platform")

    if not url or not platform:
        return jsonify({"error": "URL and platform are required"}), 400

    video_url = ""
    if platform == "facebook":
        video_url = get_facebook_video(url)
    elif platform == "tiktok":
        video_url = get_tiktok_video(url)
    elif platform == "instagram":
        video_url = get_instagram_video(url)

    if video_url:
        return jsonify({"video_url": video_url})
    return jsonify({"error": "Failed to fetch video"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
