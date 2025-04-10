import sys
import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QSizeGrip, QApplication)
from PySide6.QtCore import Qt, QPoint, QSize, Signal, QEvent
from PySide6.QtGui import QFont, QIcon, QCursor
import pyttsx3

class FloatingWindow(QWidget):
    """悬浮窗类，用于显示单词和相关操作"""
    
    # 自定义信号
    closed = Signal()  # 窗口关闭信号
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.config_manager = config_manager
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowOpacity(0.95)  # 设置窗口透明度
        
        # 初始化TTS引擎
        self.tts_engine = pyttsx3.init()
        
        # 窗口拖动相关变量
        self.dragging = False
        self.drag_position = QPoint()
        
        # 当前模式：学习模式或复习模式
        self.mode = "learn"  # "learn" 或 "review"
        
        # 当前单词索引
        self.current_index = 0
        
        # 单词列表（示例数据，实际应从单词本加载）
        self.words = [
            {"word": "apple", "meaning": "n. 苹果"},
            {"word": "banana", "meaning": "n. 香蕉"},
            {"word": "orange", "meaning": "n. 橙子; adj. 橙色的"},
        ]
        
        self.init_ui()
        self.setup_connections()
        
        # 加载配置
        self.load_config()
        
        # 显示第一个单词
        self.update_word_display()
    
    def init_ui(self):
        """初始化UI"""
        # 设置窗口大小
        self.resize(400, 250)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建标题栏
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(30)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(5, 0, 5, 0)
        
        # 添加标题
        title_label = QLabel("VocabWindow")
        title_label.setObjectName("titleLabel")
        
        # 添加控制按钮
        self.pin_button = QPushButton("📌")
        self.pin_button.setObjectName("pinButton")
        self.pin_button.setToolTip("置顶窗口")
        self.pin_button.setCheckable(True)
        self.pin_button.setChecked(True)
        
        self.mode_button = QPushButton("复习模式")
        self.mode_button.setObjectName("modeButton")
        self.mode_button.setToolTip("切换学习/复习模式")
        
        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("closeButton")
        self.close_button.setToolTip("关闭窗口")
        
        # 将控件添加到标题栏布局
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self.pin_button)
        title_bar_layout.addWidget(self.mode_button)
        title_bar_layout.addWidget(self.close_button)
        
        # 创建内容区域
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setFrameShape(QFrame.StyledPanel)
        content_layout = QVBoxLayout(content_frame)
        
        # 单词显示区域
        self.word_label = QLabel()
        self.word_label.setObjectName("wordLabel")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setFont(QFont("Arial", 20, QFont.Bold))
        
        self.meaning_label = QLabel()
        self.meaning_label.setObjectName("meaningLabel")
        self.meaning_label.setAlignment(Qt.AlignCenter)
        self.meaning_label.setFont(QFont("Arial", 14))
        
        # 复习模式按钮区域
        self.review_buttons_widget = QWidget()
        review_buttons_layout = QHBoxLayout(self.review_buttons_widget)
        
        self.know_button = QPushButton("认识")
        self.know_button.setObjectName("knowButton")
        
        self.dont_know_button = QPushButton("不认识")
        self.dont_know_button.setObjectName("dontKnowButton")
        
        review_buttons_layout.addWidget(self.know_button)
        review_buttons_layout.addWidget(self.dont_know_button)
        
        # 将单词区域添加到内容布局
        content_layout.addWidget(self.word_label)
        content_layout.addWidget(self.meaning_label)
        content_layout.addWidget(self.review_buttons_widget)
        
        # 创建操作按钮区域
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加操作按钮
        self.speak_button = QPushButton("🔊")
        self.speak_button.setObjectName("speakButton")
        self.speak_button.setToolTip("朗读单词")
        
        self.prev_button = QPushButton("◀")
        self.prev_button.setObjectName("prevButton")
        self.prev_button.setToolTip("上一个单词")
        
        self.next_button = QPushButton("▶")
        self.next_button.setObjectName("nextButton")
        self.next_button.setToolTip("下一个单词")
        
        self.skip_button = QPushButton("跳过")
        self.skip_button.setObjectName("skipButton")
        self.skip_button.setToolTip("跳过该单词")
        
        self.favorite_button = QPushButton("★")
        self.favorite_button.setObjectName("favoriteButton")
        self.favorite_button.setToolTip("收藏该单词")
        self.favorite_button.setCheckable(True)
        
        # 将按钮添加到布局
        buttons_layout.addWidget(self.speak_button)
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addWidget(self.skip_button)
        buttons_layout.addWidget(self.favorite_button)
        
        # 将各部分添加到主布局
        main_layout.addWidget(title_bar)
        main_layout.addWidget(content_frame, 1)  # 1表示拉伸因子
        main_layout.addWidget(buttons_widget)
        
        # 添加大小调整手柄
        size_grip = QSizeGrip(self)
        main_layout.addWidget(size_grip, 0, Qt.AlignBottom | Qt.AlignRight)
        
        # 设置样式表
        self.set_stylesheet()
        
        # 默认为学习模式
        self.set_mode("learn")
    
    def setup_connections(self):
        """设置信号连接"""
        # 标题栏按钮
        self.pin_button.clicked.connect(self.toggle_pin)
        self.mode_button.clicked.connect(self.toggle_mode)
        self.close_button.clicked.connect(self.close)
        
        # 操作按钮
        self.speak_button.clicked.connect(self.speak_word)
        self.prev_button.clicked.connect(self.show_prev_word)
        self.next_button.clicked.connect(self.show_next_word)
        self.skip_button.clicked.connect(self.skip_word)
        self.favorite_button.clicked.connect(self.toggle_favorite)
        
        # 复习模式按钮
        self.know_button.clicked.connect(self.mark_as_known)
        self.dont_know_button.clicked.connect(self.mark_as_unknown)
    
    def set_stylesheet(self):
        """设置样式表"""
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
            }
            #titleBar {
                background-color: #2c3e50;
                color: white;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            #titleLabel {
                color: white;
                font-weight: bold;
            }
            #pinButton, #modeButton, #closeButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 2px;
                font-size: 14px;
            }
            #pinButton:hover, #modeButton:hover, #closeButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 3px;
            }
            #closeButton:hover {
                background-color: #e74c3c;
            }
            #contentFrame {
                background-color: white;
                border-radius: 5px;
                padding: 10px;
            }
            #wordLabel {
                color: #2c3e50;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            #meaningLabel {
                color: #34495e;
                font-size: 16px;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            #knowButton {
                background-color: #2ecc71;
            }
            #knowButton:hover {
                background-color: #27ae60;
            }
            #dontKnowButton {
                background-color: #e74c3c;
            }
            #dontKnowButton:hover {
                background-color: #c0392b;
            }
            #favoriteButton:checked {
                background-color: #f1c40f;
            }
        """)
    
    def load_config(self):
        """加载配置"""
        # 从配置管理器加载窗口位置和大小
        # 这里使用默认值，实际应用中应从配置文件加载
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = screen_geometry.width() - self.width() - 20
        y = 100
        self.move(x, y)
    
    def update_word_display(self):
        """更新单词显示"""
        if 0 <= self.current_index < len(self.words):
            current_word = self.words[self.current_index]
            self.word_label.setText(current_word["word"])
            
            # 在学习模式下显示含义，复习模式下隐藏含义
            if self.mode == "learn":
                self.meaning_label.setText(current_word["meaning"])
            else:
                self.meaning_label.setText("")
    
    def set_mode(self, mode):
        """设置模式（学习或复习）"""
        self.mode = mode
        if mode == "learn":
            self.mode_button.setText("复习模式")
            self.review_buttons_widget.hide()
            self.meaning_label.show()
        else:  # review mode
            self.mode_button.setText("学习模式")
            self.review_buttons_widget.show()
            self.meaning_label.hide()
        
        # 更新单词显示
        self.update_word_display()
    
    def toggle_mode(self):
        """切换模式"""
        if self.mode == "learn":
            self.set_mode("review")
        else:
            self.set_mode("learn")
    
    def toggle_pin(self):
        """切换窗口置顶状态"""
        flags = self.windowFlags()
        if self.pin_button.isChecked():
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()  # 需要重新显示窗口以应用新的标志
    
    def speak_word(self):
        """朗读当前单词"""
        if 0 <= self.current_index < len(self.words):
            word = self.words[self.current_index]["word"]
            self.tts_engine.say(word)
            self.tts_engine.runAndWait()
    
    def show_prev_word(self):
        """显示上一个单词"""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_word_display()
    
    def show_next_word(self):
        """显示下一个单词"""
        if self.current_index < len(self.words) - 1:
            self.current_index += 1
            self.update_word_display()
    
    def skip_word(self):
        """跳过当前单词"""
        # 在实际应用中，应将该单词标记为跳过
        self.show_next_word()
    
    def toggle_favorite(self):
        """切换收藏状态"""
        # 在实际应用中，应将收藏状态保存到数据库
        pass
    
    def mark_as_known(self):
        """标记为认识"""
        # 在实际应用中，应更新单词的学习状态
        self.show_next_word()
    
    def mark_as_unknown(self):
        """标记为不认识"""
        # 在实际应用中，应更新单词的学习状态
        # 显示单词含义
        if 0 <= self.current_index < len(self.words):
            self.meaning_label.setText(self.words[self.current_index]["meaning"])
            self.meaning_label.show()
    
    def mousePressEvent(self, event):
        """鼠标按下事件处理"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件处理"""
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件处理"""
        self.dragging = False
    
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 发送关闭信号
        self.closed.emit()
        event.accept()