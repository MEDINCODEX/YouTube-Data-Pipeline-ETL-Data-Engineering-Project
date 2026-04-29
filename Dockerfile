# ختارينا نسخة خفيفة ديال بايثون
FROM python:3.10-slim

# حددنا مجلد العمل وسط الكونتينر
WORKDIR /app

# نسخنا ملف المكتبات وطلبنا من دوكر يأنطاليهم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخنا مجلد الكود ديالنا
COPY src/ ./src/

# هاد الأمر هو لي غيخدم فاش نرانيو الكونتينر
CMD ["python", "src/main.py"]