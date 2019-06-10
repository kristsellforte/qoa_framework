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
    pm = PerformanceMonitor(task_name='filter_data_date', pipeline_id=params['pipeline_id'])
    store = Store(performance_monitor=pm, bucket_name='forecasting-pipeline-files')
    pm.start()
    try:
        quality_setting = 'high'
        quality_presets_path = 'config/quality.json'
        data_path = 'data/train.csv'
        presets = store.get_json(quality_presets_path)
        preset = presets[quality_setting]
        df = store.get_csv(data_path)

        pm.log_analytics_metric(json.dumps({ "original_data_rows": df.shape[0] }))
        print('Shape 1:', flush=True)
        print(df.shape, flush=True)

        df = df[df['date'].str.contains('2018')==True]

        pm.log_analytics_metric(json.dumps({ "filtered_data_rows": df.shape[0] }))
        print('Shape 2:', flush=True)
        print(df.shape, flush=True)
        # df[preset['y']] = df['volume'] * df['unit_price']
        save_result(df, data_path.split('/')[-1])
        store.save_file(data_path)
        pm.stop()
    except Exception as e:
        logging.fatal(e, exc_info=True)
        pm.stop()

if __name__ == "__main__":

    main()
