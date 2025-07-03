import time
import threading
import os
from TableProcessor import TableProcessor

class TimerRunner:
    def __init__(self, source_frame, processing_frame, output_folder, interval_seconds=3600):
        self.source_frame = source_frame
        self.processing_frame = processing_frame
        self.output_folder = output_folder
        self.interval = interval_seconds
        self._stop_flag = False
        self.thread = None

    def start(self):
        self._stop_flag = False
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self._stop_flag = True

    def _run_loop(self):
        while not self._stop_flag:
            file_path = self.source_frame.get_file_by_template()
            if file_path and os.path.exists(file_path):
                print(f"[Таймер] Обнаружен файл: {file_path}")
                self._process_file(file_path)
            else:
                print("[Таймер] Файл по шаблону не найден.")

            time.sleep(self.interval)

    def _process_file(self, file_path):
        processor = TableProcessor(file_path)
        if not processor.load():
            print("[Таймер] Ошибка загрузки файла.")
            return

        mode = self.processing_frame.process_mode.get()

        try:
            if mode == "clean":
                processor.clean_empty_rows()
            elif mode == "rows":
                start, end = map(int, self.processing_frame.rows_range.get().split())
                processor.filter_rows(start - 1, end - 1)
            elif mode == "cols":
                start, end = map(int, self.processing_frame.cols_range.get().split())
                processor.filter_columns(start - 1, end - 1)
        except Exception as e:
            print(f"[Таймер] Ошибка обработки: {e}")
            return

        output_file = os.path.join(self.output_folder, "обработанный_файл_по_таймеру.xlsx")
        if processor.export(output_file):
            print(f"[Таймер] Файл обработан и сохранён: {output_file}")
        else:
            print("[Таймер] Не удалось сохранить файл.")