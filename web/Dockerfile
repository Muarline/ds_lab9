FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD ["python", "main.py"]

EXPOSE 8000
