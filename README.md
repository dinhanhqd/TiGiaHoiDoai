1.	Dataset 
1.1 Dataset cho model dự đoán tỉ giá
Dataset chúng em lấy từ web kaggle về lĩnh vực Dữ liệu lịch sử cặp ngoại hối EUR USD (2002 - 2020)
Tập dữ liệu này chứa dữ liệu lịch sử được lưu từ Oanda Brokerage. Các cột biểu thị giá Bid và Ask cho mỗi phút/giờ. Ngoài ra còn có tin tức được tải xuống từ Investing.com. Chúng có thể được sử dụng để dự báo xu hướng của thị trường Forex bằng kỹ thuật học máy.
Link data
https://www.kaggle.com/datasets/imetomi/eur-usd-forex-pair-historical-data-2002-2019?resource=download
Sơ lược về data : 
 Dataset gồm 93084 hàng và 12 cột.
-	Date : Cột chữ dữ liệu ngày
-	Time: Giờ mà giá được đo
-	BO: Giá mở thầu
-	BH: Giá thầu cao nhất trong khoảng thời gian 1 giờ
-	BL: Giá thầu thấp nhất trong khoảng thời gian một giờ
-	BC: Giá đóng thầu
-	BCh: Thay đổi giữa giá mở và giá đóng
-	AO: Giá mở cửa
-	AH: Giá chào bán cao nhất trong khoảng thời gian một giờ
-	AL: Giá chào bán thấp nhất trong khoảng thời gian một giờ
  
![image](https://github.com/user-attachments/assets/f49ac08e-9015-4aac-97d9-48cac6510c3f)

Dataset cho model phân thích tình cảm 
Dataset chúng em lấy từ web kaggle
Đây là tập dữ liệu tin tức dành cho thị trường hàng hóa nơi đã chú thích thủ công hơn 10.000 tiêu đề tin tức trên nhiều chiều vào nhiều loại khác nhau. Tập dữ liệu đã được lấy mẫu trong khoảng thời gian hơn 20 năm (2000-2021). 
Tập dữ liệu đã được thu thập từ nhiều nguồn tin tức khác nhau và được chú thích bởi ba người chú thích là chuyên gia về chủ đề này. Ví dụ: mỗi tiêu đề tin tức được đánh giá theo nhiều khía cạnh khác nhau - nếu tiêu đề là tin tức liên quan đến giá thì hướng biến động giá mà nó đang nói đến là gì; tiêu đề tin tức đang nói về quá khứ hay tương lai; liệu mục tin tức có nói về việc so sánh tài sản hay không; vân vân. 
Link: https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-in-commodity-market-gold 
Data gồm 10571 dòng và 10 cột
-	Date: Ngày của tiêu đề tin tức
-	URL: URL của tin tức
-	New : Tiêu đề tin tức
-	Price Direction Up: Tiêu đề tin tức có ngụ ý hướng giá đi ngang (không thay đổi)
-	Price Direction Constant: Tiêu đề tin tức có ngụ ý hướng giá đi xuống
-	Asset Comparision: Tài sản có được so sánh không?
-	Past Information: Tiêu đề tin tức có nói về quá khứ không?
-	Future Information: Tiêu đề tin tức có nói về tương lai không?
-	Price Sentiment : Tâm lý giá hàng hóa dựa trên tiêu đề
  
![image](https://github.com/user-attachments/assets/8cd0dfea-dcc1-44d2-8997-4846243dcde3)

![image](https://github.com/user-attachments/assets/62be7eaa-816b-47b2-abbd-9b6ecaee112c)

. Xây dự model cho chatbot RAG

 	![image](https://github.com/user-attachments/assets/0cc2cdd5-42c3-425f-ae0a-ad5b9e020517)

Xây dựng model dự đoán tỉ giá
Với tính năng dự đoán tỉ giá chúng em lấy model tự training với dữ liệu đã thu thập trước đó. 
 Model được xây dựng trên kiến trúc LSTM
 
![image](https://github.com/user-attachments/assets/4707b344-cb56-401f-999d-c5b0c9678f34)

![image](https://github.com/user-attachments/assets/5b841cff-f5e4-473e-8a8f-61a0bc89a397)

![image](https://github.com/user-attachments/assets/8040e1bc-3611-46ad-ab15-00e3e85d2903)

web demo

![image](https://github.com/user-attachments/assets/fa27cb34-9c0d-43a9-934a-595e87ec06bb)

![image](https://github.com/user-attachments/assets/85677d65-c088-4897-a260-24223e77691d)

![image](https://github.com/user-attachments/assets/5496521c-569c-41aa-a2c5-abbade650b45)


