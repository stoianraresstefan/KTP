import json
from typing import Any, Dict, Optional


class Logic:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data = self._read_file()
        self.facts = self.data.get("Facts", [])
        self.rules = self.data.get("Rules", [])
        self.knowledge_base = self.data.get("Knowledge base", [])
        self.completed_topics = []  # Useful for tracking stuff

    def _read_file(self) -> dict:
        "Reads the JSON"
        with open(self.filename, "r") as file:
            return json.load(file)

    def update_file(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=4)

    def find_topic(self, current_topic: str) -> dict:
        "Iterates trough the knowledge base and returns the topic if it matches the current one"
        for item in self.knowledge_base:
            if item["topic"] == current_topic:
                return item
        return None

    def apply_rules(self, current_topic: str) -> str: # A LOT OF TIMES ISSUES WITH THE PROGRAM ARE HERE
        "Applies the rules for current topic and check which one follows"
        print(f"Applying rules for topic: {current_topic}")
        for rule in self.rules:
            if rule["current topic"] == current_topic:
                # Check if all required issues are present in facts
                if all(issue in self.facts for issue in rule["required issues"]):
                    if current_topic not in self.completed_topics:
                        self.completed_topics.append(current_topic)  # Mark topic as completed
                    return rule.get("new direction", "conclusion")
                else:
                    return rule.get("else", "conclusion")
        return "conclusion"

    def determine_category(self, is_perishable: str) -> str:
        "Determines the vehicle category"
        if is_perishable == "yes":
            return "category_a"
        else:
            return "category_b"

    def calculate_volume(self, dimensions: str) -> float:
        "Calculates the volume"
        try:
            h, l, w = map(float, dimensions.split(","))
            return h * l * w
        except ValueError:
            return 0

    def determine_vehicle(self, volume: float) -> str:
        "Determines which vehicle is most optimal"
        vehicles = [
            ("van", 1.5),
            ("box_truck", 2.5),
            ("semi_trailer_truck", 31),
            ("jumbo_truck", 60)
        ]

        # Here we check which trucks are available
        if "all_trucks_available" in self.facts:
            available_vehicles = [vehicle for vehicle, _ in vehicles]
        else:
            available_vehicles = [
                vehicle for vehicle, _ in vehicles if f"{vehicle}_available" in self.facts
            ]

        for vehicle, max_volume in vehicles:
            if vehicle in available_vehicles and volume <= max_volume:
                if "is_perishable" in self.facts:
                    return f"{vehicle}_fridge"
                if "is_fragile" in self.facts:
                    return f"{vehicle}_fragile"
                if "is_hazardous" in self.facts:
                    return f"{vehicle}_hazardous"
                if "requires_extra_security" in self.facts:
                    return f"{vehicle}_extra_security"
                else:
                    return f"{vehicle}_normal"

        return "no_vehicle"

    def reset_facts(self) -> None:
        "Resets the JSON"
        self.facts.clear() 
        self.update_file()
