import os
import json
from .word_manager import WordManager

class ConfigManager:
    """配置管理器类，负责加载、保存和管理应用程序的配置"""
    
    def __init__(self):
        # 配置文件路径
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        self.config_file = os.path.join(self.config_dir, 'config.json')
        self.vocabularies_dir = os.path.join(self.config_dir, 'vocabularies')
        self.data_dir = os.path.join(self.config_dir, 'data')
        
        # 确保目录存在
        self._ensure_dirs_exist()
        
        # 默认配置
        self.default_config = {
            # 常规设置
            'general': {
                'daily_goal': 20,
                'auto_start_float': False,
                'auto_save': True,
                'data_path': self.data_dir
            },
            # 外观设置
            'appearance': {
                'float_window_size': {'width': 400, 'height': 250},
                'opacity': 95,
                'word_font_size': 20,
                'meaning_font_size': 14,
                'click_through': True,
                'theme': '默认主题'
            },
            # 复习策略
            'review': {
                'strategy': '艾宾浩斯记忆曲线',
                'intervals': [1, 2, 4, 7, 15],  # 自定义复习间隔（天）
                'mix_ratio': 70  # 新词与复习词的比例
            },
            # 快捷键
            'shortcuts': {
                'toggle_float': 'Ctrl+Space',
                'next_word': 'Ctrl+Right',
                'prev_word': 'Ctrl+Left',
                'speak_word': 'Ctrl+S',
                'toggle_mode': 'Ctrl+M'
            },
            # 单词本
            'vocabularies': [],
            # 学习记录
            'learning_records': {
                'last_study_date': None,
                'daily_records': {}
            }
        }
        
        # 当前配置
        self.config = self.default_config.copy()
        
        # 加载配置
        self.load_config()
        
        # 初始化单词管理器
        self.word_manager = WordManager(self)
    
    def _ensure_dirs_exist(self):
        """确保必要的目录存在"""
        for directory in [self.config_dir, self.vocabularies_dir, self.data_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # 更新配置，保留默认值
                self._update_dict(self.config, loaded_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
    
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def _update_dict(self, target, source):
        """递归更新字典，保留默认值"""
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    self._update_dict(target[key], value)
                else:
                    target[key] = value
    
    def get_setting(self, section, key=None):
        """获取设置值"""
        if section in self.config:
            if key is None:
                return self.config[section]
            elif key in self.config[section]:
                return self.config[section][key]
        return None
    
    def set_setting(self, section, key, value):
        """设置值"""
        if section in self.config:
            if key in self.config[section]:
                self.config[section][key] = value
                return True
        return False