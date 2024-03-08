from flask import Flask, request, session
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pandas as pd
import os
import secrets
import requests
import shutil

app = Flask(__name__)
app.secret_key = "abc123"

@app.route('/process',methods=['POST'])
def process():
    if 'session_id' not in session:
        session['session_id'] = secrets.token_urlsafe(32)

    csv = request.files['file']
    basePath = "/app/temp/"+session['session_id']
    os.makedirs(basePath)
    csv.save(basePath+"/"+csv.filename)
    
    spark = SparkSession\
            .builder\
            .appName("nss-integrator")\
            .config("spark.some.config.option","some-value")\
            .getOrCreate()

    df = spark.read.csv(basePath+"/"+csv.filename)
    processedPath = basePath+"/processed"
    df.write.csv(path=processedPath,nullValue="NULL",mode="overwrite")

    processedCSV = [f for f in os.listdir(processedPath) if f.endswith(".csv")][0]
    url = "https://w20003691.nuwebspace.co.uk/api/access?upload"
    files = {'file': open(processedPath+"/"+processedCSV, "rb")}
    response = requests.post(url, files=files)
    shutil.rmtree(basePath, ignore_errors=True)
    session.clear()
    return response.text

if __name__ == "__main__":
   app.run(debug=True)