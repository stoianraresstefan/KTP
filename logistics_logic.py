import json
from typing import Any, Dict, Optional


class Logic:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data = self._read_file()
        self.facts = self.data["Facts"]
        self.rules = self.data["Rules"]
        self.knowledge_base = self.data["Knowledge base"]

    def _read_file(self) -> Dict[str, Any]:
        with open(self.filename, "r") as file:
            return json.load(file)

    def update_file(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def reset_facts(self) -> None:
        self.data["Facts"].clear()
        self.update_file()

    def find_topic(self, current_topic: str) -> Optional[Dict[str, Any]]:
        for item in self.knowledge_base:
            if item["topic"] == current_topic:
                return item
        return None

    def apply_rules(self, current_topic: str) -> str:
        for rule in self.rules:
            if rule["current topic"] == current_topic:
                counter = sum(1 for issue in rule["required issues"] if issue in self.facts)
                if counter >= rule["number"]:
                    return rule.get("new direction", "conclusion")
                else:
                    return rule.get("else", "conclusion")
        return "conclusion"
