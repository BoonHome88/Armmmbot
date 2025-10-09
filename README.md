# ✅ Discord Bot - Railway Ready

บอท Discord สำหรับส่งข้อความอัตโนมัติตามเวลาที่กำหนด พร้อมรองรับ Railway Deployment

## 🛠 ไฟล์ที่สำคัญ

- `bot.py` - โค้ดหลักของบอท
- `requirements.txt` - ไลบรารีที่ต้องติดตั้ง
- `.env.example` - ตัวอย่างการตั้งค่า ENV
- `.gitignore` - กันไม่ให้ .env ถูกอัปขึ้น GitHub

## 🚀 Deploy ขึ้น Railway

1. สร้าง GitHub Repo แล้วอัปโหลดไฟล์ทั้งหมด (ยกเว้น `.env`)
2. เข้า https://railway.app → New Project → Deploy from GitHub
3. ไปที่แท็บ **Variables** → เพิ่ม:
   - `DISCORD_TOKEN` = ใส่ Token ของคุณ
   - `CHANNEL_ID` = ใส่ Channel ID ของห้อง Discord

4. เสร็จแล้ว Railway จะรันบอทให้ทันที

## 🧪 ทดสอบบนเครื่อง

```bash
pip install -r requirements.txt
# สร้างไฟล์ .env แล้วใส่ DISCORD_TOKEN กับ CHANNEL_ID
python bot.py
```

