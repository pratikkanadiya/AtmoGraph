MATCH path =
(s:Supplier)-[:SUPPLIES]->
(m:Manufacturer)-[:PRODUCES]->
(p:Product)-[:BELONGS_TO]->
(i:Industry)
RETURN path;

MATCH (p:Port {id: "PORT_ROT"})
RETURN
    p.id AS id,
    p.name AS name,
    p.risk_level AS risk_level,
    p.risk_score AS risk_score,
    p.risk_status AS risk_status,
    p.risk_confidence AS risk_confidence,
    p.risk_reason AS risk_reason,
    p.last_updated AS last_updated;