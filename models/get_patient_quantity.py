def get_patients_quantity(patients_collection, department_name):
    query = {}

    if department_name:
        query["department"] = department_name

    patients = list(patients_collection.find(query, {"_id": 0}))

    disease_count = {}

    for patient in patients:
        disease = patient["disease"]
        if disease in disease_count:
            disease_count[disease] += 1
        else:
            disease_count[disease] = 1

    if department_name:
        custom_title = f"Bệnh nhân mắc bệnh trong khoa {department_name}"
    else:
        custom_title = "Bệnh nhân mắc bệnh trong toàn bệnh viện"

    return disease_count, custom_title
