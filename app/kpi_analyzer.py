import os
import re
from glob import glob
import pandas as pd


class KpiAnalyzer(object):
    def __init__(self, path: str):
        self.app_path = path
        self.unique_timestamps = self.get_unique_timestamps()
        self.files_per_timestamp = {}
        self.kpi_service_list = []
        self.set_files_per_timestamp()

    def get_unique_timestamps(self) -> set:
        all_files = [os.path.basename(x) for x in glob(os.path.join(self.app_path, "*.txt"))]
        res = [re.findall("ipflow_data.ts-*[0-9]+", file) for file in all_files]
        return set(" ".join(f[0] for f in res).split())

    def set_files_per_timestamp(self):
        for timestamp in self.unique_timestamps:
            all_files_per_timestamp = glob(os.path.join(self.app_path, f"{timestamp}*.txt"))
            self.files_per_timestamp[timestamp] = all_files_per_timestamp

    def get_service_kpis(self) -> list:
        service_kpi_list = []
        for timestamp in self.unique_timestamps:

            frame = pd.concat((pd.read_csv(f) for f in self.files_per_timestamp[timestamp]), ignore_index=True)

            new_f = frame.groupby(by=["service_id"])[["bytes_uplink", "bytes_downlink"]].sum()
            new_f["total_bytes"] = new_f["bytes_uplink"] + new_f["bytes_downlink"]
            service_kpi = new_f.nlargest(3, ["total_bytes"]).reset_index().drop(["bytes_uplink", "bytes_downlink"], axis=1)
            service_kpi.insert(0, "interval_start_timestamp", [frame["interval_start_timestamp"][0]] * 3)
            service_kpi.insert(1, "interval_end_timestamp", [frame["interval_end_timestamp"][0]] * 3)
            service_kpi_list.append(service_kpi)
        return service_kpi_list

    def get_cell_kpis(self) -> list:
        service_kpi_list = []
        for timestamp in self.unique_timestamps:
            frame = pd.concat((pd.read_csv(f) for f in self.files_per_timestamp[timestamp]), ignore_index=True)

            new_f = frame.groupby('cell_id')['msisdn'].apply(lambda x: pd.unique(x))
            new_f["total_bytes"] = new_f["bytes_uplink"] + new_f["bytes_downlink"]
            service_kpi = new_f.nlargest(3, ["total_bytes"]).reset_index().drop(["bytes_uplink", "bytes_downlink"], axis=1)
            service_kpi.insert(0, "interval_start_timestamp", [frame["interval_start_timestamp"][0]] * 3)
            service_kpi.insert(1, "interval_end_timestamp", [frame["interval_end_timestamp"][0]] * 3)
            service_kpi_list.append(service_kpi)
        return service_kpi_list
