import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import datetime
import json
from pathlib import Path

class ModernFolderRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Folder Renamer - Kozen")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Загрузка конфигурации атак
        self.config_file = "attack_config.json"
        self.load_attack_config()
        
        # Стили
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Настройка цветовой схемы
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2c3e50',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#34495e',
            'light': '#ecf0f1',
            'text': '#2c3e50'
        }
        
        # Конфигурация стилей
        self.style.configure('TFrame', background=self.colors['secondary'])
        self.style.configure('TLabel', background=self.colors['secondary'], foreground=self.colors['light'])
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Primary.TButton', background=self.colors['primary'], foreground='white')
        self.style.configure('Success.TButton', background=self.colors['success'], foreground='white')
        self.style.configure('Warning.TButton', background=self.colors['warning'], foreground='white')
        self.style.configure('TRadiobutton', background=self.colors['secondary'], foreground=self.colors['light'])
        self.style.configure('TCheckbutton', background=self.colors['secondary'], foreground=self.colors['light'])
        
    def load_attack_config(self):
        """Загрузка конфигурации атак из JSON файла"""
        default_config = {
            "2": {"kozen 10": (91, 170), "kozen 12": (171, 250)},
            "3": {"kozen 10": (251, 346), "kozen 12": (347, 442)},
            "4": {"kozen 10": (443, 458), "kozen 12": (459, 474)},
            "5": {"kozen 10": (475, 514), "kozen 12": (515, 554)},
            "6": {"kozen 10": (555, 594)},
            "7": {"kozen 12": (595, 634)},
            "8": {"kozen 10": (635, 733)},
            "9": {"kozen 12": (734, 832)}
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.attack_ranges = json.load(f)
            else:
                self.attack_ranges = default_config
                self.save_attack_config()
        except:
            self.attack_ranges = default_config
            self.save_attack_config()
    
    def save_attack_config(self):
        """Сохранение конфигурации атак в JSON файл"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.attack_ranges, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log(f"Ошибка сохранения конфигурации: {str(e)}")
    
    def setup_ui(self):
        # Заголовок
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        title_label = tk.Label(header_frame, text="Modern Folder Renamer - Kozen", 
                              font=("Arial", 18, "bold"), 
                              bg=self.colors['secondary'], 
                              fg=self.colors['light'])
        title_label.pack()
        
        # Основной контейнер с вкладками
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Вкладка основного функционала
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="Основной функционал")
        
        # Вкладка замены папок
        replace_tab = ttk.Frame(notebook)
        notebook.add(replace_tab, text="Замена папок")
        
        # Вкладка настроек атак
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="Настройки атак")
        
        self.setup_main_tab(main_tab)
        self.setup_replace_tab(replace_tab)
        self.setup_settings_tab(settings_tab)
        
        # Область для логов
        self.setup_log_area()
    
    def setup_main_tab(self, parent):
        # Фрейм для выбора папок
        folder_frame = ttk.LabelFrame(parent, text="Выбор папок", padding=10)
        folder_frame.pack(fill="x", padx=10, pady=5)
        
        # Исходная папка
        ttk.Label(folder_frame, text="Исходная папка:").grid(row=0, column=0, sticky="w", pady=2)
        self.source_entry = ttk.Entry(folder_frame, font=("Arial", 10))
        self.source_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        ttk.Button(folder_frame, text="Обзор", command=self.browse_source).grid(row=0, column=2, padx=5)
        
        # Папка назначения
        ttk.Label(folder_frame, text="Папка назначения:").grid(row=1, column=0, sticky="w", pady=2)
        self.dest_entry = ttk.Entry(folder_frame, font=("Arial", 10))
        self.dest_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ttk.Button(folder_frame, text="Обзор", command=self.browse_dest).grid(row=1, column=2, padx=5)
        
        folder_frame.columnconfigure(1, weight=1)
        
        # Фрейм для настроек
        settings_frame = ttk.LabelFrame(parent, text="Настройки переименования", padding=10)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Устройство
        ttk.Label(settings_frame, text="Устройство:").grid(row=0, column=0, sticky="w", pady=5)
        self.device_var = tk.StringVar(value="kozen 10")
        device_frame = ttk.Frame(settings_frame)
        device_frame.grid(row=0, column=1, sticky="w", pady=5)
        ttk.Radiobutton(device_frame, text="Kozen 10", variable=self.device_var, 
                       value="kozen 10", command=self.update_range_info).pack(side="left")
        ttk.Radiobutton(device_frame, text="Kozen 12", variable=self.device_var, 
                       value="kozen 12", command=self.update_range_info).pack(side="left", padx=(20, 0))
        
        # Атака
        ttk.Label(settings_frame, text="Атака:").grid(row=1, column=0, sticky="w", pady=5)
        self.attack_var = tk.StringVar(value="2")
        self.attack_combo = ttk.Combobox(settings_frame, textvariable=self.attack_var, 
                                       values=list(self.attack_ranges.keys()), state="readonly")
        self.attack_combo.grid(row=1, column=1, sticky="w", pady=5)
        self.attack_combo.bind("<<ComboboxSelected>>", self.update_range_info)
        
        # Чекбокс проверки содержимого
        self.check_content_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Проверять содержимое папок", 
                       variable=self.check_content_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)
        
        # Информация о диапазоне
        self.range_info = tk.Label(settings_frame, text="", font=("Arial", 10, "bold"), 
                                  bg=self.colors['dark'], fg=self.colors['light'])
        self.range_info.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Кнопка выполнения
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Выполнить переименование", 
                  command=self.execute_renaming, style="Success.TButton").pack(pady=10)
        
        self.update_range_info()
    
    def setup_replace_tab(self, parent):
        # Фрейм для замены папок
        replace_frame = ttk.LabelFrame(parent, text="Замена отдельных папок", padding=10)
        replace_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(replace_frame, text="Номера папок для замены:").grid(row=0, column=0, sticky="w", pady=5)
        self.replace_entry = ttk.Entry(replace_frame, font=("Arial", 10))
        self.replace_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(replace_frame, text="Пример: 101,102,105-110,115").grid(row=1, column=1, sticky="w", pady=2)
        
        replace_frame.columnconfigure(1, weight=1)
        
        # Кнопка замены
        ttk.Button(parent, text="Выполнить замену", 
                  command=self.execute_replacement, style="Warning.TButton").pack(pady=10)
    
    def setup_settings_tab(self, parent):
        # Фрейм для редактирования атак
        edit_frame = ttk.LabelFrame(parent, text="Редактирование атак", padding=10)
        edit_frame.pack(fill="x", padx=10, pady=5)
        
        # Выбор атаки для редактирования
        ttk.Label(edit_frame, text="Атака:").grid(row=0, column=0, sticky="w", pady=5)
        self.edit_attack_var = tk.StringVar()
        self.edit_attack_combo = ttk.Combobox(edit_frame, textvariable=self.edit_attack_var, 
                                            values=list(self.attack_ranges.keys()), state="readonly")
        self.edit_attack_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.edit_attack_combo.bind("<<ComboboxSelected>>", self.load_attack_data)
        
        # Поля для диапазонов
        ttk.Label(edit_frame, text="Kozen 10 (начало-конец):").grid(row=1, column=0, sticky="w", pady=5)
        self.kozen10_entry = ttk.Entry(edit_frame, font=("Arial", 10))
        self.kozen10_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(edit_frame, text="Kozen 12 (начало-конец):").grid(row=2, column=0, sticky="w", pady=5)
        self.kozen12_entry = ttk.Entry(edit_frame, font=("Arial", 10))
        self.kozen12_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(edit_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Сохранить", 
                  command=self.save_attack_data, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Новая атака", 
                  command=self.new_attack, style="Primary.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Удалить атаку", 
                  command=self.delete_attack, style="Danger.TButton").pack(side="left", padx=5)
        
        edit_frame.columnconfigure(1, weight=1)
    
    def setup_log_area(self):
        log_frame = ttk.LabelFrame(self.root, text="Лог выполнения", padding=10)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=("Consolas", 9),
                                                 bg='#1a1a1a', fg='#00ff00', insertbackground='white')
        self.log_text.pack(fill="both", expand=True)
        
        # Кнопка очистки логов
        ttk.Button(log_frame, text="Очистить логи", 
                  command=self.clear_logs).pack(anchor="e", pady=5)
    
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
        
        if attack in self.attack_ranges and device in self.attack_ranges[attack]:
            start, end = self.attack_ranges[attack][device]
            total = end - start + 1
            self.range_info.config(text=f"Диапазон: {start}-{end} (всего: {total} номеров)")
        else:
            self.range_info.config(text="Выбранная комбинация недоступна")
    
    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "WARNING":
            formatted_message = f"[{timestamp}] ⚠️  {message}\n"
            self.log_text.insert(tk.END, formatted_message, "warning")
        elif level == "ERROR":
            formatted_message = f"[{timestamp}] ❌  {message}\n"
            self.log_text.insert(tk.END, formatted_message, "error")
        elif level == "SUCCESS":
            formatted_message = f"[{timestamp}] ✅  {message}\n"
            self.log_text.insert(tk.END, formatted_message, "success")
        else:
            formatted_message = f"[{timestamp}] ℹ️  {message}\n"
            self.log_text.insert(tk.END, formatted_message)
        
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
    
    def check_folder_content(self, folder_path):
        """Проверка содержимого папки"""
        try:
            items = os.listdir(folder_path)
            folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
            
            # Проверка количества папок
            if len(folders) != 3:
                self.log(f"ПРЕДУПРЕЖДЕНИЕ: В папке {os.path.basename(folder_path)} найдено {len(folders)} папок вместо 3!", "WARNING")
                return False
            
            # Проверка наличия BestShot файла
            bestshot_files = [f for f in files if "BestShot" in f]
            if not bestshot_files:
                self.log(f"ПРЕДУПРЕЖДЕНИЕ: В папке {os.path.basename(folder_path)} не найден файл BestShot!", "WARNING")
                return False
            
            # Проверка что папки не пустые
            for folder in folders:
                folder_full_path = os.path.join(folder_path, folder)
                if not os.listdir(folder_full_path):
                    self.log(f"ПРЕДУПРЕЖДЕНИЕ: Папка {folder} в {os.path.basename(folder_path)} пустая!", "WARNING")
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"Ошибка проверки папки {folder_path}: {str(e)}", "ERROR")
            return False
    
    def parse_number_range(self, range_str):
        """Парсинг диапазона номеров (например: '101,102,105-110,115')"""
        numbers = []
        parts = range_str.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                try:
                    numbers.extend(range(int(start), int(end) + 1))
                except ValueError:
                    return None
            else:
                try:
                    numbers.append(int(part))
                except ValueError:
                    return None
        
        return sorted(set(numbers))
    
    def execute_renaming(self):
        source_folder = self.source_entry.get()
        dest_folder = self.dest_entry.get()
        device = self.device_var.get()
        attack = self.attack_var.get()
        check_content = self.check_content_var.get()
        
        # Проверка введенных данных
        if not source_folder or not dest_folder:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите исходную папку и папку назначения")
            return
        
        if not os.path.exists(source_folder):
            messagebox.showerror("Ошибка", "Исходная папка не существует")
            return
        
        # Проверка доступности комбинации атаки и устройства
        if attack not in self.attack_ranges or device not in self.attack_ranges[attack]:
            messagebox.showerror("Ошибка", f"Выбранная комбинация атаки {attack} и устройства {device} недоступна")
            return
        
        start_num, end_num = self.attack_ranges[attack][device]
        
        try:
            # Создаем папку назначения если не существует
            os.makedirs(dest_folder, exist_ok=True)
            
            # Создаем подпапку для атаки и устройства
            attack_folder = os.path.join(dest_folder, f"attack_{attack}")
            device_folder = os.path.join(attack_folder, device)
            os.makedirs(device_folder, exist_ok=True)
            
            self.log("=" * 60, "SUCCESS")
            self.log(f"Начало обработки...", "SUCCESS")
            self.log(f"Источник: {source_folder}")
            self.log(f"Назначение: {device_folder}")
            self.log(f"Устройство: {device}")
            self.log(f"Атака: {attack}")
            self.log(f"Диапазон номеров: {start_num} - {end_num}")
            self.log(f"Проверка содержимого: {'ВКЛ' if check_content else 'ВЫКЛ'}")
            
            # Получаем список папок для обработки и сортируем по имени
            folders = [f for f in os.listdir(source_folder) 
                      if os.path.isdir(os.path.join(source_folder, f))]
            
            # Сортируем папки по имени (по возрастанию)
            folders.sort()
            
            if not folders:
                messagebox.showwarning("Предупреждение", "В исходной папке не найдено папок для обработки")
                return
            
            self.log(f"Найдено папок для обработки: {len(folders)}")
            
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
            content_warnings = 0
            
            for folder in folders:
                old_path = os.path.join(source_folder, folder)
                new_name = str(current_number)
                new_path = os.path.join(device_folder, new_name)
                
                # Проверка содержимого если включено
                if check_content:
                    if not self.check_folder_content(old_path):
                        content_warnings += 1
                
                # Удаляем существующую папку (перезапись)
                if os.path.exists(new_path):
                    shutil.rmtree(new_path)
                    self.log(f"Удалена существующая папка: {new_name}")
                
                # Копируем и переименовываем папку
                shutil.copytree(old_path, new_path)
                self.log(f"Переименовано: {folder} -> {new_name}", "SUCCESS")
                processed_count += 1
                
                current_number += 1
            
            self.log("=" * 60, "SUCCESS")
            self.log(f"Обработка завершена!", "SUCCESS")
            self.log(f"Успешно обработано: {processed_count}")
            self.log(f"Предупреждений по содержимому: {content_warnings}")
            
            if content_warnings > 0:
                self.log(f"ВНИМАНИЕ: Обнаружено {content_warnings} папок с проблемным содержимым!", "WARNING")
            
            messagebox.showinfo("Успех", 
                               f"Обработка завершена!\n"
                               f"Успешно обработано: {processed_count}\n"
                               f"Предупреждений: {content_warnings}")
            
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}", "ERROR")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def execute_replacement(self):
        source_folder = self.source_entry.get()
        dest_folder = self.dest_entry.get()
        device = self.device_var.get()
        attack = self.attack_var.get()
        replace_numbers_str = self.replace_entry.get()
        check_content = self.check_content_var.get()
        
        if not replace_numbers_str:
            messagebox.showerror("Ошибка", "Введите номера папок для замены")
            return
        
        # Парсим номера
        replace_numbers = self.parse_number_range(replace_numbers_str)
        if replace_numbers is None:
            messagebox.showerror("Ошибка", "Неверный формат номеров. Используйте: 101,102,105-110,115")
            return
        
        # Проверяем доступность диапазона
        if attack not in self.attack_ranges or device not in self.attack_ranges[attack]:
            messagebox.showerror("Ошибка", f"Выбранная комбинация атаки {attack} и устройства {device} недоступна")
            return
        
        start_num, end_num = self.attack_ranges[attack][device]
        
        # Проверяем что номера входят в диапазон
        for num in replace_numbers:
            if num < start_num or num > end_num:
                messagebox.showerror("Ошибка", f"Номер {num} вне диапазона {start_num}-{end_num}")
                return
        
        try:
            attack_folder = os.path.join(dest_folder, f"attack_{attack}")
            device_folder = os.path.join(attack_folder, device)
            
            if not os.path.exists(device_folder):
                messagebox.showerror("Ошибка", f"Папка назначения {device_folder} не существует")
                return
            
            # Получаем список папок для замены
            source_folders = [f for f in os.listdir(source_folder) 
                            if os.path.isdir(os.path.join(source_folder, f))]
            source_folders.sort()
            
            if len(source_folders) != len(replace_numbers):
                messagebox.showerror("Ошибка", 
                    f"Количество папок в исходной папке ({len(source_folders)}) "
                    f"не соответствует количеству номеров для замены ({len(replace_numbers)})")
                return
            
            self.log("=" * 60, "SUCCESS")
            self.log(f"Начало замены папок...", "SUCCESS")
            self.log(f"Заменяемые номера: {replace_numbers}")
            
            content_warnings = 0
            
            for i, folder in enumerate(source_folders):
                if i >= len(replace_numbers):
                    break
                    
                old_path = os.path.join(source_folder, folder)
                new_name = str(replace_numbers[i])
                new_path = os.path.join(device_folder, new_name)
                
                # Проверка содержимого если включено
                if check_content:
                    if not self.check_folder_content(old_path):
                        content_warnings += 1
                
                # Удаляем старую папку и копируем новую
                if os.path.exists(new_path):
                    shutil.rmtree(new_path)
                
                shutil.copytree(old_path, new_path)
                self.log(f"Заменена папка: {new_name} (из {folder})", "SUCCESS")
            
            self.log("=" * 60, "SUCCESS")
            self.log(f"Замена завершена!", "SUCCESS")
            self.log(f"Заменено папок: {len(replace_numbers)}")
            
            messagebox.showinfo("Успех", f"Замена завершена!\nЗаменено папок: {len(replace_numbers)}")
            
        except Exception as e:
            self.log(f"ОШИБКА при замене: {str(e)}", "ERROR")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def load_attack_data(self, event=None):
        """Загрузка данных выбранной атаки для редактирования"""
        attack = self.edit_attack_var.get()
        if attack in self.attack_ranges:
            ranges = self.attack_ranges[attack]
            
            kozen10 = ranges.get("kozen 10", (0, 0))
            kozen12 = ranges.get("kozen 12", (0, 0))
            
            self.kozen10_entry.delete(0, tk.END)
            self.kozen10_entry.insert(0, f"{kozen10[0]}-{kozen10[1]}" if kozen10 != (0,0) else "")
            
            self.kozen12_entry.delete(0, tk.END)
            self.kozen12_entry.insert(0, f"{kozen12[0]}-{kozen12[1]}" if kozen12 != (0,0) else "")
    
    def save_attack_data(self):
        """Сохранение изменений атаки"""
        attack = self.edit_attack_var.get()
        if not attack:
            messagebox.showerror("Ошибка", "Выберите атаку для редактирования")
            return
        
        try:
            # Парсим диапазоны
            kozen10_str = self.kozen10_entry.get().strip()
            kozen12_str = self.kozen12_entry.get().strip()
            
            new_ranges = {}
            
            if kozen10_str:
                start, end = map(int, kozen10_str.split('-'))
                new_ranges["kozen 10"] = (start, end)
            
            if kozen12_str:
                start, end = map(int, kozen12_str.split('-'))
                new_ranges["kozen 12"] = (start, end)
            
            if not new_ranges:
                messagebox.showerror("Ошибка", "Заполните хотя бы один диапазон")
                return
            
            self.attack_ranges[attack] = new_ranges
            self.save_attack_config()
            
            # Обновляем комбобоксы
            attacks = list(self.attack_ranges.keys())
            self.attack_combo['values'] = attacks
            self.edit_attack_combo['values'] = attacks
            
            self.log(f"Атака {attack} успешно сохранена", "SUCCESS")
            messagebox.showinfo("Успех", f"Атака {attack} успешно сохранена")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")
    
    def new_attack(self):
        """Создание новой атаки"""
        attack = tk.simpledialog.askstring("Новая атака", "Введите номер новой атаки:")
        if attack:
            if attack in self.attack_ranges:
                messagebox.showerror("Ошибка", "Атака с таким номером уже существует")
                return
            
            self.attack_ranges[attack] = {}
            self.save_attack_config()
            
            # Обновляем комбобоксы
            attacks = list(self.attack_ranges.keys())
            self.attack_combo['values'] = attacks
            self.edit_attack_combo['values'] = attacks
            
            self.edit_attack_var.set(attack)
            self.load_attack_data()
            
            self.log(f"Создана новая атака: {attack}", "SUCCESS")
    
    def delete_attack(self):
        """Удаление атаки"""
        attack = self.edit_attack_var.get()
        if not attack:
            messagebox.showerror("Ошибка", "Выберите атаку для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить атаку {attack}?"):
            del self.attack_ranges[attack]
            self.save_attack_config()
            
            # Обновляем комбобоксы
            attacks = list(self.attack_ranges.keys())
            self.attack_combo['values'] = attacks
            self.edit_attack_combo['values'] = attacks
            
            self.edit_attack_var.set("")
            self.kozen10_entry.delete(0, tk.END)
            self.kozen12_entry.delete(0, tk.END)
            
            self.log(f"Атака {attack} удалена", "SUCCESS")

def main():
    root = tk.Tk()
    
    # Настройка цветов для текста в логах
    root.option_add('*Text.warning.foreground', 'orange')
    root.option_add('*Text.error.foreground', 'red')
    root.option_add('*Text.success.foreground', 'green')
    
    app = ModernFolderRenamer(root)
    root.mainloop()

if __name__ == "__main__":
    import tkinter.simpledialog
    main()