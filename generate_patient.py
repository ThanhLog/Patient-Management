import random
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient  # Thêm thư viện pymongo

# Dữ liệu khoa với các bệnh phụ trách
departments = [
    {
        "name": "Khoa Nhi",
        "capacity": 50,
        "responsible_diseases": ["Sốt xuất huyết", "Sởi", "Thủy đậu"],
    },
    {
        "name": "Khoa Nội Tổng Quát",
        "capacity": 100,
        "responsible_diseases": ["Cảm cúm", "Đau đầu", "Dị ứng"],
    },
    {
        "name": "Khoa Nội Tiết",
        "capacity": 100,
        "responsible_diseases": ["Tiểu đường", "Tăng huyết áp", "Bệnh hô hấp"],
    },
    {
        "name": "Khoa Nội Lão",
        "capacity": 100,
        "responsible_diseases": ["Viêm phổi", "Gout", "Bệnh tim mạch"],
    },
    {
        "name": "Khoa Lão Khoa",
        "capacity": 100,
        "responsible_diseases": ["Alzheimer", "Bệnh xương khớp", "Bệnh tim mạch"],
    },
]

# Khởi tạo đối tượng Faker
fake = Faker()

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017")  # Thay đổi URI nếu cần
db = client["HospitalManagement"]  # Chọn cơ sở dữ liệu
patients_collection = db["Patients"]  # Chọn collection để lưu dữ liệu bệnh nhân


# Xác định bệnh theo độ tuổi và giới tính
def get_disease_by_age_and_gender(age, sex, department_diseases):
    if age < 18:  # Xử lý trường hợp bệnh nhân dưới 18 tuổi
        diseases = [
            disease
            for disease in department_diseases
            if disease in ["Sốt xuất huyết", "Sởi", "Thủy đậu"]
        ]
    elif 18 <= age <= 30:
        diseases = [
            disease
            for disease in department_diseases
            if disease in ["Cảm cúm", "Đau đầu", "Dị ứng"]
        ]
    elif 31 <= age <= 50:
        diseases = [
            disease
            for disease in department_diseases
            if disease in ["Tiểu đường", "Tăng huyết áp", "Bệnh hô hấp"]
        ]
    elif 51 <= age <= 70:
        diseases = [
            disease
            for disease in department_diseases
            if disease in ["Viêm phổi", "Gout", "Bệnh tim mạch"]
        ]
    elif age > 70:
        diseases = [
            disease
            for disease in department_diseases
            if disease in ["Alzheimer", "Bệnh xương khớp", "Bệnh tim mạch"]
        ]
    else:
        return None

    # Kiểm tra nếu danh sách bệnh không rỗng
    if diseases:
        return random.choice(diseases)
    else:
        return random.choice(
            department_diseases
        )  # Nếu không có bệnh phù hợp, trả về bệnh ngẫu nhiên trong khoa


def generate_patient_data(num_patients):
    for i in range(num_patients):
        name = fake.name()  # Tạo tên ngẫu nhiên
        age = random.randint(1, 100)  # Tạo tuổi ngẫu nhiên
        sex = random.choice(["Male", "Female"])  # Giới tính ngẫu nhiên
        treatment_cost = round(
            random.uniform(100, 5000), 2
        )  # Chi phí điều trị từ 100 đến 5000

        # Ngày nhập viện trong 30 ngày qua
        admission_date = datetime.now() - timedelta(days=random.randint(1, 30))

        # Tính ngày xuất viện ít nhất sau 7 ngày kể từ ngày nhập viện
        discharge_date = admission_date + timedelta(days=random.randint(7, 14))

        # Chọn ngẫu nhiên khoa từ mảng
        department = random.choice(departments)

        # Lấy bệnh theo độ tuổi, giới tính và bệnh phụ trách của khoa
        disease = get_disease_by_age_and_gender(
            age, sex, department["responsible_diseases"]
        )

        # Kiểm tra bệnh "Thai kỳ" và "Nạo thai"
        if disease == "Thai kỳ":
            if (
                sex == "Male" or age < 18 or age > 50
            ):  # Bệnh nhân phải là nữ và trong độ tuổi sinh sản
                disease = random.choice(department["responsible_diseases"])
        elif disease == "Nạo thai":
            if sex == "Male":  # Nạo thai chỉ áp dụng cho bệnh nhân nữ
                disease = random.choice(department["responsible_diseases"])

        # Tạo đối tượng bệnh nhân
        patient = {
            "name": name,
            "age": age,
            "disease": disease,
            "sex": sex,
            "treatment_cost": treatment_cost,
            "admission_date": admission_date.strftime("%Y-%m-%d"),
            "discharge_date": discharge_date.strftime("%Y-%m-%d"),  # Ngày xuất viện
            "department": department["name"],  # Lưu tên khoa phụ trách
        }

        # Lưu bệnh nhân vào MongoDB
        patients_collection.insert_one(patient)

        # In ra số bệnh nhân đã được tạo sau mỗi 100 bệnh nhân
        if (i + 1) % 100 == 0:
            print(f"Đã tạo bệnh nhân thứ {i + 1}")


# Gọi hàm tạo dữ liệu bệnh nhân
patients_collection.delete_many({})
generate_patient_data(2000)

print("Đã lưu dữ liệu bệnh nhân vào MongoDB.")
