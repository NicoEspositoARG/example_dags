# python -m unittest test_dag_validation.py
import unittest
import logging
from airflow.models import DagBag


class TestDAGValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        log = logging.getLogger()
        handler = logging.FileHandler("dag_validation.log", mode="w")

        handler.setLevel(logging.INFO)
        log.addHandler(handler)
        cls.log = log

    def test_no_import_errors(self):
        dag_bag = DagBag(dag_folder="dags/", include_examples=False)
        self.log.info(f"How Many DAGs?: {dag_bag.size()}")
        self.log.info(f"Import errors: {len(dag_bag.import_errors)}")
        assert len(dag_bag.import_errors) == 0, "No Import Failures"
