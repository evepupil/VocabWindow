class Word:
    """
    单词类，表示一个单词及其相关信息
    """
    
    def __init__(self, word, meaning, phonetic=None, examples=None, tags=None):
        """
        初始化单词对象
        
        Args:
            word (str): 单词
            meaning (str): 单词含义
            phonetic (str, optional): 音标. Defaults to None.
            examples (list, optional): 例句列表. Defaults to None.
            tags (list, optional): 标签列表. Defaults to None.
        """
        self.word = word
        self.meaning = meaning
        self.phonetic = phonetic or ""
        self.examples = examples or []
        self.tags = tags or []
        
        # 学习状态: unlearned(未学), learned(已学), skipped(跳过), favorite(收藏)
        self.status = "unlearned"
        
        # 学习记录
        self.learn_count = 0  # 学习次数
        self.review_count = 0  # 复习次数
        self.last_learn_time = None  # 最后学习时间
        self.next_review_time = None  # 下次复习时间
        self.mastery_level = 0  # 掌握程度 (0-5)
    
    def to_dict(self):
        """
        将单词对象转换为字典，用于JSON序列化
        
        Returns:
            dict: 单词字典
        """
        return {
            "word": self.word,
            "meaning": self.meaning,
            "phonetic": self.phonetic,
            "examples": self.examples,
            "tags": self.tags,
            "status": self.status,
            "learn_count": self.learn_count,
            "review_count": self.review_count,
            "last_learn_time": self.last_learn_time,
            "next_review_time": self.next_review_time,
            "mastery_level": self.mastery_level
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建单词对象
        
        Args:
            data (dict): 单词字典
            
        Returns:
            Word: 单词对象
        """
        word = cls(
            word=data["word"],
            meaning=data["meaning"],
            phonetic=data.get("phonetic", ""),
            examples=data.get("examples", []),
            tags=data.get("tags", [])
        )
        
        word.status = data.get("status", "unlearned")
        word.learn_count = data.get("learn_count", 0)
        word.review_count = data.get("review_count", 0)
        word.last_learn_time = data.get("last_learn_time", None)
        word.next_review_time = data.get("next_review_time", None)
        word.mastery_level = data.get("mastery_level", 0)
        
        return word
    
    def mark_as_learned(self, timestamp=None):
        """
        标记为已学习
        
        Args:
            timestamp (float, optional): 时间戳. Defaults to None.
        """
        self.status = "learned"
        self.learn_count += 1
        self.last_learn_time = timestamp
    
    def mark_as_reviewed(self, timestamp=None):
        """
        标记为已复习
        
        Args:
            timestamp (float, optional): 时间戳. Defaults to None.
        """
        self.review_count += 1
        self.last_learn_time = timestamp
    
    def mark_as_skipped(self):
        """
        标记为跳过
        """
        self.status = "skipped"
    
    def toggle_favorite(self):
        """
        切换收藏状态
        
        Returns:
            bool: 切换后的收藏状态
        """
        if self.status == "favorite":
            self.status = "learned" if self.learn_count > 0 else "unlearned"
            return False
        else:
            self.status = "favorite"
            return True
    
    def update_mastery_level(self, level):
        """
        更新掌握程度
        
        Args:
            level (int): 掌握程度 (0-5)
        """
        if 0 <= level <= 5:
            self.mastery_level = level
    
    def __str__(self):
        """
        返回单词的字符串表示
        
        Returns:
            str: 单词字符串
        """
        return f"{self.word} - {self.meaning}"