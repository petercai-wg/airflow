from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from jinja2 import Template

import datetime

default_args = {
    "owner": "airflow",
    "retries": 5,
    "retry_delay": datetime.timedelta(minutes=2),
    "executor": "LocalExecutor",
}


def get_name(ti):
    ti.xcom_push(key="first_name", value="Peter")
    ti.xcom_push(key="last_name", value="Cai")


def greet(some_dict, ti):
    print("some dict: ", some_dict)
    based_string = """
        This is a for-loop example
        {% for k,v in input_dict.items() %}
        {{ k }} : {{ v }}
        {% endfor %}
        Finish Loop
    """
    output_string = Template(based_string).render(input_dict=some_dict)
    print(output_string)

    first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
    last_name = ti.xcom_pull(task_ids="get_name", key="last_name")

    print(f"Hello World! My name is {first_name} {last_name}, ")


# A DAG represents a workflow, a collection of tasks
with DAG(
    dag_id="my_echo_dag",
    default_args=default_args,
    description="This is an example dag",
    start_date=datetime.datetime(2024, 11, 29, 2),
    schedule_interval="0 3 * * Tue-Fri",
) as dag:
    task1 = BashOperator(
        task_id="first_task", bash_command="echo hello world, this is the first task!"
    )

    @task()
    def task2():
        print("this is the second task!")

    task3 = PythonOperator(task_id="get_name", python_callable=get_name)

    task4 = PythonOperator(
        task_id="greet",
        python_callable=greet,
        op_kwargs={"some_dict": {"a": 1, "b": 2}},
    )
    [task1, task3] >> task2 >> task4
