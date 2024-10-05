from pymongo import MongoClient

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["HospitalManagement"]  # Chọn cơ sở dữ liệu

# Tạo collection cho các khoa
department_collection = db["Departments"]

# Tạo dữ liệu về khoa và bệnh
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

# Xóa các khoa cũ và thêm các khoa mới vào collection
department_collection.delete_many({})  # Xóa tất cả tài liệu trong collection
department_collection.insert_many(departments)  # Thêm dữ liệu khoa mới
print("Dữ liệu khoa và các bệnh đã được thêm vào cơ sở dữ liệu.")
