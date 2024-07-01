import streamlit as st
import pandas as pd
import os
import tensorflow as tf
import chardet
import matplotlib.pyplot as plt
import numpy as np

# Đường dẫn đến các thư mục data_model và models
data_model_dir = "data_model"
models_dir = "model_data"


def load_model(model_path):
    return tf.keras.models.load_model(model_path)


def prepare_data(data):
    # Giữ chỉ cột "close"
    if 'close' not in data.columns:
        raise ValueError("The CSV file does not contain a 'close' column.")
    data = data[['close']]

    # Thêm cột "H" với giá trị tăng dần từ 0
    data['H'] = range(len(data))

    # Lấy 50 dòng cuối cùng của cột "close"
    last_50_close = data['close'].tail(50).values.copy()

    # Shuffle the last 50 close prices randomly
    np.random.shuffle(last_50_close)

    # Reshape the shuffled data for prediction
    last_50_close = last_50_close.reshape((1, 50, 1))

    return data, last_50_close


def read_csv_with_encoding_detection(file_path):
    # List of alternative encodings to try
    encodings_to_try = ['utf-8', 'iso-8859-1', 'latin1']

    for encoding in encodings_to_try:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except Exception:
            continue

    # If all encodings fail, raise an error
    raise ValueError("Failed to read CSV with any encoding.")


def main():
    st.title("Model Management")
    st.write("- Đưa data tối thiểu là 50 dòng trong CSV")

    # Tạo hai cột sử dụng layout của Streamlit
    col1, col2 = st.columns(2)

    # Selectbox để chọn model
    with col1:
        st.write("### Chọn Model")
        model_files = os.listdir(models_dir)
        selected_model = st.selectbox("Chọn một model", model_files)

    # Selectbox để chọn data
    with col2:
        st.write("### Chọn Data")
        data_files = os.listdir(data_model_dir)
        selected_data = st.selectbox("Chọn một file data", data_files)

    # Sidebar để upload file CSV
    st.sidebar.title("Upload File CSV")
    uploaded_csv = st.sidebar.file_uploader("Chọn một file CSV", type=["csv"])

    # Thêm thanh trượt để thay đổi số lần lặp lại (num_iterations)
    num_iterations = st.sidebar.slider("Chọn số lần dự đoán", min_value=1, max_value=100, value=30)

    if uploaded_csv:
        # Lưu file CSV được upload trong thư mục data_model
        csv_file_path = f"{data_model_dir}/{uploaded_csv.name}"
        with open(csv_file_path, "wb") as f:
            f.write(uploaded_csv.getbuffer())

        # Xử lý file CSV được upload
        try:
            df = read_csv_with_encoding_detection(csv_file_path)
            st.sidebar.write(f"Uploaded CSV file: {csv_file_path}")
            st.sidebar.write(f"Data shape: {df.shape}")

            # Hiển thị 50 dòng đầu tiên của dữ liệu CSV
            st.write("50 dòng đầu tiên của file CSV được upload:")
            st.write(df.head(50))
        except ValueError as e:
            st.sidebar.error(f"Lỗi đọc file CSV: {e}")

    # Thêm button để dự đoán
    if st.button("Dự đoán"):
        if selected_model and selected_data:
            # Load model được chọn
            model_path = os.path.join(models_dir, selected_model)
            model = load_model(model_path)

            # Load và chuẩn bị dữ liệu được chọn
            data_path = os.path.join(data_model_dir, selected_data)
            data = read_csv_with_encoding_detection(data_path)
            try:
                data, last_50_close = prepare_data(data)
            except ValueError as e:
                st.error(f"Lỗi chuẩn bị dữ liệu: {e}")
                return

            # Số lần lặp lại để dự đoán
            predicted_values = []

            for i in range(num_iterations):
                # Dự đoán trên 50 dòng cuối cùng của cột "close"
                predictions = model.predict(last_50_close)

                # Lưu trữ dự đoán mới
                predicted_values.append(predictions[0][0])

                # Cập nhật dữ liệu với các dự đoán mới
                data_length = len(data)
                data.loc[data_length] = [predictions[0][0], data.loc[data_length - 1, 'H'] + 1]

                # Shuffle the last 50 close prices randomly
                np.random.shuffle(last_50_close[:, :, 0])

                # Lấy 50 dòng cuối cùng của cột "close" để dự đoán tiếp
                #last_50_close = data['close'].tail(50).values.reshape((1, 50, 1))
                # Extract the last 100 values of the "close" column
                last_50_close = data['close'].tail(50).values.copy()

                # Shuffle the last 100 close prices randomly
                np.random.shuffle(last_50_close)

                # Reshape the shuffled data for prediction
                last_50_close = last_50_close.reshape((1, 50, 1))

            # Vẽ biểu đồ
            plt.figure(figsize=(10, 6))
            plt.plot(data['H'], data['close'], label='Close', color='blue')
            plt.plot(data.tail(num_iterations)['H'], predicted_values, label='Predictions', color='red')
            plt.xlabel('Time')
            plt.ylabel('Close')
            plt.title('Close Price with Predictions')
            plt.legend()
            plt.grid(True)
            st.pyplot(plt)
        else:
            st.write("Vui lòng chọn cả model và file data trước khi dự đoán.")


if __name__ == "__main__":
    main()
