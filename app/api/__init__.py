from flask import Blueprint

bp = Blueprint("api", __name__)

from . import service_kpis, cell_kpi, responses
