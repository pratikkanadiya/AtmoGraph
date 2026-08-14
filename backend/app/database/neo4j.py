from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def verify_connection():

    with driver.session(database="neo4j") as session:

        result = session.run(
            "RETURN 'AtmoGraph Neo4j Connected' AS message"
        )

        return result.single()["message"]