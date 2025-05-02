FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .

# 빌드에 필요한 패키지 설치
RUN apt-get update && apt-get install -y gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && apt-get autoremove -y && apt-get clean

COPY . .
EXPOSE 80
CMD ["python", "main.py"]
