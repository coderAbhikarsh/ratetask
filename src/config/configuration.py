import os

import docker
import psycopg2
import time
from src.config.read_properties import read_props

"""
This class helps in building the docker container 
and establishing connection with postgres db
"""


class Configuration:

    def __init__(self):
        self.properties = read_props.read_properties()

    def build_postgres_image(self):
        client = docker.from_env()
        print("Building PostgreSQL Docker image...")
        try:
            image, build_logs = client.images.build(
                path=os.path.dirname(os.getcwd()),
                tag=self.properties.get('container_name'),
                quiet=False
            )
            print("Docker image built successfully:", image.tags)
            return self.run_postgres_container()
        except docker.errors.APIError as e:
            print("Error building Docker image:", e)
            return None

    # Function to run a PostgreSQL container
    def run_postgres_container(self):
        client = docker.from_env()
        print("Creating and starting PostgreSQL container...")
        container = client.containers.run(
            self.properties.get('container_name'),
            detach=True,
            name=self.properties.get('container_name'),
            ports={self.properties.get('db_port'): self.properties.get('db_port')}
        )

        # Wait for PostgreSQL to be ready
        print("Waiting for PostgreSQL to start...")
        time.sleep(5)
        return container

    # Function to connect to PostgreSQL database
    def connect_to_postgres(self):
        try:
            print("Connecting to PostgreSQL database...")
            connection = psycopg2.connect(
                user=self.properties.get('db_username'),
                password=self.properties.get('db_password'),
                host="localhost",
                port=self.properties.get('db_port'),
            )
            self.check_postgre_version(connection)
            return connection
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)
            return None

    # Function to run some queries
    def check_postgre_version(self, connection):
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        print("PostgreSQL version:", cursor.fetchone()[0])
        cursor.close()
