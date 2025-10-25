import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import datetime
import json
import tkinter.simpledialog
import re
import sys
icon_path = os.path.join(os.path.dirname(sys.executable), 'logo.ico')
app.iconbitmap(icon_path)

class ModernFolderRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Manager - Kozen")
        self.root.geometry("900x800")
        self.root.configure(bg='#f8f9fa')
        
        # Центрирование окна
        self.center_window()
        
        # Загрузка конфигурации атак
        self.config_file = "attack_config.json"
        self.load_attack_config()
        
        # Стили
        self.setup_styles()
        self.setup_ui()
        
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Современная цветовая схема
        self.colors = {
            'primary': '#4f46e5',
            'primary_light': '#6366f1',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'background': '#f8f9fa',
            'surface': '#ffffff',
            'text_primary': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0'
        }
        
        # Конфигурация стилей с скруглёнными краями
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text_primary'])
        self.style.configure('TButton', font=('Segoe UI', 10), borderwidth=0, focuscolor='none')
        self.style.configure('Rounded.TButton', 
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(20, 10))
        self.style.map('Rounded.TButton',
                      background=[('active', self.colors['primary_light']),
                                ('pressed', self.colors['primary'])])
        
        self.style.configure('Secondary.TButton',
                           background=self.colors['surface'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           relief='solid')
        self.style.map('Secondary.TButton',
                      background=[('active', self.colors['border'])])

        self.style.configure('Success.TButton',
                           background=self.colors['success'],
                           foreground='white')
        self.style.map('Success.TButton',
                      background=[('active', '#34d399')])

        self.style.configure('Warning.TButton',
                           background=self.colors['warning'],
                           foreground='white')
        self.style.map('Warning.TButton',
                      background=[('active', '#fbbf24')])

        # Стили для фреймов с скруглёнными краями
        self.style.configure('Rounded.TFrame', 
                           background=self.colors['surface'],
                           relief='solid',
                           borderwidth=1)
        
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
                    # Конвертируем строки обратно в кортежи
                    for attack, devices in self.attack_ranges.items():
                        for device, range_tuple in devices.items():
                            if isinstance(range_tuple, list):
                                self.attack_ranges[attack][device] = tuple(range_tuple)
            else:
                self.attack_ranges = default_config
                self.save_attack_config()
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            self.attack_ranges = default_config
            self.save_attack_config()
    
    def save_attack_config(self):
        """Сохранение конфигурации атак в JSON файл"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.attack_ranges, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log(f"Ошибка сохранения конфигурации: {str(e)}")
    
    def create_rounded_frame(self, parent, **kwargs):
        """Создание фрейма с скруглёнными краями"""
        frame = tk.Frame(parent, 
                        bg=self.colors['surface'],
                        relief='solid',
                        bd=1,
                        **kwargs)
        return frame
    
    def setup_ui(self):
        # Заголовок
        header_frame = self.create_rounded_frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=15)
        
        title_label = tk.Label(header_frame, 
                              text="📁 Folder Manager - Kozen", 
                              font=("Segoe UI", 20, "bold"), 
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'],
                              pady=15)
        title_label.pack()
        
        # Основной контейнер с вкладками
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Вкладка основного функционала
        main_tab = self.create_rounded_frame(notebook)
        notebook.add(main_tab, text="🔄 Основные функции")
        
        # Вкладка настроек атак
        settings_tab = self.create_rounded_frame(notebook)
        notebook.add(settings_tab, text="⚙️ Настройки атак")
        
        self.setup_main_tab(main_tab)
        self.setup_settings_tab(settings_tab)
        
        # Область для логов
        self.setup_log_area()
    
    def setup_main_tab(self, parent):
        # Фрейм для выбора папок
        folder_frame = self.create_rounded_frame(parent)
        folder_frame.pack(fill="x", padx=15, pady=10)
        
        # Исходная папка
        tk.Label(folder_frame, text="📂 Исходная папка:", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)
        
        input_frame1 = tk.Frame(folder_frame, bg=self.colors['surface'])
        input_frame1.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        input_frame1.columnconfigure(0, weight=1)
        
        self.source_entry = ttk.Entry(input_frame1, font=("Segoe UI", 10))
        self.source_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(input_frame1, text="Обзор", 
                  command=self.browse_source, style="Secondary.TButton").grid(row=0, column=1)
        
        # Папка назначения
        tk.Label(folder_frame, text="📁 Папка назначения:", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['surface']).grid(row=2, column=0, sticky="w", pady=(10, 5), padx=15)
        
        input_frame2 = tk.Frame(folder_frame, bg=self.colors['surface'])
        input_frame2.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))
        input_frame2.columnconfigure(0, weight=1)
        
        self.dest_entry = ttk.Entry(input_frame2, font=("Segoe UI", 10))
        self.dest_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ttk.Button(input_frame2, text="Обзор", 
                  command=self.browse_dest, style="Secondary.TButton").grid(row=0, column=1)
        
        folder_frame.columnconfigure(0, weight=1)
        
        # Фрейм для настроек
        settings_frame = self.create_rounded_frame(parent)
        settings_frame.pack(fill="x", padx=15, pady=10)
        
        # Устройство
        tk.Label(settings_frame, text="📱 Устройство:", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w", pady=(15, 10), padx=15)
        
        self.device_var = tk.StringVar(value="kozen 10")
        device_frame = tk.Frame(settings_frame, bg=self.colors['surface'])
        device_frame.grid(row=0, column=1, sticky="w", pady=(15, 10), padx=15)
        
        ttk.Radiobutton(device_frame, text="Kozen 10", variable=self.device_var, 
                       value="kozen 10", command=self.update_range_info).pack(side="left", padx=(0, 20))
        ttk.Radiobutton(device_frame, text="Kozen 12", variable=self.device_var, 
                       value="kozen 12", command=self.update_range_info).pack(side="left")
        
        # Атака
        tk.Label(settings_frame, text="🎯 Тип атаки:", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['surface']).grid(row=1, column=0, sticky="w", pady=10, padx=15)
        
        self.attack_var = tk.StringVar(value="2")
        self.attack_combo = ttk.Combobox(settings_frame, textvariable=self.attack_var, 
                                       values=list(self.attack_ranges.keys()), 
                                       state="readonly", font=("Segoe UI", 10))
        self.attack_combo.grid(row=1, column=1, sticky="w", pady=10, padx=15)
        self.attack_combo.bind("<<ComboboxSelected>>", self.update_range_info)
        
        # Чекбокс проверки содержимого
        self.check_content_var = tk.BooleanVar(value=False)
        check_frame = tk.Frame(settings_frame, bg=self.colors['surface'])
        check_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=10, padx=15)
        
        ttk.Checkbutton(check_frame, text="🔍 Проверять содержимое папок (3 папки + BestShot файл)", 
                       variable=self.check_content_var).pack(side="left")
        
        # Информация о диапазоне
        self.range_info = tk.Label(settings_frame, text="", font=("Segoe UI", 10), 
                                  bg=self.colors['surface'], fg=self.colors['primary'],
                                  pady=10)
        self.range_info.grid(row=3, column=0, columnspan=2, sticky="w", padx=15)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Фрейм для замены папок
        replace_frame = self.create_rounded_frame(parent)
        replace_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(replace_frame, text="🔧 Замена отдельных папок", 
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(15, 10), padx=15)
        
        tk.Label(replace_frame, text="Номера папок для замены:", 
                font=("Segoe UI", 10),
                bg=self.colors['surface']).pack(anchor="w", padx=15)
        
        input_frame = tk.Frame(replace_frame, bg=self.colors['surface'])
        input_frame.pack(fill="x", padx=15, pady=10)
        input_frame.columnconfigure(0, weight=1)
        
        self.replace_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
        self.replace_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        tk.Label(replace_frame, text="Пример: 101,102,105-110,115", 
                font=("Segoe UI", 9),
                bg=self.colors['surface'],
                fg=self.colors['text_secondary']).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Кнопки выполнения
        button_frame = tk.Frame(parent, bg=self.colors['background'])
        button_frame.pack(fill="x", padx=15, pady=15)
        
        ttk.Button(button_frame, text="🚀 Выполнить переименование", 
                  command=self.execute_renaming, 
                  style="Rounded.TButton").pack(pady=5)
        
        ttk.Button(button_frame, text="🔄 Выполнить замену", 
                  command=self.execute_replacement, 
                  style="Warning.TButton").pack(pady=5)
        
        self.update_range_info()
    
    def setup_settings_tab(self, parent):
        # Фрейм для редактирования атак
        edit_frame = self.create_rounded_frame(parent)
        edit_frame.pack(fill="x", padx=15, pady=15)
        
        tk.Label(edit_frame, text="⚙️ Управление настройками атак", 
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(15, 20), padx=15)
        
        # Выбор атаки для редактирования
        input_frame1 = tk.Frame(edit_frame, bg=self.colors['surface'])
        input_frame1.pack(fill="x", padx=15, pady=10)
        
        tk.Label(input_frame1, text="Атака:", 
                font=("Segoe UI", 10),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w")
        
        self.edit_attack_var = tk.StringVar()
        self.edit_attack_combo = ttk.Combobox(input_frame1, textvariable=self.edit_attack_var, 
                                            values=list(self.attack_ranges.keys()), 
                                            state="readonly", font=("Segoe UI", 10))
        self.edit_attack_combo.grid(row=0, column=1, sticky="ew", padx=10)
        self.edit_attack_combo.bind("<<ComboboxSelected>>", self.load_attack_data)
        
        input_frame1.columnconfigure(1, weight=1)
        
        # Поля для диапазонов
        input_frame2 = tk.Frame(edit_frame, bg=self.colors['surface'])
        input_frame2.pack(fill="x", padx=15, pady=10)
        
        tk.Label(input_frame2, text="Kozen 10 (начало-конец):", 
                font=("Segoe UI", 10),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w", pady=5)
        
        self.kozen10_entry = ttk.Entry(input_frame2, font=("Segoe UI", 10))
        self.kozen10_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        tk.Label(input_frame2, text="Kozen 12 (начало-конец):", 
                font=("Segoe UI", 10),
                bg=self.colors['surface']).grid(row=1, column=0, sticky="w", pady=5)
        
        self.kozen12_entry = ttk.Entry(input_frame2, font=("Segoe UI", 10))
        self.kozen12_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        input_frame2.columnconfigure(1, weight=1)
        
        # Кнопки управления
        button_frame = tk.Frame(edit_frame, bg=self.colors['surface'])
        button_frame.pack(fill="x", padx=15, pady=20)
        
        ttk.Button(button_frame, text="💾 Сохранить", 
                  command=self.save_attack_data, style="Success.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="➕ Новая атака", 
                  command=self.new_attack, style="Rounded.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="✏️ Переименовать", 
                  command=self.rename_attack, style="Secondary.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="🗑️ Удалить атаку", 
                  command=self.delete_attack, style="Secondary.TButton").pack(side="left", padx=5)
    
    def setup_log_area(self):
        log_frame = self.create_rounded_frame(self.root)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(log_frame, text="📋 Лог выполнения", 
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(15, 10), padx=15)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=("Consolas", 9),
                                                 bg='#1e293b', fg='#e2e8f0', 
                                                 insertbackground='white',
                                                 relief='flat',
                                                 padx=10, pady=10)
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Настройка тегов для цветного текста
        self.log_text.tag_config("SUCCESS", foreground="#10b981")
        self.log_text.tag_config("WARNING", foreground="#f59e0b")
        self.log_text.tag_config("ERROR", foreground="#ef4444")
        self.log_text.tag_config("INFO", foreground="#e2e8f0")
        
        # Кнопка очистки логов
        btn_frame = tk.Frame(log_frame, bg=self.colors['surface'])
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ttk.Button(btn_frame, text="🧹 Очистить логи", 
                  command=self.clear_logs, style="Secondary.TButton").pack(side="right")
    
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
            self.range_info.config(text=f"📊 Диапазон: {start}-{end} (всего: {total} номеров)")
        else:
            self.range_info.config(text="❌ Выбранная комбинация недоступна")
    
    def log(self, message, level="INFO"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if level == "WARNING":
            icon = "⚠️"
            tag = "WARNING"
        elif level == "ERROR":
            icon = "❌"
            tag = "ERROR"
        elif level == "SUCCESS":
            icon = "✅"
            tag = "SUCCESS"
        else:
            icon = "ℹ️"
            tag = "INFO"
        
        formatted_message = f"[{timestamp}] {icon} {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, tag)
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Логи очищены", "INFO")
    
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
    
    def natural_sort_key(self, s):
        """Ключ для естественной сортировки как в проводнике Windows"""
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]
    
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
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"Начало обработки...", "SUCCESS")
            self.log(f"Источник: {source_folder}")
            self.log(f"Назначение: {device_folder}")
            self.log(f"Устройство: {device}")
            self.log(f"Атака: {attack}")
            self.log(f"Диапазон номеров: {start_num} - {end_num}")
            self.log(f"Проверка содержимого: {'ВКЛ' if check_content else 'ВЫКЛ'}")
            
            # Получаем список папок для обработки
            folders = [f for f in os.listdir(source_folder) 
                      if os.path.isdir(os.path.join(source_folder, f))]
            
            # Сортируем папки по имени с естественной сортировкой
            folders.sort(key=self.natural_sort_key)
            
            if not folders:
                messagebox.showwarning("Предупреждение", "В исходной папке не найдено папок для обработки")
                return
            
            self.log(f"Найдено папок для обработки: {len(folders)}")
            self.log(f"Первые 5 папок после сортировки: {folders[:5]}")
            
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
                    self.log(f"Удалена существующая папка: {new_name}", "WARNING")
                
                # Копируем и переименовываем папку
                shutil.copytree(old_path, new_path)
                self.log(f"Переименовано: {folder} -> {new_name}", "SUCCESS")
                processed_count += 1
                
                current_number += 1
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"Обработка завершена успешно!", "SUCCESS")
            self.log(f"Успешно обработано: {processed_count} папок")
            if content_warnings > 0:
                self.log(f"Обнаружено предупреждений по содержимому: {content_warnings}", "WARNING")
            
            messagebox.showinfo("Успех", 
                               f"Обработка завершена!\n\n"
                               f"✅ Успешно обработано: {processed_count} папок\n"
                               f"⚠️ Предупреждений: {content_warnings}")
            
        except Exception as e:
            self.log(f"Критическая ошибка: {str(e)}", "ERROR")
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
            
            # Сортируем папки по имени с естественной сортировкой
            source_folders.sort(key=self.natural_sort_key)
            
            if len(source_folders) != len(replace_numbers):
                messagebox.showerror("Ошибка", 
                    f"Количество папок в исходной папке ({len(source_folders)}) "
                    f"не соответствует количеству номеров для замены ({len(replace_numbers)})")
                return
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"Начало замены папок...", "SUCCESS")
            self.log(f"Заменяемые номера: {replace_numbers}")
            self.log(f"Найденные папки: {source_folders}")
            
            content_warnings = 0
            replaced_count = 0
            
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
                self.log(f"Заменена папка {replace_numbers[i]}: {folder} -> {new_name}", "SUCCESS")
                replaced_count += 1
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"Замена завершена успешно!", "SUCCESS")
            self.log(f"Заменено папок: {replaced_count}")
            
            messagebox.showinfo("Успех", f"Замена завершена!\n\n✅ Заменено папок: {replaced_count}")
            
        except Exception as e:
            self.log(f"Ошибка при замене: {str(e)}", "ERROR")
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
    
    def rename_attack(self):
        """Переименование существующей атаки"""
        old_attack = self.edit_attack_var.get()
        if not old_attack:
            messagebox.showerror("Ошибка", "Выберите атаку для переименования")
            return
        
        new_attack = tk.simpledialog.askstring("Переименование атаки", 
                                              f"Введите новое название для атаки {old_attack}:",
                                              initialvalue=old_attack)
        if new_attack:
            if new_attack in self.attack_ranges:
                messagebox.showerror("Ошибка", "Атака с таким названием уже существует")
                return
            
            # Сохраняем данные старой атаки
            attack_data = self.attack_ranges[old_attack]
            
            # Удаляем старую атаку и создаем новую
            del self.attack_ranges[old_attack]
            self.attack_ranges[new_attack] = attack_data
            self.save_attack_config()
            
            # Обновляем комбобоксы
            attacks = list(self.attack_ranges.keys())
            self.attack_combo['values'] = attacks
            self.edit_attack_combo['values'] = attacks
            
            # Устанавливаем новое значение
            self.attack_var.set(new_attack)
            self.edit_attack_var.set(new_attack)
            self.load_attack_data()
            
            self.log(f"Атака переименована: {old_attack} -> {new_attack}", "SUCCESS")
            messagebox.showinfo("Успех", f"Атака успешно переименована: {old_attack} -> {new_attack}")
    
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
            
            if attacks:
                self.edit_attack_var.set(attacks[0])
                self.load_attack_data()
            else:
                self.edit_attack_var.set("")
                self.kozen10_entry.delete(0, tk.END)
                self.kozen12_entry.delete(0, tk.END)
            
            self.log(f"Атака {attack} удалена", "SUCCESS")

def main():
    root = tk.Tk()
    app = ModernFolderRenamer(root)
    root.mainloop()

if __name__ == "__main__":
    main()