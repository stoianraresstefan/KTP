from logistics_app import App
from logistics_logic import Logic
import tkinter as tk
from typing import Callable, Dict


class UI:
    def __init__(self, app: App, logic: Logic) -> None:
        self.app = app
        self.logic = logic

    def update_text_frame(self, txt: str) -> None:
        label = tk.Label(master=self.app.main_frame, text=txt, bg="white", wraplength=400, justify="left")
        label.pack(pady=20)

    def update_buttons(self, question: str, yes_callback: Callable[[], None], no_callback: Callable[[], None]) -> None:
        question_label = tk.Label(master=self.app.main_frame, text=question, bg="white")
        question_label.pack(pady=20)
        yes_btn = tk.Button(master=self.app.main_frame, text="Yes", command=yes_callback)
        yes_btn.pack(side="left", padx=5)
        no_btn = tk.Button(master=self.app.main_frame, text="No", command=no_callback)
        no_btn.pack(side="right", padx=5)

    def start_welcome_screen(self) -> None:
        self.app.clear_frame()
        self.update_text_frame("Welcome to your Logistics Assistant!")
        continue_btn = tk.Button(
            master=self.app.main_frame,
            text="Continue",
            command=self.start_questioning
        )
        continue_btn.pack(pady=20)

    def start_questioning(self) -> None:
        self.app.clear_frame()
        current_topic = "logistics_start"
        while "conclusion" not in current_topic:
            topic = self.logic.find_topic(current_topic)
            if not topic:
                break
            for issue in topic["issues"]:
                if issue["name"] not in self.logic.facts and f"no {issue['name']}" not in self.logic.facts:
                    self.ask_yes_no_question(issue, current_topic)
                    return
            current_topic = self.logic.apply_rules(current_topic)
        self.display_conclusion(current_topic)

    def ask_yes_no_question(self, issue: Dict[str, str], current_topic: str) -> None:
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
        self.app.clear_frame()
        conclusions = self.logic.data.get("Conclusions", {})
        advice = conclusions.get(conclusion_key, "Thanks for using the logistics knowledge base")
        self.update_text_frame(advice)
