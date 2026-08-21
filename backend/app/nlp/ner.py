import spacy


class NEREngine:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):

        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        return entities