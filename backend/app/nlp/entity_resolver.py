from app.database.neo4j import driver


NODE_LABELS = [
    "Port",
    "Supplier",
    "Manufacturer",
    "Warehouse",
    "Product",
    "Industry",
    "Country"
]


def normalize_entity_name(name):
    """
    Normalize entity text before matching.
    """

    name = name.strip().lower()

    # Remove common leading articles
    for prefix in ["the ", "a ", "an "]:
        if name.startswith(prefix):
            name = name[len(prefix):]

    return name.strip()


def resolve_entity(entity_name):
    """
    Search Neo4j for a matching supply-chain entity.
    """

    normalized_name = normalize_entity_name(entity_name)

    query = """
    MATCH (n)
    WHERE any(label IN labels(n)
              WHERE label IN $node_labels)
      AND n.name IS NOT NULL

    WITH n,
         toLower(trim(n.name)) AS db_name,
         toLower(trim($entity_name)) AS input_name

    WHERE db_name = input_name
       OR db_name CONTAINS input_name
       OR input_name CONTAINS db_name

    RETURN
        n.id AS id,
        n.name AS name,
        labels(n) AS labels,
        n.country AS country

    LIMIT 1
    """

    with driver.session(database="neo4j") as session:

        result = session.run(
            query,
            entity_name=normalized_name,
            node_labels=NODE_LABELS
        )

        record = result.single()

        if record is None:
            return None

        labels = record["labels"]

        return {
            "id": record["id"],
            "name": record["name"],
            "label": labels[0] if labels else None,
            "country": record["country"]
        }