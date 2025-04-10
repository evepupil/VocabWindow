import sys
import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QListWidget, QStackedWidget, 
                             QFileDialog, QSlider, QCheckBox, QComboBox, QLineEdit, 
                             QMessageBox, QListWidgetItem, QFrame)
from PySide6.QtCore import Qt, QSize, Signal as pyqtSignal
from PySide6.QtGui import QFont, QIcon

from ui.floating_window import FloatingWindow
from ui.home_page import HomePage
from ui.vocabulary_page import VocabularyPage
from ui.settings_page import SettingsPage

class MainWindow(QMainWindow):
    """主窗口类，包含左侧菜单和右侧内容区域"""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.floating_window = None
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化UI"""
        # 设置窗口标题和大小
        self.setWindowTitle("VocabWindow - 桌面悬浮单词学习")
        self.resize(900, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建左侧菜单区域
        self.menu_widget = QWidget()
        self.menu_widget.setObjectName("menuWidget")
        self.menu_widget.setFixedWidth(200)
        menu_layout = QVBoxLayout(self.menu_widget)
        menu_layout.setContentsMargins(10, 20, 10, 20)
        menu_layout.setSpacing(10)
        
        # 添加应用标题
        app_title = QLabel("VocabWindow")
        app_title.setObjectName("appTitle")
        app_title.setAlignment(Qt.AlignCenter)
        app_title.setFont(QFont("Arial", 16, QFont.Bold))
        menu_layout.addWidget(app_title)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        menu_layout.addWidget(separator)
        menu_layout.addSpacing(20)
        
        # 创建菜单列表
        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menuList")
        self.menu_list.setFont(QFont("Arial", 12))
        self.menu_list.setFrameShape(QFrame.NoFrame)
        self.menu_list.setSpacing(5)
        
        # 添加菜单项
        menu_items = ["首页", "单词本", "系统设置"]
        for item in menu_items:
            list_item = QListWidgetItem(item)
            list_item.setTextAlignment(Qt.AlignCenter)
            self.menu_list.addItem(list_item)
        
        menu_layout.addWidget(self.menu_list)
        menu_layout.addStretch()
        
        # 添加启动悬浮窗按钮
        self.start_floating_btn = QPushButton("启动悬浮窗")
        self.start_floating_btn.setObjectName("startFloatingBtn")
        self.start_floating_btn.setFont(QFont("Arial", 12))
        self.start_floating_btn.setMinimumHeight(40)
        menu_layout.addWidget(self.start_floating_btn)
        
        # 创建右侧内容区域
        self.content_widget = QStackedWidget()
        self.content_widget.setObjectName("contentWidget")
        
        # 创建各个页面
        self.home_page = HomePage(self.config_manager)
        self.vocabulary_page = VocabularyPage(self.config_manager)
        self.settings_page = SettingsPage(self.config_manager)
        
        # 将页面添加到堆叠部件中
        self.content_widget.addWidget(self.home_page)
        self.content_widget.addWidget(self.vocabulary_page)
        self.content_widget.addWidget(self.settings_page)
        
        # 将左侧菜单和右侧内容添加到主布局
        main_layout.addWidget(self.menu_widget)
        main_layout.addWidget(self.content_widget)
        
        # 设置样式表
        self.set_stylesheet()
        
        # 默认选中首页
        self.menu_list.setCurrentRow(0)
    
    def setup_connections(self):
        """设置信号连接"""
        # 菜单项切换页面
        self.menu_list.currentRowChanged.connect(self.content_widget.setCurrentIndex)
        
        # 启动悬浮窗按钮
        self.start_floating_btn.clicked.connect(self.toggle_floating_window)
    
    def toggle_floating_window(self):
        """切换悬浮窗的显示状态"""
        if self.floating_window is None or not self.floating_window.isVisible():
            # 创建并显示悬浮窗
            if self.floating_window is None:
                self.floating_window = FloatingWindow(self.config_manager)
                self.floating_window.closed.connect(self.on_floating_window_closed)
            self.floating_window.show()
            self.start_floating_btn.setText("关闭悬浮窗")
        else:
            # 关闭悬浮窗
            self.floating_window.close()
            self.start_floating_btn.setText("启动悬浮窗")
    
    def on_floating_window_closed(self):
        """悬浮窗关闭事件处理"""
        self.start_floating_btn.setText("启动悬浮窗")
    
    def set_stylesheet(self):
        """设置样式表"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #333333;
            }
            #menuWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: none;
            }
            #appTitle {
                color: #ecf0f1;
                padding: 10px;
            }
            #menuList {
                background-color: transparent;
                color: #ecf0f1;
                border: none;
            }
            #menuList::item {
                padding: 10px;
                border-radius: 5px;
            }
            #menuList::item:selected {
                background-color: #34495e;
            }
            #menuList::item:hover {
                background-color: #34495e;
            }
            #startFloatingBtn {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            #startFloatingBtn:hover {
                background-color: #2980b9;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
    
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 关闭悬浮窗
        if self.floating_window is not None and self.floating_window.isVisible():
            self.floating_window.close()
        event.accept()