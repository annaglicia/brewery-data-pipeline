# brewery-data-pipeline

This pipeline was created with the simplest possible design in mind and to run locally only.

## How to make it work

Assuming you already have **Docker Desktop** installed and the **Docker extension** enabled in Visual Studio Code, follow the steps below to run the project locally:

**1. Build the Docker Image:**
Right-click on the Dockerfile and select **"Build Image..."**.

**2. Start the Containers Using Docker Compose:**
Right-click on the docker-compose.yml and select **"Compose Up"**.

**3. Access the Airflow Web UI:**
Once the containers are running, open your browser and navigate to: **http://localhost:8080/**

**4. Retrieve the Admin Password:**
The default admin password can be found in the file: **simple_auth_manager_passwords.json**

**5. Set Up the HTTP Connection in Airflow:**
In the Airflow UI, go to Admin > Connections > Add Connection. Then fill in the fields as follows:
- Connection Id: http_default
- Connection Type: HTTP
- Host: https://api.openbrewerydb.org

**6. Trigger the DAG:**
Return to the DAGs page in Airflow, locate your DAG, and click Trigger to start the pipeline.

## Visualize the tables and a few charts

In the repository directory, run the command `streamlit run dataviz.py`.

## Monitoring
It is possible to monitor tasks using Prometheus and Grafana for custom metrics and visual alerts. In Airflow's own UI, you can view errors and access detailed logs.

While still configuring DAGs, you can set `retries`, `retry_delay`, and `execution_timeout` for each task, and use `on_failure_callback` to execute a custom function upon failure (e.g., logging to a database, triggering another system, etc.). You can also configure notifications via email or Slack, or use the `SlackWebhookOperator` or `HttpOperator` to send custom notifications through Slack, Teams, and other platforms, in case of errors.
