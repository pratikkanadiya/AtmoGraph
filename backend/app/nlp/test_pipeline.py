from app.nlp.ner import NEREngine
from app.nlp.entity_resolver import resolve_entity
from app.nlp.risk_analyzer import calculate_risk
from app.services.risk_updater import update_node_risk


text = """
Workers at the Port of Rotterdam announced
a major strike causing severe shipping delays.
"""

ner = NEREngine()

entities = ner.extract_entities(text)

print("\n--- NER RESULTS ---")

for entity in entities:
    print(entity)


print("\n--- ENTITY RESOLUTION ---")

resolved_entities = []

for entity in entities:

    resolved = resolve_entity(entity["text"])

    if resolved:

        print(
            f"{entity['text']} -> "
            f"{resolved['label']} -> "
            f"{resolved['id']}"
        )

        resolved_entities.append(resolved)


EVENTS = [
    "strike",
    "blockade",
    "shutdown",
    "fire",
    "earthquake",
    "closure",
    "shortage",
    "congestion",
    "delay",
    "disruption"
]


event = None

text_lower = text.lower()

for e in EVENTS:

    if e in text_lower:
        event = e
        break


print("\n--- EVENT ---")
print(event)


if resolved_entities and event:

    risk = calculate_risk(
        text=text,
        entity_found=True,
        event=event
    )

    print("\n--- RISK ANALYSIS ---")
    print(risk)

    # Update the first resolved Neo4j node
    node = resolved_entities[0]

    updated_node = update_node_risk(
        node_id=node["id"],
        risk_score=risk["risk_score"],
        confidence=risk["confidence"],
        risk_level=risk["risk_level"],
        risk_status="DISRUPTED",
        risk_reason=text.strip()
    )

    print("\n--- NEO4J UPDATED NODE ---")
    print(updated_node)