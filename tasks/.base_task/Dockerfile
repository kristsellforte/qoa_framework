FROM qoa_framework_base

RUN cat requirements.txt > requirements_base.txt
COPY requirements.txt /
RUN cat requirements.txt > requirements_task.txt
RUN cat requirements_base.txt requirements_task.txt > requirements.txt

# will be overwriten should `docker run` pass a proper env
ENV EXECUTION_ID 111111

RUN pip install virtualenv
RUN virtualenv -p python3 qoa_framework_task
RUN /bin/bash -c "source /qoa_framework_task/bin/activate"
RUN pip install -r /requirements.txt

COPY code.py ./main/code.py

WORKDIR main
ENTRYPOINT ["python", "code.py"]