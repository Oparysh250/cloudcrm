FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .

# Используем зеркало, чтобы обойти проблему с DNS
RUN pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]