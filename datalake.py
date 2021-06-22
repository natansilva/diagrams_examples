from diagrams import Cluster, Diagram
# from diagrams.custom import Custom
from diagrams.gcp.analytics import Bigquery, Pubsub, Dataflow
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.storage import Storage
from diagrams.onprem.analytics import Superset, Spark, Metabase
from diagrams.onprem.database import Mariadb, Mongodb, Mysql, Neo4J, Oracle, Postgresql
from diagrams.onprem.queue import Kafka
from diagrams.onprem.workflow import Airflow, Nifi, Kubeflow


graph_attr = {
    "fontsize": "45"
}

edge_attr = {
    "arrowhead": "open"
}

node_attr = {
    "fontsize": "14"
}

sql_server_icon = "images/sql_server.png"

with Diagram(
    "Data lake",
    filename="images/data_lake_architeture",
    # show=False,
    graph_attr=graph_attr,
    edge_attr=edge_attr,
    node_attr=node_attr
    ) as diagram:

    with Cluster("Sources"):

        with Cluster("Stream sources"):
            kafka = Kafka("Kafka cluster")
            pubsub = Pubsub("PubSub")

            pubsub - kafka

        with Cluster("Data sources"):
            mongo = Mongodb("Mongodb")
            mysql = Mysql("Mysql")
            neo4j = Neo4J("Neo4J")
            oracle = Oracle("Oracle")
            postgre = Postgresql("Postgre SQL")
            maria =  Mariadb("Mariadb")

            mongo - mysql
            neo4j - postgre
            maria - oracle
    
    with Cluster("GCP"):

        with Cluster("Stream processing"):
            dataflow = Dataflow("Dataflow")
        
        with Cluster("Batch processing"):
            nifi = Nifi("Nifi")
            airflow = Airflow("Airflow")
        
        with Cluster("Data entrance layer"):
            raw = Storage("Raw layer")

        with Cluster("Transforming tools"):
            spark = Spark("Spark")

        with Cluster("Consumer layer"):
            trusted = Bigquery("Trusted layer")
            refined = Bigquery("Refined layer")
            data_marts = Bigquery("Data marts")

            final_layer = [
                trusted,
                refined,
                data_marts
            ]
        
        with Cluster("Data viz"):
            superset = Superset("Superset")
            metabase = Metabase("Metabase")

            superset - metabase
        
        with Cluster("Machine learning"):
            notebooks = AIPlatform("Jupyter\nnotebooks")
            kubeflow = Kubeflow("Kubeflow")

            notebooks >> kubeflow

    kafka >> dataflow
    postgre >> airflow
    dataflow >> raw
    airflow >> raw
    raw >> spark
    spark >> final_layer
    refined >> superset
    refined >> notebooks


diagram