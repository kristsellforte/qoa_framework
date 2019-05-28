import logging
# custom libs
from performance_monitor import PerformanceMonitor as PerformanceMonitor
import utils


def main():
    params = utils.get_args_params(sys.argv)
    # Put in the task_name in the call below
    pm = PerformanceMonitor(task_name='', pipeline_id=params['pipeline_id'])
    pm.start()
    try:
    	# Put your custom task related code here
        pm.stop()
    except Exception as e:
        logging.fatal(e, exc_info=True)
        pm.stop()

if __name__ == "__main__":

    main()