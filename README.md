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

# Using the PerformanceMonitor class
The default code in the code.py of a task initialzies the PerformanceMonitor class with default options. This means that the cost is calculated based on AWS Fargate costs. You can add your own cost function and save additional high level metrics by providing a custom metrics object callback function. The callback function is called once per a defined interval. The default interval is 1 second but the user can provide a different interval by specifying the interval argument when initializing the object for example `interval=X` where `X` is the intrerval in seconds. The callback function has the following signature `define_metrics_object(cpu, ram, elapsed_time, previous_result)`. Where cpu is the CPU percentage consumed at that point of time, ram is the RAM used at that point of time, elapsed_time is the time elapsed since the start of the task and previous_result is the result calculated in the previous (t - interval) call of the function. After defining your own function it can be passed through the define_metrics_object argument. If we put it all together we should get a class init call similar to the one below.
```
def define_metrics_object(cpu, ram, elapsed_time, previous_result):
	...
	
pm = PerformanceMonitor(task_name='', pipeline_id=params['pipeline_id'], interval=1, define_metrics_object=define_metrics_object)
```

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
