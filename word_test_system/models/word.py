from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Word:
    """单词模型类"""
    word: str                      # 单词
    page: int                      # 页码
    times: int = 0                 # 测试次数
    score: float = 0.0             # 当前分数
    skip_count: int = 0            # 跳过次数
    last_tested: Optional[datetime] = None  # 最后测试时间
    
    def update_score(self, score: int) -> None:
        """更新分数"""
        self.score += score
        self.times += 1
        self.last_tested = datetime.now()
    
    def skip(self) -> None:
        """跳过单词"""
        self.skip_count += 1
        self.last_tested = datetime.now()
    
    def days_since_last_test(self) -> Optional[int]:
        """获取距离上次测试的天数"""
        if self.last_tested is None:
            return None
        delta = datetime.now() - self.last_tested
        return delta.days
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'word': self.word,
            'page': self.page,
            'times': self.times,
            'score': self.score,
            'skip_count': self.skip_count,
            'last_tested': self.last_tested.strftime('%Y-%m-%d %H:%M:%S')
                if self.last_tested else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Word':
        """从字典创建实例"""
        last_tested = None
        if data.get('last_tested'):
            try:
                last_tested = datetime.strptime(
                    data['last_tested'],
                    '%Y-%m-%d %H:%M:%S'
                )
            except ValueError:
                pass
        
        return cls(
            word=data['word'],
            page=data['page'],
            times=data.get('times', 0),
            score=data.get('score', 0.0),
            skip_count=data.get('skip_count', 0),
            last_tested=last_tested
        )