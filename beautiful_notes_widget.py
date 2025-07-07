# -*- coding: utf-8 -*-
import customtkinter as ctk
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
import threading
import time

class BeautifulNotesWidget:
    def __init__(self):
        # Настройка темы и внешнего вида
        ctk.set_appearance_mode("dark")  # Темная тема
        ctk.set_default_color_theme("blue")  # Синяя цветовая схема
        
        # Создание главного окна
        self.root = ctk.CTk()
        self.root.title("Заметки")
        self.root.geometry("350x700")  # Увеличили высоту на 300 пикселей
        
        # Настройка окна
        self.root.attributes('-topmost', True)  # Поверх всех окон
        self.root.attributes('-alpha', 0.95)  # Легкая прозрачность
        self.root.overrideredirect(True)  # Убираем стандартную рамку
        
        # Переменные для перетаскивания
        self.drag_x = 0
        self.drag_y = 0
        self.is_dragging = False
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка заметок
        self.notes_file = "notes.json"
        self.load_notes()
        
        # Привязка событий
        self.bind_events()
        
        # Анимация появления
        self.animate_appearance()
        
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Главный контейнер
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок с градиентом
        self.title_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, height=50)
        self.title_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="📝 Мои Заметки", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("white", "white")
        )
        self.title_label.pack(side="left", padx=15, pady=10)
        
        # Кнопки управления
        self.control_frame = ctk.CTkFrame(self.title_frame, fg_color="transparent")
        self.control_frame.pack(side="right", padx=10)
        
        # Кнопка сворачивания
        self.minimize_btn = ctk.CTkButton(
            self.control_frame,
            text="−",
            width=30,
            height=25,
            command=self.toggle_minimize,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.minimize_btn.pack(side="left", padx=2)
        
        # Кнопка закрытия
        self.close_btn = ctk.CTkButton(
            self.control_frame,
            text="×",
            width=30,
            height=25,
            command=self.root.quit,
            fg_color="transparent",
            hover_color=("red", "darkred"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.close_btn.pack(side="left", padx=2)
        
        # Контейнер для заметок
        self.notes_container = ctk.CTkScrollableFrame(
            self.main_frame,
            corner_radius=10,
            height=200
        )
        self.notes_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Поле ввода новой заметки
        self.input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.input_frame.pack(fill="x", padx=10, pady=5)
        
        # Заголовок поля ввода
        self.input_label = ctk.CTkLabel(
            self.input_frame,
            text="✏️ Новая заметка:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.input_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Текстовое поле
        self.note_entry = ctk.CTkTextbox(
            self.input_frame,
            height=80,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            wrap="word"  # Перенос слов
        )
        self.note_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Устанавливаем фокус на текстовое поле
        self.note_entry.focus_set()
        
        # Привязываем Enter для сохранения заметки
        self.note_entry.bind("<Control-Return>", lambda event: self.save_note())
        
        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(
            self.input_frame,
            text="💾 Сохранить заметку",
            command=self.save_note,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("blue", "darkblue"),
            hover_color=("darkblue", "blue")
        )
        self.save_btn.pack(padx=15, pady=(0, 15))
        
        # Статистика
        self.stats_label = ctk.CTkLabel(
            self.main_frame,
            text="📊 Всего заметок: 0",
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        self.stats_label.pack(pady=(0, 10))
        
    def bind_events(self):
        """Привязка событий для перетаскивания"""
        self.title_frame.bind("<Button-1>", self.start_drag)
        self.title_frame.bind("<B1-Motion>", self.on_drag)
        self.title_frame.bind("<ButtonRelease-1>", self.stop_drag)
        
        # Привязка к заголовку тоже
        self.title_label.bind("<Button-1>", self.start_drag)
        self.title_label.bind("<B1-Motion>", self.on_drag)
        self.title_label.bind("<ButtonRelease-1>", self.stop_drag)
        
    def start_drag(self, event):
        """Начало перетаскивания"""
        self.is_dragging = True
        self.drag_x = event.x
        self.drag_y = event.y
        
    def on_drag(self, event):
        """Перетаскивание окна"""
        if self.is_dragging:
            x = self.root.winfo_x() + (event.x - self.drag_x)
            y = self.root.winfo_y() + (event.y - self.drag_y)
            self.root.geometry(f"+{x}+{y}")
            
    def stop_drag(self, event):
        """Окончание перетаскивания"""
        self.is_dragging = False
        
    def toggle_minimize(self):
        """Сворачивание/разворачивание окна"""
        if self.root.winfo_height() > 100:
            # Сворачиваем
            self.root.geometry(f"{self.root.winfo_width()}x80")
            # Скрываем элементы
            self.notes_container.pack_forget()
            self.input_frame.pack_forget()
            self.stats_label.pack_forget()
            # Обновляем кнопку
            self.minimize_btn.configure(text="□")
        else:
            # Разворачиваем
            self.root.geometry("350x700")  # Увеличили высоту на 300 пикселей
            # Показываем элементы
            self.notes_container.pack(fill="both", expand=True, padx=10, pady=5)
            self.input_frame.pack(fill="x", padx=10, pady=5)
            self.stats_label.pack(pady=(0, 10))
            # Обновляем кнопку
            self.minimize_btn.configure(text="−")
            
    def save_note(self):
        """Сохранение новой заметки"""
        try:
            note_text = self.note_entry.get("1.0", "end-1c").strip()
            if note_text:
                # Создаем новую заметку с правильным ID
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Находим максимальный ID и добавляем 1
                max_id = max([note.get('id', 0) for note in self.notes]) if self.notes else 0
                new_note = {
                    "text": note_text,
                    "timestamp": timestamp,
                    "id": max_id + 1
                }
                
                self.notes.append(new_note)
                self.save_to_file()
                
                # Очищаем поле ввода
                self.note_entry.delete("1.0", "end")
                
                # Обновляем интерфейс
                self.update_notes_display()
                
                # Показываем уведомление
                self.show_notification("✅ Заметка сохранена!")
                
                # Возвращаем фокус на поле ввода
                self.note_entry.focus_set()
        except Exception as e:
            self.show_notification(f"❌ Ошибка: {str(e)}")
            
    def update_notes_display(self):
        """Обновление отображения заметок"""
        # Очищаем контейнер
        for widget in self.notes_container.winfo_children():
            widget.destroy()
            
        # Обновляем статистику
        self.stats_label.configure(text=f"📊 Всего заметок: {len(self.notes)}")
        
        # Отображаем заметки в обратном порядке (новые сверху)
        for note in reversed(self.notes):
            self.create_note_widget(note)
            
    def create_note_widget(self, note):
        """Создание виджета для одной заметки"""
        # Фрейм для заметки
        note_frame = ctk.CTkFrame(
            self.notes_container,
            corner_radius=10,
            fg_color=("gray90", "gray20")
        )
        note_frame.pack(fill="x", padx=5, pady=3)
        
        # Заголовок с датой
        header_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Номер заметки
        note_id = note.get('id', '?')
        note_id_label = ctk.CTkLabel(
            header_frame,
            text=f"#{note_id}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("blue", "lightblue")
        )
        note_id_label.pack(side="left")
        
        # Дата
        date_label = ctk.CTkLabel(
            header_frame,
            text=note['timestamp'],
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60")
        )
        date_label.pack(side="right")
        
        # Текст заметки
        text_label = ctk.CTkLabel(
            note_frame,
            text=note['text'],
            font=ctk.CTkFont(size=12),
            wraplength=300,
            justify="left"
        )
        text_label.pack(fill="x", padx=10, pady=(0, 10))
        
        # Кнопка удаления
        note_id = note.get('id', '?')
        delete_btn = ctk.CTkButton(
            note_frame,
            text="🗑️",
            width=30,
            height=25,
            command=lambda: self.delete_note(note_id),
            fg_color="transparent",
            hover_color=("red", "darkred"),
            font=ctk.CTkFont(size=12)
        )
        delete_btn.pack(anchor="e", padx=10, pady=(0, 10))
        
    def delete_note(self, note_id):
        """Удаление заметки"""
        self.notes = [note for note in self.notes if note['id'] != note_id]
        self.save_to_file()
        self.update_notes_display()
        self.show_notification("🗑️ Заметка удалена!")
        
    def show_notification(self, message):
        """Показ уведомления"""
        # Создаем временное уведомление
        notification = ctk.CTkLabel(
            self.root,
            text=message,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("green", "darkgreen"),
            text_color="white",
            corner_radius=8
        )
        notification.place(relx=0.5, rely=0.1, anchor="center")
        
        # Удаляем через 2 секунды
        self.root.after(2000, notification.destroy)
        
    def load_notes(self):
        """Загрузка заметок из файла"""
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
                # Добавляем ID для старых заметок, если их нет
                for i, note in enumerate(self.notes):
                    if 'id' not in note:
                        note['id'] = i + 1
            except:
                self.notes = []
        else:
            self.notes = []
            
    def save_to_file(self):
        """Сохранение заметок в файл"""
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
            
    def animate_appearance(self):
        """Анимация появления окна"""
        # Устанавливаем начальную прозрачность
        self.root.attributes('-alpha', 0.0)
        
        def fade_in():
            alpha = 0.0
            while alpha < 0.95:
                alpha += 0.05
                try:
                    self.root.attributes('-alpha', alpha)
                    time.sleep(0.02)
                except:
                    break  # Если окно закрыто, прерываем анимацию
                
        # Запускаем анимацию в отдельном потоке
        threading.Thread(target=fade_in, daemon=True).start()
        
    def run(self):
        """Запуск приложения"""
        self.update_notes_display()  # Первоначальное отображение заметок
        self.root.mainloop()

if __name__ == "__main__":
    widget = BeautifulNotesWidget()
    widget.run() 