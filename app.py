from flask import Flask, request, jsonify, render_template
import pyrebase
import time

# Cấu hình Firebase
firebase_config = {
    "apiKey": "AIzaSyANnDxikLdbDLygzVgOle_AYY3PLzmPgA8",
    "authDomain": "bt-iot-7af8a.firebaseapp.com",
    "databaseURL": "https://bt-iot-7af8a-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "bt-iot-7af8a",
    "storageBucket": "bt-iot-7af8a.appspot.com",
    "messagingSenderId": "121771695080",
    "appId": "1:121771695080:web:f846c6d46def80cd00225d",
    "measurementId": "G-0MHC1VME9H"
}

# Khởi tạo Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Khởi tạo Flask
app = Flask(__name__)

# API để cập nhật trạng thái thiết bị
@app.route('/update', methods=['POST'])
def update_device_state():
    data = request.json  # Nhận dữ liệu JSON từ client
    
    # Chuyển tất cả các giá trị sang kiểu số (number) nếu có thể
    for key in data:
        try:
            # Cố gắng chuyển các giá trị thành số (int hoặc float)
            data[key] = float(data[key]) if '.' in str(data[key]) else int(data[key])
        except ValueError:
            # Nếu không thể chuyển thành số, giữ nguyên giá trị gốc
            continue
    
    try:
        ref = db
        ref.update(data)  # Cập nhật dữ liệu lên Firebase
        return jsonify({"message": "Device state updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to update device state", "details": str(e)}), 500


# API để lấy trạng thái thiết bị
@app.route('/get', methods=['GET'])
def get_device_state():
    try:
        data = db.get().val()  # Lấy dữ liệu từ Firebase
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch device state", "details": str(e)}), 500

# Trang hiển thị trạng thái thiết bị
@app.route('/')
def index():
    try:
        data = db.get().val()  # Lấy toàn bộ dữ liệu
        return render_template('index.html', data=data)
    except Exception as e:
        return render_template('index.html', data={})
    # Trang hiển thị trạng thái thiết bị

@app.route('/test')
def test():
    try:
        data = db.get().val()  # Lấy toàn bộ dữ liệu
        return render_template('test.html', data=data)
    except Exception as e:
        return render_template('test.html', data={})


# API cho client gửi yêu cầu định kỳ
@app.route('/poll', methods=['GET'])
def poll():
    try:
        data = db.get().val()  # Lấy dữ liệu từ Firebase
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch device state", "details": str(e)}), 500

# Chạy Flask app
if __name__ == "__main__":
    app.run(debug=True)
