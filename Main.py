from Source import SourceFrame
from Processing import ProcessingFrame
from SummaryFrame import SummaryFrame
import tkinter as tk
from tkinter import ttk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Обработка Excel файлов")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.source_frame = SourceFrame(self, self)
        self.source_frame.grid(row=0, column=0, sticky="nsew")

        self.processing_frame = ProcessingFrame(self, self)
        self.processing_frame.grid(row=1, column=0, sticky="nsew")

        self.summary_frame = SummaryFrame(self, self)
        self.summary_frame.grid(row=2, column=0, sticky="nsew")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
