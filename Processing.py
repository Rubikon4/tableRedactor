import tkinter as tk
from tkinter import ttk

class ProcessingFrame(ttk.Frame):
    def __init__(self, Main, controller):
        super().__init__(Main, padding=10, borderwidth=2, relief="solid")
        self.controller = controller

        self.process_mode = tk.StringVar(value="clean")
        self.rows_range = tk.StringVar()
        self.cols_range = tk.StringVar()
        # self.delete_rows_mode = tk.StringVar()
        self.title_row_master = tk.StringVar()
        self.entry_rows_master = tk.StringVar()
        self.whithoutDate_mode_master = tk.StringVar()
        self.fromCell_mode_master = tk.StringVar()
        self.autoDetectDate_mode_master = tk.StringVar()
        self.cellDate_master = tk.StringVar()
        # self.dateToTitle_mode = tk.StringVar()
        # self.entry_dateColumn_master = tk.StringVar
        
        self.build_ui()
        self.update_input_state()

    def build_ui(self):

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=8)

        # Другие обработки
        self.label = ttk.Label(self, text="Выберите тип обработки:")
        self.label.grid(row=0, column=0, sticky="w")

        self.radio_clean = ttk.Radiobutton(self, text="Очистить пустые строки",
                                           variable=self.process_mode, value="clean",
                                           command=lambda: [self.update_input_state(), self.controller.summary_frame.update_summary()])
        self.radio_rows = ttk.Radiobutton(self, text="Выгрузить строки от-до",
                                          variable=self.process_mode, value="rows",
                                          command=lambda: [self.update_input_state(), self.controller.summary_frame.update_summary()])
        self.radio_cols = ttk.Radiobutton(self, text="Выгрузить столбцы от-до",
                                          variable=self.process_mode, value="cols",
                                          command=lambda: [self.update_input_state(), self.controller.summary_frame.update_summary()])

        self.radio_clean.grid(row=1, column=0, sticky="w")
        self.radio_rows.grid(row=2, column=0, sticky="w")
        self.radio_cols.grid(row=3, column=0, sticky="w")

        self.entry_rows = ttk.Entry(self, textvariable=self.rows_range)
        self.entry_rows.bind("<Return>", lambda e: [self.controller.summary_frame.update_summary(), # Для отзывчивого поведения интерфейса, 
                                                    self.entry_rows.master.focus_set()])            # убирает фокус (курсор) с поля ввода
        self.entry_cols = ttk.Entry(self, textvariable=self.cols_range)
        self.entry_cols.bind("<Return>", lambda e: [self.controller.summary_frame.update_summary(), # Для отзывчивого поведения интерфейса, 
                                                    self.entry_cols.master.focus_set()])            # убирает фокус (курсор) с поля ввода
        self.entry_rows.grid(row=2, column=1, sticky="w")
        self.entry_cols.grid(row=3, column=1, sticky="w")

        # Расширенная обработка
        self.label_master = ttk.Label(self, text="Настройки расширенной обработки:")
        self.ckbtn_deleteRows_master = ttk.Checkbutton(self, text="Очистить пустые строки?",
                                                        # variable=self.delete_rows_mode,
                                                        command=lambda: [self.update_input_state(),
                                                                         self.controller.summary_frame.update_summary()])
        self.label_titleRowNum_master = ttk.Label(self, text="Номер строки заголовка")
        self.entry_titleRowNum_master = ttk.Entry(self, textvariable=self.title_row_master)                                 # добавь focus_set
        self.label_enterRows_master = ttk.Label(self, text="Выгрузить строки от-до")
        self.entry_enterRows_master = ttk.Entry(self, textvariable=self.entry_rows_master)                                  # добавь focus_set
        self.label_dateMode_master = ttk.Label(self, text="Настройки даты")
        self.robtn_noDate_master = ttk.Radiobutton(self, text="Без даты",
                                                   variable=self.whithoutDate_mode_master, value="empty",
                                                   command=lambda: [self.update_input_state(), 
                                                                    self.controller.summary_frame.update_summary()])
        self.robtn_autoDate_master = ttk.Radiobutton(self, text="Найти автоматически",
                                                     variable=self.autoDetectDate_mode_master, value="auto",
                                                     command=lambda: [self.update_input_state(), 
                                                                      self.controller.summary_frame.update_summary()])
        self.robtn_cellDate_master = ttk.Radiobutton(self, text="Из ячейки",
                                                     variable=self.fromCell_mode_master, value="cell",
                                                     command=lambda: [self.update_input_state(), 
                                                                      self.controller.summary_frame.update_summary()])
        self.entry_cell_master = ttk.Entry(self, textvariable=self.cellDate_master)                                         # добавь focus_set
        # self.ckbtn_dateToTitle_master = ttk.Checkbutton(self, text="Добавить дату в название?",
                                                        #dateToTitle_mode variable=self.dateToTitle_mode,
                                                        # command=lambda: [self.update_input_state(),
                                                                        #  self.controller.summary_frame.update_summary()])
        # self.entry_dateToColumn_master = ttk.Entry(self, textvariable=self.entry_dateColumn_master)

        self.onceAndTimer_widgets = [
            self.radio_clean,
            self.radio_cols,
            self.radio_rows,
            self.entry_cols,
            self.entry_rows
        ]
        self.master_widgets = [
            self.ckbtn_deleteRows_master,
            self.entry_titleRowNum_master,
            self.entry_enterRows_master,
            self.robtn_noDate_master,
            self.robtn_autoDate_master,
            self.robtn_cellDate_master,
            self.entry_cell_master
        ]        

        self.label_master.grid(row=4, column=0, sticky="w")
        self.ckbtn_deleteRows_master.grid(row=5, column=0, sticky="w")
        self.label_titleRowNum_master.grid(row=6, column=0, sticky="w")
        self.entry_titleRowNum_master.grid(row=6, column=1, sticky="w")
        self.label_enterRows_master.grid(row=7, column=0, sticky="w")
        self.entry_enterRows_master.grid(row=7, column=1, sticky="w")
        self.label_dateMode_master.grid(row=8, column=0, sticky="w")
        self.robtn_noDate_master.grid(row=9, column=1, sticky="w")
        self.robtn_autoDate_master.grid(row=10, column=1, sticky="w")
        self.robtn_cellDate_master.grid(row=11, column=1, sticky="w")
        self.entry_cell_master.grid(row=11, column=2, sticky="w")
        # self.ckbtn_dateToTitle_master.grid(row=, column=, sticky="w")
        # self.entry_dateToColumn_master.grid(row=, column=, sticky="w")
        

    def update_input_state(self):                                                                                               # обновил название (убрал s на конце)
        mode = self.process_mode.get()
        self.entry_rows.state(["!disabled"] if mode == "rows" else ["disabled"])
        self.entry_cols.state(["!disabled"] if mode == "cols" else ["disabled"])
        
    def refresh_window(self):
        """Обновляет доступность в зависимости от выбронного режима"""
        mode = self.controller.source_frame.mode.get()
        if mode == "master":
            for w in self.onceAndTimer_widgets:
                w.state(["disabled"])
        if mode == "once" or "timer":
            for w in self.master_widgets:
                w.state(["disabled"])