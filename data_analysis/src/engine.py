# src/engine.py
import numpy as np
from data_analysis.src.config import EXAM_SETTINGS


class ClinicalEngine:
    def __init__(self):
        self.settings = EXAM_SETTINGS

    def _get_range(self, exam_key, sex_value):
        config = self.settings.get(exam_key.lower())
        if not config:
            return None

        ranges = config['ranges']
        gender = "male" if sex_value == 0 else "female"

        return ranges.get(gender, ranges.get("default"))

    def classify_all_exams(self, df):
        df = df.copy()

        for exam_key in self.settings.keys():
            col_name = exam_key.upper()
            if col_name in df.columns:
                df[f"{col_name}_class"] = df.apply(
                    lambda row: self._logic(row[col_name], self._get_range(exam_key, row['Sex'])),
                    axis=1
                )
        return df

    def _logic(self, value, limits):

        if not limits: return 1
        low, high = limits
        if value < low: return 0
        if value > high: return 2
        return 1

    def generate_health_score(self, df):

        class_cols = [c for c in df.columns if c.endswith('_class')]
        df['total_alerts'] = (df[class_cols] != 1).sum(axis=1)

        df['status_message'] = np.where(
            df['total_alerts'] > 0,
            "Alterações detectadas - Procure um médico",
            "Resultados dentro da normalidade"
        )
        return df