import pandas as pd
import csv
import sys
import json
import logging
import time
# custom libs
from performance_monitor import PerformanceMonitor as PerformanceMonitor
from store import Store as Store
import utils

def save_result(df, data_path):
    df.to_csv(data_path, sep=',', encoding='utf-8')


def main():
    params = utils.get_args_params(sys.argv)
    pm = PerformanceMonitor(task_name='clean_data', pipeline_id=params['pipeline_id'])
    store = Store(performance_monitor=pm, bucket_name='forecasting-pipeline-files')
    pm.start()
    try:
        quality_setting = 'high'
        quality_presets_path = 'config/quality.json'
        original_data_path = 'data/train_original.csv'
        transformed_data_path = 'data/train.csv'
        presets = store.get_json(quality_presets_path)
        preset = presets[quality_setting]
        df = store.get_csv(original_data_path)
        df[preset['y']] = df['volume'] * df['unit_price']
        save_result(df, transformed_data_path.split('/')[-1])
        store.save_file(transformed_data_path)
        pm.stop()
    except Exception as e:
        logging.fatal(e, exc_info=True)
        pm.stop()

if __name__ == "__main__":

    main()