from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon

class HomePage(QWidget):
    """首页类，显示应用程序的基本信息和快速入口"""
    
    # 自定义信号
    start_learning_signal = Signal()  # 开始学习信号
    start_review_signal = Signal()    # 开始复习信号
    start_test_signal = Signal()      # 开始测验信号
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 添加欢迎标题
        welcome_label = QLabel("欢迎使用 VocabWindow")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # 添加应用描述
        description_label = QLabel("VocabWindow 是一款桌面悬浮单词学习软件，帮助您随时随地学习和记忆单词。")
        description_label.setObjectName("descriptionLabel")
        description_label.setFont(QFont("Arial", 12))
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        main_layout.addWidget(description_label)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # 添加功能卡片区域
        cards_widget = QWidget()
        cards_layout = QHBoxLayout(cards_widget)
        cards_layout.setSpacing(15)
        
        # 学习卡片
        learn_card = self.create_feature_card(
            "学习单词",
            "开始学习新单词，按照您的设置进行学习。",
            "开始学习"
        )
        
        # 复习卡片
        review_card = self.create_feature_card(
            "复习单词",
            "复习已学过的单词，巩固记忆。",
            "开始复习"
        )
        
        # 测验卡片
        test_card = self.create_feature_card(
            "单词测验",
            "测试您对已学单词的掌握程度。",
            "开始测验"
        )
        
        # 将卡片添加到布局
        cards_layout.addWidget(learn_card)
        cards_layout.addWidget(review_card)
        cards_layout.addWidget(test_card)
        
        main_layout.addWidget(cards_widget)
        main_layout.addStretch(1)
        
        # 添加今日统计区域
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_frame.setFrameShape(QFrame.StyledPanel)
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("今日学习统计")
        stats_title.setObjectName("statsTitle")
        stats_title.setFont(QFont("Arial", 14, QFont.Bold))
        stats_layout.addWidget(stats_title)
        
        # 统计数据
        stats_data_layout = QHBoxLayout()
        
        # 新学单词
        new_words_layout = QVBoxLayout()
        new_words_count = QLabel("0")
        new_words_count.setObjectName("statsCount")
        new_words_count.setAlignment(Qt.AlignCenter)
        new_words_count.setFont(QFont("Arial", 24, QFont.Bold))
        new_words_label = QLabel("新学单词")
        new_words_label.setAlignment(Qt.AlignCenter)
        new_words_layout.addWidget(new_words_count)
        new_words_layout.addWidget(new_words_label)
        
        # 复习单词
        review_words_layout = QVBoxLayout()
        review_words_count = QLabel("0")
        review_words_count.setObjectName("statsCount")
        review_words_count.setAlignment(Qt.AlignCenter)
        review_words_count.setFont(QFont("Arial", 24, QFont.Bold))
        review_words_label = QLabel("复习单词")
        review_words_label.setAlignment(Qt.AlignCenter)
        review_words_layout.addWidget(review_words_count)
        review_words_layout.addWidget(review_words_label)
        
        # 测验单词
        test_words_layout = QVBoxLayout()
        test_words_count = QLabel("0")
        test_words_count.setObjectName("statsCount")
        test_words_count.setAlignment(Qt.AlignCenter)
        test_words_count.setFont(QFont("Arial", 24, QFont.Bold))
        test_words_label = QLabel("测验单词")
        test_words_label.setAlignment(Qt.AlignCenter)
        test_words_layout.addWidget(test_words_count)
        test_words_layout.addWidget(test_words_label)
        
        # 将统计数据添加到布局
        stats_data_layout.addLayout(new_words_layout)
        stats_data_layout.addLayout(review_words_layout)
        stats_data_layout.addLayout(test_words_layout)
        
        stats_layout.addLayout(stats_data_layout)
        
        main_layout.addWidget(stats_frame)
        
        # 设置样式表
        self.set_stylesheet()
    
    def create_feature_card(self, title, description, button_text):
        """创建功能卡片"""
        card = QFrame()
        card.setObjectName("featureCard")
        card.setFrameShape(QFrame.StyledPanel)
        
        card_layout = QVBoxLayout(card)
        
        # 添加标题
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        # 添加描述
        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        
        # 添加按钮
        button = QPushButton(button_text)
        button.setObjectName("cardButton")
        button.setProperty("title", title)  # 用于在点击事件中识别按钮
        
        # 将控件添加到布局
        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)
        card_layout.addStretch(1)
        card_layout.addWidget(button)
        
        return card
    
    def setup_connections(self):
        """设置信号连接"""
        # 查找所有卡片按钮并连接点击事件
        for button in self.findChildren(QPushButton, "cardButton"):
            button.clicked.connect(self.on_card_button_clicked)
    
    def on_card_button_clicked(self):
        """卡片按钮点击事件处理"""
        button = self.sender()
        title = button.property("title")
        
        if title == "学习单词":
            self.start_learning_signal.emit()
        elif title == "复习单词":
            self.start_review_signal.emit()
        elif title == "单词测验":
            self.start_test_signal.emit()
    
    def set_stylesheet(self):
        """设置样式表"""
        self.setStyleSheet("""
            #welcomeLabel {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            #descriptionLabel {
                color: #7f8c8d;
                margin-bottom: 20px;
            }
            
            #featureCard {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                min-height: 200px;
            }
            
            #cardTitle {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            #cardDescription {
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            
            #cardButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            
            #cardButton:hover {
                background-color: #2980b9;
            }
            
            #statsFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
            
            #statsTitle {
                color: #2c3e50;
                margin-bottom: 15px;
            }
            
            #statsCount {
                color: #3498db;
                font-size: 24px;
                font-weight: bold;
            }
        """)