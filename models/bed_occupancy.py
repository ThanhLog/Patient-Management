from datetime import datetime, timedelta


def calculate_bed_occupancy(
    patients_collection,
    departments_collection,
    start_date,
    end_date,
    department_name=None,
    disease_name=None,
):
    occupancy_data = {}

    # Tạo khoảng thời gian cho từng ngày
    delta = end_date - start_date
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        occupancy_data[day.strftime("%Y-%m-%d")] = 0

    # Tạo điều kiện truy vấn cơ bản
    query = {
        "admission_date": {"$lte": end_date.strftime("%Y-%m-%d")},
        "discharge_date": {"$gte": start_date.strftime("%Y-%m-%d")},
    }

    # Thêm điều kiện lọc theo khoa nếu có
    if department_name:
        query["department"] = department_name

    # Thêm điều kiện lọc theo bệnh nếu có
    if disease_name:
        query["disease"] = disease_name

    # Tìm bệnh nhân theo điều kiện
    patients = patients_collection.find(query)

    # Cập nhật công suất giường
    for patient in patients:
        admission_date = datetime.strptime(patient["admission_date"], "%Y-%m-%d")
        discharge_date = datetime.strptime(patient["discharge_date"], "%Y-%m-%d")

        # Giới hạn bệnh nhân trong khoảng thời gian
        actual_start = max(admission_date, start_date)
        actual_end = min(discharge_date, end_date)

        # Tăng công suất giường cho từng ngày bệnh nhân nằm
        delta_patient = actual_end - actual_start
        for j in range(delta_patient.days + 1):
            day = actual_start + timedelta(days=j)
            occupancy_data[day.strftime("%Y-%m-%d")] += 1

    # Nếu có tên khoa, truy vấn dữ liệu khoa để lấy thông tin sức chứa (capacity)
    if department_name:
        department_info = departments_collection.find_one({"name": department_name})
        if department_info and "capacity" in department_info:
            capacity = department_info["capacity"]

            # Tính tỉ lệ công suất giường (giường sử dụng / sức chứa)
            for day in occupancy_data:
                occupancy_data[day] = (occupancy_data[day] / capacity) * 100

    return occupancy_data
