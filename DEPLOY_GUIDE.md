# 🚀 คู่มือ Deploy บน Railway.app

คู่มือนี้จะพาคุณ Deploy ระบบจองสถานี Workshop บน Railway.app ภายใน **5 นาที**

---

## 📋 สิ่งที่ต้องเตรียม

1. ✅ บัญชี GitHub (ถ้ายังไม่มี สมัครที่ github.com)
2. ✅ ไฟล์โปรเจกต์ (มีอยู่แล้ว)
3. ✅ อีเมล (สำหรับสมัคร Railway)

---

## 🎯 ขั้นตอนการ Deploy

### Step 1: สมัคร GitHub (ถ้ายังไม่มี)

1. ไปที่ https://github.com
2. คลิก **Sign up**
3. กรอกข้อมูล:
   - Username: เช่น `gem-workshop`
   - Email: อีเมลของคุณ
   - Password: รหัสผ่านที่ปลอดภัย
4. ยืนยันอีเมล
5. เสร็จสิ้น!

---

### Step 2: สร้าง Repository บน GitHub

1. ไปที่ https://github.com/new
2. กรอกข้อมูล:
   - **Repository name:** `gem-workshop-booking`
   - **Description:** `GEM Coupler Workshop Booking System`
   - **Public** (เลือก Public)
3. คลิก **Create repository**
4. **อย่าปิดหน้านี้!** เดี๋ยวจะใช้

---

### Step 3: Upload Code ขึ้น GitHub

เปิด Terminal และรันคำสั่งนี้:

```bash
cd ~/booking_system

# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: GEM Workshop Booking System"

# เชื่อมกับ GitHub (แทน YOUR_USERNAME ด้วย username จริง)
git remote add origin https://github.com/YOUR_USERNAME/gem-workshop-booking.git

# Push ขึ้น GitHub
git branch -M main
git push -u origin main
```

**หมายเหตุ:** ถ้า Git ขอ Login ให้ใส่:
- Username: GitHub username ของคุณ
- Password: ใช้ **Personal Access Token** (ไม่ใช่รหัสผ่านปกติ)

**วิธีสร้าง Personal Access Token:**
1. ไปที่ https://github.com/settings/tokens
2. คลิก **Generate new token (classic)**
3. ตั้งชื่อ: `Railway Deploy`
4. เลือก scope: `repo` (ทั้งหมด)
5. คลิก **Generate token**
6. **คัดลอก token** (จะเห็นแค่ครั้งเดียว!)
7. ใช้ token นี้แทนรหัสผ่าน

---

### Step 4: สมัคร Railway.app

1. ไปที่ https://railway.app
2. คลิก **Login**
3. เลือก **Login with GitHub**
4. อนุญาต Railway เข้าถึง GitHub
5. เสร็จสิ้น!

---

### Step 5: Deploy Project

1. ใน Railway Dashboard คลิก **New Project**
2. เลือก **Deploy from GitHub repo**
3. เลือก Repository: `gem-workshop-booking`
4. คลิก **Deploy Now**
5. รอ Deploy เสร็จ (1-2 นาที)

**Railway จะ:**
- ติดตั้ง Python
- ติดตั้ง packages จาก `requirements.txt`
- รัน `init_database.py` (สร้าง Database)
- รัน `gunicorn app:app` (เริ่ม Server)

---

### Step 6: เปิด Public URL

1. คลิกที่ Project ที่เพิ่ง Deploy
2. ไปที่แท็บ **Settings**
3. หัวข้อ **Networking** → คลิก **Generate Domain**
4. Railway จะสร้าง URL ให้ เช่น:
   ```
   https://gem-workshop-booking-production.up.railway.app
   ```
5. **คัดลอก URL นี้!**

---

### Step 7: อัพเดท Frontend

ต้องแก้ไข URL ใน Frontend ให้ชี้ไปที่ Railway:

1. เปิดไฟล์ `frontend/script.js`
2. แก้บรรทัดนี้:
   ```javascript
   const API_BASE_URL = 'http://localhost:5000/api';
   ```
   เป็น:
   ```javascript
   const API_BASE_URL = 'https://YOUR-RAILWAY-URL/api';
   ```
   (แทน `YOUR-RAILWAY-URL` ด้วย URL ที่ได้จาก Railway)

3. Save ไฟล์

---

### Step 8: Deploy Frontend

มี 2 ทางเลือก:

#### ทางเลือก A: Deploy Frontend บน Netlify (แนะนำ)

1. ไปที่ https://netlify.com
2. Login with GitHub
3. คลิก **Add new site** → **Import an existing project**
4. เลือก Repository เดียวกัน
5. ตั้งค่า:
   - **Base directory:** `frontend`
   - **Build command:** (ว่างไว้)
   - **Publish directory:** `frontend`
6. คลิก **Deploy**
7. ได้ URL เช่น: `https://gem-workshop.netlify.app`

#### ทางเลือก B: Deploy Frontend บน Railway (เดียวกัน)

1. ใน Railway Project เดิม
2. คลิก **New** → **Empty Service**
3. ตั้งชื่อ: `frontend`
4. ไปที่ **Settings**
5. **Start Command:**
   ```
   cd frontend && python3 -m http.server $PORT
   ```
6. **Generate Domain**
7. เสร็จสิ้น!

---

### Step 9: ทดสอบระบบ

1. เปิด Frontend URL ในเบราว์เซอร์
2. ลองจองสถานี
3. ตรวจสอบว่าทุกอย่างทำงานปกติ
4. เสร็จสิ้น! 🎉

---

## 🔧 การอัพเดท Code

เมื่อต้องการแก้ไข Code:

```bash
cd ~/booking_system

# แก้ไขไฟล์ที่ต้องการ

# Commit และ Push
git add .
git commit -m "Update: คำอธิบายการแก้ไข"
git push

# Railway จะ Auto Deploy ให้อัตโนมัติ!
```

---

## 📊 ดู Logs และ Monitoring

1. ใน Railway Dashboard
2. คลิกที่ Project
3. ไปที่แท็บ **Deployments**
4. คลิกที่ Deployment ล่าสุด
5. ดู **Logs** ได้เลย

---

## 💰 ค่าใช้จ่าย

**ฟรี $5/เดือน** (Hobby Plan)

**พอสำหรับ:**
- Workshop 2-3 สัปดาห์
- ผู้เข้าร่วม 93 คน
- Traffic ปกติ

**ถ้าเกิน:** อัพเกรดเป็น $5/เดือน (ไม่จำกัด)

---

## 🆘 Troubleshooting

### ปัญหา: Build failed
**แก้ไข:** ตรวจสอบ `requirements.txt` และ `Procfile`

### ปัญหา: Database not found
**แก้ไข:** ตรวจสอบว่า `init_database.py` รันหรือยัง

### ปัญหา: CORS error
**แก้ไข:** ตรวจสอบ `flask-cors` ใน `app.py`

### ปัญหา: 404 Not Found
**แก้ไข:** ตรวจสอบ API URL ใน `frontend/script.js`

---

## 📞 Support

มีปัญหา?
- 📧 Railway Support: https://railway.app/help
- 💬 Railway Discord: https://discord.gg/railway
- 📖 Railway Docs: https://docs.railway.app

---

## ✅ Checklist

- [ ] สมัคร GitHub
- [ ] สร้าง Repository
- [ ] Upload Code
- [ ] สมัคร Railway
- [ ] Deploy Backend
- [ ] Generate Domain
- [ ] อัพเดท Frontend URL
- [ ] Deploy Frontend
- [ ] ทดสอบระบบ
- [ ] แชร์ URL ให้ผู้เข้าร่วม

---

## 🎉 เสร็จสิ้น!

ระบบจองของคุณพร้อมใช้งานแล้ว!

**URL ที่ได้:**
- Backend API: `https://your-app.up.railway.app`
- Frontend: `https://your-app-frontend.up.railway.app`

**แชร์ URL Frontend ให้ผู้เข้าร่วมเพื่อเริ่มรับจอง! 🚀**

---

**ขอให้การจัด Workshop ประสบความสำเร็จครับ! 🎊**
