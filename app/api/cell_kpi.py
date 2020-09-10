import pandas as pd
import json
from flask import jsonify, request
from app.api import bp
from app import db
from app.api import responses


@bp.route("/cell-kpis/", methods=["GET"])
def list_cell_kpis():
    end_timestamp = request.args.get("end_timestamp")
    try:
        if end_timestamp:
            res = pd.read_sql_query(f"select * from cell_kpi where cell_kpi.interval_end_timestamp = {end_timestamp};", con=db.engine)
        else:
            res = pd.read_sql_table(table_name="cell_kpi", con=db.engine)
        json_res = json.loads(res.to_json(orient='records'))
    except (ValueError, Exception) as e:
        return responses.internal_server_error(message=str(e))
    return jsonify(json_res)
