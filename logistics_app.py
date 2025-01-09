from PIL import Image, ImageTk
import tkinter as tk


class App:
    def __init__(self, window_title: str = "Logistics Assistant",
                 window_size: str = "1500x700",
                 image_path: str = "background.png") -> None:
        self.window = tk.Tk()
        self.window.geometry(window_size)
        self.window.title(window_title)

        self.image_path = image_path
        self.background_image = Image.open(self.image_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = tk.Label(self.window, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.user_response_var = tk.StringVar()
        self.main_frame = None
        self._initialize_grid()
        self._create_main_frame()

    def _initialize_grid(self) -> None:
        for i in range(3):
            self.window.columnconfigure(i, weight=1, minsize=200)
            self.window.rowconfigure(i, weight=1, minsize=100)

    def _create_main_frame(self) -> None:
        self.main_frame = tk.Frame(master=self.window, width=200, height=400, background="white")
        self.main_frame.grid(row=1, column=1)
        self.main_frame.lift()

    def clear_frame(self) -> None:
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def run(self) -> None:
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self) -> None:
        self.user_response_var.set("close")
        self.window.destroy()
