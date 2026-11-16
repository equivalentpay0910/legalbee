"""
LegalBee - rules step (Asthra)

1. match(topic): takes a topic and returns its law IDs from rules/topic_map.yaml.
2. run_questionnaire(answers): takes the user's answers to rules/questionnaire.yaml
   and returns the topic, the law IDs, any notes, and an out-of-scope message if needed.
No AI here: the same answers always give the same laws.

    from rules.match import match, run_questionnaire
    match("deposit")  # ["CIV-1950.5"]
    run_questionnaire({"location": "san_jose", "housing": "renting",
                       "time_lived": "over_12_months", "issue": "deposit"})
    # {"topic": "deposit", "law_ids": ["CIV-1950.5"], "notes": [], "out_of_scope": None}

Try it in the terminal:  python3 rules/match.py
"""

from pathlib import Path

import yaml

RULES_DIR = Path(__file__).resolve().parent
TOPIC_MAP_FILE = RULES_DIR / "topic_map.yaml"
QUESTIONNAIRE_FILE = RULES_DIR / "questionnaire.yaml"


def _load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_topic_map():
    """Read topic_map.yaml. Returns {domain: {topic: [law IDs]}}."""
    return _load_yaml(TOPIC_MAP_FILE)


def all_topics():
    """Flatten the map to {topic: [law IDs]} across every domain."""
    topics = {}
    for domain_topics in load_topic_map().values():
        topics.update(domain_topics or {})
    return topics


def match(topic):
    """Return the list of law IDs for a topic, or [] if the topic is unknown."""
    key = topic.strip().lower().replace(" ", "_").replace("-", "_")
    return list(all_topics().get(key, []))


def load_questionnaire(area="tenant"):
    """Return the list of questions for an area, for the website to show."""
    return _load_yaml(QUESTIONNAIRE_FILE).get(area, [])


def run_questionnaire(answers, area="tenant"):
    """
    answers: {question id: chosen value}, e.g. {"issue": "deposit"}
    Returns {"topic", "law_ids", "notes", "out_of_scope"}.
    out_of_scope is None, or the message to show instead of an answer.
    """
    data = _load_yaml(QUESTIONNAIRE_FILE)
    result = {"topic": None, "law_ids": [], "notes": [], "out_of_scope": None}

    for question in data.get(area, []):
        chosen = answers.get(question["id"])
        choice = next((c for c in question["choices"] if c["value"] == chosen), None)
        if choice is None:
            continue
        if "out_of_scope" in choice:
            result["out_of_scope"] = data["out_of_scope"][choice["out_of_scope"]]
            return result
        if "note" in choice:
            result["notes"].append(choice["note"])
        if "topic" in choice:
            result["topic"] = choice["topic"]

    if result["topic"]:
        result["law_ids"] = match(result["topic"])
    return result


if __name__ == "__main__":
    # Answer the questionnaire by typing a number for each question
    answers = {}
    for q in load_questionnaire():
        print("\n" + q["question"])
        for i, c in enumerate(q["choices"], 1):
            print(f"  {i}. {c['label']}")
        pick = int(input("Your choice: ")) - 1
        answers[q["id"]] = q["choices"][pick]["value"]
    print("\nResult:", run_questionnaire(answers))
