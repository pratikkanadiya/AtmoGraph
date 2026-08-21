from app.database.neo4j import driver


def update_node_risk(
    node_id,
    risk_score,
    confidence,
    risk_level,
    risk_status,
    risk_reason
):

    query = """
    MATCH (n {id: $node_id})

    SET n.risk_score = $risk_score,
        n.risk_confidence = $confidence,
        n.risk_level = $risk_level,
        n.risk_status = $risk_status,
        n.risk_reason = $risk_reason,
        n.last_updated = datetime()

    RETURN
        n.id AS node_id,
        n.name AS name,
        labels(n) AS labels,
        n.risk_score AS risk_score,
        n.risk_confidence AS risk_confidence,
        n.risk_level AS risk_level,
        n.risk_status AS risk_status,
        n.risk_reason AS risk_reason,
        n.last_updated AS last_updated
    """

    with driver.session(database="neo4j") as session:

        result = session.run(
            query,
            node_id=node_id,
            risk_score=risk_score,
            confidence=confidence,
            risk_level=risk_level,
            risk_status=risk_status,
            risk_reason=risk_reason
        )

        record = result.single()

        if record is None:
            raise ValueError(
                f"Node not found: {node_id}"
            )

        return dict(record)