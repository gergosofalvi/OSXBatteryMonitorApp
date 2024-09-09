import sys
import subprocess
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QHBoxLayout

class BatteryMonitorApp(QWidget):
    def __init__(self):
        super().__init__()

        # Alapértelmezett téma: dark mode
        self.is_dark_mode = True
        self.init_ui()

        # Timer a töltési információk frissítéséhez
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wattage)
        self.timer.start(100)  # 0.1 másodpercenként frissít

    def init_ui(self):
        self.setWindowTitle('Battery Monitor')
        self.setGeometry(300, 300, 400, 250)

        # Betöltési címke
        self.wattage_label = QLabel('Wattage: -- W', self)
        self.wattage_label.setAlignment(Qt.AlignCenter)
        self.wattage_label.setFont(QFont('Arial', 24))

        # Töltés animáció (QProgressBar)
        self.charge_progress = QProgressBar(self)
        self.charge_progress.setMinimum(0)
        self.charge_progress.setMaximum(140)
        self.charge_progress.setValue(0)
        self.charge_progress.setTextVisible(False)

        # 0W és 140W címkék
        self.min_watt_label = QLabel('0W', self)
        self.max_watt_label = QLabel('140W', self)

        # Emoji gomb a téma váltáshoz
        self.theme_button = QPushButton('🌙', self)  # Holdacska emoji dark mode-hoz
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.clicked.connect(self.toggle_theme)

        # Emoji gomb jobb felső sarokba helyezése
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.theme_button)
        header_layout.addStretch()  # Gombot jobbra igazítja

        # Layout elrendezése
        layout = QVBoxLayout()
        layout.addLayout(header_layout)
        layout.addWidget(self.wattage_label)

        # Hozzáadjuk a 0W és 140W címkéket a progress bar mellé
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.min_watt_label)
        progress_layout.addWidget(self.charge_progress)
        progress_layout.addWidget(self.max_watt_label)

        layout.addLayout(progress_layout)
        self.setLayout(layout)

        # Alapértelmezett dark mode beállítása
        self.apply_dark_mode()

    def toggle_theme(self):
        if self.is_dark_mode:
            self.apply_light_mode()
            self.theme_button.setText('🌞')  # Napocska emoji világos módhoz
        else:
            self.apply_dark_mode()
            self.theme_button.setText('🌙')  # Holdacska emoji dark módhoz

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: 1px solid #777777;
            }
            QProgressBar {
                background-color: #555555;
                border: 1px solid #777777;
            }
        """)
        self.is_dark_mode = True

    def apply_light_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                color: #000000;
            }
            QPushButton {
                background-color: #DDDDDD;
                color: #000000;
                border: 1px solid #AAAAAA;
            }
            QProgressBar {
                background-color: #DDDDDD;
                border: 1px solid #AAAAAA;
            }
        """)
        self.is_dark_mode = False

    def update_wattage(self):
        wattage = self.get_wattage()
        if wattage is not None:
            wattage_value = float(wattage)
            self.wattage_label.setText(f'Wattage: {wattage_value} W')
            self.charge_progress.setValue(int(wattage_value))

            # Színkód beállítása a töltés szintje alapján
            if wattage_value > 60:
                self.charge_progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")
            elif 20 < wattage_value <= 60:
                self.charge_progress.setStyleSheet("QProgressBar::chunk { background-color: yellow; }")
            else:
                self.charge_progress.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        else:
            self.wattage_label.setText('No charging, plug in the charger.')
            self.charge_progress.setValue(0)
            self.charge_progress.setStyleSheet("QProgressBar::chunk { background-color: grey; }")

    def get_wattage(self):
        try:
            result = subprocess.check_output(['/usr/sbin/system_profiler', 'SPPowerDataType']).decode('utf-8')
            for line in result.split('\n'):
                if 'Wattage' in line:
                    # Visszaadja a watt értéket
                    wattage_value = line.split(':')[-1].strip().replace('W', '').strip()
                    return wattage_value
            return None
        except subprocess.CalledProcessError as e:
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = BatteryMonitorApp()
    monitor.show()
    sys.exit(app.exec_())
