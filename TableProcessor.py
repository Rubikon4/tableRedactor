import pandas as pd

class TableProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load(self):
        """Загружает Excel-файл в DataFrame"""
        try:
            self.df = pd.read_excel(self.filepath, engine='openpyxl')
            return True
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            return False

    def clean_empty_rows(self):
        """Удаляет полностью пустые строки"""
        if self.df is not None:
            self.df.dropna(how='all', inplace=True)

    def filter_rows(self, start: int, end: int):
        """Оставляет строки от start до end включительно (0-based index)"""
        if self.df is not None:
            self.df = self.df.iloc[start:end+1]

    def filter_columns(self, start: int, end: int):
        """Оставляет столбцы от start до end включительно (0-based index)"""
        if self.df is not None:
            self.df = self.df.iloc[:, start:end+1]

    def export(self, output_path: str, format: str = 'xlsx'):
        """Сохраняет файл в указанный путь в формате xlsx или csv"""
        if self.df is not None:
            try:
                if format == 'csv':
                    self.df.to_csv(output_path, index=False)
                elif format == 'xlsx':
                    self.df.to_excel(output_path, index=False, engine='openpyxl')
                else:
                    raise ValueError("Неподдерживаемый формат")
                return True
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")
                return False
        return False