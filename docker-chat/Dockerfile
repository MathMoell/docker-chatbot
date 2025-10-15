FROM python:3.11-alpine

WORKDIR /app

# Kopeeri sõltuvused ja installi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopeeri kood
COPY . .

# Non-root user
RUN adduser -D -s /bin/sh appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
