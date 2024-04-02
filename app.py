from flask import Flask, request, session, jsonify, abort
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
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

    base_df = spark.read.csv("/app/expected-schema.csv", inferSchema=True, header=True)
    target_df = spark.read.csv(basePath+"/"+csv.filename, inferSchema=True, header=True)

    if set(target_df.schema.names) <= set(base_df.schema.names):

        subjects = requests.get("https://w20003691.nuwebspace.co.uk/api/access?integration")
        if subjects.text.strip().lower() != "null" :
            existing_sub = set([item for sublist in subjects.json() for item in sublist])
            uploading_sub = set((target_df.select("CAH_NAME").distinct()).rdd.map(lambda row: row[0]).collect())
            intersect_chk = uploading_sub.intersection(existing_sub)
            if intersect_chk:
                shutil.rmtree(basePath, ignore_errors=True)
                session.clear()
                return jsonify({"message":f"Opps! Looks like there is already an existing subject! {str(intersect_chk)}"}), 404
            
        if not set(target_df.schema) <= set(base_df.schema):
            for target in target_df.schema:
                base = next(f for f in base_df.schema if f.name == target.name)
                if target.dataType != base.dataType:
                    target_df = target_df.withColumn(target.name, col(target.name).cast(base.dataType))
                
        processedPath = basePath+"/processed"
        target_df.write.csv(path=processedPath,nullValue="NULL",mode="overwrite")

        processedCSV = [f for f in os.listdir(processedPath) if f.endswith(".csv")][0]
        url = "https://w20003691.nuwebspace.co.uk/api/access?upload"
        files = {'file': open(processedPath+"/"+processedCSV, "rb")}
        response = requests.post(url, files=files)
        shutil.rmtree(basePath, ignore_errors=True)
        session.clear()
        return "Test"
    else:
        shutil.rmtree(basePath, ignore_errors=True)
        session.clear()
        return jsonify({"message":f"Opps! Looks like the CSV file does not contains the correct data column!"}), 404

if __name__ == "__main__":
   app.run(debug=True)