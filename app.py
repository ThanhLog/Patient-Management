from flask import Flask, jsonify, send_file, request
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask_cors import CORS

from charts.chart_ulits import create_bar_chart, create_line_chart, create_pie_chart
from models.get_age_distribution import get_age_distribution
from models.get_treatment_cost import get_treatment_cost
from models.bed_occupancy import calculate_bed_occupancy

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Cho phép yêu cầu từ localhost:5173


# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["HospitalManagement"]
patients_collection = db["Patients"]
departments_collection = db["Departments"]

@app.route("/api/departments", methods=["GET"])
def get_departments():
    departments = list(departments_collection.find({}, {"_id": 0}))
    return jsonify(departments)
    

@app.route("/api/chart", methods=["POST"])
def generate_chart():
    # Lấy dữ liệu từ yêu cầu POST
    request_data = request.json  # Sử dụng request.json để lấy dữ liệu JSON
    chart_type = request_data.get("chart_type")
    data_type = request_data.get("data_type")
    department_name = request_data.get("department_name")
    disease_name = request_data.get("disease_name")


    # Lấy dữ liệu từ MongoDB
    if data_type == "age_distribution":
        data, custom_title = get_age_distribution(patients_collection, department_name, disease_name)
    elif data_type == "treatment_cost":
        data, custom_title = get_treatment_cost(patients_collection, department_name, disease_name)
    else:
        return jsonify({"error": "Invalid data type"}), 400

    # Vẽ biểu đồ theo yêu cầu của người dùng
    if chart_type == "bar":
        img = create_bar_chart(data, custom_title)
    elif chart_type == "pie":
        img = create_pie_chart(data, custom_title)
    elif chart_type == "line":
        img = create_line_chart(data, custom_title)
    else:
        return jsonify({"error": "Invalid chart type"}), 400

    return send_file(img, mimetype="image/png")


@app.route("/api/bed-occupancy", methods=["POST"])
def bed_occupancy_chart():
    request_data = request.json
    chart_type = request_data.get("chart_type", "line")
    time_range = request_data.get("time_range")
    department_name = request_data.get("department_name")
    disease_name = request_data.get("disease_name")

    # Xác định thời gian theo yêu cầu
    end_date = datetime.now()
    if time_range == "1_Week":
        start_date = end_date - timedelta(days=7)
        time_title = "1 tuần"
    elif time_range == "1_Month":
        start_date = end_date - timedelta(days=30)
        time_title = "1 tháng"
    elif time_range == "3_Month":
        start_date = end_date - timedelta(days=90)
        time_title = "3 tháng"
    elif time_range == "6_Month":
        start_date = end_date - timedelta(days=180)
        time_title = "6 tháng"
    else:
        return jsonify({"Error": "Khoảng thời gian không hợp lệ"}), 400

    # Tính công suất giường bệnh trong khoảng thời gian
    occupancy_data = calculate_bed_occupancy(
        patients_collection,
        departments_collection,
        start_date,
        end_date,
        department_name,
        disease_name,
    )

    # Vẽ biểu đồ
    if chart_type == "line":
        img = create_line_chart(
            occupancy_data,
            "Ngày",  # X label
            "Công suất giường",  # Y label
            f"Biểu đồ công suất giường{(" bệnh " + disease_name) if disease_name else ""} {department_name if department_name else 'bệnh viện'} ({time_title})",  # Title
        )
    else:
        return jsonify({"error": "Invalid chart type"}), 400

    return send_file(img, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
