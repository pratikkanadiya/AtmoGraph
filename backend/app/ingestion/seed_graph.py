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


def create_graph(tx):

    tx.run("""
        UNWIND $countries AS country
        MERGE (c:Country {id: country.id})
        SET c.name = country.name
    """, countries=[
        {"id": "DE", "name": "Germany"},
        {"id": "NL", "name": "Netherlands"},
        {"id": "US", "name": "United States"},
        {"id": "CN", "name": "China"},
        {"id": "JP", "name": "Japan"}
    ])

    tx.run("""
        UNWIND $ports AS port
        MERGE (p:Port {id: port.id})
        SET p.name = port.name,
            p.country = port.country
    """, ports=[
        {
            "id": "PORT_ROT",
            "name": "Port of Rotterdam",
            "country": "NL"
        },
        {
            "id": "PORT_HAM",
            "name": "Port of Hamburg",
            "country": "DE"
        },
        {
            "id": "PORT_LA",
            "name": "Port of Los Angeles",
            "country": "US"
        },
        {
            "id": "PORT_SHA",
            "name": "Port of Shanghai",
            "country": "CN"
        }
    ])
    
    tx.run("""
        UNWIND $suppliers AS supplier
        MERGE (s:Supplier {id: supplier.id})
        SET s.name = supplier.name,
            s.country = supplier.country
    """, suppliers=[
        {
            "id": "SUP_001",
            "name": "Euro Components GmbH",
            "country": "DE"
        },
        {
            "id": "SUP_002",
            "name": "Shanghai Semiconductor Ltd",
            "country": "CN"
        },
        {
            "id": "SUP_003",
            "name": "Tokyo Electronics Supply",
            "country": "JP"
        }
    ])

    tx.run("""
        UNWIND $manufacturers AS manufacturer
        MERGE (m:Manufacturer {id: manufacturer.id})
        SET m.name = manufacturer.name,
            m.country = manufacturer.country
    """, manufacturers=[
        {
            "id": "MAN_001",
            "name": "Global Electronics Factory",
            "country": "US"
        },
        {
            "id": "MAN_002",
            "name": "North America Devices",
            "country": "US"
        }
    ])

    tx.run("""
        UNWIND $warehouses AS warehouse
        MERGE (w:Warehouse {id: warehouse.id})
        SET w.name = warehouse.name,
            w.country = warehouse.country
    """, warehouses=[
        {
            "id": "WH_001",
            "name": "Chicago Distribution Center",
            "country": "US"
        },
        {
            "id": "WH_002",
            "name": "California Distribution Center",
            "country": "US"
        }
    ])

    tx.run("""
        UNWIND $products AS product
        MERGE (p:Product {id: product.id})
        SET p.name = product.name
    """, products=[
        {
            "id": "PROD_001",
            "name": "Semiconductor"
        },
        {
            "id": "PROD_002",
            "name": "Smartphone"
        },
        {
            "id": "PROD_003",
            "name": "Consumer Electronics"
        }
    ])

    tx.run("""
        UNWIND $industries AS industry
        MERGE (i:Industry {id: industry.id})
        SET i.name = industry.name
    """, industries=[
        {
            "id": "IND_001",
            "name": "Semiconductor"
        },
        {
            "id": "IND_002",
            "name": "Consumer Electronics"
        },
        {
            "id": "IND_003",
            "name": "Technology"
        }
    ])

    tx.run("""
        MATCH (c:Country), (p:Port)
        WHERE c.id = p.country
        MERGE (c)-[:HAS_PORT]->(p)
    """)

    tx.run("""
        MATCH (s:Supplier), (c:Country)
        WHERE s.country = c.id
        MERGE (s)-[:LOCATED_IN]->(c)
    """)

    tx.run("""
        MATCH (s:Supplier {id: "SUP_001"}),
              (m:Manufacturer {id: "MAN_001"})
        MERGE (s)-[:SUPPLIES]->(m)

        WITH 1 AS dummy

        MATCH (s:Supplier {id: "SUP_002"}),
              (m:Manufacturer {id: "MAN_001"})
        MERGE (s)-[:SUPPLIES]->(m)

        WITH 1 AS dummy

        MATCH (s:Supplier {id: "SUP_003"}),
              (m:Manufacturer {id: "MAN_002"})
        MERGE (s)-[:SUPPLIES]->(m)
    """)

    tx.run("""
        MATCH (m:Manufacturer {id: "MAN_001"}),
              (p:Product {id: "PROD_003"})
        MERGE (m)-[:PRODUCES]->(p)

        WITH 1 AS dummy

        MATCH (m:Manufacturer {id: "MAN_002"}),
              (p:Product {id: "PROD_002"})
        MERGE (m)-[:PRODUCES]->(p)
    """)

    tx.run("""
        MATCH (p:Product {id: "PROD_001"}),
              (i:Industry {id: "IND_001"})
        MERGE (p)-[:BELONGS_TO]->(i)

        WITH 1 AS dummy

        MATCH (p:Product {id: "PROD_002"}),
              (i:Industry {id: "IND_002"})
        MERGE (p)-[:BELONGS_TO]->(i)

        WITH 1 AS dummy

        MATCH (p:Product {id: "PROD_003"}),
              (i:Industry {id: "IND_002"})
        MERGE (p)-[:BELONGS_TO]->(i)
    """)

    tx.run("""
        MATCH (m:Manufacturer {id: "MAN_001"}),
              (w:Warehouse {id: "WH_002"})
        MERGE (m)-[:SHIPS_TO]->(w)

        WITH 1 AS dummy

        MATCH (m:Manufacturer {id: "MAN_002"}),
              (w:Warehouse {id: "WH_001"})
        MERGE (m)-[:SHIPS_TO]->(w)
    """)

    tx.run("""
        MATCH (a:Port {id: "PORT_SHA"}),
              (b:Port {id: "PORT_ROT"})
        MERGE (a)-[:CONNECTED_TO {
            transport: "Sea",
            transit_days: 30
        }]->(b)

        WITH 1 AS dummy

        MATCH (a:Port {id: "PORT_ROT"}),
              (b:Port {id: "PORT_LA"})
        MERGE (a)-[:CONNECTED_TO {
            transport: "Sea",
            transit_days: 25
        }]->(b)

        WITH 1 AS dummy

        MATCH (a:Port {id: "PORT_HAM"}),
              (b:Port {id: "PORT_LA"})
        MERGE (a)-[:CONNECTED_TO {
            transport: "Sea",
            transit_days: 28
        }]->(b)
    """)


def main():

    with driver.session() as session:
        session.execute_write(create_graph)

    print("AtmoGraph supply-chain graph created successfully.")

    driver.close()


if __name__ == "__main__":
    main()