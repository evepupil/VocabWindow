from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QScrollArea, QListWidget, QListWidgetItem,
                             QFileDialog, QMessageBox, QTabWidget, QSplitter)
from PySide6.QtCore import Qt, Signal as pyqtSignal
from PySide6.QtGui import QFont, QIcon
import os
import json

class VocabularyPage(QWidget):
    """单词本页面，用于管理单词本和查看单词列表"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        
        # 当前选中的单词本
        self.current_vocabulary = None
        
        # 单词本列表（示例数据，实际应从配置加载）
        self.vocabularies = []
        
        self.init_ui()
        self.setup_connections()
        self.load_vocabularies()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 添加页面标题
        title_label = QLabel("单词本管理")
        title_label.setObjectName("pageTitle")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # 创建分割器，左侧为单词本列表，右侧为单词列表
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧单词本管理区域
        vocab_management_widget = QWidget()
        vocab_management_layout = QVBoxLayout(vocab_management_widget)
        vocab_management_layout.setContentsMargins(0, 0, 0, 0)
        
        # 单词本列表标题
        vocab_list_title = QLabel("我的单词本")
        vocab_list_title.setObjectName("sectionTitle")
        vocab_list_title.setFont(QFont("Arial", 14, QFont.Bold))
        vocab_management_layout.addWidget(vocab_list_title)
        
        # 单词本列表
        self.vocab_list = QListWidget()
        self.vocab_list.setObjectName("vocabList")
        vocab_management_layout.addWidget(self.vocab_list)
        
        # 单词本操作按钮
        vocab_buttons_layout = QHBoxLayout()
        
        self.import_vocab_btn = QPushButton("导入单词本")
        self.import_vocab_btn.setObjectName("importVocabBtn")
        
        self.delete_vocab_btn = QPushButton("删除单词本")
        self.delete_vocab_btn.setObjectName("deleteVocabBtn")
        self.delete_vocab_btn.setEnabled(False)  # 初始禁用
        
        vocab_buttons_layout.addWidget(self.import_vocab_btn)
        vocab_buttons_layout.addWidget(self.delete_vocab_btn)
        
        vocab_management_layout.addLayout(vocab_buttons_layout)
        
        # 右侧单词列表区域
        word_list_widget = QWidget()
        word_list_layout = QVBoxLayout(word_list_widget)
        word_list_layout.setContentsMargins(0, 0, 0, 0)
        
        # 单词列表标题
        self.word_list_title = QLabel("单词列表")
        self.word_list_title.setObjectName("sectionTitle")
        self.word_list_title.setFont(QFont("Arial", 14, QFont.Bold))
        word_list_layout.addWidget(self.word_list_title)
        
        # 创建选项卡部件
        self.tabs = QTabWidget()
        
        # 全部单词选项卡
        self.all_words_tab = QListWidget()
        self.all_words_tab.setObjectName("wordList")
        
        # 已学单词选项卡
        self.learned_words_tab = QListWidget()
        self.learned_words_tab.setObjectName("wordList")
        
        # 未学单词选项卡
        self.unlearned_words_tab = QListWidget()
        self.unlearned_words_tab.setObjectName("wordList")
        
        # 跳过单词选项卡
        self.skipped_words_tab = QListWidget()
        self.skipped_words_tab.setObjectName("wordList")
        
        # 今日任务选项卡
        self.today_words_tab = QListWidget()
        self.today_words_tab.setObjectName("wordList")
        
        # 将选项卡添加到选项卡部件
        self.tabs.addTab(self.all_words_tab, "全部单词")
        self.tabs.addTab(self.learned_words_tab, "已学单词")
        self.tabs.addTab(self.unlearned_words_tab, "未学单词")
        self.tabs.addTab(self.skipped_words_tab, "跳过单词")
        self.tabs.addTab(self.today_words_tab, "今日任务")
        
        word_list_layout.addWidget(self.tabs)
        
        # 单词操作按钮
        word_buttons_layout = QHBoxLayout()
        
        self.start_learning_btn = QPushButton("开始学习")
        self.start_learning_btn.setObjectName("startLearningBtn")
        self.start_learning_btn.setEnabled(False)  # 初始禁用
        
        self.start_review_btn = QPushButton("开始复习")
        self.start_review_btn.setObjectName("startReviewBtn")
        self.start_review_btn.setEnabled(False)  # 初始禁用
        
        word_buttons_layout.addWidget(self.start_learning_btn)
        word_buttons_layout.addWidget(self.start_review_btn)
        
        word_list_layout.addLayout(word_buttons_layout)
        
        # 将左右两侧添加到分割器
        splitter.addWidget(vocab_management_widget)
        splitter.addWidget(word_list_widget)
        
        # 设置分割器的初始大小
        splitter.setSizes([300, 600])
        
        main_layout.addWidget(splitter)
        
        # 设置样式表
        self.set_stylesheet()
    
    def setup_connections(self):
        """设置信号连接"""
        # 单词本列表选择变化
        self.vocab_list.currentItemChanged.connect(self.on_vocabulary_selected)
        
        # 单词本操作按钮
        self.import_vocab_btn.clicked.connect(self.import_vocabulary)
        self.delete_vocab_btn.clicked.connect(self.delete_vocabulary)
        
        # 单词操作按钮
        self.start_learning_btn.clicked.connect(self.start_learning)
        self.start_review_btn.clicked.connect(self.start_review)
    
    def load_vocabularies(self):
        """加载单词本列表"""
        # 在实际应用中，应从配置文件或数据库加载单词本列表
        # 这里使用示例数据
        self.vocabularies = [
            {"name": "CET-4 核心词汇", "path": "data/cet4.json", "count": 2200},
            {"name": "CET-6 核心词汇", "path": "data/cet6.json", "count": 2500},
            {"name": "TOEFL 核心词汇", "path": "data/toefl.json", "count": 5000},
        ]
        
        # 更新单词本列表
        self.update_vocabulary_list()
    
    def update_vocabulary_list(self):
        """更新单词本列表"""
        self.vocab_list.clear()
        
        for vocab in self.vocabularies:
            item = QListWidgetItem(f"{vocab['name']} ({vocab['count']}词)")
            item.setData(Qt.UserRole, vocab)  # 存储单词本数据
            self.vocab_list.addItem(item)
    
    def on_vocabulary_selected(self, current, previous):
        """单词本选择变化事件处理"""
        if current is not None:
            # 获取选中的单词本数据
            self.current_vocabulary = current.data(Qt.UserRole)
            
            # 更新标题
            self.word_list_title.setText(f"单词列表 - {self.current_vocabulary['name']}")
            
            # 加载单词列表
            self.load_word_list()
            
            # 启用相关按钮
            self.delete_vocab_btn.setEnabled(True)
            self.start_learning_btn.setEnabled(True)
            self.start_review_btn.setEnabled(True)
        else:
            self.current_vocabulary = None
            self.word_list_title.setText("单词列表")
            
            # 清空单词列表
            self.clear_word_lists()
            
            # 禁用相关按钮
            self.delete_vocab_btn.setEnabled(False)
            self.start_learning_btn.setEnabled(False)
            self.start_review_btn.setEnabled(False)
    
    def load_word_list(self):
        """加载单词列表"""
        # 清空所有选项卡
        self.clear_word_lists()
        
        # 在实际应用中，应从文件或数据库加载单词列表
        # 这里使用示例数据
        words = [
            {"word": "apple", "meaning": "n. 苹果", "status": "learned"},
            {"word": "banana", "meaning": "n. 香蕉", "status": "unlearned"},
            {"word": "orange", "meaning": "n. 橙子; adj. 橙色的", "status": "learned"},
            {"word": "grape", "meaning": "n. 葡萄", "status": "skipped"},
            {"word": "watermelon", "meaning": "n. 西瓜", "status": "unlearned"},
        ]
        
        # 更新各选项卡
        for word in words:
            # 添加到全部单词选项卡
            self.add_word_to_list(self.all_words_tab, word)
            
            # 根据状态添加到相应选项卡
            if word["status"] == "learned":
                self.add_word_to_list(self.learned_words_tab, word)
            elif word["status"] == "unlearned":
                self.add_word_to_list(self.unlearned_words_tab, word)
            elif word["status"] == "skipped":
                self.add_word_to_list(self.skipped_words_tab, word)
            
            # 添加到今日任务（示例：所有未学单词）
            if word["status"] == "unlearned":
                self.add_word_to_list(self.today_words_tab, word)
    
    def add_word_to_list(self, list_widget, word):
        """将单词添加到列表部件"""
        item = QListWidgetItem(f"{word['word']} - {word['meaning']}")
        item.setData(Qt.UserRole, word)  # 存储单词数据
        list_widget.addItem(item)
    
    def clear_word_lists(self):
        """清空所有单词列表"""
        self.all_words_tab.clear()
        self.learned_words_tab.clear()
        self.unlearned_words_tab.clear()
        self.skipped_words_tab.clear()
        self.today_words_tab.clear()
    
    def import_vocabulary(self):
        """导入单词本"""
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入单词本",
            "",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # 在实际应用中，应解析文件并导入单词
                # 这里简单地添加到单词本列表
                file_name = os.path.basename(file_path)
                name, _ = os.path.splitext(file_name)
                
                # 创建新单词本
                new_vocab = {
                    "name": name,
                    "path": file_path,
                    "count": 100  # 示例数量
                }
                
                # 添加到单词本列表
                self.vocabularies.append(new_vocab)
                
                # 更新单词本列表
                self.update_vocabulary_list()
                
                # 选中新导入的单词本
                self.vocab_list.setCurrentRow(len(self.vocabularies) - 1)
                
                QMessageBox.information(self, "导入成功", f"成功导入单词本：{name}")
            except Exception as e:
                QMessageBox.critical(self, "导入失败", f"导入单词本失败：{str(e)}")
    
    def delete_vocabulary(self):
        """删除单词本"""
        if self.current_vocabulary is None:
            return
        
        # 确认删除
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除单词本 {self.current_vocabulary['name']} 吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 获取当前选中的索引
            current_index = self.vocab_list.currentRow()
            
            # 从列表中删除
            if 0 <= current_index < len(self.vocabularies):
                del self.vocabularies[current_index]
                
                # 更新单词本列表
                self.update_vocabulary_list()
                
                # 如果还有单词本，选中第一个
                if self.vocabularies:
                    self.vocab_list.setCurrentRow(0)
                else:
                    # 清空单词列表
                    self.clear_word_lists()
                    self.current_vocabulary = None
                    self.word_list_title.setText("单词列表")
                    
                    # 禁用相关按钮
                    self.delete_vocab_btn.setEnabled(False)
                    self.start_learning_btn.setEnabled(False)
                    self.start_review_btn.setEnabled(False)
    
    def start_learning(self):
        """开始学习"""
        if self.current_vocabulary is None:
            return
        
        # 在实际应用中，应启动悬浮窗并加载单词
        QMessageBox.information(
            self,
            "开始学习",
            f"开始学习单词本：{self.current_vocabulary['name']}"
        )
    
    def start_review(self):
        """开始复习"""
        if self.current_vocabulary is None:
            return
        
        # 在实际应用中，应启动悬浮窗并加载单词
        QMessageBox.information(
            self,
            "开始复习",
            f"开始复习单词本：{self.current_vocabulary['name']}"
        )
    
    def set_stylesheet(self):
        """设置样式表"""
        self.setStyleSheet("""
            #pageTitle {
                color: #2c3e50;
                margin-bottom: 20px;
            }
            
            #sectionTitle {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            #vocabList, #wordList {
                background-color: white;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #ddd;
            }
            
            #vocabList::item, #wordList::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            
            #vocabList::item:selected, #wordList::item:selected {
                background-color: #3498db;
                color: white;
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
            
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 8px 12px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border: 1px solid #ddd;
                border-bottom: none;
            }
        """)