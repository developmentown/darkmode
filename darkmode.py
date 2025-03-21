import sys
import winreg
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class DarkModeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Dark Mode Toggle")
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Koyu Mod Durumu: Bilinmiyor")
        layout.addWidget(self.label)
        
        self.toggle_button = QPushButton("Koyu Modu Aç")
        self.toggle_button.clicked.connect(self.toggle_dark_mode)
        layout.addWidget(self.toggle_button)
        
        self.setLayout(layout)
        self.update_ui()

    def get_dark_mode_status(self):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0
        except Exception:
            return None

    def set_dark_mode(self, enable):
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0 if enable else 1)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0 if enable else 1)
        except Exception as e:
            print(f"Hata: {e}")

    def toggle_dark_mode(self):
        current_status = self.get_dark_mode_status()
        if current_status is not None:
            self.set_dark_mode(not current_status)
        self.update_ui()

    def update_ui(self):
        status = self.get_dark_mode_status()
        if status is None:
            self.label.setText("Durum okunamıyor")
        elif status:
            self.label.setText("Koyu Mod Açık")
            self.toggle_button.setText("Koyu Modu Kapat")
        else:
            self.label.setText("Koyu Mod Kapalı")
            self.toggle_button.setText("Koyu Modu Aç")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DarkModeApp()
    window.show()
    sys.exit(app.exec())
