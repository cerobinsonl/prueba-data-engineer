FROM python:3.9

WORKDIR /app

COPY microservicio_uploader/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservicio_uploader /app  
COPY compartidos /app/compartidos 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
