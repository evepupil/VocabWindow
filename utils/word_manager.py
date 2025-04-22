import os
import json
import datetime

class WordManager:
    """单词管理器类，负责管理单词本和学习记录"""
    """
    {
  "name": "CET6英语",
  "verbs": [
    {
      "word": "abandon",
      "meaning": "放弃",
      "phonetic": "/əˈbændən/",
      "examples": {"He abandoned his wife and children."},
      "word_type": "v"
    },
    
  ]
}
    """
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.vocabularies_dir = config_manager.vocabularies_dir
        self.config = config_manager.config
    
    def get_vocabularies(self):
        """获取单词本列表"""
        return self.config['vocabularies']
    
    def add_vocabulary(self, vocabulary):
        """添加单词本"""
        self.config['vocabularies'].append(vocabulary)
        self.config_manager.save_config()
    
    def remove_vocabulary(self, index):
        """删除单词本"""
        if 0 <= index < len(self.config['vocabularies']):
            del self.config['vocabularies'][index]
            self.config_manager.save_config()
            return True
        return False
    
    def load_vocabulary_words(self, vocab_path):
        """加载单词本中的单词"""
        if os.path.exists(vocab_path):
            try:
                with open(vocab_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载单词本失败: {e}")
        return []
    
    def save_vocabulary_words(self, vocab_path, words):
        """保存单词本中的单词"""
        try:
            with open(vocab_path, 'w', encoding='utf-8') as f:
                json.dump(words, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存单词本失败: {e}")
            return False
    
    def update_learning_record(self, word_id, status):
        """更新学习记录"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 初始化今日记录
        if today not in self.config['learning_records']['daily_records']:
            self.config['learning_records']['daily_records'][today] = {
                'new_words': 0,
                'review_words': 0,
                'test_words': 0,
                'words': {}
            }
        
        # 更新单词状态
        self.config['learning_records']['daily_records'][today]['words'][word_id] = {
            'status': status,
            'timestamp': datetime.datetime.now().timestamp()
        }
        
        # 更新计数
        if status == 'new':
            self.config['learning_records']['daily_records'][today]['new_words'] += 1
        elif status == 'review':
            self.config['learning_records']['daily_records'][today]['review_words'] += 1
        elif status == 'test':
            self.config['learning_records']['daily_records'][today]['test_words'] += 1
        
        # 更新最后学习日期
        self.config['learning_records']['last_study_date'] = today
        
        # 保存配置
        if self.config['general']['auto_save']:
            self.config_manager.save_config()
    
    def get_today_stats(self):
        """获取今日学习统计"""
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if today in self.config['learning_records']['daily_records']:
            return self.config['learning_records']['daily_records'][today]
        return {'new_words': 0, 'review_words': 0, 'test_words': 0, 'words': {}}
    
    def get_word_status(self, word_id):
        """获取单词的学习状态"""
        # 遍历所有日期的记录，查找最新的状态
        latest_status = None
        latest_timestamp = 0
        
        for date, record in self.config['learning_records']['daily_records'].items():
            if word_id in record['words']:
                word_record = record['words'][word_id]
                if word_record['timestamp'] > latest_timestamp:
                    latest_timestamp = word_record['timestamp']
                    latest_status = word_record['status']
        
        return latest_status
    
    def get_words_by_status(self, vocab_path, status):
        """获取指定状态的单词列表"""
        words = self.load_vocabulary_words(vocab_path)
        result = []
        
        for word in words:
            word_id = f"{vocab_path}:{word['word']}"
            word_status = self.get_word_status(word_id)
            
            if status == 'all' or word_status == status:
                result.append(word)
        
        return result
    
    def get_review_words(self, vocab_path):
        """获取需要复习的单词"""
        words = self.load_vocabulary_words(vocab_path)
        result = []
        
        # 获取复习策略
        strategy = self.config['review']['strategy']
        intervals = self.config['review']['intervals']
        
        for word in words:
            word_id = f"{vocab_path}:{word['word']}"
            word_status = self.get_word_status(word_id)
            
            # 只考虑已学过的单词
            if word_status in ['learned', 'reviewed']:
                # 获取最后一次学习的时间
                last_time = self._get_last_study_time(word_id)
                
                if last_time is not None:
                    # 计算距离上次学习的天数
                    days = (datetime.datetime.now() - last_time).days
                    
                    # 根据复习策略判断是否需要复习
                    if self._need_review(days, strategy, intervals):
                        result.append(word)
        
        return result
    
    def _get_last_study_time(self, word_id):
        """获取单词最后一次学习的时间"""
        latest_timestamp = 0
        
        for date, record in self.config['learning_records']['daily_records'].items():
            if word_id in record['words']:
                word_record = record['words'][word_id]
                if word_record['timestamp'] > latest_timestamp:
                    latest_timestamp = word_record['timestamp']
        
        if latest_timestamp > 0:
            return datetime.datetime.fromtimestamp(latest_timestamp)
        return None
    
    def _need_review(self, days, strategy, intervals):
        """根据复习策略判断是否需要复习"""
        if strategy == '艾宾浩斯记忆曲线':
            # 艾宾浩斯记忆曲线: 1, 2, 4, 7, 15天后复习
            ebbinghaus_intervals = [1, 2, 4, 7, 15]
            return days in ebbinghaus_intervals
        elif strategy == '间隔重复系统':
            # 间隔重复系统: 根据记忆效果动态调整间隔
            # 这里简化为固定间隔: 1, 3, 6, 10, 20天后复习
            srs_intervals = [1, 3, 6, 10, 20]
            return days in srs_intervals
        elif strategy == '自定义策略':
            # 自定义策略: 使用用户设置的间隔
            return days in intervals
        
        return False