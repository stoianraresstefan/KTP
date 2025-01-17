from logistics_app import App
from logistics_logic import Logic
import tkinter as tk
from typing import Callable, Dict


class UI:
    def __init__(self, app: App, logic: Logic) -> None:
        self.app = app
        self.logic = logic

    def update_text_frame(self, txt: str) -> None:
        "Updates the text in the main frame."
        label = tk.Label(master=self.app.main_frame, text=txt, bg="white", fg="black", wraplength=400, justify="left")
        label.pack(pady=20)

    def update_buttons(self, question: str, yes_callback: Callable[[], None], no_callback: Callable[[], None]) -> None:
        "Updates the main frame with Yes/No buttons."
        question_label = tk.Label(master=self.app.main_frame, text=question, bg="white", fg="black", wraplength=400)
        question_label.pack(pady=20)
        yes_btn = tk.Button(master=self.app.main_frame, text="Yes", command=yes_callback, bg="green", fg="black")
        yes_btn.pack(side="left", padx=10, pady=10)
        no_btn = tk.Button(master=self.app.main_frame, text="No", command=no_callback, bg="red", fg="black")
        no_btn.pack(side="right", padx=10, pady=10)

    def ask_text_input(self, issue: Dict[str, str], current_topic: str) -> None: # CAUSES A LOT OF ERRORS
        "Displays a text input box for the user to respond to a question."

        def submit() -> None:
            response = entry.get().strip()
            if response:  # Ensure the response is not empty
                result = self.logic.calculate_volume(response)
                if isinstance(result, tuple) and len(result) == 2:  # Ensure we have a tuple with two values
                    volume, weight = result
                    if volume > 0 and weight > 0:
                        vehicle = self.logic.determine_vehicle(volume, weight)
                        self.display_conclusion(vehicle)
                    else:
                        self.display_conclusion("conclusion_invalid_dimensions")  # Invalid input
                else:
                    self.display_conclusion("conclusion_invalid_format")  # Invalid input format

        # Visuals
        self.app.clear_frame()
        label = tk.Label(master=self.app.main_frame, text=issue["question"], bg="white", fg="black", wraplength=400)
        label.pack(pady=20)
        entry = tk.Entry(master=self.app.main_frame)
        entry.pack(pady=10)
        submit_btn = tk.Button(master=self.app.main_frame, text="Submit", command=submit)
        submit_btn.pack(pady=20)

    def start_welcome_screen(self) -> None:
        "Displays the welcome screen."
        self.app.clear_frame()
        self.update_text_frame("Welcome to your Logistics Assistant!")
        continue_btn = tk.Button(
            master=self.app.main_frame,
            text="Continue",
            command=self.start_questioning
        )
        continue_btn.pack(pady=20)

    def start_questioning(self) -> None:
        "Manages the flow of questioning based on topics and rules."
        self.app.clear_frame()
        current_topic = "shipment_check"
        while "conclusion" not in current_topic:
            topic = self.logic.find_topic(current_topic)
            if not topic:  # May cause the error
                self.display_conclusion("conclusion_invalid_dimensions")
                return

            for issue in topic["issues"]:
                if issue["name"] in self.logic.facts or f"no {issue['name']}" in self.logic.facts:
                    continue
                # Determine the type of question
                if issue["type"] == "text_input":
                    self.ask_text_input(issue, current_topic)
                    return
                elif issue["type"] == "yes_no":
                    self.ask_yes_no_question(issue, current_topic)
                    return

            current_topic = self.logic.apply_rules(current_topic)

        self.display_conclusion(current_topic)

    def ask_yes_no_question(self, issue: Dict[str, str], current_topic: str) -> None:
        "Displays a yes/no question and processes the user's response."
        def yes() -> None:
            self.logic.facts.append(issue["name"])
            self.logic.update_file()
            self.start_questioning()

        def no() -> None:
            self.logic.facts.append(f"no {issue['name']}")
            self.logic.update_file()
            self.start_questioning()

        self.app.clear_frame()
        self.update_buttons(issue["question"], yes, no)

    def display_conclusion(self, conclusion_key: str) -> None:
        "Displays the conclusion based on the provided key."
        self.app.clear_frame()
        conclusions = self.logic.data.get("Conclusions", {})
        advice = conclusions.get(conclusion_key, "Thanks for using the logistics knowledge base.")
        self.update_text_frame(advice)
