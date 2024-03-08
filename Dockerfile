FROM jeremyellman/kf7032_21s

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir Flask

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]