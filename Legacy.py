import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QLineEdit, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt
import pyautogui
import keyboard
import random

class LegacyClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.left_clicking = False
        self.left_cps = 20  # Default CPS changed to start from 20
        self.hotkey = 'f6'
        self.hotkey_set = False
        self.click_log = []

        self.initUI()  # Initialize UI after setting attributes

    def initUI(self):
        layout = QVBoxLayout()

        self.left_cps_label = QLabel(f'Left Click CPS: {self.left_cps}', self)
        layout.addWidget(self.left_cps_label)

        self.left_cps_slider = QSlider(Qt.Horizontal, self)
        self.left_cps_slider.setMinimum(20)  # Set minimum CPS to 20
        self.left_cps_slider.setMaximum(50)   # Set maximum CPS to 50
        self.left_cps_slider.setValue(self.left_cps)  # Set default CPS value
        self.left_cps_slider.valueChanged.connect(self.update_left_cps)
        layout.addWidget(self.left_cps_slider)

        self.hotkey_label = QLabel(f'Set Hotkey: (default is {self.hotkey})', self)
        layout.addWidget(self.hotkey_label)

        self.hotkey_input = QLineEdit(self)
        self.hotkey_input.setText(self.hotkey)
        layout.addWidget(self.hotkey_input)

        self.start_button = QPushButton('Set Hotkey', self)
        self.start_button.clicked.connect(self.set_hotkey)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Clicking', self)
        self.stop_button.clicked.connect(self.toggle_clicking)  # Connect stop button to toggle function
        layout.addWidget(self.stop_button)

        self.log_button = QPushButton('Show Click Log', self)
        self.log_button.clicked.connect(self.show_click_log)
        layout.addWidget(self.log_button)

        # New feature: Customizable Click Area
        self.click_area_label = QLabel('Custom Click Area: (x, y, width, height)', self)
        layout.addWidget(self.click_area_label)
        
        self.click_area_input = QLineEdit(self)
        layout.addWidget(self.click_area_input)

        # New feature: Randomized CPS Variation
        self.random_cps_checkbox = QCheckBox('Enable Random CPS Variation', self)
        self.random_cps_checkbox.setChecked(False)
        layout.addWidget(self.random_cps_checkbox)

        # New feature: Click Count Limit
        self.click_limit_label = QLabel('Set Click Limit:', self)
        layout.addWidget(self.click_limit_label)

        self.click_limit_input = QLineEdit(self)
        layout.addWidget(self.click_limit_input)

        # New feature: Pause and Resume Functionality
        self.pause_button = QPushButton('Pause Clicking', self)
        self.pause_button.clicked.connect(self.pause_clicking)
        layout.addWidget(self.pause_button)

        self.resume_button = QPushButton('Resume Clicking', self)
        self.resume_button.clicked.connect(self.resume_clicking)
        layout.addWidget(self.resume_button)

        self.setLayout(layout)
        self.setWindowTitle('Legacy Clicker')
        self.setGeometry(300, 300, 300, 400)

        # Additional Feature: Add animations and theme changes
        self.setStyleSheet("background-color: lightblue; color: darkblue; font-size: 12pt;")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        self.show()

    def update_left_cps(self, value):
        self.left_cps = value
        self.left_cps_label.setText(f'Left Click CPS: {value}')

    def set_hotkey(self):
        try:
            if self.hotkey_set:
                keyboard.remove_hotkey(self.hotkey)
            self.hotkey = self.hotkey_input.text()
            if not self.hotkey:
                raise ValueError('Hotkey cannot be empty')
            keyboard.add_hotkey(self.hotkey, self.toggle_clicking)
            self.hotkey_set = True
            self.hotkey_label.setText(f'Set Hotkey: {self.hotkey}')
        except ValueError as e:
            self.hotkey_label.setText(f'Invalid Hotkey: {self.hotkey}')

    def toggle_clicking(self):
        if self.left_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if not self.left_clicking:
            self.left_clicking = True
            threading.Thread(target=self.left_click_thread, daemon=True).start()

    def stop_clicking(self):
        self.left_clicking = False

    def pause_clicking(self):
        self.left_clicking = False

    def resume_clicking(self):
        if not self.left_clicking:
            self.left_clicking = True
            threading.Thread(target=self.left_click_thread, daemon=True).start()

    def left_click_thread(self):
        interval = 1 / self.left_cps
        click_count = 0
        
        while self.left_clicking:
            start_time = time.perf_counter()
            
            # New feature: Customizable Click Area
            if self.click_area_input.text():
                x, y, width, height = map(int, self.click_area_input.text().split(','))
                pyautogui.click(x=random.randint(x, x + width), y=random.randint(y, y + height), button='left')
            else:
                pyautogui.click(button='left')
            
            self.log_click()
            elapsed = time.perf_counter() - start_time
            
            # New feature: Randomized CPS Variation
            if self.random_cps_checkbox.isChecked():
                interval = random.uniform(interval * 0.8, interval * 1.2)
            
            if elapsed < interval:
                time.sleep(interval - elapsed)

            click_count += 1

            # New feature: Click Count Limit
            if self.click_limit_input.text() and click_count >= int(self.click_limit_input.text()):
                self.stop_clicking()

    def log_click(self):
        self.click_log.append(time.strftime("%Y-%m-%d %H:%M:%S"))

    def show_click_log(self):
        log_text = "\n".join(self.click_log[-10:])  # Show last 10 clicks
        QMessageBox.information(self, "Click Log", log_text if log_text else "No clicks logged yet.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LegacyClicker()
    sys.exit(app.exec_())
