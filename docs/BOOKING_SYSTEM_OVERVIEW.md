# ระบบจองสถานี Workshop
## GEM Coupler | OSSEOLAB Plate | Leica Microscope

---

## 📊 ความจุระบบ

### สรุปความจุ

| สถานี | โต๊ะ | เวลา/คน | รอบทั้งหมด | ความจุ | %  |
|---|---|---|---|---|---|
| **GEM Coupler** | 3 | 15 นาที | 18 รอบ | **54 คน** | 58% |
| **OSSEOLAB Plate** | 2 | 20 นาที | 13 รอบ | **26 คน** | 28% |
| **Leica Microscope** | 1 | 20 นาที | 13 รอบ | **13 คน** | 14% |
| **รวม** | **6** | - | - | **93 คน** | 100% |

**⏰ เวลา:** 12:30-17:00 น. (4.5 ชั่วโมง = 270 นาที)

---

## 🎯 กฎการจอง

### 1. แต่ละคนเลือกได้เพียง 1 สถานี
- ✅ GEM Coupler (15 นาที)
- ✅ OSSEOLAB Plate (20 นาที)  
- ✅ Leica Microscope (20 นาที)

### 2. จองได้ 1 รอบเท่านั้น
- ไม่สามารถจองซ้ำในสถานีเดียวกัน
- ไม่สามารถเปลี่ยนสถานีหลังจองแล้ว

### 3. First Come, First Served
- ใครจองก่อนได้ก่อน
- เมื่อเต็มจะปิดรับอัตโนมัติ

---

## 🗓️ Timeline Workshop

```
12:30-13:00  Registration & Opening (30 นาที)
13:00-16:30  Workshop Sessions (210 นาที)
16:30-17:00  Closing & Certificate (30 นาที)
```

### ตารางเวลาแต่ละสถานี

#### 🔹 GEM Coupler (18 รอบ × 15 นาที)
```
รอบ 1:  13:00-13:15
รอบ 2:  13:15-13:30
รอบ 3:  13:30-13:45
...
รอบ 18: 16:15-16:30
```

#### 🔹 OSSEOLAB Plate (13 รอบ × 20 นาที)
```
รอบ 1:  13:00-13:20
รอบ 2:  13:20-13:40
รอบ 3:  13:40-14:00
...
รอบ 13: 15:50-16:10
```

#### 🔹 Leica Microscope (13 รอบ × 20 นาที)
```
รอบ 1:  13:00-13:20
รอบ 2:  13:20-13:40
รอบ 3:  13:40-14:00
...
รอบ 13: 15:50-16:10
```

---

## 💻 ระบบจอง (3 ส่วน)

### 1. Frontend (หน้าเว็บจอง)
**เทคโนโลยี:** HTML + CSS + JavaScript

**ฟีเจอร์:**
- เลือกสถานี (1 จาก 3)
- เลือกช่วงเวลา (Time Slot)
- กรอกข้อมูลส่วนตัว
- ยืนยันการจอง

**หน้าเว็บ:**
- `/` — หน้าแรก
- `/booking` — หน้าจอง
- `/confirmation` — หน้ายืนยัน
- `/my-booking` — ดูการจองของตัวเอง

---

### 2. Backend (API Server)
**เทคโนโลยี:** Python Flask

**API Endpoints:**

#### GET `/api/stations`
ดูข้อมูลสถานีทั้งหมด

**Response:**
```json
{
  "stations": [
    {
      "id": "gem",
      "name": "GEM Coupler",
      "tables": 3,
      "time_per_person": 15,
      "total_capacity": 54,
      "available": 42
    },
    {
      "id": "plate",
      "name": "OSSEOLAB Plate",
      "tables": 2,
      "time_per_person": 20,
      "total_capacity": 26,
      "available": 18
    },
    {
      "id": "leica",
      "name": "Leica Microscope",
      "tables": 1,
      "time_per_person": 20,
      "total_capacity": 13,
      "available": 7
    }
  ]
}
```

---

#### GET `/api/timeslots?station=gem`
ดูช่วงเวลาว่างของสถานี

**Response:**
```json
{
  "station": "gem",
  "timeslots": [
    {
      "slot_id": "gem_1",
      "time": "13:00-13:15",
      "table": 1,
      "available": true
    },
    {
      "slot_id": "gem_2",
      "time": "13:00-13:15",
      "table": 2,
      "available": true
    },
    {
      "slot_id": "gem_3",
      "time": "13:00-13:15",
      "table": 3,
      "available": false
    }
  ]
}
```

---

#### POST `/api/booking`
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
  "slot_id": "gem_1"
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

---

#### GET `/api/booking/:booking_id`
ดูข้อมูลการจอง

**Response:**
```json
{
  "booking_id": "BK20251004001",
  "name": "Dr. สมชาย ใจดี",
  "email": "somchai@example.com",
  "station": "GEM Coupler",
  "time": "13:00-13:15",
  "table": 1,
  "status": "confirmed",
  "qr_code": "https://api.qrserver.com/v1/create-qr-code/?data=BK20251004001"
}
```

---

#### DELETE `/api/booking/:booking_id`
ยกเลิกการจอง

**Response:**
```json
{
  "success": true,
  "message": "ยกเลิกการจองสำเร็จ"
}
```

---

### 3. Database (SQLite)
**เทคโนโลยี:** SQLite (ง่าย ไม่ต้องติดตั้ง Server)

**Tables:**

#### `stations`
```sql
CREATE TABLE stations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tables INTEGER NOT NULL,
    time_per_person INTEGER NOT NULL,
    total_capacity INTEGER NOT NULL
);
```

#### `timeslots`
```sql
CREATE TABLE timeslots (
    slot_id TEXT PRIMARY KEY,
    station_id TEXT NOT NULL,
    round_number INTEGER NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    table_number INTEGER NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (station_id) REFERENCES stations(id)
);
```

#### `bookings`
```sql
CREATE TABLE bookings (
    booking_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    institution TEXT NOT NULL,
    position TEXT NOT NULL,
    slot_id TEXT NOT NULL,
    status TEXT DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_id) REFERENCES timeslots(slot_id)
);
```

---

## 🚀 วิธีติดตั้งและใช้งาน

### Step 1: ติดตั้ง Dependencies
```bash
cd ~/booking_system/backend
pip3 install flask flask-cors sqlite3
```

### Step 2: สร้าง Database
```bash
python3 init_database.py
```

### Step 3: รัน Backend Server
```bash
python3 app.py
```
**Server จะรันที่:** http://localhost:5000

### Step 4: เปิด Frontend
```bash
cd ~/booking_system/frontend
python3 -m http.server 8080
```
**Frontend จะรันที่:** http://localhost:8080

---

## 📱 User Flow

### 1. ผู้เข้าร่วมเข้าเว็บไซต์
```
https://workshop.example.com
```

### 2. เลือกสถานี
- เห็นความจุและที่ว่างของแต่ละสถานี
- เลือก 1 สถานี

### 3. เลือกช่วงเวลา
- เห็นตารางเวลาว่างทั้งหมด
- เลือก 1 ช่วงเวลา

### 4. กรอกข้อมูล
- ชื่อ-นามสกุล
- อีเมล
- เบอร์โทร
- สถาบัน
- ตำแหน่ง

### 5. ยืนยันการจอง
- ตรวจสอบข้อมูล
- กดยืนยัน

### 6. ได้รับ Email ยืนยัน
- Booking ID
- QR Code
- รายละเอียดการจอง

### 7. วันงาน
- Scan QR Code เช็คอิน
- เข้าสถานีตามเวลาที่จอง

---

## 🎨 หน้าจอ UI/UX

### หน้าแรก
```
┌──────────────────────────────────────────┐
│  🔬 GEM Coupler Workshop                 │
│  Booking System                          │
└──────────────────────────────────────────┘

📅 วันที่: 15 ตุลาคม 2025
⏰ เวลา: 12:30-17:00 น.
📍 สถานที่: โรงพยาบาลรามาธิบดี

┌──────────────────────────────────────────┐
│  เลือกสถานีที่ต้องการ:                   │
│                                          │
│  🔹 GEM Coupler                          │
│     15 นาที | 54/54 ที่ว่าง             │
│     [จองเลย]                             │
│                                          │
│  🔹 OSSEOLAB Plate                       │
│     20 นาที | 26/26 ที่ว่าง             │
│     [จองเลย]                             │
│                                          │
│  🔹 Leica Microscope                     │
│     20 นาที | 13/13 ที่ว่าง             │
│     [จองเลย]                             │
└──────────────────────────────────────────┘
```

---

### หน้าเลือกเวลา
```
┌──────────────────────────────────────────┐
│  🔹 GEM Coupler                          │
│  เลือกช่วงเวลา (15 นาที)                 │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│  โต๊ะ 1                                  │
│  ○ 13:00-13:15  ○ 13:15-13:30  ● 13:30  │
│  ○ 13:45-14:00  ○ 14:00-14:15  ○ 14:15  │
│  ...                                     │
│                                          │
│  โต๊ะ 2                                  │
│  ○ 13:00-13:15  ● 13:15-13:30  ○ 13:30  │
│  ○ 13:45-14:00  ○ 14:00-14:15  ○ 14:15  │
│  ...                                     │
│                                          │
│  โต๊ะ 3                                  │
│  ○ 13:00-13:15  ○ 13:15-13:30  ○ 13:30  │
│  ○ 13:45-14:00  ○ 14:00-14:15  ○ 14:15  │
│  ...                                     │
└──────────────────────────────────────────┘

○ ว่าง  ● เต็ม

[ถัดไป]
```

---

### หน้ากรอกข้อมูล
```
┌──────────────────────────────────────────┐
│  📋 กรอกข้อมูลส่วนตัว                     │
└──────────────────────────────────────────┘

ชื่อ-นามสกุล: [________________]
อีเมล: [________________]
เบอร์โทร: [________________]
สถาบัน/โรงพยาบาล: [________________]
ตำแหน่ง: [▼ เลือก]

[กลับ]  [ยืนยันการจอง]
```

---

### หน้ายืนยัน
```
┌──────────────────────────────────────────┐
│  ✅ จองสำเร็จ!                           │
└──────────────────────────────────────────┘

📋 รายละเอียดการจอง:

Booking ID: BK20251004001
ชื่อ: Dr. สมชาย ใจดี
สถานี: GEM Coupler
เวลา: 13:00-13:15 น.
โต๊ะ: 1

📱 QR Code สำหรับเช็คอิน:
[QR Code Image]

✉️ ข้อมูลการจองได้ส่งไปที่อีเมลแล้ว

[ดาวน์โหลด QR Code]  [กลับหน้าแรก]
```

---

## 🔐 ความปลอดภัย

### 1. จำกัดการจอง
- 1 อีเมล = 1 การจอง
- ตรวจสอบ Email Format
- ตรวจสอบเบอร์โทร Format

### 2. Prevent Double Booking
- ล็อก Timeslot เมื่อมีคนจอง
- ตรวจสอบความว่างก่อนยืนยัน

### 3. Rate Limiting
- จำกัดการเรียก API (100 requests/นาที)
- ป้องกัน Bot

---

## 📊 Admin Dashboard

### ดูสถิติ Real-time
```
┌──────────────────────────────────────────┐
│  📊 Dashboard                            │
└──────────────────────────────────────────┘

จำนวนการจองทั้งหมด: 87/93 คน (93%)

🔹 GEM Coupler: 52/54 (96%)
🔹 OSSEOLAB Plate: 24/26 (92%)
🔹 Leica Microscope: 11/13 (85%)

───────────────────────────────────────────

📈 กราฟการจองตามเวลา:
[กราฟแท่ง]

───────────────────────────────────────────

📋 รายชื่อผู้จองล่าสุด:
1. Dr. สมชาย ใจดี - GEM (13:00)
2. Dr. สมหญิง ดีใจ - Plate (13:00)
3. Dr. สมศักดิ์ มีสุข - Leica (13:00)
...

[Export Excel]  [Export PDF]
```

---

## 💡 Tips สำหรับความสำเร็จ

1. **เปิดรับจองล่วงหน้า 2-3 สัปดาห์**
2. **ประชาสัมพันธ์ผ่านหลายช่องทาง**
3. **มี Reminder Email** (1 สัปดาห์ก่อน, 1 วันก่อน)
4. **เตรียม Backup Plan** (เผื่อระบบล่ม)
5. **มีทีมงาน IT** (ดูแลระบบในวันงาน)

---

## 🎉 สรุป

ระบบจองนี้จะช่วยให้:

1. **รองรับผู้เข้าร่วมได้ถึง 93 คน**
2. **จองง่าย ใช้งานง่าย**
3. **จัดการอัตโนมัติ**
4. **มี QR Code เช็คอิน**
5. **Admin ดูสถิติ Real-time**

**ระบบมืออาชีพ พร้อมใช้งานจริง! 🚀**

---

**สร้างโดย:** Manus AI  
**วันที่:** 4 ตุลาคม 2025  
**เวอร์ชัน:** 1.0
