# nss-integration-api

The repository contains Rest API created as part of the KF7029 dissertation module at Northumbria University.
NSS Integration API is a web API created using Flask with Apache Spark to handle data transformation and data inspection. 
This API provides endpoints for handling data and performing appropriate inspection and transformation before uploading into database.

## Features

- **Data Transformation**: Utilize Apache Spark to perform efficient data transformation tasks.
- **Data Inspection**: Examine data properties and statistics for insightful analysis.
- **RESTful API**: Implement endpoints following RESTful principles for easy integration with other applications.

## Endpoint

### [POST] /process
> The API endpoint will retrieve the CSV file posted and launch a Spark Session. As of the current version, the API will automatically replace `,,` with `,NULL,` before posting it to the PHP API server for upload.

## NSS Dashboard Repository

The repository is a backend system. If you are interested in how my frontend looks like and another API written in PHP, please check out this repo:
https://github.com/steven-appdev/nss-dashboard
