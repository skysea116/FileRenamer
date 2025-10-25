import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FolderRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Renamer - Kozen")
        self.root.geometry("600x500")
        
        # Словарь с диапазонами номеров для каждого устройства и атаки
        self.ranges = {
            2: {"kozen 10": (91, 170), "kozen 12": (171, 250)},
            3: {"kozen 10": (251, 346), "kozen 12": (347, 442)},
            4: {"kozen 10": (443, 458), "kozen 12": (459, 474)},
            5: {"kozen 10": (475, 514), "kozen 12": (515, 554)},
            6: {"kozen 10": (555, 594)},
            7: {"kozen 12": (595, 634)},
            8: {"kozen 10": (635, 733)},
            9: {"kozen 12": (734, 832)}
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Folder Renamer - Kozen", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм для выбора исходной папки
        source_frame = tk.Frame(self.root)
        source_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(source_frame, text="Исходная папка:").pack(anchor="w")
        
        source_input_frame = tk.Frame(source_frame)
        source_input_frame.pack(fill="x", pady=5)
        
        self.source_entry = tk.Entry(source_input_frame, font=("Arial", 10))
        self.source_entry.pack(side="left", fill="x", expand=True)
        
        source_btn = tk.Button(source_input_frame, text="Обзор", command=self.browse_source)
        source_btn.pack(side="right", padx=(5, 0))
        
        # Фрейм для выбора папки назначения
        dest_frame = tk.Frame(self.root)
        dest_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(dest_frame, text="Папка назначения:").pack(anchor="w")
        
        dest_input_frame = tk.Frame(dest_frame)
        dest_input_frame.pack(fill="x", pady=5)
        
        self.dest_entry = tk.Entry(dest_input_frame, font=("Arial", 10))
        self.dest_entry.pack(side="left", fill="x", expand=True)
        
        dest_btn = tk.Button(dest_input_frame, text="Обзор", command=self.browse_dest)
        dest_btn.pack(side="right", padx=(5, 0))
        
        # Фрейм для выбора устройства
        device_frame = tk.Frame(self.root)
        device_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(device_frame, text="Устройство:").pack(anchor="w")
        
        self.device_var = tk.StringVar(value="kozen 10")
        
        device_radio_frame = tk.Frame(device_frame)
        device_radio_frame.pack(fill="x", pady=5)
        
        tk.Radiobutton(device_radio_frame, text="Kozen 10", variable=self.device_var, 
                      value="kozen 10").pack(side="left")
        tk.Radiobutton(device_radio_frame, text="Kozen 12", variable=self.device_var, 
                      value="kozen 12").pack(side="left", padx=(20, 0))
        
        # Фрейм для выбора атаки
        attack_frame = tk.Frame(self.root)
        attack_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(attack_frame, text="Атака:").pack(anchor="w")
        
        self.attack_var = tk.IntVar(value=2)
        
        attack_combo = ttk.Combobox(attack_frame, textvariable=self.attack_var, 
                                   values=list(self.ranges.keys()), state="readonly")
        attack_combo.pack(fill="x", pady=5)
        
        # Информация о диапазоне
        self.range_info = tk.Label(self.root, text="", font=("Arial", 10), fg="blue")
        self.range_info.pack(pady=5)
        
        # Кнопка выполнения
        execute_btn = tk.Button(self.root, text="Выполнить переименование", 
                               command=self.execute_renaming, font=("Arial", 12, "bold"),
                               bg="#4CAF50", fg="white", padx=20, pady=10)
        execute_btn.pack(pady=20)
        
        # Область для логов
        log_frame = tk.Frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="Лог выполнения:").pack(anchor="w")
        
        self.log_text = tk.Text(log_frame, height=10, font=("Consolas", 9))
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязка событий для обновления информации
        attack_combo.bind("<<ComboboxSelected>>", self.update_range_info)
        self.device_var.trace("w", lambda *args: self.update_range_info())
        
        # Первоначальное обновление информации
        self.update_range_info()
    
    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)
    
    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, folder)
    
    def update_range_info(self, event=None):
        attack = self.attack_var.get()
        device = self.device_var.get()
        
        if attack in self.ranges and device in self.ranges[attack]:
            start, end = self.ranges[attack][device]
            self.range_info.config(text=f"Диапазон номеров: {start} - {end} (всего: {end - start + 1})")
        else:
            self.range_info.config(text="Выбранная комбинация атаки и устройства недоступна")
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def execute_renaming(self):
        source_folder = self.source_entry.get()
        dest_folder = self.dest_entry.get()
        device = self.device_var.get()
        attack = self.attack_var.get()
        
        # Проверка введенных данных
        if not source_folder or not dest_folder:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите исходную папку и папку назначения")
            return
        
        if not os.path.exists(source_folder):
            messagebox.showerror("Ошибка", "Исходная папка не существует")
            return
        
        # Проверка доступности комбинации атаки и устройства
        if attack not in self.ranges or device not in self.ranges[attack]:
            messagebox.showerror("Ошибка", f"Выбранная комбинация атаки {attack} и устройства {device} недоступна")
            return
        
        start_num, end_num = self.ranges[attack][device]
        
        try:
            # Создаем папку назначения если не существует
            os.makedirs(dest_folder, exist_ok=True)
            
            # Создаем подпапку для устройства
            device_folder = os.path.join(dest_folder, device)
            os.makedirs(device_folder, exist_ok=True)
            
            self.log("=" * 50)
            self.log(f"Начало обработки...")
            self.log(f"Источник: {source_folder}")
            self.log(f"Назначение: {device_folder}")
            self.log(f"Устройство: {device}")
            self.log(f"Атака: {attack}")
            self.log(f"Диапазон номеров: {start_num} - {end_num}")
            
            # Получаем список папок для обработки и сортируем по имени
            folders = [f for f in os.listdir(source_folder) 
                      if os.path.isdir(os.path.join(source_folder, f))]
            
            # Сортируем папки по имени (по возрастанию)
            folders.sort()
            
            if not folders:
                messagebox.showwarning("Предупреждение", "В исходной папке не найдено папок для обработки")
                return
            
            self.log(f"Найдено папок для обработки: {len(folders)}")
            self.log(f"Первые 3 папки после сортировки: {folders[:3]}")
            
            # Проверяем достаточно ли номеров в диапазоне
            available_numbers = end_num - start_num + 1
            if len(folders) > available_numbers:
                messagebox.showerror("Ошибка", 
                    f"Недостаточно номеров в диапазоне! "
                    f"Нужно: {len(folders)}, доступно: {available_numbers}")
                return
            
            # Обрабатываем папки
            current_number = start_num
            processed_count = 0
            skipped_count = 0
            
            for folder in folders:
                old_path = os.path.join(source_folder, folder)
                new_name = str(current_number)
                new_path = os.path.join(device_folder, new_name)
                
                # Проверяем, существует ли уже папка с таким номером
                if os.path.exists(new_path):
                    self.log(f"ПРОПУЩЕНО: {folder} -> {new_name} (папка уже существует)")
                    skipped_count += 1
                else:
                    # Копируем и переименовываем папку
                    shutil.copytree(old_path, new_path)
                    self.log(f"Переименовано: {folder} -> {new_name}")
                    processed_count += 1
                
                current_number += 1
            
            self.log("=" * 50)
            self.log(f"Обработка завершена!")
            self.log(f"Успешно обработано: {processed_count}")
            self.log(f"Пропущено (уже существуют): {skipped_count}")
            self.log(f"Всего: {processed_count + skipped_count}")
            
            messagebox.showinfo("Успех", 
                               f"Обработка завершена!\n"
                               f"Успешно обработано: {processed_count}\n"
                               f"Пропущено: {skipped_count}")
            
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

def main():
    root = tk.Tk()
    app = FolderRenamerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()