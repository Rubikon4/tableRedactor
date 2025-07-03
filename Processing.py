import tkinter as tk
from tkinter import ttk

class ProcessingFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10, borderwidth=1, relief="solid")
        self.controller = controller

        self.process_mode = tk.StringVar(value="clean")
        self.rows_range = tk.StringVar()
        self.cols_range = tk.StringVar()

        self.build_ui()
        self.update_input_states()

    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        label = ttk.Label(self, text="Выберите тип обработки:")
        label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.radio_clean = ttk.Radiobutton(self, text="Очистить пустые строки",
                                           variable=self.process_mode, value="clean",
                                           command=self.update_input_states)
        self.radio_rows = ttk.Radiobutton(self, text="Выгрузить строки от-до",
                                          variable=self.process_mode, value="rows",
                                          command=self.update_input_states)
        self.radio_cols = ttk.Radiobutton(self, text="Выгрузить столбцы от-до",
                                          variable=self.process_mode, value="cols",
                                          command=self.update_input_states)

        self.radio_clean.grid(row=1, column=0, sticky="w")
        self.radio_rows.grid(row=2, column=0, sticky="w")
        self.radio_cols.grid(row=3, column=0, sticky="w")

        self.entry_rows = ttk.Entry(self, textvariable=self.rows_range)
        self.entry_cols = ttk.Entry(self, textvariable=self.cols_range)
        self.entry_rows.grid(row=2, column=1, sticky="w")
        self.entry_cols.grid(row=3, column=1, sticky="w")

    def update_input_states(self):
        mode = self.process_mode.get()
        self.entry_rows.state(["!disabled"] if mode == "rows" else ["disabled"])
        self.entry_cols.state(["!disabled"] if mode == "cols" else ["disabled"])