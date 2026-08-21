EVENT_SEVERITY = {
    "strike": 0.90,
    "blockade": 0.95,
    "shutdown": 0.95,
    "fire": 0.90,
    "earthquake": 1.00,
    "closure": 0.90,
    "shortage": 0.70,
    "congestion": 0.60,
    "delay": 0.50,
    "disruption": 0.60
}

IMPACT_WORDS = {
    "major": 0.90,
    "severe": 1.00,
    "critical": 1.00,
    "significant": 0.80,
    "delayed": 0.60,
    "delay": 0.50,
    "minor": 0.20
}


def calculate_risk(text, entity_found, event):

    text_lower = text.lower()


    event_score = EVENT_SEVERITY.get(
        event.lower(),
        0.30
    )


    impact_scores = []

    for word, score in IMPACT_WORDS.items():

        if word in text_lower:
            impact_scores.append(score)

    if impact_scores:
        impact_score = max(impact_scores)
    else:
        impact_score = 0.30


    confidence = 0.0

    # Entity found
    if entity_found:
        confidence += 0.40

    # Disruption event found
    if event.lower() in text_lower:
        confidence += 0.30

    # Impact information found
    if impact_scores:
        confidence += 0.20

    # Strong impact wording
    strong_words = [
        "major",
        "severe",
        "critical"
    ]

    if any(word in text_lower for word in strong_words):
        confidence += 0.10

    # Keep confidence between 0 and 1
    confidence = min(confidence, 1.0)


    risk_score = (
        0.5 * event_score +
        0.3 * impact_score +
        0.2 * confidence
    )

    risk_score = min(
        max(risk_score, 0.0),
        1.0
    )


    if risk_score >= 0.75:
        risk_level = "HIGH"

    elif risk_score >= 0.45:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_score": round(risk_score, 3),
        "risk_level": risk_level,
        "confidence": round(confidence, 3),
        "event_score": event_score,
        "impact_score": impact_score
    }