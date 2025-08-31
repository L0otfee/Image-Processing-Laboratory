# Streamlit Image Processing App

# วิชา 241-353 ARTIFICIAL INTELLIGENCE ECOSYSTEM

## 6510110683

## โดย ลุตฟี ซาและ (วิศวกรรมปัญญาประดิษฐ์)

## บทนำ

Streamlit Image Processing App เป็นแอปพลิเคชันที่พัฒนาด้วย Streamlit สำหรับการประมวลผลภาพ โดยมีฟีเจอร์ที่ช่วยให้ผู้ใช้สามารถอัปโหลดภาพ ปรับแต่ง และวิเคราะห์ภาพได้อย่างง่ายดาย

## วัตถุประสงค์

- เพื่อให้ผู้ใช้สามารถประมวลผลภาพได้อย่างง่ายดายผ่านเว็บแอปพลิเคชัน
- เพื่อแสดงผลการปรับแต่งภาพแบบเรียลไทม์
- เพื่อให้ผู้ใช้สามารถดาวน์โหลดภาพที่ปรับแต่งแล้วและสถิติของภาพ

## ฟีเจอร์

- อัปโหลดภาพจากไฟล์หรือกล้อง
- การปรับแต่งภาพ เช่น การปรับความสว่าง คอนทราสต์ และการเบลอ
- การตรวจจับขอบภาพและการประมวลผลเชิงสัณฐานวิทยา
- การแสดงกราฟและสถิติของภาพ
- การดาวน์โหลดภาพและข้อมูลสถิติ

## เทคโนโลยีที่ใช้

- **Python**: ภาษาโปรแกรมหลัก
- **Streamlit**: เฟรมเวิร์กสำหรับการพัฒนาเว็บแอปพลิเคชัน
- **OpenCV**: สำหรับการประมวลผลภาพ
- **NumPy**: สำหรับการจัดการข้อมูลเชิงตัวเลข
- **Pillow**: สำหรับการจัดการไฟล์ภาพ
- **Plotly**: สำหรับการสร้างกราฟแบบโต้ตอบ

## Clone โปรเจกต์

```bash
git clone git@github.com:L0otfee/Image-Processing-Laboratory.git
cd prototype
```

## การใช้งาน

1. ติดตั้ง dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. รันแอปพลิเคชัน:
   ```bash
   streamlit run streamlit_image_app.py
   ```
3. เปิดเว็บเบราว์เซอร์และไปที่:
   ```
   http://localhost:8501
   ```

## โครงสร้างไฟล์

- **streamlit_image_app.py**: ไฟล์หลักของแอปพลิเคชัน
- **requirements.txt**: รายการ dependencies ที่ต้องติดตั้ง

## ตัวอย่างผลการแสดง

- หน้าหลักของแอปพลิเคชัน
- การแสดงภาพต้นฉบับและภาพที่ปรับแต่ง
- กราฟและสถิติของภาพ

## รายละเอียดการใช้งานแต่ละฟีเจอร์

### 1. อัปโหลดภาพ
- ผู้ใช้สามารถอัปโหลดภาพจากไฟล์ในเครื่อ
- รองรับไฟล์ประเภท PNG, JPG, JPEG
<img width="1440" height="848" alt="Screenshot 2568-08-31 at 13 39 41" src="https://github.com/user-attachments/assets/34e67c6c-f7f8-40c0-ae53-f61aa9fe280b" />

- เลือกใช้กล้องเพื่อถ่ายภาพใหม่
<img width="1433" height="846" alt="Screenshot 2568-08-31 at 13 18 35" src="https://github.com/user-attachments/assets/2d83a9db-e072-45ea-b1e0-8cedf0f4bf6b" />


### 2. การปรับแต่งภาพ
- **การแปลงภาพเป็น Grayscale**: แปลงภาพสีให้เป็นภาพขาวดำ เหมาะสำหรับการลดความซับซ้อนของข้อมูลภาพ
- **ความสว่าง (Brightness)**: ปรับเพิ่มหรือลดความสว่างของภาพ
- **คอนทราสต์ (Contrast)**: ปรับความแตกต่างระหว่างส่วนมืดและสว่าง
- **การเบลอ (Gaussian Blur)**: เพิ่มความเบลอให้กับภาพ
<img width="1440" height="849" alt="Screenshot 2568-08-31 at 13 38 28" src="https://github.com/user-attachments/assets/f3922a85-11c2-4457-ad3f-c0e462c5498b" />

### 3. การตรวจจับขอบภาพ (Edge Detection)
- ใช้ตัวเลือก "Enable Edge Detection" เพื่อเปิดใช้งาน
- สามารถปรับค่าความไวของการตรวจจับขอบได้ด้วย "Low Threshold" และ "High Threshold"
<img width="1440" height="850" alt="Screenshot 2568-08-31 at 13 43 47" src="https://github.com/user-attachments/assets/6791c40d-8444-4a75-a88b-dacd03feb76d" />

### 4. การประมวลผลเชิงสัณฐานวิทยา (Morphological Operations)
- เลือกประเภทการประมวลผล เช่น Erosion, Dilation, Opening, Closing
- ปรับขนาด Kernel เพื่อควบคุมผลลัพธ์
![Image 31-8-2568 BE at 13 45](https://github.com/user-attachments/assets/ada90e43-8015-43a4-b5c4-4c8a77533d2f)

### 5. การแสดงผล
- แสดงภาพต้นฉบับและภาพที่ปรับแต่งในรูปแบบเปรียบเทียบ
- มีกราฟ Histogram และการเปรียบเทียบสถิติ เช่น Mean, Std, Min, Max
<img width="1051" height="697" alt="Screenshot 2568-08-31 at 13 49 55" src="https://github.com/user-attachments/assets/304152ca-60cf-40b5-b858-91b846fe0848" />
<img width="1048" height="625" alt="Screenshot 2568-08-31 at 13 50 15" src="https://github.com/user-attachments/assets/880cd710-4777-4b64-b56c-8936d5025a16" />
<img width="1048" height="625" alt="Screenshot 2568-08-31 at 13 50 25" src="https://github.com/user-attachments/assets/3355594c-b234-438b-b8bc-ebd3218ae973" />
<img width="1051" height="790" alt="Screenshot 2568-08-31 at 13 51 12" src="https://github.com/user-attachments/assets/1c734ec7-1c7d-4f76-b290-c4cc1ee25e3d" />


### 6. การดาวน์โหลด
- ดาวน์โหลดภาพที่ปรับแต่งแล้วในรูปแบบ PNG
- ดาวน์โหลดข้อมูลสถิติของภาพในรูปแบบ CSV
<img width="364" height="309" alt="Screenshot 2568-08-31 at 13 53 06" src="https://github.com/user-attachments/assets/cfc2583c-f85b-43df-9343-6eb7e91b9b82" />


## สร้างโดย ลุตฟี ซาและ

Email: Lutfee2salaeh@gmail.com

ขอบคุณที่สนใจในโปรเจกต์นี้!
