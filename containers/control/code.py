import time
from control_consumer import ControlConsumer as ControlConsumer

def main():
    cc = ControlConsumer()
    
    print('Initialized consumer listener', flush=True)
    
    # Wait for the system to initialize
    time.sleep(180)
    
    cc.start()


if __name__ == "__main__":

    main()