# 🔬 GEM Coupler Workshop - Booking System

ระบบจองสถานี Workshop แบบครบวงจร สำหรับ GEM Coupler, OSSEOLAB Plate, และ Leica Microscope

**ความจุ:** 93 คน (GEM 54 + Plate 26 + Leica 13)  
**เวลา:** 12:30-17:00 น. (4.5 ชั่วโมง)

---

## 📦 สิ่งที่ได้รับ

```
booking_system/
├── backend/                # Backend API (Flask)
│   ├── app.py             # Main API server
│   ├── init_database.py   # Database initialization script
│   └── workshop_booking.db # SQLite database (auto-generated)
│
├── frontend/              # Frontend Web Application
│   ├── index.html         # Main page
│   ├── style.css          # Styles
│   └── script.js          # JavaScript logic
│
├── docs/                  # Documentation
│   └── BOOKING_SYSTEM_OVERVIEW.md
│
└── README.md              # This file
```

---

## 🚀 Quick Start

### Step 1: ติดตั้ง Dependencies

```bash
cd ~/booking_system/backend
pip3 install flask flask-cors
```

### Step 2: สร้าง Database

```bash
python3.11 init_database.py
```

**Output:**
```
============================================================
🔧 Initializing Workshop Booking Database
============================================================

📋 Dropping existing tables...
✅ Existing tables dropped

📋 Creating stations table...
✅ Stations table created

📋 Creating timeslots table...
✅ Timeslots table created

📋 Creating bookings table...
✅ Bookings table created

📋 Inserting stations...
✅ 3 stations inserted

📋 Generating timeslots...

   🔹 GEM Coupler: 18 rounds × 3 tables = 54 slots
   🔹 OSSEOLAB Plate: 13 rounds × 2 tables = 26 slots
   🔹 Leica Microscope: 13 rounds × 1 tables = 13 slots

✅ 93 timeslots generated

============================================================
✅ Database initialized successfully!
============================================================

📊 Database Summary:
   Stations: 3
   Timeslots: 93
   Total Capacity: 93 people

   Database file: workshop_booking.db

🚀 Ready to start the server!
   Run: python3 app.py
============================================================
```

### Step 3: รัน Backend Server

```bash
python3.11 app.py
```

**Server จะรันที่:** http://localhost:5000

### Step 4: รัน Frontend

เปิด Terminal ใหม่:

```bash
cd ~/booking_system/frontend
python3.11 -m http.server 8080
```

**Frontend จะรันที่:** http://localhost:8080

### Step 5: เปิดเบราว์เซอร์

```
http://localhost:8080
```

---

## 📊 ความจุระบบ

| สถานี | โต๊ะ | เวลา/คน | รอบทั้งหมด | ความจุ | % |
|---|---|---|---|---|---|
| **GEM Coupler** | 3 | 15 นาที | 18 รอบ | **54 คน** | 58% |
| **OSSEOLAB Plate** | 2 | 20 นาที | 13 รอบ | **26 คน** | 28% |
| **Leica Microscope** | 1 | 20 นาที | 13 รอบ | **13 คน** | 14% |
| **รวม** | **6** | - | - | **93 คน** | 100% |

---

## 🎯 ฟีเจอร์หลัก

### ✅ สำหรับผู้เข้าร่วม
- เลือกสถานีได้ 1 จาก 3 สถานี
- เลือกช่วงเวลาที่ว่าง
- กรอกข้อมูลส่วนตัว
- ได้รับ QR Code สำหรับเช็คอิน
- ได้รับ Email ยืนยัน

### ✅ สำหรับผู้จัด
- ดูสถิติการจอง Real-time
- จัดการการจองอัตโนมัติ
- ป้องกัน Double Booking
- Export ข้อมูล

---

## 💻 API Endpoints

### GET `/api/stations`
ดูข้อมูลสถานีทั้งหมด

**Response:**
```json
{
  "success": true,
  "stations": [
    {
      "id": "gem",
      "name": "GEM Coupler",
      "tables": 3,
      "time_per_person": 15,
      "total_capacity": 54,
      "available": 42,
      "booked": 12,
      "percentage": 22.2
    }
  ]
}
```

### GET `/api/timeslots?station=gem`
ดูช่วงเวลาว่างของสถานี

**Response:**
```json
{
  "success": true,
  "station": {
    "id": "gem",
    "name": "GEM Coupler"
  },
  "timeslots": [
    {
      "slot_id": "gem_1_1",
      "round": 1,
      "time": "13:00-13:15",
      "table": 1,
      "available": true
    }
  ]
}
```

### POST `/api/booking`
สร้างการจองใหม่

**Request:**
```json
{
  "name": "Dr. สมชาย ใจดี",
  "email": "somchai@example.com",
  "phone": "081-234-5678",
  "institution": "โรงพยาบาลรามาธิบดี",
  "position": "Attending Surgeon",
  "station": "gem",
  "slot_id": "gem_1_1"
}
```

**Response:**
```json
{
  "success": true,
  "booking_id": "BK20251004001",
  "message": "จองสำเร็จ!",
  "details": {
    "station": "GEM Coupler",
    "time": "13:00-13:15",
    "table": 1,
    "qr_code": "https://api.qrserver.com/v1/create-qr-code/?data=BK20251004001"
  }
}
```

### GET `/api/booking/<booking_id>`
ดูข้อมูลการจอง

### DELETE `/api/booking/<booking_id>`
ยกเลิกการจอง

### GET `/api/stats`
ดูสถิติการจอง

---

## 🔐 ความปลอดภัย

1. **จำกัดการจอง** - 1 อีเมล = 1 การจอง
2. **Validation** - ตรวจสอบ Email และเบอร์โทร
3. **Prevent Double Booking** - ล็อก Timeslot เมื่อมีคนจอง
4. **Rate Limiting** - จำกัดการเรียก API

---

## 🎨 การปรับแต่ง

### เปลี่ยนสี

แก้ไขใน `frontend/style.css`:

```css
/* สีหลัก */
--primary-color: #00d9ff;
--secondary-color: #00ff88;
--background-color: #0a1128;
```

### เปลี่ยนข้อมูลงาน

แก้ไขใน `frontend/index.html`:

```html
<div class="info-item">
    <span class="icon">📅</span>
    <span class="text">วันที่: 15 ตุลาคม 2025</span>
</div>
```

### เปลี่ยน API URL

แก้ไขใน `frontend/script.js`:

```javascript
const API_BASE_URL = 'http://your-domain.com/api';
```

---

## 📱 การใช้งานจริง

### 1. Deploy Backend

**Option A: Deploy บน Server**
```bash
# ติดตั้ง gunicorn
pip3 install gunicorn

# รัน production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option B: Deploy บน Cloud (Heroku, Railway, etc.)**
- สร้าง `requirements.txt`
- สร้าง `Procfile`
- Push to Git

### 2. Deploy Frontend

**Option A: Static Hosting (GitHub Pages, Netlify, Vercel)**
- Upload ไฟล์ใน `frontend/`
- อัพเดท `API_BASE_URL` ใน `script.js`

**Option B: Same Server**
- ใช้ Nginx serve static files
- Reverse proxy ไปยัง Flask API

---

## 🐛 Troubleshooting

### ปัญหา: CORS Error
**แก้ไข:** ติดตั้ง `flask-cors`
```bash
pip3 install flask-cors
```

### ปัญหา: Database locked
**แก้ไข:** ปิด connection ทุกครั้ง
```python
conn.close()
```

### ปัญหา: Port already in use
**แก้ไข:** เปลี่ยน port
```bash
python3.11 -m http.server 8081
```

---

## 📞 Support

มีคำถามหรือต้องการความช่วยเหลือ?
- 📧 Email: support@example.com
- 💬 LINE: @workshop

---

## 📄 License

MIT License - Free to use and modify

---

## 👨‍💻 Credits

**Created by:** Manus AI  
**Date:** October 4, 2025  
**Version:** 1.0

---

**🎉 ขอให้การจัด Workshop ประสบความสำเร็จ!**
