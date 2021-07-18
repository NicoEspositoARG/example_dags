# Collection of demo DAGs exploring Apache Airflow

To easily understand the examples and follow along with the code,
it may be helpful to **debug the DAGs execution** and take advantage of **IntelliSense** to access the _Airflow_ documentation and implementation.

This can be done using VSCode by following these steps:

- [Create a Virtual Environment](https://docs.python.org/3/library/venv.html#module-venv)
- [Install Airflow locally](https://airflow.apache.org/docs/apache-airflow/stable/installation.html#installation-script)
  _( Before running the official script, you can define the root folder with_ ` export AIRFLOW_HOME=/home/user/my_airflow_folder`)
- Make sure the selected [Python Interpreter](https://code.visualstudio.com/docs/python/python-tutorial#_select-a-python-interpreter) matches your virtual environment path (_i.e: ./env/bin/python_)
- [Configure and run the debugger](https://code.visualstudio.com/docs/python/debugging) placing these settings in `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "internalConsole",
      "justMyCode": false,
      "env": {
        "AIRFLOW__CORE__EXECUTOR": "DebugExecutor",
        "AIRFLOW__DEBUG__FAIL_FAST": "True"
      }
    }
  ]
}
```

- Open any DAG from this repo and start debugging pressing by F5

- **Look for StackOverflow reference link in each DAG docs**
