import time
# ElasticsearchConsumer class
from elasticsearch_consumer import ElasticsearchConsumer as ElasticsearchConsumer
# secrets
from credentials import credentials as credentials

def main():
    ec = ElasticsearchConsumer(credentials=credentials)
    
    # Wait for the system to initialize
    time.sleep(180)
    
    ec.start()


if __name__ == "__main__":

    main()