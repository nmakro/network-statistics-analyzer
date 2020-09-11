from app import create_app, db
from app.kpi_analyzer import KpiAnalyzer

app = create_app()

if __name__ == "__main__":

    kpi_analyzer = KpiAnalyzer()
    service_kpis = kpi_analyzer.get_service_kpis()
    cell_kpis = kpi_analyzer.get_cell_kpis()

    with app.app_context():
        for service_kpi, cell_kpi in zip(service_kpis, cell_kpis):
            service_kpi.to_sql(
                "service_kpi", con=db.engine, if_exists="append", index=False
            )
            cell_kpi.to_sql("cell_kpi", con=db.engine, if_exists="append", index=False)

    app.run()
