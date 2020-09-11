import os
import re
from glob import glob
import datetime
import dateutil.relativedelta

import pandas as pd


class KpiAnalyzer(object):
    def __init__(self):
        self.data_path = os.getenv("DATA_DIR")
        self.unique_timestamps = self.get_unique_timestamps()
        self.files_per_timestamp = {}
        self.kpi_service_list = []
        self.set_files_per_timestamp()

    def get_unique_timestamps(self) -> set:
        all_files = [
            os.path.basename(x) for x in glob(os.path.join(self.data_path, "*.txt"))
        ]
        res = [re.findall("ipflow_data.ts-*[0-9]+", file) for file in all_files]
        return set(" ".join(f[0] for f in res).split())

    def set_files_per_timestamp(self):
        all_files = [
            os.path.basename(x) for x in glob(os.path.join(self.data_path, "*.txt"))
        ]
        for timestamp in self.unique_timestamps:
            pattern = timestamp + "\.\d+\.txt"
            match = re.findall(rf"{pattern}", " ".join(all_files))
            self.files_per_timestamp[timestamp] = match

        for i, v in self.files_per_timestamp.items():
            for index, value in enumerate(v):
                v[index] = os.path.join(self.data_path, value)

    def get_service_kpis(self) -> list:
        service_kpi_list = []
        for timestamp in self.unique_timestamps:
            frame = pd.concat(
                (pd.read_csv(f) for f in self.files_per_timestamp[timestamp]),
                ignore_index=True,
            )

            new_f = frame.groupby(by=["service_id"])[
                ["bytes_uplink", "bytes_downlink"]
            ].sum()
            new_f["total_bytes"] = new_f["bytes_uplink"] + new_f["bytes_downlink"]
            service_kpi = (
                new_f.nlargest(3, ["total_bytes"])
                    .reset_index()
                    .drop(["bytes_uplink", "bytes_downlink"], axis=1)
            )
            service_kpi.insert(
                0,
                "interval_start_timestamp",
                [frame["interval_start_timestamp"][0]] * 3,
            )
            service_kpi.insert(
                1, "interval_end_timestamp", [frame["interval_end_timestamp"][0]] * 3
            )
            interval = get_minute_difference(frame["interval_end_timestamp"][0], frame["interval_start_timestamp"][0])
            service_kpi.insert(4, "interval", [interval] * 3)

            service_kpi_list.append(service_kpi)
        return service_kpi_list

    def get_cell_kpis(self) -> list:
        cell_kpi_list = []
        for timestamp in self.unique_timestamps:
            frame = pd.concat(
                (pd.read_csv(f) for f in self.files_per_timestamp[timestamp]),
                ignore_index=True,
            )

            new_f = frame.groupby("cell_id", as_index=False).agg(
                {"msisdn": pd.Series.nunique}
            )
            cell_kpi = new_f.nlargest(3, ["msisdn"])
            cell_kpi.insert(
                0,
                "interval_start_timestamp",
                [frame["interval_start_timestamp"][0]] * 3,
            )
            cell_kpi.insert(
                0, "interval_end_timestamp", [frame["interval_end_timestamp"][0]] * 3
            )
            cell_kpi.rename(columns={"msisdn": "number_of_unique_users"}, inplace=True)
            interval = get_minute_difference(frame["interval_end_timestamp"][0], frame["interval_start_timestamp"][0])
            cell_kpi.insert(4, "interval", [interval] * 3)
            cell_kpi.reset_index(inplace=True, drop=True)

            cell_kpi_list.append(cell_kpi)
        return cell_kpi_list


def get_minute_difference(t1, t2) -> int:
    dt1 = datetime.datetime.fromtimestamp(t1 / 1000)
    dt2 = datetime.datetime.fromtimestamp(t2 / 1000)
    rd = dateutil.relativedelta.relativedelta(dt1, dt2)
    return rd.minutes
