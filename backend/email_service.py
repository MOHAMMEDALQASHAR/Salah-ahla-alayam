import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT_TLS = 587
SMTP_PORT_SSL = 465
SENDER_EMAIL = os.getenv("EMAIL_SENDER", "salhahlyalayam@gmail.com")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
RECEIVER_EMAIL = "salhahlyalayam@gmail.com"

STATUS_AR = {
    "pending": "قيد الانتظار",
    "confirmed": "مؤكد",
    "cancelled": "ملغي",
}

def send_booking_notification(booking: dict):
    """إرسال إيميل إشعار للقاعة عند ورود حجز جديد"""
    if not SENDER_PASSWORD:
        print("⚠️  EMAIL_PASSWORD غير مضبوط - لم يُرسل الإيميل")
        return

    try:
        deposit_text = "نعم ✅" if booking.get("pay_deposit") == "نعم" else "لا ❌"
        receipt_text = booking.get("deposit_receipt", "")
        receipt_html = (
            f'<a href="http://localhost:8000/uploads/{receipt_text}" style="color:#d4af37;">عرض السند 📸</a>'
            if receipt_text else "لا يوجد"
        )

        html_body = f"""
        <html dir="rtl">
        <head>
          <meta charset="UTF-8">
          <style>
            body {{ font-family: Arial, sans-serif; background: #0f0f0f; color: #e0e0e0; margin: 0; padding: 20px; }}
            .card {{ background: #1a1a1a; border: 1px solid #d4af37; border-radius: 12px; max-width: 560px; margin: auto; padding: 30px; }}
            .header {{ text-align: center; border-bottom: 2px solid #d4af37; padding-bottom: 16px; margin-bottom: 24px; }}
            .header h1 {{ color: #d4af37; font-size: 22px; margin: 0; }}
            .header p {{ color: #888; font-size: 13px; margin: 6px 0 0; }}
            .row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #2a2a2a; }}
            .label {{ color: #888; font-size: 14px; }}
            .value {{ color: #fff; font-size: 14px; font-weight: bold; }}
            .badge {{ display: inline-block; background: #d4af37; color: #000; padding: 3px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 24px; color: #555; font-size: 12px; }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="header">
              <h1>🎊 طلب حجز جديد</h1>
              <p>قاعة أحلى الأيام</p>
            </div>

            <div class="row">
              <span class="label">📅 تاريخ المناسبة</span>
              <span class="value">{booking.get('date', '')}</span>
            </div>
            <div class="row">
              <span class="label">👤 اسم العميل</span>
              <span class="value">{booking.get('customer_name', '')}</span>
            </div>
            <div class="row">
              <span class="label">📞 رقم الهاتف</span>
              <span class="value" dir="ltr">{booking.get('contact_phone', '')}</span>
            </div>
            <div class="row">
              <span class="label">🪪 رقم البطاقة</span>
              <span class="value">{booking.get('id_card_number', '—')}</span>
            </div>
            <div class="row">
              <span class="label">🎉 نوع المناسبة</span>
              <span class="value">{booking.get('event_type', '—')}</span>
            </div>
            <div class="row">
              <span class="label">💰 العربون</span>
              <span class="value">{deposit_text}</span>
            </div>
            <div class="row">
              <span class="label">📸 سند التحويل</span>
              <span class="value">{receipt_html}</span>
            </div>
            <div class="row">
              <span class="label">📋 الحالة</span>
              <span class="value"><span class="badge">قيد الانتظار</span></span>
            </div>

            <div class="footer">
              يرجى الدخول إلى لوحة التحكم لتأكيد أو رفض الحجز
            </div>
          </div>
        </body>
        </html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🔔 حجز جديد - {booking.get('customer_name', '')} | {booking.get('date', '')}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        # جرب SSL port 465 اولاً، ثم TLS 587
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT_SSL, context=context) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        except Exception:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT_TLS) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print("[EMAIL] Sent OK:", booking.get('customer_name', ''))

    except Exception as e:
        print("[EMAIL] Error:", str(e))
