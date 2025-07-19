import tkinter as tk
from tkinter import ttk, messagebox
import os
from TableProcessor import TableProcessor
from TimerRunner import TimerRunner


class SummaryFrame(ttk.Frame):
    def __init__(self, Main, controller):
        super().__init__(Main, padding=10, borderwidth=2, relief="solid")
        self.controller = controller
        self.timer = None

        self.columnconfigure(0, weight=1)

        self.summary_text = tk.Text(self, height=4, width=80, state='disabled', wrap='word')
        self.summary_text.grid(row=0, column=0, sticky="w")

        # self.label_status = ttk.Label(self, text="", foreground="red") ХЗ че это 
        # self.label_status.grid(row=1, column=0, sticky="w") ХЗ че это 

        self.run_button = ttk.Button(self, text="ЗАПУСК", command=self.on_run)
        self.run_button.grid(row=2, column=0, sticky="w")
        
        self.update_summary()


    def update_summary(self):
        mode = self.controller.source_frame.mode.get()
        if mode == "once":
            mode_text="Единоразовая обработка файла"
        elif mode == "timer":
            mode_text="Обработка по таймеру (мониторинг)"
        elif mode == "master":
            mode_text="Расширенный режим"
        source = self.controller.source_frame.source_file if mode == "once" else self.controller.source_frame.source_folder
        output = self.controller.source_frame.output_folder
        process_mode = self.controller.processing_frame.process_mode.get()
        if process_mode == "clean":
            process_text = "Очистить пустые строки"
        elif process_mode == "rows":
            process_text = f"Строки: {self.controller.processing_frame.rows_range.get()}"
        elif process_mode == "cols":
            process_text = f"Столбцы: {self.controller.processing_frame.cols_range.get()}"
        else:
            process_text = "Не выбрано"
            ### Для отображения шаблона в режиме таймера
        template = "-"
        if mode == "timer":
            template_value = self.controller.source_frame.template_name.get().strip()
            template = template_value if template_value else ""
        summary = (
            f"Режим: {mode_text}\n\n"
            f"Шаблон: {template}\n\n"
            f"Источник: {source}\n\n"
            f"Конечная папка: {output}\n\n"
            f"Обработка: {process_text}" )
        self.summary_text.configure(state='normal')
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.configure(state='disabled')
        # Автоматически подстроить высоту по количеству строк
        lines = summary.count("\n") + 1
        self.summary_text.configure(height=lines)

    def on_run(self):
        source_frame = self.controller.source_frame
        processing_frame = self.controller.processing_frame

        mode = source_frame.mode.get()
        mode_master = source_frame.mode_master.get()
        if mode in ("once", "timer"):   # путь файла/папки от режима
            if mode == "timer":
                source_path = source_frame.source_folder 
            elif mode == "once":
                source_path = source_frame.source_file
        elif mode == "master":
            source_filePath_master = source_frame.source_file
            source_folderPath_master =source_frame.source_folder  
        output_path = source_frame.output_folder
        process_mode = processing_frame.process_mode.get()
        date_mode = processing_frame.date_mode.get()
        
        """     Обработка ошибок     """

        # if not source_path or not output_path:
        #     messagebox.showwarning("Ошибка", "Не выбран источник или конечная папка.")
        #     self.reset_all()
        #     return

        if process_mode == "rows" and not processing_frame.rows_range.get().strip():
            messagebox.showwarning("Ошибка", "Не указан диапазон строк.")
            self.reset_all()
            return
        
        if mode == "master" and not processing_frame.master_rows_range.get().strip(): # добавь сброс введенного
            messagebox.showwarning("Ошибка", "Не указан диапазон строк.")
            return

        if process_mode == "cols" and not processing_frame.cols_range.get().strip():
            messagebox.showwarning("Ошибка", "Не указан диапазон столбцов.")
            self.reset_all()
            return
        
        """

        ДОБАВИТЬ ОБРАБОТКУ ОШИБОК ДЛЯ MASTER (для столбцов уже реализовал)
        
        """

        """     Запуск     """

        if mode == "once":
            processor = TableProcessor(source_path)
            if not processor.load():
                messagebox.showwarning("Ошибка", "Не удалось загрузить файл.")
                return

            if process_mode == "clean":
                processor.clean_empty_rows()
            elif process_mode == "rows":
                try:
                    start, end = map(int, processing_frame.rows_range.get().split())
                    processor.filter_rows(start - 1, end - 1)
                except:
                    messagebox.showwarning("Ошибка", "Неверный формат диапазона строк (ожидается: 1 4).")
                    self.reset_all()
                    return
            elif process_mode == "cols":
                try:
                    start, end = map(int, processing_frame.cols_range.get().split())
                    processor.filter_columns(start - 1, end - 1)
                except:
                    messagebox.showwarning("Ошибка", "Неверный формат диапазона столбцов (ожидается: 1 3).")
                    self.reset_all()
                    return
            export_path = os.path.join(output_path, "обработанный_файл.xlsx")
            success = processor.export(export_path)
            if success:
                messagebox.showinfo("Успех", f"Файл обработан и сохранён:\n{export_path}")
                self.reset_all()
            else:
                messagebox.showwarning("Ошибка", "Не удалось сохранить файл.")

        elif mode == "timer":
            self.label_status.config(text="ИДЁТ ОБРАБОТКА...")
            self.timer = TimerRunner(source_path, output_path,
                                     processing_frame.process_mode.get(),
                                     processing_frame.rows_range.get(),
                                     processing_frame.cols_range.get())
            self.timer.start()
            messagebox.showinfo("Успех", "Таймер обработки запущен. Ожидайте...")

        elif mode == "master":
            """     Если файл то 1 если папка то 2    """
            if mode_master == "once":
                process_once = TableProcessor(source_filePath_master)
                if not process_once.load():
                    messagebox.showwarning("Ошибка", "Не удалось загрузить файл.")
                    return
                date_mode = processing_frame.date_mode.get()
                date_cell = processing_frame.cellDate_master.get() if date_mode == "cell" else None
                process_once.clean_empty_rows_master() if processing_frame.delete_rows_mode.get() == True else None
                process_once.set_header_by_number(processing_frame.master_title_row.get())
                process_once.select_rows(processing_frame.master_rows_range.get()) # добавить полноценную проверку ошибки
                process_once.extract_date(date_mode, date_cell)
                process_once.add_date_column()
                export_path = os.path.join(output_path, "обработанный_файл.xlsx") # обработанный файл должен быть ретерном из функции
                success = process_once.export_master(export_path)

            # else:
            #     self.label_status.config(text="ИДЁТ ОБРАБОТКА...")
            #     self.process_timer = TimerRunner(source_folderPath_master, output_path,
            #                                processing_frame.delete_rows_mode.get(),
            #                                processing_frame.master_title_row.get(),
            #                                processing_frame.master_rows_row.get(),
            #                                processing_frame.date_mode.get(),
            #                                processing_frame.cellDate_master.get() if processing_frame.date_mode.get() == "cell" else None)
            #     self.process_timer.start()


    def reset_all(self):
        self.controller.source_frame.template_name.set("")
        self.controller.source_frame.source_file = ""
        self.controller.source_frame.source_folder = ""
        self.controller.source_frame.output_folder = ""

        self.controller.processing_frame.process_mode.set("clean")
        self.controller.processing_frame.rows_range.set("")
        self.controller.processing_frame.cols_range.set("")

        self.label_status.config(text="")
        self.update_summary()