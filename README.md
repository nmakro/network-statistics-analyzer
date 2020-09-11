# A network statistics analyzer.

This project includes a system for calculating mobile subscriber and network statistics from raw data based
on open source software components. The raw data are produced by a 3 rd party system and refer to
the user activity in 5-minute time periods. They are produced in the form of CSV text files and contain
the following fields:


| Field                     | Description   |
| ------------------------- | ------------- |
| interval_start_timestamp  | Start time of the interval (Unix timestamp in milliseconds)  |
| interval_end_timestamp    | End time of the interval (Unix timestamp in milliseconds)  |
| msisdn                    | MSISDN of mobile user (64bit integer). This is a unique identifier for the mobile user.
| bytes_uplink              | Number of uplink bytes (64bit integer)
| bytes_downlink            | Number of downlink bytes (64bit integer)
| service_id                | Identifier of traffic class (32bit integer). Traffic class can be facebook, youtube, instagram etc.
| cell_id                   | Cell ID of mobile user (64bit integer) 


# Purpose

The purpose of the application is to calculate user and network KPIs (Key Performance Indicators) for
5-minute and 1-hour intervals and store them in the database. The KPIs to be calculated are the
following:


KPI1: Top 3 services by traffic volume: the top 10 services (as identified by service_id) which
generated the largest traffic volume in terms of bytes (downlink_bytes + uplink_bytes) for the
interval.

KPI2: Top 3 cells by number of unique users: the top 10 cells (as identified by cell_id) which
served the highest number of unique users (as identified by msisdn) for the interval.

The result should be stored in one database table for each KPI. For the 1 st KPI, the table should contain
the following fields:

| Field                     | Description   |
| ------------------------- | ------------- |
| interval_start_timestamp  | Start time of the interval (Unix timestamp in milliseconds)  |
| interval_end_timestamp    | End time of the interval (Unix timestamp in milliseconds)  |
| service_id                | Identifier of traffic class (32bit integer). Traffic class can be facebook, youtube, instagram etc.
| total_bytes               | Total number of bytes for the service
| interval                  | 5-minute or 1-hour (in minutes)

For the 2 nd KPI, the table should contain:

| Field                     | Description   |
| ------------------------- | ------------- |
| interval_start_timestamp  | Start time of the interval (Unix timestamp in milliseconds)  |
| interval_end_timestamp    | End time of the interval (Unix timestamp in milliseconds)  |
| cell_id                   | Cell ID of mobile user
| number_of_unique_users    | Number of unique users for the cell
| interval                  | 5-minute or 1-hour (in minutes)



# Usage for using the application .

- Create python3 venv environment and type pip3 install -r requirements.txt 

- Start your database of choice

- Congigure the `DATABASE_URL` environmental variable like: `mysql+mysqldb://root:rootdb@localhost/dbname`

- Configure the `DATA_DIR` environmental variable like where the raw data files are.

- From the current dir run `python3 main.py`

- To list the service-kpis you can use the endpoint `/api/v1/services-kpis/`. The optional argument end_timestamp can be used, to list the kpis for the specific timestamp.

- To list the cell-kpis you can use the endpoint `/api/v1/cell-kpis/`. The optional argument end_timestamp can be used, to list the kpis for the specific timestamp.

- To run the tests `coverage run --omit=venv/* -m unittest discover app/tests/`

- To see the test coverage type `coverage report`

