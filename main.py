from app import create_app, db
from app.kpi_analyzer import KpiAnalyzer
import os

if __name__ == "__main__":
    app = create_app()
    path = os.getcwd()
    kpi_analyzer = KpiAnalyzer(os.path.join(path, "static"))
    service_kpis = kpi_analyzer.get_service_kpis()

    with app.app_context():
        for service_kpi in service_kpis:
            service_kpi.to_sql("service_kpi", con=db.engine, if_exists="append", index=False)
        kpi_analyzer.get_cell_kpis()
    # app.run()
