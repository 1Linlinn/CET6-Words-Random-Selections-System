from typing import Dict, Optional, Tuple
from .data_loader import DataLoader
from .word_selector import WordSelector

class Tester:
    def __init__(self, data_loader: DataLoader, word_selector: WordSelector):
        self.data_loader = data_loader
        self.word_selector = word_selector
        self.feedback_levels = {
            '2': '非常熟悉',
            '1': '熟悉',
            '0': '模糊',
            '-1': '不熟悉',
            '-2': '完全不知道'
        }
    
    def test_word(self, word_idx: int) -> Tuple[str, Optional[int]]:
        """测试单个单词
        
        Returns:
            Tuple[str, Optional[int]]: (操作结果, 分数)
            操作结果可能是: 'continue', 'skip', 'quit'
            分数在操作结果为'continue'时有效
        """
        if self.data_loader.df is None or word_idx >= len(self.data_loader.df):
            return 'quit', None
            
        word_row = self.data_loader.df.loc[word_idx]
        word = word_row['Words']
        page = word_row['Page']
        
        print(f"\n单词: {word} (页码: {page})")
        print("请选择熟悉程度:")
        for score, desc in self.feedback_levels.items():
            print(f"{score}. {desc}")
        print("s. 跳过")
        print("q. 退出")
        print("e. 查看例句(如果存在)")
        
        while True:
            choice = input("你的选择: ").strip().lower()
            
            if choice in self.feedback_levels:
                score = int(choice)
                # 更新单词数据
                self.data_loader.update_word_data(word_idx, score)
                # 记录历史
                self.data_loader.record_test_history(word_idx, score)
                return 'continue', score
                
            elif choice == 's':
                # 跳过
                self.data_loader.df.at[word_idx, 'SkipCount'] += 1
                self.data_loader.record_test_history(word_idx, 'skip')
                return 'skip', None
                
            elif choice == 'q':
                return 'quit', None
                
            elif choice == 'e':
                # 查看例句功能待实现
                print("例句功能待实现")
                
            else:
                print("无效输入，请重新选择")
    
    def batch_test(self, num: int = 10, mode: str = 'random', auto_save: bool = True) -> Dict:
        """批量测试
        
        Args:
            num: 测试单词数量
            mode: 测试模式 ('random', 'focus', 'review')
            auto_save: 是否自动保存
            
        Returns:
            Dict: 测试统计信息
        """
        stats = {
            'total': 0,
            'completed': 0,
            'skipped': 0,
            'avg_score': 0.0,
            'scores': []
        }
        
        for i in range(num):
            word_idx = self.word_selector.select_word(self.data_loader.df, mode)
            if word_idx is None:
                break
                
            result, score = self.test_word(word_idx)
            
            if result == 'quit':
                break
                
            stats['total'] += 1
            
            if result == 'continue':
                stats['completed'] += 1
                stats['scores'].append(score)
            elif result == 'skip':
                stats['skipped'] += 1
            
            # 每5次测试自动保存
            if auto_save and i > 0 and i % 5 == 0:
                self.data_loader.save_data()
        
        # 计算平均分
        if stats['scores']:
            stats['avg_score'] = sum(stats['scores']) / len(stats['scores'])
        
        # 最后保存一次
        if auto_save:
            self.data_loader.save_data()
        
        return stats