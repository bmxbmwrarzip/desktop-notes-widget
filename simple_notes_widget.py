# -*- coding: utf-8 -*-
import customtkinter as ctk
import json
import os
from datetime import datetime

class SimpleNotesWidget:
    def __init__(self):
        # Настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Создание главного окна
        self.root = ctk.CTk()
        self.root.title("Простой виджет заметок")
        self.root.geometry("400x800")  # Увеличили высоту на 300 пикселей
        
        # Настройка окна
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        
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
        
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Главный контейнер
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="📝 Мои Заметки", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        # Кнопки управления
        self.control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.control_frame.pack(fill="x", padx=10, pady=5)
        
        # Кнопка сворачивания
        self.minimize_btn = ctk.CTkButton(
            self.control_frame,
            text="Свернуть",
            command=self.toggle_minimize,
            width=80
        )
        self.minimize_btn.pack(side="left", padx=5)
        
        # Кнопка закрытия
        self.close_btn = ctk.CTkButton(
            self.control_frame,
            text="Закрыть",
            command=self.root.quit,
            width=80,
            fg_color="red",
            hover_color="darkred"
        )
        self.close_btn.pack(side="right", padx=5)
        
        # Контейнер для заметок
        self.notes_container = ctk.CTkScrollableFrame(
            self.main_frame,
            corner_radius=10,
            height=200
        )
        self.notes_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Поле ввода новой заметки
        self.input_label = ctk.CTkLabel(
            self.main_frame,
            text="✏️ Новая заметка:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.input_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Текстовое поле
        self.note_entry = ctk.CTkTextbox(
            self.main_frame,
            height=100,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.note_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(
            self.main_frame,
            text="💾 Сохранить заметку",
            command=self.save_note,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.save_btn.pack(padx=15, pady=(0, 15))
        
        # Статистика
        self.stats_label = ctk.CTkLabel(
            self.main_frame,
            text="📊 Всего заметок: 0",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.pack(pady=(0, 10))
        
        # Устанавливаем фокус на текстовое поле
        self.note_entry.focus_set()
        
    def bind_events(self):
        """Привязка событий для перетаскивания"""
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
        if self.root.winfo_height() > 200:
            # Сворачиваем
            self.root.geometry(f"{self.root.winfo_width()}x150")
            self.notes_container.pack_forget()
            self.input_label.pack_forget()
            self.note_entry.pack_forget()
            self.save_btn.pack_forget()
            self.stats_label.pack_forget()
            self.minimize_btn.configure(text="Развернуть")
        else:
            # Разворачиваем
            self.root.geometry("400x800")  # Увеличили высоту на 300 пикселей
            self.notes_container.pack(fill="both", expand=True, padx=10, pady=10)
            self.input_label.pack(anchor="w", padx=15, pady=(10, 5))
            self.note_entry.pack(fill="x", padx=15, pady=(0, 10))
            self.save_btn.pack(padx=15, pady=(0, 15))
            self.stats_label.pack(pady=(0, 10))
            self.minimize_btn.configure(text="Свернуть")
            
    def save_note(self):
        """Сохранение новой заметки"""
        try:
            note_text = self.note_entry.get("1.0", "end-1c").strip()
            if note_text:
                # Создаем новую заметку
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                
                # Возвращаем фокус
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
        
        # Отображаем заметки
        for note in reversed(self.notes):
            self.create_note_widget(note)
            
    def create_note_widget(self, note):
        """Создание виджета для одной заметки"""
        # Фрейм для заметки
        note_frame = ctk.CTkFrame(
            self.notes_container,
            corner_radius=10
        )
        note_frame.pack(fill="x", padx=5, pady=3)
        
        # Заголовок
        header_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Номер заметки
        note_id = note.get('id', '?')
        note_id_label = ctk.CTkLabel(
            header_frame,
            text=f"#{note_id}",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        note_id_label.pack(side="left")
        
        # Дата
        date_label = ctk.CTkLabel(
            header_frame,
            text=note['timestamp'],
            font=ctk.CTkFont(size=10)
        )
        date_label.pack(side="right")
        
        # Текст заметки
        text_label = ctk.CTkLabel(
            note_frame,
            text=note['text'],
            font=ctk.CTkFont(size=12),
            wraplength=350,
            justify="left"
        )
        text_label.pack(fill="x", padx=10, pady=(0, 10))
        
        # Кнопка удаления
        delete_btn = ctk.CTkButton(
            note_frame,
            text="🗑️ Удалить",
            width=80,
            height=25,
            command=lambda: self.delete_note(note_id),
            fg_color="red",
            hover_color="darkred",
            font=ctk.CTkFont(size=10)
        )
        delete_btn.pack(anchor="e", padx=10, pady=(0, 10))
        
    def delete_note(self, note_id):
        """Удаление заметки"""
        self.notes = [note for note in self.notes if note.get('id') != note_id]
        self.save_to_file()
        self.update_notes_display()
        self.show_notification("🗑️ Заметка удалена!")
        
    def show_notification(self, message):
        """Показ уведомления"""
        notification = ctk.CTkLabel(
            self.root,
            text=message,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="green",
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
                # Добавляем ID для старых заметок
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
            
    def run(self):
        """Запуск приложения"""
        self.update_notes_display()
        self.root.mainloop()

if __name__ == "__main__":
    widget = SimpleNotesWidget()
    widget.run() 