from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/get_video", methods=["GET"])
def get_video():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"error": "Thiếu URL video!"}), 400

    ydl_opts = {
        "quiet": True,
        "format": "best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_link = info["url"]
        return jsonify({"video_url": video_link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
