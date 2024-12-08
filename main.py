import os
import sys
import vlc
import sqlite3
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QStyle, QMessageBox, QInputDialog, QMenu, \
    QListWidgetItem, QCheckBox, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QIcon
from PyQt6 import uic
from io import StringIO

# наша XML разметка
template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>800</width>
    <height>600</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>EasyPlayer</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QMainWindow, QWidget {
    background-color: #1e1e1e;
    color: #cccccc;
}

QListWidget {
    background-color: #2d2d2d;
    color: #E0E0E0;
    border: none;
    border-radius: 5px;
    padding: 15px;
    margin: 15px;
}
QListWidget::item:selected {
    background-color: #404040;
    color: #FFFFFF;
}
QListWidget::item:hover {
    background-color: #353535;
}

QLabel {
    color: #cccccc;
    font-size: 12px;
}

QSlider::groove:horizontal {
    background: #2d2d2d;
    height: 4px;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #4d4d4d;
    width: 10px;
    margin: -4px 0;
    border-radius: 5px;
    border: 1px solid #5d5d5d;
}
QSlider::sub-page:horizontal {
    background: #007acc;
    height: 4px;
    border-radius: 2px;
}

QPushButton {
    background-color: #404040;
    color: #ffffff;
    border: 1px solid #505050;
    border-radius: 2px;
    padding: 3px;
    min-width: 28px;
    min-height: 28px;
    margin: 0px;
}
QPushButton:hover {
    background-color: #454545;
    border: 1px solid #555555;
}
QPushButton:pressed {
    background-color: #505050;
    border: 1px solid #606060;
}</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QHBoxLayout" name="horizontalLayout_main">
    <property name="spacing">
     <number>5</number>
    </property>
    <item>
     <widget class="QListWidget" name="playlists_widget">
      <property name="maximumSize">
       <size>
        <width>200</width>
        <height>16777215</height>
       </size>
      </property>
      <property name="minimumSize">
       <size>
        <width>0</width>
        <height>400</height>
       </size>
      </property>
      <property name="styleSheet">
       <string>QListWidget {
           background-color: #2d2d2d;
           color: #E0E0E0;
           border: none;
           border-radius: 10px;
           padding: 15px;
           margin: 15px;
       }
       QListWidget::item:selected {
           background-color: #404040;
           color: #FFFFFF;
       }
       QListWidget::item:hover {
           background-color: #353535;
       }</string>
      </property>
     </widget>
    </item>
    <item>
     <layout class="QVBoxLayout" name="verticalLayout">
      <property name="spacing">
       <number>10</number>
      </property>
      <property name="leftMargin">
       <number>0</number>
      </property>
      <property name="topMargin">
       <number>10</number>
      </property>
      <property name="rightMargin">
       <number>10</number>
      </property>
      <property name="bottomMargin">
       <number>10</number>
      </property>
      <item>
       <widget class="QListWidget" name="playlist_widget">
        <property name="minimumSize">
         <size>
          <width>0</width>
          <height>400</height>
         </size>
        </property>
        <property name="styleSheet">
         <string>QListWidget {
             background-color: #2d2d2d;
             color: #E0E0E0;
             border: none;
             border-radius: 10px;
             padding: 5px;
             margin: 5px;
         }
         QListWidget::item:selected {
             background-color: #404040;
             color: #FFFFFF;
         }
         QListWidget::item:hover {
             background-color: #353535;
         }</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QWidget" name="controls_container" native="true">
        <layout class="QVBoxLayout" name="verticalLayout_2">
         <property name="spacing">
          <number>15</number>
         </property>
         <item>
          <widget class="QLabel" name="track_info">
           <property name="text">
            <string>Нет воспроизводимого трека</string>
           </property>
           <property name="alignment">
            <set>Qt::AlignCenter</set>
           </property>
          </widget>
         </item>
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout">
           <item>
            <spacer name="horizontalSpacer">
             <property name="orientation">
              <enum>Qt::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QWidget" name="buttons_volume_container" native="true">
             <property name="maximumSize">
              <size>
               <width>300</width>
               <height>16777215</height>
              </size>
             </property>
             <layout class="QVBoxLayout" name="verticalLayout_3">
              <property name="spacing">
               <number>15</number>
              </property>
              <item>
               <layout class="QHBoxLayout" name="volume_layout">
                <item>
                 <widget class="QLabel" name="volume_icon">
                  <property name="minimumSize">
                   <size>
                    <width>16</width>
                    <height>16</height>
                   </size>
                  </property>
                  <property name="maximumSize">
                   <size>
                    <width>16</width>
                    <height>16</height>
                   </size>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSlider" name="volume_slider">
                  <property name="maximumSize">
                   <size>
                    <width>200</width>
                    <height>16777215</height>
                   </size>
                  </property>
                  <property name="maximum">
                   <number>100</number>
                  </property>
                  <property name="value">
                   <number>100</number>
                  </property>
                  <property name="orientation">
                   <enum>Qt::Horizontal</enum>
                  </property>
                 </widget>
                </item>
               </layout>
              </item>
              <item>
               <layout class="QHBoxLayout" name="buttons_layout">
                <property name="spacing">
                 <number>10</number>
                </property>
                <item>
                 <widget class="QPushButton" name="prev_button"/>
                </item>
                <item>
                 <widget class="QPushButton" name="play_button"/>
                </item>
                <item>
                 <widget class="QPushButton" name="stop_button"/>
                </item>
                <item>
                 <widget class="QPushButton" name="next_button"/>
                </item>
               </layout>
              </item>
             </layout>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_2">
             <property name="orientation">
              <enum>Qt::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
         <item>
          <layout class="QHBoxLayout" name="horizontalLayout_2">
           <item>
            <spacer name="horizontalSpacer_3">
             <property name="orientation">
              <enum>Qt::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
           <item>
            <widget class="QPushButton" name="add_button">
             <property name="minimumSize">
              <size>
               <width>120</width>
               <height>0</height>
              </size>
             </property>
             <property name="maximumSize">
              <size>
               <width>120</width>
               <height>16777215</height>
              </size>
             </property>
             <property name="text">
              <string>Добавить файлы</string>
             </property>
            </widget>
           </item>
           <item>
            <spacer name="horizontalSpacer_4">
             <property name="orientation">
              <enum>Qt::Horizontal</enum>
             </property>
             <property name="sizeHint" stdset="0">
              <size>
               <width>40</width>
               <height>20</height>
              </size>
             </property>
            </spacer>
           </item>
          </layout>
         </item>
        </layout>
       </widget>
      </item>
      <item>
       <layout class="QHBoxLayout" name="horizontalLayout_3">
        <property name="spacing">
         <number>15</number>
        </property>
        <item>
         <spacer name="horizontalSpacer_5">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
        <item>
         <widget class="QWidget" name="progress_widget" native="true">
          <property name="minimumWidth">
           <number>400</number>
          </property>
          <property name="maximumWidth">
           <number>800</number>
          </property>
          <layout class="QVBoxLayout" name="verticalLayout_4">
           <item>
            <widget class="QSlider" name="progress_slider">
             <property name="sizePolicy">
              <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
               <horstretch>0</horstretch>
               <verstretch>0</verstretch>
              </sizepolicy>
             </property>
             <property name="orientation">
              <enum>Qt::Horizontal</enum>
             </property>
            </widget>
           </item>
           <item>
            <widget class="QLabel" name="time_label">
             <property name="text">
              <string>--:-- / --:--</string>
             </property>
             <property name="alignment">
              <set>Qt::AlignCenter</set>
             </property>
            </widget>
           </item>
          </layout>
         </widget>
        </item>
        <item>
         <spacer name="horizontalSpacer_6">
          <property name="orientation">
           <enum>Qt::Horizontal</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>40</width>
            <height>20</height>
           </size>
          </property>
         </spacer>
        </item>
       </layout>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>"""


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        # Инициализация таблиц базы данных
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_tracks (
                playlist_id INTEGER,
                stored_path TEXT NOT NULL,
                filename TEXT NOT NULL,
                position INTEGER
            )
        ''')

        self.cursor.execute('''
            INSERT OR IGNORE INTO playlists (id, name) 
            VALUES (1, 'Основной плейлист')
        ''')
        self.conn.commit()

    def get_playlists(self):
        # Получение списка плейлистов
        self.cursor.execute('SELECT id, name FROM playlists ORDER BY name')
        return self.cursor.fetchall()

    def get_tracks(self, playlist_id):
        # Получение треков плейлиста
        self.cursor.execute('''
            SELECT stored_path, filename 
            FROM playlist_tracks 
            WHERE playlist_id = ?
            ORDER BY position
        ''', (playlist_id,))
        return self.cursor.fetchall()

    def add_track(self, playlist_id, stored_path, filename):
        # Добавление трека в плейлист
        self.cursor.execute('''
            INSERT INTO playlist_tracks (playlist_id, stored_path, filename, position)
            VALUES (?, ?, ?, (
                SELECT COALESCE(MAX(position), 0) + 1
                FROM playlist_tracks
                WHERE playlist_id = ?
            ))
        ''', (playlist_id, stored_path, filename, playlist_id))
        self.conn.commit()

    def remove_track(self, playlist_id, stored_path):
        # Удаление трека из плейлиста
        self.cursor.execute('''
            DELETE FROM playlist_tracks 
            WHERE playlist_id = ? AND stored_path = ?
        ''', (playlist_id, stored_path))
        self.conn.commit()

    def create_playlist(self, name):
        # Создание нового плейлиста
        self.cursor.execute('INSERT INTO playlists (name) VALUES (?)', (name,))
        self.conn.commit()

    def delete_playlist(self, playlist_id):
        # Удаление плейлиста"
        self.cursor.execute('DELETE FROM playlist_tracks WHERE playlist_id = ?', (playlist_id,))
        self.cursor.execute('DELETE FROM playlists WHERE id = ?', (playlist_id,))
        self.conn.commit()

    def rename_playlist(self, playlist_id, new_name):
        # Переименование плейлиста
        self.cursor.execute('UPDATE playlists SET name = ? WHERE id = ?', (new_name, playlist_id))
        self.conn.commit()

    def update_stored_path(self, old_path, new_path):
        # Обновление пути к файлу
        self.cursor.execute('''
            UPDATE playlist_tracks 
            SET stored_path = ? 
            WHERE stored_path = ?
        ''', (new_path, old_path))
        self.conn.commit()


class FileManager:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        os.makedirs(self.music_dir, exist_ok=True)

    def copy_file_to_storage(self, file_path):
        # Копирование файла в хранилище
        filename = os.path.basename(file_path)
        new_path = os.path.join(self.music_dir, filename)
        try:
            shutil.copy2(file_path, new_path)
        except shutil.SameFileError:
            pass  # Файл уже существует
        return new_path

    def move_files_to_new_directory(self, new_dir):
        # Перемещение файлов в новую директорию
        if os.path.exists(self.music_dir):
            for file in os.listdir(self.music_dir):
                old_path = os.path.join(self.music_dir, file)
                new_path = os.path.join(new_dir, file)
                shutil.move(old_path, new_path)
        self.music_dir = new_dir


class MediaPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.current_media = None
        self.current_file = None
        self.is_playing = False

    def play_file(self, file_path):
        # Воспроизведение трека
        if os.path.exists(file_path):
            if self.current_file == file_path and self.current_media:
                self.player.play()
                self.is_playing = True
                return True

            try:
                self.current_media = self.instance.media_new(file_path)
                self.player.set_media(self.current_media)
                self.player.play()
                self.is_playing = True
                self.current_file = file_path
                return True
            except Exception:
                return False

    def format_time(self, ms):
        # Форматирование времени из миллисекунд в MM:SS
        if ms < 0:
            return "--:--"
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_current_time(self):
        # Получение текущего времени воспроизведения
        if not self.current_media:
            return "--:--", "--:--", 0

        current = self.player.get_time()
        duration = self.current_media.get_duration()

        if current < 0 or duration < 0:
            return "--:--", "--:--", 0

        progress = (current / duration * 100) if duration > 0 else 0
        return self.format_time(current), self.format_time(duration), progress

    def pause(self):
        # Пауза
        self.player.pause()
        self.is_playing = not self.is_playing

    def stop(self):
        # Остановка
        self.player.stop()
        self.is_playing = False
        self.current_file = None

    def set_volume(self, volume):
        # Установка громкости
        self.player.audio_set_volume(volume)

    def set_position(self, position):
        # Установка позиции воспроизведения
        if self.current_media:
            self.player.set_position(position / 100.0)


class EasyPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(StringIO(template), self)

        # Инициализация компонентов
        self.init_storage()
        self.db_manager = DatabaseManager(self.db_path)
        self.file_manager = FileManager(self.music_dir)
        self.media_player = MediaPlayer()

        # Таймер для обновления времени
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_time_label)
        self.update_timer.start(1000)  # Обновление каждую секунду

        # Инициализация UI
        self.init_storage_controls()
        self.setup_icons()
        self.setup_connections()

        # Инициализация состояния
        self.current_playlist_id = None
        self.files_list = []
        self.current_volume = 100
        self.volume_slider.setValue(self.current_volume)
        self.is_seeking = False

        # Загрузка плейлистов
        self.load_playlists()

    def init_storage(self):
        # Инициализация путей хранения
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.music_dir = os.path.join(os.path.expanduser("~"), "Downloads", "music_storage")
        self.db_path = os.path.join(self.app_dir, 'playlist.db')
        os.makedirs(self.music_dir, exist_ok=True)

    def init_storage_controls(self):
        # Инициализация элементов управления хранилищем
        storage_widget = QWidget()
        storage_layout = QHBoxLayout()

        self.save_locally_checkbox = QCheckBox("Локально сохранять новые треки")
        self.save_locally_checkbox.setChecked(True)

        self.change_dir_button = QPushButton("Изменить директорию")
        self.change_dir_button.clicked.connect(self.change_storage_directory)

        storage_layout.addWidget(self.save_locally_checkbox)
        storage_layout.addWidget(self.change_dir_button)
        storage_layout.addStretch()

        storage_widget.setLayout(storage_layout)
        self.verticalLayout.insertWidget(0, storage_widget)

    def setup_icons(self):
        # Настройка иконок
        style = self.style()
        self.prev_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward))
        self.play_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.stop_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.next_button.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.volume_icon.setPixmap(style.standardIcon(QStyle.StandardPixmap.SP_MediaVolume).pixmap(16, 16))

    def setup_connections(self):
        # Подключение обработчиков событий
        self.add_button.clicked.connect(self.add_files)
        self.play_button.clicked.connect(self.play_pause)
        self.stop_button.clicked.connect(self.stop)
        self.prev_button.clicked.connect(self.prev_track)
        self.next_button.clicked.connect(self.next_track)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.playlist_widget.itemDoubleClicked.connect(self.play_file)

        # Подключаем события для перемотки
        self.progress_slider.sliderPressed.connect(self.on_seek_start)
        self.progress_slider.sliderReleased.connect(self.on_seek_end)
        self.progress_slider.valueChanged.connect(self.on_seek_change)

        self.playlists_widget.itemDoubleClicked.connect(self.change_playlist)
        self.playlists_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlists_widget.customContextMenuRequested.connect(self.show_playlist_menu)

        self.playlist_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlist_widget.customContextMenuRequested.connect(self.show_track_menu)

    def load_playlists(self):
        # Загрузка списка плейлистов
        try:
            self.playlists_widget.clear()
            playlists = self.db_manager.get_playlists()

            for playlist_id, name in playlists:
                item = QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, playlist_id)
                self.playlists_widget.addItem(item)

            if not self.current_playlist_id:
                self.current_playlist_id = 1
                self.playlists_widget.setCurrentRow(0)
                self.load_tracks_from_db()

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке плейлистов: {e}")

    def load_tracks_from_db(self):
        # Загрузка треков текущего плейлиста
        try:
            tracks = self.db_manager.get_tracks(self.current_playlist_id)
            self.files_list.clear()
            self.playlist_widget.clear()

            for stored_path, filename in tracks:
                if os.path.exists(stored_path):
                    self.files_list.append(stored_path)
                    self.playlist_widget.addItem(filename)

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при загрузке треков: {e}")

    def add_files(self):
        # Добавление новых файлов
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выбрать файлы",
            "",
            "Audio Files (*.mp3)"
        )

        for file in files:
            if os.path.exists(file):
                filename = os.path.basename(file)
                if self.save_locally_checkbox.isChecked():
                    new_path = self.file_manager.copy_file_to_storage(file)
                else:
                    new_path = file

                self.db_manager.add_track(self.current_playlist_id, new_path, filename)

        self.load_tracks_from_db()

    def play_file(self):
        # Воспроизведение выбранного файла
        current_row = self.playlist_widget.currentRow()
        if 0 <= current_row < len(self.files_list):
            file_path = self.files_list[current_row]
            if self.media_player.play_file(file_path):
                self.track_info.setText(os.path.basename(file_path))
                self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            else:
                self.track_info.setText("Ошибка воспроизведения")

    def play_pause(self):
        # Воспроизведение/пауза
        if not self.media_player.current_media:
            self.play_file()
            return

        self.media_player.pause()
        icon = QStyle.StandardPixmap.SP_MediaPause \
            if self.media_player.is_playing else QStyle.StandardPixmap.SP_MediaPlay
        self.play_button.setIcon(self.style().standardIcon(icon))

    def stop(self):
        # Остановка воспроизведения
        self.media_player.stop()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.progress_slider.setValue(0)
        self.time_label.setText("--:-- / --:--")

    def next_track(self):
        # Следующий трек
        current = self.playlist_widget.currentRow()
        if current < self.playlist_widget.count() - 1:
            self.playlist_widget.setCurrentRow(current + 1)
            self.play_file()

    def prev_track(self):
        # Предыдущий трек
        current = self.playlist_widget.currentRow()
        if current > 0:
            self.playlist_widget.setCurrentRow(current - 1)
            self.play_file()

    def set_volume(self, value):
        # Изменение громкости
        if value != self.current_volume:
            self.current_volume = value
            self.media_player.set_volume(value)

    def change_playlist(self, item):
        # Смена текущего плейлиста
        playlist_id = item.data(Qt.ItemDataRole.UserRole)
        if playlist_id != self.current_playlist_id:
            self.current_playlist_id = playlist_id
            self.load_tracks_from_db()

    def show_playlist_menu(self, position):
        # Показ контекстного меню плейлиста
        menu = QMenu()
        add_action = menu.addAction("Создать плейлист")
        delete_action = menu.addAction("Удалить плейлист")
        rename_action = menu.addAction("Переименовать")

        item = self.playlists_widget.itemAt(position)
        action = menu.exec(QCursor.pos())

        if action == add_action:
            self.create_playlist()
        elif action == delete_action and item:
            self.delete_playlist(item)
        elif action == rename_action and item:
            self.rename_playlist(item)

    def show_track_menu(self, position):
        # Показ контекстного меню трека
        menu = QMenu()
        remove_action = menu.addAction("Удалить")

        item = self.playlist_widget.itemAt(position)
        if item and menu.exec(QCursor.pos()) == remove_action:
            self.remove_track(item)

    def create_playlist(self):
        # Создание нового плейлиста
        name, ok = QInputDialog.getText(self, "Новый плейлист", "Введите название плейлиста:")
        if ok and name:
            try:
                self.db_manager.create_playlist(name)
                self.load_playlists()
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при создании плейлиста: {e}")

    def delete_playlist(self, item):
        # Удаление плейлиста
        playlist_id = item.data(Qt.ItemDataRole.UserRole)
        if playlist_id != 1:  # Не удаляем основной плейлист
            try:
                self.db_manager.delete_playlist(playlist_id)
                self.current_playlist_id = 1
                self.load_playlists()
                self.load_tracks_from_db()
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при удалении плейлиста: {e}")

    def rename_playlist(self, item):
        # Переименование плейлиста
        playlist_id = item.data(Qt.ItemDataRole.UserRole)
        if playlist_id == 1:
            QMessageBox.warning(self, "Ошибка", "Нельзя переименовать основной плейлист")
            return

        name, ok = QInputDialog.getText(
            self,
            "Переименовать плейлист",
            "Введите новое название:",
            text=item.text()
        )
        if ok and name:
            try:
                self.db_manager.rename_playlist(playlist_id, name)
                self.load_playlists()
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка при переименовании плейлиста: {e}")

    def remove_track(self, item):
        # Удаление трека
        if not item:
            return

        row = self.playlist_widget.row(item)
        stored_path = self.files_list[row]
        self.db_manager.remove_track(self.current_playlist_id, stored_path)
        self.load_tracks_from_db()

    def change_storage_directory(self):
        # Изменение директории для сохранения музыки
        new_dir = QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию для сохранения музыки",
            self.music_dir
        )

        if new_dir:
            os.makedirs(new_dir, exist_ok=True)

            if os.path.exists(self.music_dir) and os.listdir(self.music_dir):
                reply = QMessageBox.question(
                    self,
                    'Перемещение файлов',
                    'Переместить существующие файлы в новую директорию?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    try:
                        for file in os.listdir(self.music_dir):
                            old_path = os.path.join(self.music_dir, file)
                            new_path = os.path.join(new_dir, file)
                            shutil.move(old_path, new_path)
                            self.db_manager.update_stored_path(old_path, new_path)
                    except Exception as e:
                        QMessageBox.warning(
                            self,
                            'Ошибка',
                            f'Ошибка при перемещении файлов: {str(e)}'
                        )
                        return

            self.file_manager.music_dir = new_dir
            self.music_dir = new_dir
            self.load_tracks_from_db()

            QMessageBox.information(
                self,
                'Успешно',
                f'Директория сохранения изменена на:\n{new_dir}'
            )

    def update_time_label(self):
        # Обновление отображения времени воспроизведения
        if not self.is_seeking:  # Обновляем только если не идет перемотка
            current, duration, progress = self.media_player.get_current_time()
            self.time_label.setText(f"{current} / {duration}")
            self.progress_slider.setValue(int(progress))

    def on_seek_start(self):
        # Начало перемотки
        self.is_seeking = True

    def on_seek_end(self):
        # Конец перемотки
        self.is_seeking = False

    def on_seek_change(self, value):
        # Изменение позиции перемотки
        if self.is_seeking:
            self.media_player.set_position(value)

    def closeEvent(self, event):
        # Обработка закрытия окна
        self.media_player.stop()
        if hasattr(self, 'db_manager'):
            self.db_manager.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.ico'))
    app.setWindowIcon(app_icon)
    player = EasyPlayer()
    player.show()
    sys.exit(app.exec())
