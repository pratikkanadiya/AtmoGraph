from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database.neo4j import verify_connection
from app.nlp.ner import NEREngine
from app.nlp.entity_resolver import resolve_entity
from app.nlp.risk_analyzer import calculate_risk
from app.services.risk_updater import update_node_risk

from fastapi.middleware.cors import CORSMiddleware
from app.database.neo4j import driver


app = FastAPI(
    title="AtmoGraph API",
    description="Supply Chain Ripple Effect Predictor",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ner_engine = NEREngine()


class NewsRequest(BaseModel):
    text: str


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


def detect_event(text: str):

    text_lower = text.lower()

    for event in EVENTS:

        if event in text_lower:
            return event

    return None


@app.get("/")
def root():

    return {
        "project": "AtmoGraph",
        "status": "running",
        "version": "0.2.0"
    }


@app.get("/health")
def health():

    try:

        message = verify_connection()

        return {
            "status": "healthy",
            "database": "Neo4j",
            "connection": message
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "Neo4j",
            "error": str(e)
        }


@app.post("/process-news")
def process_news(request: NewsRequest):

    text = request.text.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="News text cannot be empty."
        )


    entities = ner_engine.extract_entities(text)


    resolved_entities = []

    for entity in entities:

        resolved = resolve_entity(entity["text"])

        if resolved:

            resolved_entities.append({
                "extracted_text": entity["text"],
                "ner_label": entity["label"],
                "neo4j_id": resolved["id"],
                "neo4j_name": resolved["name"],
                "neo4j_label": resolved["label"],
                "country": resolved["country"]
            })


    event = detect_event(text)

    if event is None:

        raise HTTPException(
            status_code=422,
            detail={
                "message": "No supported disruption event detected.",
                "supported_events": EVENTS
            }
        )


    if not resolved_entities:

        raise HTTPException(
            status_code=404,
            detail={
                "message": "No matching Neo4j supply-chain entity found.",
                "entities_detected": entities
            }
        )


    risk = calculate_risk(
        text=text,
        entity_found=True,
        event=event
    )


    updated_nodes = []

    for entity in resolved_entities:

        updated_node = update_node_risk(
            node_id=entity["neo4j_id"],
            risk_score=risk["risk_score"],
            confidence=risk["confidence"],
            risk_level=risk["risk_level"],
            risk_status="DISRUPTED",
            risk_reason=text
        )

        updated_nodes.append(updated_node)


    return {
        "status": "processed",

        "news": {
            "text": text
        },

        "entities": entities,

        "resolved_entities": resolved_entities,

        "event": {
            "type": event
        },

        "risk": risk,

        "neo4j": {
            "updated": True,
            "nodes": updated_nodes
        }
    }
    
@app.get("/graph")
def get_graph():

    query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)

    RETURN
        collect(DISTINCT {
            id: n.id,
            name: n.name,
            labels: labels(n),
            country: n.country,
            risk_level: n.risk_level,
            risk_score: n.risk_score,
            risk_status: n.risk_status,
            risk_confidence: n.risk_confidence
        }) AS nodes,

        collect(DISTINCT {
            id: elementId(r),
            source: n.id,
            target: m.id,
            type: type(r)
        }) AS relationships
    """

    with driver.session(database="neo4j") as session:

        result = session.run(query)

        record = result.single()

        if record is None:
            return {
                "nodes": [],
                "relationships": []
            }

        return {
            "nodes": record["nodes"],
            "relationships": record["relationships"]
        }