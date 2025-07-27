# data-service/Dockerfile
FROM python:3.9
WORKDIR /app
COPY app.py ./
RUN pip install flask redis requests
CMD ["python", "app.py"]

