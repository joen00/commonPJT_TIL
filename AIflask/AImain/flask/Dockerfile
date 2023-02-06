FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3","-m","flask","run","--host", "i8b306.p.ssafy.io", "./app.py"]