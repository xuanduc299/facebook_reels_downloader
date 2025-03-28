from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)  # Cho phép extension gọi API

# 🔥 Hàm tải video từ TikTok API
def get_tiktok_video(url):
    api_url = f"https://www.tikwm.com/api/?url={url}"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("data", {}).get("play", "")
    except:
        return ""

# 🔥 Hàm tải video từ Instagram API
def get_instagram_video(url):
    api_url = f"https://saveig.app/api?url={url}"
    try:
        response = requests.get(api_url)
        data = response.json()
        return data.get("url", "")
    except:
        return ""

@app.route("/get_video", methods=["GET"])
def get_video():
    video_url = request.args.get("url")
    platform = request.args.get("platform")

    if not video_url or not platform:
        return jsonify({"error": "Thiếu URL hoặc nền tảng!"}), 400

    video_link = ""

    try:
        if platform == "facebook" or platform == "youtube" or platform == "instagram":  
            ydl_opts = {"quiet": True, "format": "best", "noplaylist": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                video_link = info["url"]

        elif platform == "tiktok":
            video_link = get_tiktok_video(video_url)

        # elif platform == "instagram":
        #     video_link = get_instagram_video(video_url)

        if video_link:
            return jsonify({"video_url": video_link})
        return jsonify({"error": "Không thể tải video!"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
