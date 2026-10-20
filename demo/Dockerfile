# Deliberately weak image (container + Dockerfile misconfiguration demo):
# old, unpinned-by-digest base image and the app runs as root.
FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
