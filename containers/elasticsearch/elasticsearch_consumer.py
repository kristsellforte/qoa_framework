# python imports
import json
import requests
# queue lib
import pika

INDEX_WHITELIST = ['data_logs', 'analytics', 'metrics']

class ElasticsearchConsumer:
    def __init__(self, credentials, queue_name='performance_monitor'):
        self.credentials = credentials
        self.queue_name = queue_name
        print('Elasticsearch consumer initialized', flush=True)


    def init_indexes(self):
        url = self.credentials['elasticsearch_host'] + ':' + self.credentials['elasticsearch_port']

        # Init elasticsearch indexes
        requests.put(url + '/metrics')
        requests.put(url + '/data_logs')
        requests.put(url + '/analytics')


    def start(self):
        print('Elasticsearch consumer started', flush=True)

        self.init_indexes()

        rabbitmq_credentials = pika.PlainCredentials(self.credentials['rabbitmq_user'], self.credentials['rabbitmq_password'])
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.credentials['rabbitmq_host'], self.credentials['rabbitmq_port'], '/', rabbitmq_credentials)) 
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name)

        channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()



    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        body_dict = json.loads(body)
        index = body_dict.pop('metric_type', None)
        if index and index in INDEX_WHITELIST:
            self.push_message_to_elasticsearch(body_dict, index)


    def push_message_to_elasticsearch(self, body, index):
        url_prefix = self.credentials['elasticsearch_host'] + ':' + self.credentials['elasticsearch_port']
        url = url_prefix + '/' + index + '/_doc'
        response = requests.post(url, json=body)
        print('RESPONSE FROM ES METRICS POST', response)
