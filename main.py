import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QStackedWidget, QFileDialog, QSlider, QCheckBox, QComboBox, QLineEdit, QMessageBox
from PySide6.QtCore import Qt, QPoint, QSize, QTimer, Signal as pyqtSignal, QEvent
from PySide6.QtGui import QFont, QIcon, QCursor

from ui.main_window import MainWindow
from utils.config_manager import ConfigManager

def main():
    # 确保配置目录存在
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # 初始化应用程序
    app = QApplication(sys.argv)
    app.setApplicationName("VocabWindow")
    app.setStyle("Fusion")  # 使用Fusion风格，跨平台一致性好
    
    # 加载配置
    config_manager = ConfigManager()
    
    # 创建主窗口
    main_window = MainWindow(config_manager)
    main_window.show()
    
    # 运行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()