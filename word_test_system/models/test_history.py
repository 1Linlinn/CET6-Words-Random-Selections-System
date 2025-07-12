from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Union, Optional

@dataclass
class TestRecord:
    """测试记录类"""
    timestamp: datetime           # 测试时间
    score: Union[int, str]       # 测试分数或操作（如'skip'）
    new_score: float             # 测试后的总分
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'score': self.score,
            'new_score': self.new_score
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TestRecord':
        """从字典创建实例"""
        return cls(
            timestamp=datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S'),
            score=data['score'],
            new_score=data['new_score']
        )

class TestHistory:
    """测试历史类"""
    def __init__(self):
        self.history: Dict[str, List[TestRecord]] = {}
    
    def add_record(self, word: str, score: Union[int, str],
                   new_score: float) -> None:
        """添加测试记录"""
        if word not in self.history:
            self.history[word] = []
        
        record = TestRecord(
            timestamp=datetime.now(),
            score=score,
            new_score=new_score
        )
        self.history[word].append(record)
    
    def get_word_history(self, word: str,
                         limit: Optional[int] = None) -> List[TestRecord]:
        """获取单词的测试历史"""
        records = self.history.get(word, [])
        if limit is not None:
            records = records[-limit:]
        return records
    
    def get_recent_records(self, days: int = 30) -> Dict[str, List[TestRecord]]:
        """获取最近的测试记录"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        recent = {}
        
        for word, records in self.history.items():
            recent_records = [
                record for record in records
                if record.timestamp.timestamp() > cutoff
            ]
            if recent_records:
                recent[word] = recent_records
        
        return recent
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            word: [record.to_dict() for record in records]
            for word, records in self.history.items()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TestHistory':
        """从字典创建实例"""
        history = cls()
        for word, records in data.items():
            history.history[word] = [
                TestRecord.from_dict(record) for record in records
            ]
        return history
    
    def get_statistics(self) -> dict:
        """获取测试统计信息"""
        total_tests = sum(len(records) for records in self.history.values())
        total_words = len(self.history)
        
        score_counts = {str(i): 0 for i in range(-2, 3)}
        skip_count = 0
        
        for records in self.history.values():
            for record in records:
                if isinstance(record.score, int):
                    score_counts[str(record.score)] += 1
                elif record.score == 'skip':
                    skip_count += 1
        
        return {
            'total_tests': total_tests,
            'total_words': total_words,
            'score_distribution': score_counts,
            'skip_count': skip_count
        }