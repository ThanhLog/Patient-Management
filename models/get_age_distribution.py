def get_age_distribution(patients_collection, department_name=None, disease_name=None):

    # Tìm bệnh nhân trên điều kiện khoa và bệnh
    query = {}
    if department_name:
        query["department"] = department_name
    if disease_name:
        query["disease"] = disease_name

    # Lấy danh sách bệnh nhân
    patients = patients_collection.find({}, {"age": 1, "_id": 0})
    age_groups = {"<18": 0, "18 - 30": 0, "30 - 50": 0, "50 - 70": 0, "70+": 0}

    for patient in patients:
        age = patient["age"]
        if age < 18:
            age_groups["<18"] += 1
        elif 18 <= age <= 30:
            age_groups["18 - 30"] += 1
        elif 30 < age <= 50:
            age_groups["30 - 50"] += 1
        elif 50 < age <= 70:
            age_groups["50 - 70"] += 1
        else:
            age_groups["70+"] += 1

    data = age_groups
    custom_title = f"Biểu đồ phân bố độ tuổi bệnh nhân{(" bệnh " + disease_name) if disease_name else ""} {department_name if department_name else ""}"
    return data, custom_title
