import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import datetime
import json
import tkinter.simpledialog
import re

class ModernFolderRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Manager - Kozen")
        self.root.geometry("1200x750")
        self.root.configure(bg='#f8f9fa')
        self.root.minsize(1000, 600)
        
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
        
        # Конфигурация стилей
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text_primary'])
        self.style.configure('TButton', font=('Segoe UI', 9), borderwidth=0, focuscolor='none')
        self.style.configure('Rounded.TButton', 
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(15, 8))
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

        self.style.configure('Rounded.TFrame', 
                           background=self.colors['surface'],
                           relief='solid',
                           borderwidth=1)
        
    def load_attack_config(self):
        """Загрузка конфигурации атак из JSON файла"""
        default_config = {
            "02 2D Mask": {"kozen 10": (91, 170), "kozen 12": (171, 250)},
            "03 2D Mask": {"kozen 10": (251, 346), "kozen 12": (347, 442)},
            "04 2D Mask": {"kozen 10": (443, 458), "kozen 12": (459, 474)},
            "05 2D Mask": {"kozen 10": (475, 514), "kozen 12": (515, 554)},
            "06 2D Mask": {"kozen 10": (555, 594)},
            "07 2D Mask": {"kozen 12": (595, 634)},
            "08 3D Mask": {"kozen 10": (635, 733)},
            "09 3D Mask": {"kozen 12": (734, 832)}
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.attack_ranges = json.load(f)
                    # Конвертируем списки обратно в кортежи
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
        header_frame.pack(fill="x", padx=15, pady=10)
        
        title_label = tk.Label(header_frame, 
                              text="📁 Folder Manager - Kozen", 
                              font=("Segoe UI", 18, "bold"),
                              bg=self.colors['surface'], 
                              fg=self.colors['text_primary'],
                              pady=12)
        title_label.pack()
        
        # Основной контейнер с вкладками
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=8)
        
        # Вкладка основного функционала
        main_tab = self.create_rounded_frame(notebook)
        notebook.add(main_tab, text="🔄 Основные функции")
        
        # Вкладка проверки
        check_tab = self.create_rounded_frame(notebook)
        notebook.add(check_tab, text="🔍 Проверка")
        
        # Вкладка настроек атак
        settings_tab = self.create_rounded_frame(notebook)
        notebook.add(settings_tab, text="⚙️ Настройки атак")
        
        self.setup_main_tab(main_tab)
        self.setup_check_tab(check_tab)
        self.setup_settings_tab(settings_tab)
    
    def setup_main_tab(self, parent):
        # Создаем разделяемый фрейм для левой (настройки) и правой (логи) части
        main_paned = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        main_paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Левая часть - настройки
        left_frame = self.create_rounded_frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Правая часть - логи
        right_frame = self.create_rounded_frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Настройка левой части - элементы управления
        # Фрейм для выбора папок
        folder_frame = self.create_rounded_frame(left_frame)
        folder_frame.pack(fill="x", padx=10, pady=8)
        
        # Исходная папка
        tk.Label(folder_frame, text="📂 Исходная папка:", 
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w", pady=(12, 4), padx=12)
        
        input_frame1 = tk.Frame(folder_frame, bg=self.colors['surface'])
        input_frame1.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        input_frame1.columnconfigure(0, weight=1)
        
        self.source_entry = ttk.Entry(input_frame1, font=("Segoe UI", 9))
        self.source_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        ttk.Button(input_frame1, text="Обзор", 
                  command=self.browse_source, style="Secondary.TButton").grid(row=0, column=1)
        
        # Папка назначения
        tk.Label(folder_frame, text="📁 Папка назначения:", 
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['surface']).grid(row=2, column=0, sticky="w", pady=(8, 4), padx=12)
        
        input_frame2 = tk.Frame(folder_frame, bg=self.colors['surface'])
        input_frame2.grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 12))
        input_frame2.columnconfigure(0, weight=1)
        
        self.dest_entry = ttk.Entry(input_frame2, font=("Segoe UI", 9))
        self.dest_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        ttk.Button(input_frame2, text="Обзор", 
                  command=self.browse_dest, style="Secondary.TButton").grid(row=0, column=1)
        
        folder_frame.columnconfigure(0, weight=1)
        
        # Фрейм для настроек
        settings_frame = self.create_rounded_frame(left_frame)
        settings_frame.pack(fill="x", padx=10, pady=8)
        
        # Устройство
        tk.Label(settings_frame, text="📱 Устройство:", 
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w", pady=(12, 8), padx=12)
        
        self.device_var = tk.StringVar(value="все")
        device_frame = tk.Frame(settings_frame, bg=self.colors['surface'])
        device_frame.grid(row=0, column=1, sticky="w", pady=(12, 8), padx=12)
        
        ttk.Radiobutton(device_frame, text="Все", variable=self.device_var, 
                       value="все", command=self.update_range_info).pack(side="left", padx=(0, 15))
        ttk.Radiobutton(device_frame, text="Kozen 10", variable=self.device_var, 
                       value="kozen 10", command=self.update_range_info).pack(side="left", padx=(0, 15))
        ttk.Radiobutton(device_frame, text="Kozen 12", variable=self.device_var, 
                       value="kozen 12", command=self.update_range_info).pack(side="left")
        
        # Атака
        tk.Label(settings_frame, text="🎯 Тип атаки:", 
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['surface']).grid(row=1, column=0, sticky="w", pady=8, padx=12)
        
        self.attack_var = tk.StringVar(value="02 2D Mask")
        self.attack_combo = ttk.Combobox(settings_frame, textvariable=self.attack_var, 
                                       values=list(self.attack_ranges.keys()), 
                                       state="readonly", font=("Segoe UI", 9))
        self.attack_combo.grid(row=1, column=1, sticky="w", pady=8, padx=12)
        self.attack_combo.bind("<<ComboboxSelected>>", self.update_range_info)
        
        # Чекбокс проверки содержимого
        self.check_content_var = tk.BooleanVar(value=False)
        check_frame = tk.Frame(settings_frame, bg=self.colors['surface'])
        check_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=8, padx=12)
        
        ttk.Checkbutton(check_frame, text="🔍 Проверять содержимое папок (3 папки + BestShot файл)", 
                       variable=self.check_content_var, style="TCheckbutton").pack(side="left")
        
        # Информация о диапазоне
        self.range_info = tk.Label(settings_frame, text="", font=("Segoe UI", 9),
                                  bg=self.colors['surface'], fg=self.colors['primary'],
                                  pady=8)
        self.range_info.grid(row=3, column=0, columnspan=2, sticky="w", padx=12)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Фрейм для замены папок
        replace_frame = self.create_rounded_frame(left_frame)
        replace_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Label(replace_frame, text="🔧 Замена отдельных папок", 
                font=("Segoe UI", 9, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(12, 8), padx=12)
        
        tk.Label(replace_frame, text="Номера папок для замены:", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).pack(anchor="w", padx=12)
        
        input_frame = tk.Frame(replace_frame, bg=self.colors['surface'])
        input_frame.pack(fill="x", padx=12, pady=8)
        input_frame.columnconfigure(0, weight=1)
        
        self.replace_entry = ttk.Entry(input_frame, font=("Segoe UI", 9))
        self.replace_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        
        tk.Label(replace_frame, text="Пример: 522, 530-532,528", 
                font=("Segoe UI", 8),
                bg=self.colors['surface'],
                fg=self.colors['text_secondary']).pack(anchor="w", padx=12, pady=(0, 12))
        
        # Кнопки выполнения - ВЕРТИКАЛЬНО для маленьких экранов
        button_frame = tk.Frame(left_frame, bg=self.colors['background'])
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Контейнер для кнопок - вертикальное расположение
        btn_container = tk.Frame(button_frame, bg=self.colors['background'])
        btn_container.pack(fill="x")
        
        # Кнопки одинакового размера, расположенные вертикально
        self.rename_btn = ttk.Button(btn_container, text="🚀 Выполнить переименование", 
                                   command=self.execute_renaming, 
                                   style="Rounded.TButton")
        self.rename_btn.pack(fill="x", pady=2)
        
        self.replace_btn = ttk.Button(btn_container, text="🔄 Выполнить замену", 
                                    command=self.execute_replacement, 
                                    style="Warning.TButton")
        self.replace_btn.pack(fill="x", pady=2)
        
        self.update_range_info()
        
        # Настройка правой части - логи
        log_header_frame = tk.Frame(right_frame, bg=self.colors['surface'])
        log_header_frame.pack(fill="x", padx=12, pady=(12, 8))
        
        tk.Label(log_header_frame, text="📋 Основные логи выполнения", 
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface']).pack(side="left")
        
        # Кнопка очистки логов в заголовке
        ttk.Button(log_header_frame, text="🧹 Очистить логи", 
                  command=self.clear_logs, style="Secondary.TButton").pack(side="right")
        
        # Фрейм для логов с прокруткой
        log_container = tk.Frame(right_frame, bg=self.colors['surface'])
        log_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.log_text = scrolledtext.ScrolledText(log_container, height=20, font=("Consolas", 8),
                                                 bg='#1e293b', fg='#e2e8f0', 
                                                 insertbackground='white',
                                                 relief='flat',
                                                 padx=8, pady=8)
        self.log_text.pack(fill="both", expand=True)
        
        # Настройка тегов для цветного текста
        self.log_text.tag_config("SUCCESS", foreground="#10b981")
        self.log_text.tag_config("WARNING", foreground="#f59e0b")
        self.log_text.tag_config("ERROR", foreground="#ef4444")
        self.log_text.tag_config("INFO", foreground="#e2e8f0")
        self.log_text.tag_config("CRITICAL", foreground="#ff0000", background="#330000")
        self.log_text.tag_config("HEADER", foreground="#93c5fd", font=("Consolas", 8, "bold"))
        self.log_text.tag_config("DETAIL", foreground="#94a3b8")
    
    def setup_check_tab(self, parent):
        paned_window = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Левая часть - элементы управления
        left_frame = self.create_rounded_frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # Правая часть - логи
        right_frame = self.create_rounded_frame(paned_window)
        paned_window.add(right_frame, weight=2)
        
        # Настройка левой части
        attack_check_frame = self.create_rounded_frame(left_frame)
        attack_check_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Label(attack_check_frame, text="🎯 Проверка атаки", 
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(12, 8), padx=12)
        
        input_frame1 = tk.Frame(attack_check_frame, bg=self.colors['surface'])
        input_frame1.pack(fill="x", padx=12, pady=8)
        
        tk.Label(input_frame1, text="Папка атаки:", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w")
        
        self.attack_check_entry = ttk.Entry(input_frame1, font=("Segoe UI", 9))
        self.attack_check_entry.grid(row=0, column=1, sticky="ew", padx=8)
        
        ttk.Button(input_frame1, text="Обзор", 
                  command=lambda: self.browse_folder(self.attack_check_entry),
                  style="Secondary.TButton").grid(row=0, column=2, padx=(5, 0))
        
        input_frame1.columnconfigure(1, weight=1)
        
        ttk.Button(attack_check_frame, text="🔍 Проверить атаку", 
                  command=self.check_attack, 
                  style="Rounded.TButton").pack(pady=8)
        
        # Фрейм для проверки ID
        id_check_frame = self.create_rounded_frame(left_frame)
        id_check_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Label(id_check_frame, text="🆔 Проверка ID", 
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(12, 8), padx=12)
        
        input_frame2 = tk.Frame(id_check_frame, bg=self.colors['surface'])
        input_frame2.pack(fill="x", padx=12, pady=8)
        
        tk.Label(input_frame2, text="Папка ID:", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w")
        
        self.id_check_entry = ttk.Entry(input_frame2, font=("Segoe UI", 9))
        self.id_check_entry.grid(row=0, column=1, sticky="ew", padx=8)
        
        ttk.Button(input_frame2, text="Обзор", 
                  command=lambda: self.browse_folder(self.id_check_entry),
                  style="Secondary.TButton").grid(row=0, column=2, padx=(5, 0))
        
        input_frame2.columnconfigure(1, weight=1)
        
        ttk.Button(id_check_frame, text="🔍 Проверить ID", 
                  command=self.check_id, 
                  style="Rounded.TButton").pack(pady=8)
        
        # Фрейм для общей проверки
        global_check_frame = self.create_rounded_frame(left_frame)
        global_check_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Label(global_check_frame, text="🌐 Общая проверка", 
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(12, 8), padx=12)
        
        input_frame3 = tk.Frame(global_check_frame, bg=self.colors['surface'])
        input_frame3.pack(fill="x", padx=12, pady=8)
        
        tk.Label(input_frame3, text="Общая папка проекта:", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w")
        
        self.global_check_entry = ttk.Entry(input_frame3, font=("Segoe UI", 9))
        self.global_check_entry.grid(row=0, column=1, sticky="ew", padx=8)
        
        ttk.Button(input_frame3, text="Обзор", 
                  command=lambda: self.browse_folder(self.global_check_entry),
                  style="Secondary.TButton").grid(row=0, column=2, padx=(5, 0))
        
        input_frame3.columnconfigure(1, weight=1)
        
        ttk.Button(global_check_frame, text="🔍 Выполнить общую проверку", 
                  command=self.check_global, 
                  style="Rounded.TButton").pack(pady=8)
        
        # Настройка правой части - логов проверки
        check_log_header = tk.Frame(right_frame, bg=self.colors['surface'])
        check_log_header.pack(fill="x", padx=12, pady=(12, 8))
        
        tk.Label(check_log_header, text="📋 Логи проверки", 
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface']).pack(side="left")
        
        # Кнопка очистки логов в заголовке
        ttk.Button(check_log_header, text="🧹 Очистить логи", 
                  command=self.clear_check_logs, style="Secondary.TButton").pack(side="right")
        
        # Контейнер для логов проверки
        check_log_container = tk.Frame(right_frame, bg=self.colors['surface'])
        check_log_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.check_log_text = scrolledtext.ScrolledText(check_log_container, height=20, font=("Consolas", 8),
                                                       bg='#1e293b', fg='#e2e8f0', 
                                                       insertbackground='white',
                                                       relief='flat',
                                                       padx=8, pady=8)
        self.check_log_text.pack(fill="both", expand=True)
        
        # Настройка тегов для цветного текста
        self.check_log_text.tag_config("SUCCESS", foreground="#10b981")
        self.check_log_text.tag_config("WARNING", foreground="#f59e0b")
        self.check_log_text.tag_config("ERROR", foreground="#ef4444")
        self.check_log_text.tag_config("INFO", foreground="#e2e8f0")
        self.check_log_text.tag_config("CRITICAL", foreground="#ff0000", background="#330000")
        self.check_log_text.tag_config("HEADER", foreground="#93c5fd", font=("Consolas", 8, "bold"))
        self.check_log_text.tag_config("SECTION", foreground="#cbd5e1", font=("Consolas", 8, "bold"))
        self.check_log_text.tag_config("DETAIL", foreground="#94a3b8")
    
    def setup_settings_tab(self, parent):
        edit_frame = self.create_rounded_frame(parent)
        edit_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(edit_frame, text="⚙️ Управление настройками атак", 
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['surface']).pack(anchor="w", pady=(12, 15), padx=12)
        
        input_frame1 = tk.Frame(edit_frame, bg=self.colors['surface'])
        input_frame1.pack(fill="x", padx=12, pady=8)
        
        tk.Label(input_frame1, text="Атака:", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w")
        
        self.edit_attack_var = tk.StringVar()
        self.edit_attack_combo = ttk.Combobox(input_frame1, textvariable=self.edit_attack_var, 
                                            values=list(self.attack_ranges.keys()), 
                                            state="readonly", font=("Segoe UI", 9))
        self.edit_attack_combo.grid(row=0, column=1, sticky="ew", padx=8)
        self.edit_attack_combo.bind("<<ComboboxSelected>>", self.load_attack_data)
        
        input_frame1.columnconfigure(1, weight=1)
        
        input_frame2 = tk.Frame(edit_frame, bg=self.colors['surface'])
        input_frame2.pack(fill="x", padx=12, pady=8)
        
        tk.Label(input_frame2, text="Kozen 10 (начало-конец):", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).grid(row=0, column=0, sticky="w", pady=4)
        
        self.kozen10_entry = ttk.Entry(input_frame2, font=("Segoe UI", 9))
        self.kozen10_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=4)
        
        tk.Label(input_frame2, text="Kozen 12 (начало-конец):", 
                font=("Segoe UI", 9),
                bg=self.colors['surface']).grid(row=1, column=0, sticky="w", pady=4)
        
        self.kozen12_entry = ttk.Entry(input_frame2, font=("Segoe UI", 9))
        self.kozen12_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=4)
        
        input_frame2.columnconfigure(1, weight=1)
        
        button_frame = tk.Frame(edit_frame, bg=self.colors['surface'])
        button_frame.pack(fill="x", padx=12, pady=15)
        
        # Кнопки в две строки для маленьких экранов
        top_button_frame = tk.Frame(button_frame, bg=self.colors['surface'])
        top_button_frame.pack(fill="x", pady=2)
        
        ttk.Button(top_button_frame, text="💾 Сохранить", 
                  command=self.save_attack_data, style="Success.TButton").pack(side="left", padx=2)
        ttk.Button(top_button_frame, text="➕ Новая атака", 
                  command=self.new_attack, style="Rounded.TButton").pack(side="left", padx=2)
        
        bottom_button_frame = tk.Frame(button_frame, bg=self.colors['surface'])
        bottom_button_frame.pack(fill="x", pady=2)
        
        ttk.Button(bottom_button_frame, text="✏️ Переименовать", 
                  command=self.rename_attack, style="Secondary.TButton").pack(side="left", padx=2)
        ttk.Button(bottom_button_frame, text="🗑️ Удалить атаку", 
                  command=self.delete_attack, style="Secondary.TButton").pack(side="left", padx=2)
    
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
    
    def browse_folder(self, entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)
    
    def update_range_info(self, event=None):
        attack = self.attack_var.get()
        device = self.device_var.get()
        
        if device == "все":
            min_num = None
            max_num = None
            for device_name in ["kozen 10", "kozen 12"]:
                if attack in self.attack_ranges and device_name in self.attack_ranges[attack]:
                    start, end = self.attack_ranges[attack][device_name]
                    if min_num is None or start < min_num:
                        min_num = start
                    if max_num is None or end > max_num:
                        max_num = end
            
            if min_num is not None and max_num is not None:
                total = max_num - min_num + 1
                self.range_info.config(text=f"📊 Общий диапазон: {min_num}-{max_num} (всего: {total} номеров)")
            else:
                self.range_info.config(text="❌ Нет данных о диапазонах")
        elif attack in self.attack_ranges and device in self.attack_ranges[attack]:
            start, end = self.attack_ranges[attack][device]
            total = end - start + 1
            self.range_info.config(text=f"📊 Диапазон: {start}-{end} (всего: {total} номеров)")
        else:
            self.range_info.config(text="❌ Выбранная комбинация недоступна")
    
    def get_image_date(self, image_path):
        """Получает дату съёмки из EXIF данных изображения (упрощенная версия без Pillow)"""
        try:
            # Вместо использования Pillow, используем дату изменения файла
            # Это не идеально, но работает без внешних зависимостей
            timestamp = os.path.getmtime(image_path)
            return datetime.datetime.fromtimestamp(timestamp)
        except Exception:
            return None
    
    def find_image_files(self, folder_path):
        """Находит все файлы изображений в папке"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif'}
        image_files = []
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in image_extensions):
                        image_files.append(os.path.join(root, file))
        except Exception:
            pass
        
        return image_files
    
    def get_folder_shooting_time(self, folder_path):
        """Получает время съёмки для папки на основе изображений"""
        # Сначала ищем BestShot
        bestshot_files = []
        try:
            for file in os.listdir(folder_path):
                if "bestshot" in file.lower() and any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                    bestshot_files.append(os.path.join(folder_path, file))
        except Exception:
            pass
        
        if bestshot_files:
            date = self.get_image_date(bestshot_files[0])
            if date:
                return date
        
        # Если BestShot не найден, ищем в папках Captures и Focus
        subfolders_to_check = ['Captures', 'Focus']
        
        for subfolder in subfolders_to_check:
            subfolder_path = os.path.join(folder_path, subfolder)
            if os.path.exists(subfolder_path):
                image_files = self.find_image_files(subfolder_path)
                if image_files:
                    date = self.get_image_date(image_files[0])
                    if date:
                        return date
        
        # Если ничего не найдено, ищем любые изображения в папке
        image_files = self.find_image_files(folder_path)
        if image_files:
            date = self.get_image_date(image_files[0])
            if date:
                return date
        
        return None
    
    def calculate_shooting_time(self, folders, source_folder):
        """Вычисляет время съёмки на основе дат съёмки изображений"""
        if not folders:
            return "не удалось вычислить"
        
        try:
            # Получаем времена съёмки всех папок
            shooting_times = []
            for folder in folders:
                folder_path = os.path.join(source_folder, folder)
                shooting_time = self.get_folder_shooting_time(folder_path)
                if shooting_time:
                    shooting_times.append((folder, shooting_time))
            
            if not shooting_times:
                return "не удалось вычислить"
            
            # Сортируем по времени съёмки
            shooting_times.sort(key=lambda x: x[1])
            
            # Группируем папки по дням
            days_dict = {}
            for folder_name, timestamp in shooting_times:
                date_key = timestamp.date()
                
                if date_key not in days_dict:
                    days_dict[date_key] = []
                
                days_dict[date_key].append((folder_name, timestamp))
            
            # Вычисляем общее время съёмки
            total_seconds = 0
            
            for date_key, day_folders in days_dict.items():
                if len(day_folders) > 1:
                    # Время съёмки за день = разница между последней и первой папкой
                    first_folder_time = day_folders[0][1].timestamp()
                    last_folder_time = day_folders[-1][1].timestamp()
                    day_duration = last_folder_time - first_folder_time
                    total_seconds += day_duration
                    
                    # Логируем информацию о дне
                    first_dt = day_folders[0][1]
                    last_dt = day_folders[-1][1]
                    self.log(f"📅 День {date_key}: {first_dt.strftime('%H:%M:%S')} - {last_dt.strftime('%H:%M:%S')} "
                           f"({len(day_folders)} папок, время: {self.format_duration(day_duration)})", "DETAIL")
                elif len(day_folders) == 1:
                    # Если папка одна в день - время съёмки 0
                    self.log(f"📅 День {date_key}: 1 папка, время съёмки: 00:00:00", "DETAIL")
            
            if total_seconds == 0:
                return "00:00:00"
            
            return self.format_duration(total_seconds)
            
        except Exception as e:
            self.log(f"Ошибка вычисления времени съёмки: {str(e)}", "WARNING")
            return "не удалось вычислить"
    
    def format_duration(self, total_seconds):
        """Форматирует длительность в формат HH:MM:SS"""
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def parse_number_range(self, range_str):
        """Парсинг диапазона номеров с сохранением порядка ввода"""
        numbers = []
        parts = [part.strip() for part in range_str.split(',')]
        
        for part in parts:
            if not part:
                continue
                
            if '-' in part:
                range_parts = part.split('-')
                if len(range_parts) != 2:
                    return None
                
                try:
                    start = int(range_parts[0].strip())
                    end = int(range_parts[1].strip())
                    
                    if start <= end:
                        numbers.extend(range(start, end + 1))
                    else:
                        numbers.extend(range(start, end - 1, -1))
                except ValueError:
                    return None
            else:
                try:
                    numbers.append(int(part))
                except ValueError:
                    return None
        
        return numbers
    
    def natural_sort_key(self, s):
        """Ключ для естественной сортировки как в проводнике Windows"""
        return [int(text) if text.isdigit() else text.lower()
                for text in re.split('([0-9]+)', s)]
    
    def get_attack_expected_count(self, attack_name, device):
        """Получает ожидаемое количество папок для атаки и устройства"""
        if attack_name not in self.attack_ranges:
            return 0
        
        if device == "все":
            min_num = None
            max_num = None
            for device_name in ["kozen 10", "kozen 12"]:
                if device_name in self.attack_ranges[attack_name]:
                    start, end = self.attack_ranges[attack_name][device_name]
                    if min_num is None or start < min_num:
                        min_num = start
                    if max_num is None or end > max_num:
                        max_num = end
            
            if min_num is not None and max_num is not None:
                return max_num - min_num + 1
            return 0
        else:
            if device in self.attack_ranges[attack_name]:
                start, end = self.attack_ranges[attack_name][device]
                return end - start + 1
            return 0

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
        elif level == "CRITICAL":
            icon = "🚫"
            tag = "CRITICAL"
        elif level == "HEADER":
            icon = "📋"
            tag = "HEADER"
        elif level == "DETAIL":
            icon = "  📄"
            tag = "DETAIL"
        else:
            icon = "ℹ️"
            tag = "INFO"
        
        formatted_message = f"[{timestamp}] {icon} {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, tag)
        self.log_text.see(tk.END)
        self.root.update()
    
    def check_log(self, message, level="INFO", indent=0):
        """Логирование для вкладки проверки с поддержкой отступов"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if level == "WARNING":
            icon = "⚠️"
            tag = "WARNING"
        elif level == "ERROR":
            icon = "❌"
            tag = "ERROR"
        elif level == "SUCCESS":
            icon = "✅"
            tag = "SUCCESS"
        elif level == "CRITICAL":
            icon = "🚫"
            tag = "CRITICAL"
        elif level == "HEADER":
            icon = "📋"
            tag = "HEADER"
        elif level == "SECTION":
            icon = "  📁"
            tag = "SECTION"
        elif level == "DETAIL":
            icon = "    📄"
            tag = "DETAIL"
        else:
            icon = "ℹ️"
            tag = "INFO"
        
        indent_str = "  " * indent
        formatted_message = f"{indent_str}{icon} {message}\n"
        
        self.check_log_text.insert(tk.END, formatted_message, tag)
        self.check_log_text.see(tk.END)
        self.root.update()
    
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Логи очищены", "INFO")
    
    def clear_check_logs(self):
        self.check_log_text.delete(1.0, tk.END)
        self.check_log("Логи проверки очищены", "INFO")
    
    def check_folder_content(self, folder_path, log_errors=True, indent=0, check_names=False):
        """
        Проверка содержимого папки
        check_names: если True, проверяет что имена папок числовые (для проверки атак)
        """
        try:
            items = os.listdir(folder_path)
            folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]
            files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
            
            errors = []
            warnings = []
            
            # Проверка количества папок
            if len(folders) != 3:
                errors.append(f"Найдено {len(folders)} папок вместо 3")
            
            # Проверка наличия BestShot файла
            bestshot_files = [f for f in files if "BestShot" in f]
            if not bestshot_files:
                errors.append("Не найден файл BestShot")
            elif len(bestshot_files) > 1:
                warnings.append(f"Найдено {len(bestshot_files)} файлов BestShot")
            
            # Проверка что папки не пустые
            for folder in folders:
                folder_full_path = os.path.join(folder_path, folder)
                if not os.listdir(folder_full_path):
                    errors.append(f"Папка '{folder}' пустая")
            
            # Проверка числовых имен (только при check_names=True)
            if check_names:
                non_numeric = [f for f in folders if not f.isdigit()]
                if non_numeric:
                    errors.append(f"Нечисловые имена папок: {', '.join(non_numeric)}")
            
            if log_errors:
                if errors:
                    for error in errors:
                        self.check_log(f"Ошибка: {error}", "ERROR", indent)
                if warnings:
                    for warning in warnings:
                        self.check_log(f"Предупреждение: {warning}", "WARNING", indent)
                if not errors and not warnings:
                    self.check_log("Содержимое папки в порядке", "SUCCESS", indent)
            
            return len(errors) == 0
            
        except Exception as e:
            if log_errors:
                error_msg = f"Ошибка проверки папки: {str(e)}"
                self.check_log(error_msg, "ERROR", indent)
            return False
    
    def execute_renaming(self):
        source_folder = self.source_entry.get()
        dest_folder = self.dest_entry.get()
        device = self.device_var.get()
        attack = self.attack_var.get()
        check_content = self.check_content_var.get()
        
        if not source_folder or not dest_folder:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите исходную папку и папку назначения")
            return
        
        if not os.path.exists(source_folder):
            messagebox.showerror("Ошибка", "Исходная папка не существует")
            return
        
        folders = [f for f in os.listdir(source_folder) 
                  if os.path.isdir(os.path.join(source_folder, f))]
        
        folders.sort(key=self.natural_sort_key)
        
        if not folders:
            messagebox.showwarning("Предупреждение", "В исходной папке не найдено папок для обработки")
            return
        
        shooting_time = self.calculate_shooting_time(folders, source_folder)
        
        if device != "все" and (attack not in self.attack_ranges or device not in self.attack_ranges[attack]):
            messagebox.showerror("Ошибка", f"Выбранная комбинация атаки {attack} и устройства {device} недоступна")
            return
        
        # ПРОВЕРКА КОЛИЧЕСТВА ПАПОК
        expected_count = self.get_attack_expected_count(attack, device)
        if expected_count > 0 and len(folders) < expected_count:
            response = messagebox.askyesno(
                "Предупреждение", 
                f"Количество папок в исходной папке ({len(folders)}) меньше, чем требуется для атаки ({expected_count}).\n\n"
                f"Продолжить выполнение?"
            )
            if not response:
                return
        
        try:
            os.makedirs(dest_folder, exist_ok=True)
            attack_folder = os.path.join(dest_folder, attack)
            os.makedirs(attack_folder, exist_ok=True)
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"🚀 Начало обработки...", "HEADER")
            self.log(f"📊 Найдено папок для обработки: {len(folders)}", "INFO")
            if expected_count > 0:
                self.log(f"📋 Ожидаемое количество для атаки: {expected_count}", "INFO")
            
            # ПРЕДВАРИТЕЛЬНАЯ ПРОВЕРКА СОДЕРЖИМОГО
            if check_content:
                self.log("🔍 Начинается предварительная проверка содержимого...", "INFO")
                content_errors = False
                error_details = []
                
                for folder in folders:
                    old_path = os.path.join(source_folder, folder)
                    # check_names=False - не проверяем числовые имена при выгрузке, проверяем только структуру
                    if not self.check_folder_content(old_path, log_errors=False, check_names=False):
                        content_errors = True
                        error_details.append(folder)
                
                if content_errors:
                    self.log("🚫 ОБНАРУЖЕНЫ ОШИБКИ! Переименование отменено.", "ERROR")
                    self.log(f"📂 Папки с ошибками: {', '.join(error_details)}", "ERROR")
                    messagebox.showerror("Ошибка", 
                                        "Обнаружены ошибки в содержимом папок! "
                                        "Переименование отменено. Проверьте логи для деталей.")
                    return
            
            processed_count = 0
            
            if device == "все":
                min_num = None
                max_num = None
                
                for device_name in ["kozen 10", "kozen 12"]:
                    if attack in self.attack_ranges and device_name in self.attack_ranges[attack]:
                        start_num, end_num = self.attack_ranges[attack][device_name]
                        if min_num is None or start_num < min_num:
                            min_num = start_num
                        if max_num is None or end_num > max_num:
                            max_num = end_num
                
                if min_num is None or max_num is None:
                    messagebox.showerror("Ошибка", f"Для атаки {attack} не заданы диапазоны")
                    return
                
                available_numbers = max_num - min_num + 1
                
                if len(folders) > available_numbers:
                    messagebox.showerror("Ошибка", 
                        f"Недостаточно номеров в диапазоне! "
                        f"Нужно: {len(folders)}, доступно: {available_numbers}")
                    return
                
                current_number = min_num
                
                for folder in folders:
                    old_path = os.path.join(source_folder, folder)
                    new_name = str(current_number)
                    new_path = os.path.join(attack_folder, new_name)
                    
                    if os.path.exists(new_path):
                        shutil.rmtree(new_path)
                        self.log(f"Удалена существующая папка: {new_name}", "WARNING")
                    
                    shutil.copytree(old_path, new_path)
                    self.log(f"Обработано: {folder} → {new_name}", "SUCCESS")
                    processed_count += 1
                    current_number += 1
            else:
                device_folder = os.path.join(attack_folder, device)
                os.makedirs(device_folder, exist_ok=True)
                
                start_num, end_num = self.attack_ranges[attack][device]
                available_numbers = end_num - start_num + 1
                
                if len(folders) > available_numbers:
                    messagebox.showerror("Ошибка", 
                        f"Недостаточно номеров в диапазоне! "
                        f"Нужно: {len(folders)}, доступно: {available_numbers}")
                    return
                
                current_number = start_num
                
                for folder in folders:
                    old_path = os.path.join(source_folder, folder)
                    new_name = str(current_number)
                    new_path = os.path.join(device_folder, new_name)
                    
                    if os.path.exists(new_path):
                        shutil.rmtree(new_path)
                        self.log(f"Удалена существующая папка: {new_name}", "WARNING")
                    
                    shutil.copytree(old_path, new_path)
                    self.log(f"Обработано: {folder} → {new_name}", "SUCCESS")
                    processed_count += 1
                    current_number += 1
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"✅ Обработка завершена успешно! Обработано: {processed_count} папок", "SUCCESS")
            self.log(f"⏱️ Общее время съёмки: {shooting_time}", "INFO")
            
            messagebox.showinfo("Успех", 
                               f"Обработка завершена!\n\n"
                               f"✅ Успешно обработано: {processed_count} папок\n"
                               f"⏱️ Время съёмки: {shooting_time}")
            
        except Exception as e:
            self.log(f"Ошибка: {str(e)}", "ERROR")
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
        
        replace_numbers = self.parse_number_range(replace_numbers_str)
        if replace_numbers is None:
            messagebox.showerror("Ошибка", "Неверный формат номеров. Используйте: 522,530-532,528")
            return
        
        source_folders = [f for f in os.listdir(source_folder) 
                        if os.path.isdir(os.path.join(source_folder, f))]
        
        source_folders.sort(key=self.natural_sort_key)
        
        if len(source_folders) != len(replace_numbers):
            messagebox.showerror("Ошибка", 
                f"Количество папок в исходной папке ({len(source_folders)}) "
                f"не соответствует количеству номеров для замены ({len(replace_numbers)})")
            return
        
        shooting_time = self.calculate_shooting_time(source_folders, source_folder)
        
        if device != "все" and (attack not in self.attack_ranges or device not in self.attack_ranges[attack]):
            messagebox.showerror("Ошибка", f"Выбранная комбинация атаки {attack} и устройства {device} недоступна")
            return
        
        try:
            attack_folder = os.path.join(dest_folder, attack)
            
            if device == "все":
                min_num = None
                max_num = None
                
                for device_name in ["kozen 10", "kozen 12"]:
                    if attack in self.attack_ranges and device_name in self.attack_ranges[attack]:
                        start_num, end_num = self.attack_ranges[attack][device_name]
                        if min_num is None or start_num < min_num:
                            min_num = start_num
                        if max_num is None or end_num > max_num:
                            max_num = end_num
                
                if min_num is None or max_num is None:
                    messagebox.showerror("Ошибка", f"Для атаки {attack} не заданы диапазоны")
                    return
                
                for num in replace_numbers:
                    if num < min_num or num > max_num:
                        messagebox.showerror("Ошибка", f"Номер {num} вне общего диапазона {min_num}-{max_num}")
                        return
            else:
                start_num, end_num = self.attack_ranges[attack][device]
                for num in replace_numbers:
                    if num < start_num or num > end_num:
                        messagebox.showerror("Ошибка", f"Номер {num} вне диапазона {start_num}-{end_num}")
                        return
            
            if not os.path.exists(attack_folder):
                messagebox.showerror("Ошибка", f"Папка назначения {attack_folder} не существует")
                return
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"🔄 Начало замены папок...", "HEADER")
            self.log(f"🔢 Заменяемые номера: {replace_numbers}", "INFO")
            
            # ПРЕДВАРИТЕЛЬНАЯ ПРОВЕРКА СОДЕРЖИМОГО
            if check_content:
                self.log("🔍 Начинается предварительная проверка содержимого...", "INFO")
                content_errors = False
                error_details = []
                
                for folder in source_folders:
                    old_path = os.path.join(source_folder, folder)
                    # check_names=False - не проверяем числовые имена при замене, проверяем только структуру
                    if not self.check_folder_content(old_path, log_errors=False, check_names=False):
                        content_errors = True
                        error_details.append(folder)
                
                if content_errors:
                    self.log("🚫 ОБНАРУЖЕНЫ ОШИБКИ! Замена отменена.", "ERROR")
                    self.log(f"📂 Папки с ошибками: {', '.join(error_details)}", "ERROR")
                    messagebox.showerror("Ошибка", 
                                        "Обнаружены ошибки в содержимом папок! "
                                        "Замена отменена. Проверьте логи для деталей.")
                    return
            
            replaced_count = 0
            
            if device == "все":
                for i, folder in enumerate(source_folders):
                    old_path = os.path.join(source_folder, folder)
                    target_number = replace_numbers[i]
                    new_name = str(target_number)
                    new_path = os.path.join(attack_folder, new_name)
                    
                    if os.path.exists(new_path):
                        shutil.rmtree(new_path)
                    
                    shutil.copytree(old_path, new_path)
                    self.log(f"Заменено: {folder} → {new_name}", "SUCCESS")
                    replaced_count += 1
            else:
                device_folder = os.path.join(attack_folder, device)
                
                for i, folder in enumerate(source_folders):
                    old_path = os.path.join(source_folder, folder)
                    target_number = replace_numbers[i]
                    new_name = str(target_number)
                    new_path = os.path.join(device_folder, new_name)
                    
                    if os.path.exists(new_path):
                        shutil.rmtree(new_path)
                    
                    shutil.copytree(old_path, new_path)
                    self.log(f"Заменено: {folder} → {new_name}", "SUCCESS")
                    replaced_count += 1
            
            self.log("=" * 70, "SUCCESS")
            self.log(f"✅ Замена завершена успешно! Заменено: {replaced_count} папок", "SUCCESS")
            self.log(f"⏱️ Общее время съёмки: {shooting_time}", "INFO")
            
            messagebox.showinfo("Успех", 
                               f"Замена завершена!\n\n"
                               f"✅ Заменено папок: {replaced_count}\n"
                               f"⏱️ Время съёмки: {shooting_time}")
            
        except Exception as e:
            self.log(f"Ошибка при замене: {str(e)}", "ERROR")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def check_attack(self):
        """Проверка отдельной атаки"""
        attack_folder = self.attack_check_entry.get()
        
        if not attack_folder:
            messagebox.showerror("Ошибка", "Выберите папку атаки")
            return
        
        if not os.path.exists(attack_folder):
            messagebox.showerror("Ошибка", "Папка атаки не существует")
            return
        
        self.check_log("=" * 60, "HEADER")
        self.check_log(f"🔍 ПРОВЕРКА АТАКИ: {os.path.basename(attack_folder)}", "HEADER")
        self.check_log("=" * 60, "HEADER")
        
        try:
            attack_name = os.path.basename(attack_folder)
            
            if attack_name not in self.attack_ranges:
                self.check_log(f"❌ ОШИБКА: Папка не является известной атакой", "ERROR")
                self.check_log(f"📝 Название папки: {attack_name}", "INFO")
                self.check_log(f"📋 Доступные атаки: {', '.join(self.attack_ranges.keys())}", "INFO")
                return
            
            attack_type = attack_name
            structure_info = self.check_attack_structure(attack_folder, attack_type)
            
            self.check_log(f"📁 Структура: {structure_info['structure_type']}", "INFO")
            self.check_log(f"📊 Ожидаемое количество папок: {structure_info['expected_total']}", "INFO")
            
            total_errors = 0
            total_folders = 0
            total_checked = 0
            
            if structure_info['has_kozen10'] or structure_info['has_kozen12']:
                for device in ["kozen 10", "kozen 12"]:
                    if structure_info[f'has_{device.replace(" ", "")}']:
                        device_folder = os.path.join(attack_folder, device)
                        
                        self.check_log(f"", "INFO")
                        self.check_log(f"📱 Устройство: {device}", "SECTION")
                        
                        expected_count = 0
                        if attack_type in self.attack_ranges and device in self.attack_ranges[attack_type]:
                            start, end = self.attack_ranges[attack_type][device]
                            expected_count = end - start + 1
                        
                        try:
                            all_items = os.listdir(device_folder)
                            # ПРИ ПРОВЕРКЕ АТАКИ проверяем числовые имена только для папок атак
                            folders = [f for f in all_items 
                                      if os.path.isdir(os.path.join(device_folder, f)) and f.isdigit()]
                            
                            other_items = [item for item in all_items if item not in folders]
                            if other_items:
                                self.check_log(f"⚠️ Посторонние элементы: {', '.join(other_items)}", "WARNING", 1)
                            
                            actual_count = len(folders)
                            
                            self.check_log(f"📈 Ожидалось: {expected_count}", "INFO", 1)
                            self.check_log(f"📈 Найдено: {actual_count}", 
                                         "SUCCESS" if expected_count == actual_count else "ERROR", 1)
                            
                            if expected_count > 0 and actual_count != expected_count:
                                self.check_log(f"❌ НЕСООТВЕТСТВИЕ КОЛИЧЕСТВА!", "ERROR", 1)
                                total_errors += 1
                            
                            # ПРОВЕРКА СОДЕРЖИМОГО КАЖДОЙ ПАПКИ
                            self.check_log(f"🔍 Проверка содержимого папок:", "SECTION", 1)
                            folder_errors = 0
                            for folder in folders:
                                folder_path = os.path.join(device_folder, folder)
                                self.check_log(f"📂 Папка {folder}:", "DETAIL", 2)
                                # check_names=False - внутренние папки могут называться как угодно
                                if not self.check_folder_content(folder_path, log_errors=True, indent=3, check_names=False):
                                    folder_errors += 1
                                total_checked += 1
                            
                            total_errors += folder_errors
                            total_folders += actual_count
                            
                            if folder_errors == 0:
                                self.check_log(f"✅ Все папки устройства проверены успешно", "SUCCESS", 1)
                            else:
                                self.check_log(f"❌ Ошибок в папках: {folder_errors}", "ERROR", 1)
                        except Exception as e:
                            self.check_log(f"❌ Ошибка доступа к папке устройства: {str(e)}", "ERROR", 1)
                            total_errors += 1
            else:
                self.check_log(f"", "INFO")
                self.check_log(f"📁 Папки в корне атаки", "SECTION")
                
                try:
                    all_items = os.listdir(attack_folder)
                    # ПРИ ПРОВЕРКЕ АТАКИ проверяем числовые имена только для папок атак
                    folders = [f for f in all_items 
                              if os.path.isdir(os.path.join(attack_folder, f)) and f.isdigit()]
                    
                    other_items = [item for item in all_items if item not in folders]
                    if other_items:
                        self.check_log(f"⚠️ Посторонние элементы: {', '.join(other_items)}", "WARNING", 1)
                    
                    actual_count = len(folders)
                    
                    self.check_log(f"📈 Ожидалось: {structure_info['expected_total']}", "INFO", 1)
                    self.check_log(f"📈 Найдено: {actual_count}", 
                                 "SUCCESS" if structure_info['expected_total'] == actual_count else "ERROR", 1)
                    
                    if structure_info['expected_total'] > 0 and actual_count != structure_info['expected_total']:
                        self.check_log(f"❌ НЕСООТВЕТСТВИЕ КОЛИЧЕСТВА!", "ERROR", 1)
                        total_errors += 1
                    
                    # ПРОВЕРКА СОДЕРЖИМОГО КАЖДОЙ ПАПКИ
                    self.check_log(f"🔍 Проверка содержимого папок:", "SECTION", 1)
                    folder_errors = 0
                    for folder in folders:
                        folder_path = os.path.join(attack_folder, folder)
                        self.check_log(f"📂 Папка {folder}:", "DETAIL", 2)
                        # check_names=False - внутренние папки могут называться как угодно
                        if not self.check_folder_content(folder_path, log_errors=True, indent=3, check_names=False):
                            folder_errors += 1
                        total_checked += 1
                    
                    total_errors += folder_errors
                    total_folders += actual_count
                    
                    if folder_errors == 0:
                        self.check_log(f"✅ Все папки проверены успешно", "SUCCESS", 1)
                    else:
                        self.check_log(f"❌ Ошибок в папках: {folder_errors}", "ERROR", 1)
                except Exception as e:
                    self.check_log(f"❌ Ошибка доступа к папке атаки: {str(e)}", "ERROR", 1)
                    total_errors += 1
            
            self.check_log("", "INFO")
            self.check_log("=" * 60, "HEADER")
            if total_errors == 0:
                self.check_log(f"✅ ПРОВЕРКА ЗАВЕРШЕНА УСПЕШНО!", "SUCCESS")
                self.check_log(f"📊 Проверено папок: {total_checked}", "SUCCESS")
                messagebox.showinfo("Проверка завершена", "Атака проверена успешно! Ошибок не обнаружено.")
            else:
                self.check_log(f"❌ ПРОВЕРКА ЗАВЕРШЕНА С ОШИБКАМИ", "ERROR")
                self.check_log(f"📊 Обнаружено ошибок: {total_errors}", "ERROR")
                messagebox.showwarning("Проверка завершena", f"Обнаружены ошибки: {total_errors}")
                
        except Exception as e:
            self.check_log(f"❌ Ошибка при проверке атаки: {str(e)}", "ERROR")
            messagebox.showerror("Ошибка", f"Произошла ошибка при проверке: {str(e)}")

    def check_attack_structure(self, attack_folder, attack_type):
        """Проверяет структуру папки атаки и возвращает информацию о ней"""
        try:
            items = os.listdir(attack_folder)
            
            has_kozen10 = "kozen 10" in items and os.path.isdir(os.path.join(attack_folder, "kozen 10"))
            has_kozen12 = "kozen 12" in items and os.path.isdir(os.path.join(attack_folder, "kozen 12"))
            
            structure_type = ""
            expected_total = self.get_attack_expected_count(attack_type, "все")
            
            if has_kozen10 or has_kozen12:
                structure_type = "раздельная (с устройствами)"
            else:
                structure_type = "плоская (все папки в корне)"
            
            return {
                "has_kozen10": has_kozen10,
                "has_kozen12": has_kozen12,
                "structure_type": structure_type,
                "expected_total": expected_total
            }
        except Exception as e:
            return {
                "has_kozen10": False,
                "has_kozen12": False,
                "structure_type": "ошибка доступа",
                "expected_total": 0
            }

    def check_id(self):
        """Проверка ID с проверкой содержимого папок"""
        id_folder = self.id_check_entry.get()
        
        if not id_folder:
            messagebox.showerror("Ошибка", "Выберите папку ID")
            return
        
        if not os.path.exists(id_folder):
            messagebox.showerror("Ошибка", "Папка ID не существует")
            return
        
        self.check_log("=" * 60, "HEADER")
        self.check_log(f"🆔 ПРОВЕРКА ID: {os.path.basename(id_folder)}", "HEADER")
        self.check_log("=" * 60, "HEADER")
        
        try:
            attack_folders = []
            for item in os.listdir(id_folder):
                item_path = os.path.join(id_folder, item)
                if os.path.isdir(item_path) and item in self.attack_ranges:
                    attack_folders.append((item, item_path))
            
            if not attack_folders:
                self.check_log(f"❌ ОШИБКА: В папке ID не найдено папок атак", "ERROR")
                self.check_log(f"📋 Доступные атаки: {', '.join(self.attack_ranges.keys())}", "INFO")
                return
            
            total_errors = 0
            total_attacks = len(attack_folders)
            total_content_errors = 0
            
            self.check_log(f"📊 Найдено атак: {total_attacks}", "INFO")
            self.check_log("", "INFO")
            
            for attack_name, attack_folder in attack_folders:
                self.check_log(f"🎯 Атака: {attack_name}", "SECTION")
                
                try:
                    structure_info = self.check_attack_structure(attack_folder, attack_name)
                    
                    self.check_log(f"📁 Структура: {structure_info['structure_type']}", "INFO", 1)
                    self.check_log(f"📊 Ожидаемое количество: {structure_info['expected_total']}", "INFO", 1)
                    
                    attack_errors = 0
                    content_errors = 0
                    actual_total = 0
                    
                    if structure_info['has_kozen10'] or structure_info['has_kozen12']:
                        for device in ["kozen 10", "kozen 12"]:
                            if structure_info[f'has_{device.replace(" ", "")}']:
                                device_folder = os.path.join(attack_folder, device)
                                
                                if not os.path.exists(device_folder):
                                    self.check_log(f"⚠️ Папка устройства {device} не существует", "WARNING", 2)
                                    continue
                                
                                expected_count = 0
                                if attack_name in self.attack_ranges and device in self.attack_ranges[attack_name]:
                                    start, end = self.attack_ranges[attack_name][device]
                                    expected_count = end - start + 1
                                
                                try:
                                    folders = [f for f in os.listdir(device_folder) 
                                              if os.path.isdir(os.path.join(device_folder, f)) and f.isdigit()]
                                    
                                    actual_count = len(folders)
                                    actual_total += actual_count
                                    
                                    status = "✅" if expected_count == actual_count else "❌"
                                    self.check_log(f"{status} {device}: {actual_count}/{expected_count}", 
                                                 "SUCCESS" if expected_count == actual_count else "ERROR", 2)
                                    
                                    if expected_count > 0 and actual_count != expected_count:
                                        attack_errors += 1
                                    
                                    # ПРОВЕРКА СОДЕРЖИМОГО ПАПОК ДЛЯ КАЖДОГО УСТРОЙСТВА
                                    self.check_log(f"🔍 Проверка содержимого {device}:", "SECTION", 2)
                                    device_content_errors = 0
                                    for folder in folders:
                                        folder_path = os.path.join(device_folder, folder)
                                        self.check_log(f"📂 Папка {folder}:", "DETAIL", 3)
                                        if not self.check_folder_content(folder_path, log_errors=True, indent=4, check_names=False):
                                            device_content_errors += 1
                                            content_errors += 1
                                    
                                    if device_content_errors == 0:
                                        self.check_log(f"✅ Содержимое {device} проверено успешно", "SUCCESS", 2)
                                    else:
                                        self.check_log(f"❌ Ошибок в содержимом {device}: {device_content_errors}", "ERROR", 2)
                                except Exception as e:
                                    self.check_log(f"❌ Ошибка доступа к папке устройства: {str(e)}", "ERROR", 2)
                                    attack_errors += 1
                    else:
                        try:
                            folders = [f for f in os.listdir(attack_folder) 
                                      if os.path.isdir(os.path.join(attack_folder, f)) and f.isdigit()]
                            actual_total = len(folders)
                            
                            status = "✅" if structure_info['expected_total'] == actual_total else "❌"
                            self.check_log(f"{status} Всего: {actual_total}/{structure_info['expected_total']}", 
                                         "SUCCESS" if structure_info['expected_total'] == actual_total else "ERROR", 2)
                            
                            if structure_info['expected_total'] > 0 and actual_total != structure_info['expected_total']:
                                attack_errors += 1
                            
                            # ПРОВЕРКА СОДЕРЖИМОГО ПАПОК ДЛЯ ПЛОСКОЙ СТРУКТУРЫ
                            self.check_log(f"🔍 Проверка содержимого папок:", "SECTION", 2)
                            flat_content_errors = 0
                            for folder in folders:
                                folder_path = os.path.join(attack_folder, folder)
                                self.check_log(f"📂 Папка {folder}:", "DETAIL", 3)
                                if not self.check_folder_content(folder_path, log_errors=True, indent=4, check_names=False):
                                    flat_content_errors += 1
                                    content_errors += 1
                            
                            if flat_content_errors == 0:
                                self.check_log(f"✅ Содержимое папок проверено успешно", "SUCCESS", 2)
                            else:
                                self.check_log(f"❌ Ошибок в содержимом: {flat_content_errors}", "ERROR", 2)
                        except Exception as e:
                            self.check_log(f"❌ Ошибка доступа к папке атаки: {str(e)}", "ERROR", 2)
                            attack_errors += 1
                    
                    total_content_errors += content_errors
                    
                    if attack_errors == 0 and content_errors == 0:
                        self.check_log(f"✅ Атака проверена успешно", "SUCCESS", 1)
                    else:
                        error_msg = f"❌ Атака содержит ошибок: структура={attack_errors}, содержимое={content_errors}"
                        self.check_log(error_msg, "ERROR", 1)
                        total_errors += (attack_errors + content_errors)
                    
                    self.check_log("", "INFO")
                
                except Exception as e:
                    self.check_log(f"❌ Ошибка при проверке атаки: {str(e)}", "ERROR", 1)
                    total_errors += 1
            
            self.check_log("=" * 60, "HEADER")
            if total_errors == 0:
                self.check_log(f"✅ ПРОВЕРКА ID ЗАВЕРШЕНА УСПЕШНО!", "SUCCESS")
                self.check_log(f"📊 Проверено атак: {total_attacks}", "SUCCESS")
                self.check_log(f"🔍 Ошибок содержимого: {total_content_errors}", "SUCCESS")
                messagebox.showinfo("Проверка завершена", "ID проверен успешно! Ошибок не обнаружено.")
            else:
                self.check_log(f"❌ ПРОВЕРКА ID ЗАВЕРШЕНА С ОШИБКАМИ", "ERROR")
                self.check_log(f"📊 Обнаружено ошибок: {total_errors}", "ERROR")
                self.check_log(f"🔍 Ошибок содержимого: {total_content_errors}", "ERROR")
                messagebox.showwarning("Проверка завершена", 
                                     f"Обнаружены ошибки: {total_errors}\n"
                                     f"Ошибок содержимого: {total_content_errors}")
                
        except Exception as e:
            self.check_log(f"❌ Ошибка при проверке ID: {str(e)}", "ERROR")
            messagebox.showerror("Ошибка", f"Произошла ошибка при проверке: {str(e)}")

    def check_global(self):
        """Общая проверка проекта с проверкой содержимого папок"""
        project_folder = self.global_check_entry.get()
        
        if not project_folder:
            messagebox.showerror("Ошибка", "Выберите общую папку проекта")
            return
        
        if not os.path.exists(project_folder):
            messagebox.showerror("Ошибка", "Общая папка проекта не существует")
            return
        
        self.check_log("=" * 60, "HEADER")
        self.check_log(f"🌐 ОБЩАЯ ПРОВЕРКА ПРОЕКТА", "HEADER")
        self.check_log(f"📁 Папка: {project_folder}", "HEADER")
        self.check_log("=" * 60, "HEADER")
        
        try:
            id_folders = []
            for item in os.listdir(project_folder):
                item_path = os.path.join(project_folder, item)
                if os.path.isdir(item_path):
                    try:
                        has_attacks = any(subitem in self.attack_ranges for subitem in os.listdir(item_path))
                        if has_attacks:
                            id_folders.append(item_path)
                    except:
                        continue
            
            if not id_folders:
                self.check_log(f"❌ ОШИБКА: В проекте не найдено папок ID", "ERROR")
                return
            
            total_errors = 0
            total_ids = len(id_folders)
            total_content_errors = 0
            
            self.check_log(f"📊 Найдено ID: {total_ids}", "INFO")
            self.check_log("", "INFO")
            
            for id_folder in id_folders:
                self.check_log(f"🆔 ID: {os.path.basename(id_folder)}", "SECTION")
                
                try:
                    attack_folders = []
                    unknown_folders = []
                    
                    for item in os.listdir(id_folder):
                        item_path = os.path.join(id_folder, item)
                        if os.path.isdir(item_path):
                            if item in self.attack_ranges:
                                attack_folders.append((item, item_path))
                            else:
                                unknown_folders.append(item)
                    
                    if not attack_folders:
                        self.check_log(f"❌ В папке ID не найдено папок атак", "ERROR", 1)
                        total_errors += 1
                        continue
                    
                    self.check_log(f"📊 Количество атак: {len(attack_folders)}", "INFO", 1)
                    
                    if unknown_folders:
                        self.check_log(f"⚠️ Неизвестные папки: {', '.join(unknown_folders)}", "WARNING", 1)
                    
                    id_errors = 0
                    id_content_errors = 0
                    
                    for attack_name, attack_folder in attack_folders:
                        self.check_log(f"🎯 Атака: {attack_name}", "INFO", 2)
                        
                        try:
                            structure_info = self.check_attack_structure(attack_folder, attack_name)
                            
                            actual_total = 0
                            attack_errors = 0
                            attack_content_errors = 0
                            
                            if structure_info['has_kozen10'] or structure_info['has_kozen12']:
                                for device in ["kozen 10", "kozen 12"]:
                                    if structure_info[f'has_{device.replace(" ", "")}']:
                                        device_folder = os.path.join(attack_folder, device)
                                        
                                        if not os.path.exists(device_folder):
                                            self.check_log(f"⚠️ Папка {device} не существует", "WARNING", 3)
                                            continue
                                        
                                        expected_count = 0
                                        if attack_name in self.attack_ranges and device in self.attack_ranges[attack_name]:
                                            start, end = self.attack_ranges[attack_name][device]
                                            expected_count = end - start + 1
                                        
                                        try:
                                            folders = [f for f in os.listdir(device_folder) 
                                                      if os.path.isdir(os.path.join(device_folder, f)) and f.isdigit()]
                                            
                                            actual_count = len(folders)
                                            actual_total += actual_count
                                            
                                            status = "✅" if expected_count == actual_count else "❌"
                                            self.check_log(f"{status} {device}: {actual_count}/{expected_count}", 
                                                         "SUCCESS" if expected_count == actual_count else "ERROR", 3)
                                            
                                            if expected_count > 0 and actual_count != expected_count:
                                                attack_errors += 1
                                            
                                            # ПРОВЕРКА СОДЕРЖИМОГО
                                            self.check_log(f"🔍 Проверка содержимого {device}:", "SECTION", 3)
                                            device_content_errors = 0
                                            for folder in folders:
                                                folder_path = os.path.join(device_folder, folder)
                                                self.check_log(f"📂 Папка {folder}:", "DETAIL", 4)
                                                if not self.check_folder_content(folder_path, log_errors=True, indent=5, check_names=False):
                                                    device_content_errors += 1
                                                    attack_content_errors += 1
                                            
                                            if device_content_errors == 0:
                                                self.check_log(f"✅ Содержимое {device} OK", "SUCCESS", 3)
                                            else:
                                                self.check_log(f"❌ Ошибок в {device}: {device_content_errors}", "ERROR", 3)
                                        except Exception as e:
                                            self.check_log(f"❌ Ошибка доступа к папке устройства: {str(e)}", "ERROR", 3)
                                            attack_errors += 1
                            else:
                                try:
                                    folders = [f for f in os.listdir(attack_folder) 
                                              if os.path.isdir(os.path.join(attack_folder, f)) and f.isdigit()]
                                    actual_total = len(folders)
                                    
                                    status = "✅" if structure_info['expected_total'] == actual_total else "❌"
                                    self.check_log(f"{status} Всего: {actual_total}/{structure_info['expected_total']}", 
                                                 "SUCCESS" if structure_info['expected_total'] == actual_total else "ERROR", 3)
                                    
                                    if structure_info['expected_total'] > 0 and actual_total != structure_info['expected_total']:
                                        attack_errors += 1
                                    
                                    # ПРОВЕРКА СОДЕРЖИМОГО
                                    self.check_log(f"🔍 Проверка содержимого:", "SECTION", 3)
                                    flat_content_errors = 0
                                    for folder in folders:
                                        folder_path = os.path.join(attack_folder, folder)
                                        self.check_log(f"📂 Папка {folder}:", "DETAIL", 4)
                                        if not self.check_folder_content(folder_path, log_errors=True, indent=5, check_names=False):
                                            flat_content_errors += 1
                                            attack_content_errors += 1
                                    
                                    if flat_content_errors == 0:
                                        self.check_log(f"✅ Содержимое папок OK", "SUCCESS", 3)
                                    else:
                                        self.check_log(f"❌ Ошибок в содержимом: {flat_content_errors}", "ERROR", 3)
                                except Exception as e:
                                    self.check_log(f"❌ Ошибка доступа к папке атаки: {str(e)}", "ERROR", 3)
                                    attack_errors += 1
                            
                            id_content_errors += attack_content_errors
                            total_content_errors += attack_content_errors
                            
                            if attack_errors == 0 and attack_content_errors == 0:
                                self.check_log(f"✅ Атака проверена успешно", "SUCCESS", 3)
                            else:
                                error_msg = f"❌ Ошибки: структура={attack_errors}, содержимое={attack_content_errors}"
                                self.check_log(error_msg, "ERROR", 3)
                                id_errors += (attack_errors + attack_content_errors)
                        
                        except Exception as e:
                            self.check_log(f"❌ Ошибка при проверке атаки: {str(e)}", "ERROR", 3)
                            id_errors += 1
                    
                    total_errors += id_errors
                    
                    if id_errors == 0:
                        self.check_log(f"✅ ID проверен успешно", "SUCCESS", 1)
                    else:
                        self.check_log(f"❌ ID содержит ошибок: {id_errors}", "ERROR", 1)
                
                except Exception as e:
                    self.check_log(f"❌ Ошибка при проверке ID: {str(e)}", "ERROR", 1)
                    total_errors += 1
                
                self.check_log("", "INFO")
            
            self.check_log("=" * 60, "HEADER")
            if total_errors == 0:
                self.check_log(f"✅ ОБЩАЯ ПРОВЕРКА ЗАВЕРШЕНА УСПЕШНО!", "SUCCESS")
                self.check_log(f"📊 Проверено ID: {total_ids}", "SUCCESS")
                self.check_log(f"🔍 Ошибок содержимого: {total_content_errors}", "SUCCESS")
                messagebox.showinfo("Проверка завершена", "Проект проверен успешно! Ошибок не обнаружено.")
            else:
                self.check_log(f"❌ ОБЩАЯ ПРОВЕРКА ЗАВЕРШЕНА С ОШИБКАМИ", "ERROR")
                self.check_log(f"📊 Обнаружено ошибок: {total_errors}", "ERROR")
                self.check_log(f"📊 Проверено ID: {total_ids}", "INFO")
                self.check_log(f"🔍 Ошибок содержимого: {total_content_errors}", "ERROR")
                messagebox.showwarning("Проверка завершена", 
                                     f"Обнаружены ошибки: {total_errors}\n"
                                     f"Ошибок содержимого: {total_content_errors}\n"
                                     f"Проверено ID: {total_ids}")
                
        except Exception as e:
            self.check_log(f"❌ Ошибка при общей проверке проекта: {str(e)}", "ERROR")
            messagebox.showerror("Ошибка", f"Произошла ошибка при проверке: {str(e)}")

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
            
            attacks = list(self.attack_ranges.keys())
            self.attack_combo['values'] = attacks
            self.edit_attack_combo['values'] = attacks
            
            self.log(f"Атака {attack} успешно сохранена", "SUCCESS")
            messagebox.showinfo("Успех", f"Атака {attack} успешно сохранена")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")
    
    def new_attack(self):
        """Создание новой атаки"""
        attack = tk.simpledialog.askstring("Новая атака", "Введите название новой атаки:")
        if attack:
            if attack in self.attack_ranges:
                messagebox.showerror("Ошибка", "Атака с таким названием уже существует")
                return
            
            self.attack_ranges[attack] = {}
            self.save_attack_config()
            
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
            
            attack_data = self.attack_ranges[old_attack]
            del self.attack_ranges[old_attack]
            self.attack_ranges[new_attack] = attack_data
            self.save_attack_config()
            
            attacks = list(self.attack_ranges.keys())
            self.attack_combo['values'] = attacks
            self.edit_attack_combo['values'] = attacks
            
            self.attack_var.set(new_attack)
            self.edit_attack_var.set(new_attack)
            self.load_attack_data()
            
            self.log(f"Атака переименована: {old_attack} → {new_attack}", "SUCCESS")
            messagebox.showinfo("Успех", f"Атака успешно переименована: {old_attack} → {new_attack}")
    
    def delete_attack(self):
        """Удаление атаки"""
        attack = self.edit_attack_var.get()
        if not attack:
            messagebox.showerror("Ошибка", "Выберите атаку для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить атаку {attack}?"):
            del self.attack_ranges[attack]
            self.save_attack_config()
            
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