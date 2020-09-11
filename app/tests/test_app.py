import unittest
from unittest.mock import patch
from app.kpi_analyzer import KpiAnalyzer


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher1 = patch("app.kpi_analyzer.os.getenv")
        self.patcher2 = patch("app.kpi_analyzer.glob")

        self.mock_os = self.patcher1.start()
        self.mock_glob = self.patcher2.start()

    def tearDown(self) -> None:
        self.patcher1.stop()
        self.patcher2.stop()

    def test_find_unique_timestamps(self):
        unique_timestamps = {"ipflow_data.ts-1234456", "ipflow_data.ts-12344567"}

        self.mock_os.return_value = "my/data/path"
        file_list = [
            "my/data/path/ipflow_data.ts-1234456.1.txt",
            "my/data/path/ipflow_data.ts-1234456.2.txt",
            "my/data/path/ipflow_data.ts-12344567.1.txt",
        ]
        self.mock_glob.return_value = file_list
        kpi_analyzer = KpiAnalyzer()
        self.assertEqual(unique_timestamps, kpi_analyzer.unique_timestamps)
        self.assertEqual(
            kpi_analyzer.files_per_timestamp["ipflow_data.ts-1234456"],
            [file_list[0], file_list[1]],
        )
        self.assertEqual(
            kpi_analyzer.files_per_timestamp["ipflow_data.ts-12344567"], [file_list[2]]
        )


if __name__ == "__main__":
    unittest.main()
