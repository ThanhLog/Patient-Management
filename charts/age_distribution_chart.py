import matplotlib.pyplot as plt


def categorize_age(age):
    if age < 18:
        return "Trẻ em"
    elif 18 <= age <= 30:
        return "18 - 30"
    elif 31 <= age <= 50:
        return "31 - 50"
    elif 51 <= age <= 70:
        return "51 - 70"
    else:
        return "70+"


def create_age_distribution_pie_chart(patients):
    """Tạo biểu đồ phân bố bệnh nhân theo độ tuổi (biểu đồ tròn)."""
    # Phân loại bệnh nhân theo độ tuổi
    age_categories = [categorize_age(patient["age"]) for patient in patients]

    # Tính toán số lượng bệnh nhân cho mỗi nhóm tuổi
    age_distribution = {
        "Trẻ em": age_categories.count("Trẻ em"),
        "18 - 30": age_categories.count("18 - 30"),
        "31 - 50": age_categories.count("31 - 50"),
        "51 - 70": age_categories.count("51 - 70"),
        "70+": age_categories.count("70+"),
    }

    labels = list(age_distribution.keys())
    sizes = list(age_distribution.values())

    # Tạo biểu đồ tròn
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.title("Phân Bố Bệnh Nhân Theo Độ Tuổi (Biểu Đồ Tròn)")

    # Lưu biểu đồ
    pie_chart_path = "age_distribution_pie_chart.png"
    plt.savefig(pie_chart_path)
    plt.close()

    return pie_chart_path


def create_age_distribution_bar_chart(patients):
    """Tạo biểu đồ phân bố bệnh nhân theo độ tuổi (biểu đồ cột)."""
    # Phân loại bệnh nhân theo độ tuổi
    age_categories = [categorize_age(patient["age"]) for patient in patients]

    # Tính toán số lượng bệnh nhân cho mỗi nhóm tuổi
    age_distribution = {
        "Trẻ em": age_categories.count("Trẻ em"),
        "18 - 30": age_categories.count("18 - 30"),
        "31 - 50": age_categories.count("31 - 50"),
        "51 - 70": age_categories.count("51 - 70"),
        "70+": age_categories.count("70+"),
    }

    labels = list(age_distribution.keys())
    sizes = list(age_distribution.values())

    # Tạo biểu đồ cột
    plt.figure(figsize=(12, 6))
    plt.bar(labels, sizes, color="skyblue")
    plt.xlabel("Nhóm Độ Tuổi")
    plt.ylabel("Số Lượng Bệnh Nhân")
    plt.title("Phân Bố Bệnh Nhân Theo Độ Tuổi (Biểu Đồ Cột)")

    # Lưu biểu đồ
    bar_chart_path = "age_distribution_bar_chart.png"
    plt.savefig(bar_chart_path)
    plt.close()

    return bar_chart_path
