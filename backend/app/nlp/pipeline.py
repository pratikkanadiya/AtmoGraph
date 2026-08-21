from nlp.ner import extract_entities
from nlp.entity_resolver import entity_resolver



def process_news(text):

    entities = extract_entities(text)

    node = entity_resolver.resolve(entities)

    event = detect_event(text)

    risk = calculate_risk(
        text=text,
        entity_found=True,
        event=event
    )

    # 5. Update Neo4j
    updated_node = update_node_risk(
        node_id=node["id"],
        risk_score=risk["risk_score"],
        confidence=risk["confidence"],
        risk_level=risk["risk_level"],
        risk_status="DISRUPTED",
        risk_reason=text
    )

    return {
        "entities": entities,
        "event": event,
        "risk": risk,
        "neo4j_node": updated_node
    }