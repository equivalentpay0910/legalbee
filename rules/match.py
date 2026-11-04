"""
LegalBee - rules step (Asthra)

Takes a topic and returns the law IDs for it, using rules/topic_map.yaml.
No AI here: the same topic always gives the same laws.

    from rules.match import match
    match("deposit")  # ["CIV-1950.5"]

For now the topic is typed by hand. Later it will come from the questionnaire.
"""

from pathlib import Path

import yaml

TOPIC_MAP_FILE = Path(__file__).resolve().parent / "topic_map.yaml"


def load_topic_map():
    """Read topic_map.yaml. Returns {domain: {topic: [law IDs]}}."""
    with open(TOPIC_MAP_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


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


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "deposit"
    print(f"{topic} -> {match(topic)}")
