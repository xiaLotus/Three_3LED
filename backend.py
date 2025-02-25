from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import random

app = Flask(__name__)
CORS(app)  

# 初始化燈的狀態（0, 0, 1）
lamp_status = {
    "red": 0,
    "yellow": 0,
    # 開始為綠燈
    "green": 1
}

# 每秒隨機更新燈的狀態
def randomize_lights():
    while True:
        # 只有一個燈亮
        states = [0, 0, 0]
        states[random.randint(0, 2)] = 1
        lamp_status["red"], lamp_status["yellow"], lamp_status["green"] = states
        time.sleep(1) 


threading.Thread(target=randomize_lights, daemon=True).start()


@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(lamp_status)


@app.route("/update", methods=["POST"])
def update_status():
    data = request.json
    lamp_status.update(data)
    return jsonify({"message": "Status updated", "new_status": lamp_status})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
