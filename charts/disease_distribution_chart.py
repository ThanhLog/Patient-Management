# charts/disease_distribution_chart.py
import matplotlib.pyplot as plt
from collections import Counter


def create_disease_distribution_pie_chart(patients):
    # Phân loại bệnh nhân theo loại bệnh
    disease_categories = [patient["disease"] for patient in patients]

    # Tính số lượng bệnh nhân cho mỗi loại bệnh
    disease_distribution = Counter(disease_categories)

    labels = list(disease_distribution.keys())
    sizes = list(disease_distribution.values())

    # Vẽ biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")  # Đảm bảo biểu đồ tròn

    # Lưu biểu đồ vào file
    chart_path = "disease_distribution_pie_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path


def create_disease_distribution_bar_chart(patients):
    # Lọc bỏ bệnh nhân không có giá trị 'disease'
    disease_categories = [
        patient["disease"] for patient in patients if patient["disease"]
    ]

    # Tính số lượng bệnh nhân cho mỗi loại bệnh
    disease_distribution = Counter(disease_categories)

    if not disease_distribution:
        return None  # Trả về None nếu không có dữ liệu hợp lệ

    labels = list(disease_distribution.keys())
    sizes = list(disease_distribution.values())

    # Vẽ biểu đồ cột
    plt.figure(figsize=(12, 6))
    plt.bar(labels, sizes, color="skyblue")
    plt.xlabel("Loại Bệnh")
    plt.ylabel("Số Lượng Bệnh Nhân")
    plt.title("Phân Bố Bệnh Nhân Theo Loại Bệnh")

    # Lưu biểu đồ vào file
    chart_path = "disease_distribution_bar_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path