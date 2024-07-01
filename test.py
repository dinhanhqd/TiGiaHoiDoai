import pandas as pd
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt


# Load mô hình đã lưu
model = load_model('models/model.h5')

# Đọc dữ liệu từ file CSV
data = pd.read_csv('data_model/Book1.csv')

# Tạo cột "H" với giá trị tăng dần từ 0
data['H'] = range(len(data))

# Lấy 50 dòng cuối cùng của cột "close"
last_50_close = data['close'].tail(50).values.reshape((1, 50, 1))

# Số lần lặp lại
num_iterations = 30

# Lưu trữ các dự đoán mới
predicted_values = []

for i in range(num_iterations):
    # Dự đoán trên 50 dòng cuối cùng của cột "close"
    predictions = model.predict(last_50_close)

    # Lưu trữ dự đoán mới
    predicted_values.append(predictions[0][0])

    # Cập nhật dữ liệu với các dự đoán mới
    data_length = len(data)
    data.loc[data_length, 'H'] = data.loc[data_length - 1, 'H'] + 1  # Tăng giá trị của cột "H" cho mỗi dòng mới
    data.loc[data_length, 'close'] = predictions[0][0]  # Thêm dự đoán như một giá trị đơn cho mỗi dòng

    # Lấy 50 dòng cuối cùng của cột "close" để dự đoán tiếp
    last_50_close = data['close'].tail(50).values.reshape((1, 50, 1))

# Vẽ biểu đồ
plt.figure(figsize=(10, 6))
plt.plot(data['H'], data['close'], label='Close', color='blue')
plt.plot(data.tail(num_iterations)['H'], predicted_values, label='Predictions', color='red')
plt.xlabel('time')
plt.ylabel('Close')
plt.title('Close Price with Predictions')
plt.legend()
plt.grid(True)
plt.show()