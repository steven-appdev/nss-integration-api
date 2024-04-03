FROM jeremyellman/kf7032_21s

WORKDIR /app

COPY . /app

USER root

RUN pip install --no-cache-dir Flask

RUN pip install flask-cors

RUN chmod 777 /app/temp

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]