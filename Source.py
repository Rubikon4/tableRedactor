import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class SourceFrame(ttk.Frame):
    def __init__(self, Main, controller):
        super().__init__(Main, padding=10, borderwidth=2, relief="solid")
        self.controller = controller
        self.mode = tk.StringVar(value="once")
        self.template_name = tk.StringVar()
        self.template_name.trace_add("write", self.on_template_change)
        self.source_file = ""
        self.source_folder = ""
        self.output_folder = ""
        self.build_ui()
        self.update_inputs_state()
    def build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        
        mode_label = ttk.Label(self, text="Выберите режим и конечную папку:")
        mode_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.output_button = ttk.Button(self, text="Конечная папка", 
                                        command=lambda:[
                                        self.choose_output_folder(), 
                                        self.controller.summary_frame.update_summary()])
        self.output_button.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        """    ONCE    """

        self.radio_once = ttk.Radiobutton(self, text="Единоразовая обработка",
                                          variable=self.mode, value="once",
                                          command=lambda:[
                                          self.refresh_summary_window(),
                                          self.controller.processing_frame.refresh_window(),
                                          self.controller.processing_frame.update_input_state()    
                                          ])
        self.btn_choose_file = ttk.Button(self, text="Выбрать файл",
                                          command=lambda:[
                                          self.choose_file(),
                                          self.controller.summary_frame.update_summary(),
                                          ])
        
        self.radio_once.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.btn_choose_file.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        """    TIMER    """
        
        self.radio_timer = ttk.Radiobutton(self, text="Обработка по таймеру",
                                           variable=self.mode, value="timer",
                                           command=lambda:[
                                           self.refresh_summary_window(),
                                           self.controller.processing_frame.refresh_window(),
                                           self.controller.processing_frame.update_input_state()
                                           ])
        self.btn_choose_folder = ttk.Button(self, text="Выбрать папку",
                                            command=lambda:[
                                            self.choose_folder(),
                                            self.controller.summary_frame.update_summary()])
        label_example = ttk.Label(self, text="Шаблон названия файла:")
        self.entry_template = ttk.Entry(self, textvariable=self.template_name)
        self.entry_template.bind("<Return>", lambda e: [self.validate_template(), 
                                                        self.entry_template.master.focus_set()])
        
        self.radio_timer.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.btn_choose_folder.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        label_example.grid(row=2, column=2, sticky="w", padx=5, pady=(10, 0))
        self.entry_template.grid(row=3, column=2, sticky="ew", padx=5, pady=5)
        
        """    MASTER    """

        self.radio_master = ttk.Radiobutton(self, text="Расширенная обработка",
                                            variable=self.mode, value="master",
                                            command=lambda:[
                                            self.refresh_summary_window(),
                                            self.controller.processing_frame.refresh_window()
                                            ]) 
        self.btn_master_choose_file = ttk.Button(self, text="Выбрать файл",
                                                       command=lambda:[
                                                       self.choose_file(),
                                                       self.controller.summary_frame.update_summary()])
        self.btn_master_choose_folder = ttk.Button(self, text="Выбрать папку",
                                               command=lambda:[
                                               self.choose_folder(),
                                               self.controller.summary_frame.update_summary()])
        label_master_example = ttk.Label(self, text="Шаблон названия файла:")
        self.entry_master_template = ttk.Entry(self, textvariable=self.template_name)
        self.entry_master_template.bind("<Return>", lambda e: [self.validate_template(), 
                                                   self.entry_master_template.master.focus_set()])
        
        self.radio_master.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.btn_master_choose_file.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.btn_master_choose_folder.grid(row=1, column=4, sticky="w", padx=5, pady=5)
        label_master_example.grid(row=2, column=4, sticky="w", padx=5, pady=(10, 0))
        self.entry_master_template.grid(row=3, column=4, sticky="ew", padx=5, pady=5)

    def refresh_summary_window(self):
        self.update_inputs_state()
        self.controller.summary_frame.update_summary()
    def update_inputs_state(self):
        mode = self.mode.get()
        if mode == "once":
            self.btn_choose_file.state(["!disabled"])
            self.btn_choose_folder.state(["disabled"])
            self.entry_template.state(["disabled"])
            self.btn_master_choose_file.state(["disabled"])
            self.btn_master_choose_folder.state(["disabled"])
            self.entry_master_template.state(["disabled"])
        elif mode == "timer":
            self.btn_choose_file.state(["disabled"])
            self.btn_choose_folder.state(["!disabled"])
            self.entry_template.state(["!disabled"])
            self.btn_master_choose_file.state(["disabled"])
            self.btn_master_choose_folder.state(["disabled"])
            self.entry_master_template.state(["disabled"])
        elif mode == "master":
            self.btn_choose_file.state(["disabled"])
            self.btn_choose_folder.state(["disabled"])
            self.entry_template.state(["disabled"])
            self.btn_master_choose_file.state(["!disabled"])
            self.btn_master_choose_folder.state(["!disabled"])
            self.entry_master_template.state(["!disabled"])

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.source_file = file_path
    def choose_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.source_folder = folder_path
    def choose_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder = folder_path
    def validate_template(self, event=None):
        name = self.template_name.get()
        if "." in name:
            messagebox.showinfo("Ошибка шаблона",
                                "Введите только имя файла без расширения, например: 'отчет', не 'отчет.xls'")
            self.template_name.set("")
    def get_file_by_template(self):
        folder = self.source_folder
        template = self.template_name.get().strip()
        if not folder or not template:
            return None
        for filename in os.listdir(folder):
            if filename.startswith(template) and filename.endswith(('.xls', '.xlsx')):
                return os.path.join(folder, filename)
        return None  # если ничего не найдено
    def on_template_change(self, *args):
        self.controller.summary_frame.update_summary()