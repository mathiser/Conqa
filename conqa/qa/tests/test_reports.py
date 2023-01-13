import logging
import unittest

from conqa.omics.tests.test_pyradiomics import TestPyradiomics
from conqa.omics.tests.test_z_boundaries import TestZBoundaries
from conqa.qa.reports import ReportGenerator

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class TestReports(unittest.TestCase):
    def test_generate_report_pyradiomic(self):
        self.omic_tests = TestPyradiomics()
        self.omic_tests.setUp()
        self.db = self.omic_tests.db
        self.report_generator = ReportGenerator(db=self.db)

        self.omic_tests.test_generate_pyradiomics()
        df = self.report_generator.generate_omics_report()
        self.assertNotEqual(0, len(df.columns))

    def test_generate_report_z(self):
        self.z_test = TestZBoundaries()
        self.z_test.setUp()
        self.db = self.z_test.db
        self.report_generator = ReportGenerator(db=self.db)

        self.z_test.test_find_contour_z_boundaries()
        df = self.report_generator.generate_omics_report()
        self.assertNotEqual(0, len(df.columns))


if __name__ == '__main__':
    unittest.main()
