# QoA framework
A base framework for setting up data pipelines with integrated monitoring and control. Part of my work for my masters' thesis.

# Initial setup
Download and install Docker from https://docs.docker.com/v17.12/install/.

Copy credentials_template.py to credentials.py. And in the newly copied file enter your AWS credentials (this is only needed if you plan to use S3 as the main storage engine). The other credentials can stay the same for the framework to work out of the box locally. For production these credentials should be changed.

After setting up your credentials you need to build the base containers. To do this open your terminal go to the root directory of this repository and run
```
./scripts/initialize_framework.sh
```

# Adding a task
To create a new task run from the root of this repository (with TASK_NAME being the desired name for the task).
```
./scripts/create_task.sh TASK_NAME
```
This will create a new task folder in tasks. In this folder you can edit the marked part in code.py to add logic to the task. Performance monitoring will already be setup to work with all tasks but to use the store you should import it seperately. For more details about the store you can view its source code in containers/base/store.py.

# Building the pipeline
After adding the neccessary logic to the task it has to be used in the pipeline. This can be done by editing the pipeline.py to include your task. The pipeline.py file is an Airflow DAG file so more information about the setup can be found by reading the Airflow documentation. The pipeline.py by default will hold an example task setup. All task setups have to follow or extend the given example.

# Running the pipeline
In order to run the pipeline you have to navigate to the airflow folder and run 
```
docker-compose up
```

# Different storage
The repository is meant for work with AWS S3. If a different storage approach has to be used you must edit the store.py file in containers/base and setup your own custom methods. After doing that the base continer should be rebuilt. This can be done by running (from the root of the repository)
```
./scripts/initialize_framework.sh
```
