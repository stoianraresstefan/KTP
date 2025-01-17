from logistics_app import App
from logistics_logic import Logic
from logistics_ui import UI

if __name__ == "__main__":
    app = App()
    logic = Logic(filename="logistics_knowledge_base.json")
    ui = UI(app, logic)
    logic.reset_facts()
    ui.start_welcome_screen()
    app.run()