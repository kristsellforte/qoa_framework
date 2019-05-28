FROM qoa_framework_base

# will be overwriten should `docker run` pass a proper env
ENV EXECUTION_ID 111111

RUN pip install virtualenv
RUN virtualenv -p python3 qoa_framework_control
RUN /bin/bash -c "source /qoa_framework_control/bin/activate"
RUN pip install -r /requirements.txt

COPY control_consumer.py ./main/control_consumer.py
COPY code.py ./main/code.py

WORKDIR main
ENTRYPOINT ["python", "code.py"]