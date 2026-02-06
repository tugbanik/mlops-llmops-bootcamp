FROM python:3.11-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları (sqlite için gerekebilir)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodu
COPY app ./app
COPY scripts ./scripts
COPY app/ml/train.csv ./app/ml/train.csv



# SQLite db dosyası (ilk çalışmada oluşur, volume ile kalıcı olacak)
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
