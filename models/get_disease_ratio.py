def get_disease_ratio(patients_collection, department_name):
    query = {}
    if department_name:
        query["department"] = department_name
    patients = list(patients_collection.find(query, {"_id": 0}))

    disease_count = {}
    total_patients = len(patients)
    if total_patients == 0:
        return {}, "Không có dữ liệu bệnh nhân"

    for patient in patients:
        disease = patient["disease"]
        if disease in disease_count:
            disease_count[disease] += 1
        else:
            disease_count[disease] = 1

    # Tính tỷ lệ phần trăm bệnh nhân mắc từng loại bệnh
    disease_ratio = {
        disease: (count / total_patients) * 100
        for disease, count in disease_count.items()
    }

    if department_name:
        custom_title = f"Tỷ lệ bệnh nhân mắc bệnh trong khoa {department_name}"
    else:
        custom_title = "Tỷ lệ bệnh nhân mắc bệnh trong toàn bệnh viện"

    return disease_ratio, custom_title
