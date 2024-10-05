from flask import Flask, jsonify, send_file
from pymongo import MongoClient
from charts.age_distribution_chart import (
    create_age_distribution_pie_chart,
    create_age_distribution_bar_chart,
)
from charts.disease_distribution_chart import (
    create_disease_distribution_pie_chart,
    create_disease_distribution_bar_chart,
)
from flask_cors import CORS  # Thêm dòng này để sử dụng CORS

app = Flask(__name__)
CORS(app)  # Kích hoạt CORS cho toàn bộ ứng dụng

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["HospitalManagement"]
patients_collection = db["Patients"]
departments_collection = db["Departments"]


@app.route("/api/departments", methods=["GET"])
def get_departments():
    # Lấy dữ liệu khoa từ MongoDB
    departments = list(
        departments_collection.find({}, {"_id": 0})
    )  # Loại bỏ trường _id
    return jsonify(departments)


# Phân loại bệnh nhân theo độ tuổi
@app.route("/age_distribution/pie")
def age_distribution_pie():
    # Lấy dữ liệu bệnh nhân từ MongoDB, chỉ lấy trường 'age'
    patients = list(patients_collection.find({}, {"_id": 0, "age": 1}))

    if not patients:
        return "Không có dữ liệu bệnh nhân trong hệ thống"

    # Tạo biểu đồ phân bố bệnh nhân theo độ tuổi (biểu đồ tròn)
    chart_path = create_age_distribution_pie_chart(patients)

    # Gửi file biểu đồ đến trình duyệt
    return send_file(chart_path)

@app.route("/age_distribution/bar")
def age_distribution_bar():
    # Lấy dữ liệu bệnh nhân từ MongoDB, chỉ lấy trường 'age'
    patients = list(patients_collection.find({}, {"_id": 0, "age": 1}))

    if not patients:
        return "Không có dữ liệu bệnh nhân trong hệ thống"

    # Tạo biểu đồ phân bố bệnh nhân theo độ tuổi (biểu đồ cột)
    chart_path = create_age_distribution_bar_chart(patients)

    # Gửi file biểu đồ đến trình duyệt
    return send_file(chart_path)


# Phân loại bệnh
@app.route("/disease_distribution/pie")
def disease_distribution_pie():
    # Lấy dữ liệu bệnh nhân từ MongoDB, chỉ lấy trường 'disease'
    patients = list(patients_collection.find({}, {"_id": 0, "disease": 1}))
    if not patients:
        return "Không có dữ liệu bệnh nhân trong hệ thống"
    # Tạo biểu đồ phân bố bệnh nhân theo loại bệnh (biểu đồ tròn)
    chart_path = create_disease_distribution_pie_chart(patients)
    # Gửi file biểu đồ đến trình duyệt
    return send_file(chart_path)


@app.route("/disease_distribution/bar")
def disease_distribution_bar():
    # Lấy dữ liệu bệnh nhân từ MongoDB, chỉ lấy trường 'disease'
    patients = list(patients_collection.find({}, {"_id": 0, "disease": 1}))

    if not patients:
        return "Không có dữ liệu bệnh nhân trong hệ thống"

    # Tạo biểu đồ phân bố bệnh nhân theo loại bệnh (biểu đồ cột)
    chart_path = create_disease_distribution_bar_chart(patients)

    if not chart_path:
        return "Không có dữ liệu hợp lệ để vẽ biểu đồ"

    # Gửi file biểu đồ đến trình duyệt
    return send_file(chart_path)


if __name__ == "__main__":
    app.run(debug=True)
