import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO


# Hàm vẽ biểu đồ cột
def create_bar_chart(data, title):
    plt.clf()  # Xóa biểu đồ cũ
    labels = data.keys()
    values = data.values()

    plt.figure(figsize=(10, 6))  # Điều chỉnh kích thước biểu đồ
    plt.bar(labels, values, color="blue")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


# Hàm vẽ biểu đồ tròn
def create_pie_chart(data, title):
    plt.clf()  # Xóa biểu đồ cũ
    labels = data.keys()
    sizes = data.values()

    plt.figure(figsize=(8, 8))  # Điều chỉnh kích thước biểu đồ
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.title(title)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


# Hàm vẽ biểu đồ đường
def create_line_chart(data, x_label, y_label, title):
    plt.clf()  # Xóa biểu đồ cũ
    x = list(data.keys())
    y = list(data.values())

    plt.figure(figsize=(10, 6))  # Điều chỉnh kích thước biểu đồ
    plt.plot(x, y, marker="o", color="green", label="Data Points")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf
