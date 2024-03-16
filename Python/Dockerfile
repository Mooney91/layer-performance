FROM python:3

WORKDIR /app

COPY . /app
COPY ./templates /app/templates

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysql-connector-python
RUN pip install pandas

EXPOSE 5000

ENV FLASK_APP=performance.py

CMD ["flask", "run", "--host=0.0.0.0"]