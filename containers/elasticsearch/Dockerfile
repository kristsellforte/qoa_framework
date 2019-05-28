FROM qoa_framework_base

# will be overwriten should `docker run` pass a proper env
ENV EXECUTION_ID 111111

RUN pip install virtualenv
RUN virtualenv -p python3 qoa_framework_elasticsearch
RUN /bin/bash -c "source /qoa_framework_elasticsearch/bin/activate"
RUN pip install -r /requirements.txt

COPY elasticsearch_consumer.py ./main/elasticsearch_consumer.py
COPY code.py ./main/code.py

WORKDIR main
ENTRYPOINT ["python", "code.py"]