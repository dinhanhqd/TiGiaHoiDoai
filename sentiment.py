import streamlit as st
import torch


# Assume `ModelClass` is the class of your model
class ModelClass(torch.nn.Module):
    def __init__(self):
        super(ModelClass, self).__init__()
        self.fc = torch.nn.Linear(10, 3)  # Output size changed to 3 for 3 classes
        self.softmax = torch.nn.Softmax(dim=1)  # Softmax layer for converting logits to probabilities

    def forward(self, x):
        x = self.fc(x)
        return self.softmax(x)  # Apply softmax to get probabilities


def preprocess_text(text):
    # Example preprocessing, replace with your actual preprocessing logic
    input_ids = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=torch.float32).unsqueeze(0)  # Example tensor
    return input_ids


def classify_text_by_keywords(text):
    positive_keywords = ['like', 'love', 'good', 'very good', 'fun']
    negative_keywords = ['dislike', 'not', 'angry', 'hate']

    text_lower = text.lower()
    for word in positive_keywords:
        if word in text_lower:
            return "Tích cực"
    for word in negative_keywords:
        if word in text_lower:
            return "Tiêu cực"
    return None


def main():
    st.title("Dự đoán với mô hình")

    # Instantiate the model
    model = ModelClass()

    # Define the path to the saved model
    model_save_path = "model.pth"

    # Load the model's state dictionary
    try:
        model.load_state_dict(torch.load(model_save_path))
        model.eval()  # Set the model to evaluation mode
        st.write("Mô hình đã được tải thành công")
    except Exception as e:
        st.write(f"----------")

    # Input text area
    text = st.text_area("Nhập đoạn văn bản:", "Nhập đoạn văn bản ở đây")

    if st.button("Dự đoán"):
        # First check the text for keywords
        predicted_label = classify_text_by_keywords(text)

        if predicted_label is None:
            # Preprocess the input text if no keywords matched
            input_ids = preprocess_text(text)

            # Make a prediction using the model
            with torch.no_grad():
                outputs = model(input_ids)
                probabilities = outputs.squeeze().tolist()  # Convert probabilities tensor to list
                predicted_class = torch.argmax(outputs, dim=1).item()

            # Map predicted class to label
            label_map = {0: "Tiêu cực", 1: "Trung tính", 2: "Tích cực"}
            predicted_label = label_map[predicted_class]

        st.write(f"Nhãn dự đoán: {predicted_label}")


if __name__ == "__main__":
    main()
