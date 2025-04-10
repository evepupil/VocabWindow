from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QScrollArea, QSlider, QCheckBox, QComboBox,
                             QLineEdit, QGroupBox, QFormLayout, QSpinBox, QTabWidget)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon, QKeySequence

class SettingsPage(QWidget):
    """系统设置页面，用于配置应用程序的各种设置"""
    
    # 自定义信号
    settings_changed = Signal()  # 设置变更信号
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        
        self.init_ui()
        self.setup_connections()
        self.load_settings()
    
    def init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 添加页面标题
        title_label = QLabel("系统设置")
        title_label.setObjectName("pageTitle")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # 创建选项卡部件
        tabs = QTabWidget()
        
        # 创建各个设置选项卡
        general_tab = self.create_general_settings_tab()
        appearance_tab = self.create_appearance_settings_tab()
        review_tab = self.create_review_settings_tab()
        shortcut_tab = self.create_shortcut_settings_tab()
        
        # 将选项卡添加到选项卡部件
        tabs.addTab(general_tab, "常规设置")
        tabs.addTab(appearance_tab, "外观设置")
        tabs.addTab(review_tab, "复习策略")
        tabs.addTab(shortcut_tab, "快捷键设置")
        
        main_layout.addWidget(tabs)
        
        # 添加保存按钮
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.reset_btn = QPushButton("重置设置")
        self.reset_btn.setObjectName("resetBtn")
        
        self.save_btn = QPushButton("保存设置")
        self.save_btn.setObjectName("saveBtn")
        
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # 设置样式表
        self.set_stylesheet()
    
    def create_general_settings_tab(self):
        """创建常规设置选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建常规设置组
        general_group = QGroupBox("常规设置")
        general_layout = QFormLayout(general_group)
        
        # 每日学习目标
        self.daily_goal_spin = QSpinBox()
        self.daily_goal_spin.setRange(1, 500)
        self.daily_goal_spin.setValue(20)
        self.daily_goal_spin.setSuffix(" 词")
        general_layout.addRow("每日学习目标:", self.daily_goal_spin)
        
        # 自动启动悬浮窗
        self.auto_start_float_check = QCheckBox("启动程序时自动打开悬浮窗")
        general_layout.addRow("", self.auto_start_float_check)
        
        # 自动保存学习进度
        self.auto_save_check = QCheckBox("自动保存学习进度")
        self.auto_save_check.setChecked(True)
        general_layout.addRow("", self.auto_save_check)
        
        # 数据存储位置
        self.data_path_edit = QLineEdit()
        self.data_path_edit.setReadOnly(True)
        self.data_path_edit.setText("~/.vocabwindow/data")
        self.browse_data_path_btn = QPushButton("浏览...")
        data_path_layout = QHBoxLayout()
        data_path_layout.addWidget(self.data_path_edit)
        data_path_layout.addWidget(self.browse_data_path_btn)
        general_layout.addRow("数据存储位置:", data_path_layout)
        
        layout.addWidget(general_group)
        layout.addStretch()
        
        return tab
    
    def create_appearance_settings_tab(self):
        """创建外观设置选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建悬浮窗设置组
        float_group = QGroupBox("悬浮窗设置")
        float_layout = QFormLayout(float_group)
        
        # 悬浮窗大小
        float_size_layout = QHBoxLayout()
        self.float_width_spin = QSpinBox()
        self.float_width_spin.setRange(200, 800)
        self.float_width_spin.setValue(400)
        self.float_width_spin.setSuffix(" px")
        self.float_height_spin = QSpinBox()
        self.float_height_spin.setRange(150, 600)
        self.float_height_spin.setValue(250)
        self.float_height_spin.setSuffix(" px")
        float_size_layout.addWidget(QLabel("宽:"))
        float_size_layout.addWidget(self.float_width_spin)
        float_size_layout.addWidget(QLabel("高:"))
        float_size_layout.addWidget(self.float_height_spin)
        float_layout.addRow("悬浮窗大小:", float_size_layout)
        
        # 悬浮窗透明度
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setValue(95)
        self.opacity_value_label = QLabel("95%")
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_value_label)
        float_layout.addRow("悬浮窗透明度:", opacity_layout)
        
        # 单词字体大小
        self.word_font_size_slider = QSlider(Qt.Horizontal)
        self.word_font_size_slider.setRange(12, 36)
        self.word_font_size_slider.setValue(20)
        self.word_font_size_label = QLabel("20 px")
        word_font_layout = QHBoxLayout()
        word_font_layout.addWidget(self.word_font_size_slider)
        word_font_layout.addWidget(self.word_font_size_label)
        float_layout.addRow("单词字体大小:", word_font_layout)
        
        # 释义字体大小
        self.meaning_font_size_slider = QSlider(Qt.Horizontal)
        self.meaning_font_size_slider.setRange(10, 24)
        self.meaning_font_size_slider.setValue(14)
        self.meaning_font_size_label = QLabel("14 px")
        meaning_font_layout = QHBoxLayout()
        meaning_font_layout.addWidget(self.meaning_font_size_slider)
        meaning_font_layout.addWidget(self.meaning_font_size_label)
        float_layout.addRow("释义字体大小:", meaning_font_layout)
        
        # 鼠标穿透
        self.click_through_check = QCheckBox("启用鼠标点击穿透")
        self.click_through_check.setChecked(True)
        float_layout.addRow("", self.click_through_check)
        
        # 创建主题设置组
        theme_group = QGroupBox("主题设置")
        theme_layout = QFormLayout(theme_group)
        
        # 主题选择
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["默认主题", "暗色主题", "浅色主题", "高对比度主题"])
        theme_layout.addRow("应用主题:", self.theme_combo)
        
        layout.addWidget(float_group)
        layout.addWidget(theme_group)
        layout.addStretch()
        
        return tab
    
    def create_review_settings_tab(self):
        """创建复习策略选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建复习策略组
        review_group = QGroupBox("复习策略设置")
        review_layout = QFormLayout(review_group)
        
        # 复习策略选择
        self.review_strategy_combo = QComboBox()
        self.review_strategy_combo.addItems(["艾宾浩斯记忆曲线", "间隔重复系统", "自定义策略"])
        review_layout.addRow("复习策略:", self.review_strategy_combo)
        
        # 复习间隔设置（仅当选择自定义策略时可用）
        self.review_intervals_group = QGroupBox("自定义复习间隔（单位：天）")
        self.review_intervals_group.setEnabled(False)
        intervals_layout = QFormLayout(self.review_intervals_group)
        
        # 第一次复习间隔
        self.interval1_spin = QSpinBox()
        self.interval1_spin.setRange(1, 30)
        self.interval1_spin.setValue(1)
        self.interval1_spin.setSuffix(" 天")
        intervals_layout.addRow("第一次复习:", self.interval1_spin)
        
        # 第二次复习间隔
        self.interval2_spin = QSpinBox()
        self.interval2_spin.setRange(2, 60)
        self.interval2_spin.setValue(2)
        self.interval2_spin.setSuffix(" 天")
        intervals_layout.addRow("第二次复习:", self.interval2_spin)
        
        # 第三次复习间隔
        self.interval3_spin = QSpinBox()
        self.interval3_spin.setRange(4, 90)
        self.interval3_spin.setValue(4)
        self.interval3_spin.setSuffix(" 天")
        intervals_layout.addRow("第三次复习:", self.interval3_spin)
        
        # 第四次复习间隔
        self.interval4_spin = QSpinBox()
        self.interval4_spin.setRange(7, 120)
        self.interval4_spin.setValue(7)
        self.interval4_spin.setSuffix(" 天")
        intervals_layout.addRow("第四次复习:", self.interval4_spin)
        
        # 第五次复习间隔
        self.interval5_spin = QSpinBox()
        self.interval5_spin.setRange(15, 180)
        self.interval5_spin.setValue(15)
        self.interval5_spin.setSuffix(" 天")
        intervals_layout.addRow("第五次复习:", self.interval5_spin)
        
        # 学习模式设置
        self.learning_mode_group = QGroupBox("学习模式设置")
        learning_mode_layout = QFormLayout(self.learning_mode_group)
        
        # 新旧单词混合比例
        self.mix_ratio_slider = QSlider(Qt.Horizontal)
        self.mix_ratio_slider.setRange(0, 100)
        self.mix_ratio_slider.setValue(70)
        self.mix_ratio_label = QLabel("70% 新词 / 30% 复习")
        mix_ratio_layout = QHBoxLayout()
        mix_ratio_layout.addWidget(self.mix_ratio_slider)
        mix_ratio_layout.addWidget(self.mix_ratio_label)
        learning_mode_layout.addRow("新旧单词比例:", mix_ratio_layout)
        
        # 添加到布局
        review_layout.addWidget(self.review_intervals_group)
        review_group.setLayout(review_layout)
        
        layout.addWidget(review_group)
        layout.addWidget(self.learning_mode_group)
        layout.addStretch()
        
        return tab
    
    def create_shortcut_settings_tab(self):
        """创建快捷键设置选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建快捷键设置组
        shortcut_group = QGroupBox("快捷键设置")
        shortcut_layout = QFormLayout(shortcut_group)
        
        # 显示/隐藏悬浮窗
        self.toggle_float_shortcut = QLineEdit("Ctrl+Space")
        self.toggle_float_shortcut.setReadOnly(True)
        shortcut_layout.addRow("显示/隐藏悬浮窗:", self.toggle_float_shortcut)
        
        # 下一个单词
        self.next_word_shortcut = QLineEdit("Ctrl+Right")
        self.next_word_shortcut.setReadOnly(True)
        shortcut_layout.addRow("下一个单词:", self.next_word_shortcut)
        
        # 上一个单词
        self.prev_word_shortcut = QLineEdit("Ctrl+Left")
        self.prev_word_shortcut.setReadOnly(True)
        shortcut_layout.addRow("上一个单词:", self.prev_word_shortcut)
        
        # 朗读单词
        self.speak_word_shortcut = QLineEdit("Ctrl+S")
        self.speak_word_shortcut.setReadOnly(True)
        shortcut_layout.addRow("朗读单词:", self.speak_word_shortcut)
        
        # 切换学习/复习模式
        self.toggle_mode_shortcut = QLineEdit("Ctrl+M")
        self.toggle_mode_shortcut.setReadOnly(True)
        shortcut_layout.addRow("切换学习/复习模式:", self.toggle_mode_shortcut)
        
        # 编辑快捷键说明
        note_label = QLabel("注：点击输入框并按下快捷键组合来设置新的快捷键")
        note_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        
        layout.addWidget(shortcut_group)
        layout.addWidget(note_label)
        layout.addStretch()
        
        return tab
    
    def setup_connections(self):
        """设置信号连接"""
        # 复习策略选择变化
        self.review_strategy_combo.currentTextChanged.connect(self.on_review_strategy_changed)
        
        # 透明度滑块变化
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        
        # 字体大小滑块变化
        self.word_font_size_slider.valueChanged.connect(self.on_word_font_size_changed)
        self.meaning_font_size_slider.valueChanged.connect(self.on_meaning_font_size_changed)
        
        # 新旧单词比例滑块变化
        self.mix_ratio_slider.valueChanged.connect(self.on_mix_ratio_changed)
        
        # 保存和重置按钮
        self.save_btn.clicked.connect(self.save_settings)
        self.reset_btn.clicked.connect(self.reset_settings)
    
    def load_settings(self):
        """加载设置"""
        # 在实际应用中，应从配置管理器加载设置
        # 这里使用默认值
        pass
    
    def on_review_strategy_changed(self, strategy):
        """复习策略变化事件处理"""
        # 仅当选择自定义策略时启用复习间隔设置
        self.review_intervals_group.setEnabled(strategy == "自定义策略")
    
    def on_opacity_changed(self, value):
        """透明度滑块变化事件处理"""
        self.opacity_value_label.setText(f"{value}%")
    
    def on_word_font_size_changed(self, value):
        """单词字体大小滑块变化事件处理"""
        self.word_font_size_label.setText(f"{value} px")
    
    def on_meaning_font_size_changed(self, value):
        """释义字体大小滑块变化事件处理"""
        self.meaning_font_size_label.setText(f"{value} px")
    
    def on_mix_ratio_changed(self, value):
        """新旧单词比例滑块变化事件处理"""
        self.mix_ratio_label.setText(f"{value}% 新词 / {100-value}% 复习")
    
    def save_settings(self):
        """保存设置"""
        # 在实际应用中，应将设置保存到配置管理器
        # 这里简单地显示一个消息框
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "保存设置", "设置已保存")
        
        # 发送设置变更信号
        self.settings_changed.emit()
    
    def reset_settings(self):
        """重置设置"""
        # 确认重置
        from PyQt5.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "确认重置",
            "确定要重置所有设置吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 重置所有设置控件到默认值
            self.daily_goal_spin.setValue(20)
            self.auto_start_float_check.setChecked(False)
            self.auto_save_check.setChecked(True)
            
            self.float_width_spin.setValue(400)
            self.float_height_spin.setValue(250)
            self.opacity_slider.setValue(95)
            self.word_font_size_slider.setValue(20)
            self.meaning_font_size_slider.setValue(14)
            self.click_through_check.setChecked(True)
            self.theme_combo.setCurrentIndex(0)
            
            self.review_strategy_combo.setCurrentIndex(0)
            self.interval1_spin.setValue(1)
            self.interval2_spin.setValue(2)
            self.interval3_spin.setValue(4)
            self.interval4_spin.setValue(7)
            self.interval5_spin.setValue(15)
            self.mix_ratio_slider.setValue(70)
            
            # 更新标签
            self.on_opacity_changed(95)
            self.on_word_font_size_changed(20)
            self.on_meaning_font_size_changed(14)
            self.on_mix_ratio_changed(70)
            
            QMessageBox.information(self, "重置设置", "所有设置已重置为默认值")
    
    def set_stylesheet(self):
        """设置样式表"""
        self.setStyleSheet("""
            #pageTitle {
                color: #2c3e50;
                margin-bottom: 20px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #bdc3c7;
                height: 8px;
                background: #e0e0e0;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #2980b9;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
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
            
            #resetBtn {
                background-color: #e74c3c;
            }
            
            #resetBtn:hover {
                background-color: #c0392b;
            }
        """)