FROM python:3.9-slim
USER root
WORKDIR /app
COPY . .
RUN mkdir reports && echo "SECRET_DATA_2025" > reports/report_q1.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]