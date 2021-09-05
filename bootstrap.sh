#!/usr/bin/env bash

sudo apt-get update && sudo apt-get install python3-pip -y \
&& sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
# modify max_user_watches
sudo sh -c 'echo "\nfs.inotify.max_user_watches=220000" >> /etc/sysctl.conf'

#### install PostgreSQL

echo "--- Installing PostgreSQL 12"
sudo apt-get install postgresql postgresql-contrib -y
echo "---  fixing listen_addresses on postgresql.conf"
sudo sed -i "s/#listen_address.*/listen_addresses '*'/" /etc/postgresql/12/main/postgresql.conf
echo "--- fixing postgres pg_hba.conf file"
sudo cat >> /etc/postgresql/12/main/pg_hba.conf <<EOF
# Accept all IPv4 connections - FOR DEVELOPMENT ONLY!!!
host    all         all         0.0.0.0/0             md5
EOF
echo "--- Creating postgres users and DB's"
RUN_PSQL="sudo -u postgres psql -X --set AUTOCOMMIT=on --set ON_ERROR_STOP=on postgres"
${RUN_PSQL} <<SQL
CREATE DATABASE airflow_db;
CREATE DATABASE vagrant;
CREATE USER airflow WITH PASSWORD 'airflow';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow;
CREATE USER vagrant LOGIN PASSWORD 'vagrant';
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO vagrant;
\q
SQL
echo "-- Successfully installed PostgreSQL!!"

### install Airflow 2.1.2
echo "---Installing Airflow locally"

export AIRFLOW_HOME=~/airflow

AIRFLOW_VERSION=2.1.2
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
sudo pip install "apache-airflow[postgres,http]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# initialize the database
airflow db init

airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@superhero.org

echo "-- Successfully installed Airflow!!"

### install Docker Compose
echo "-- Installing Docker Compose"
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
     -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

echo "-- Successfully completed provisioning from bootstrap.sh"
