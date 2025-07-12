import pandas as pd
from datetime import datetime
import os
import json
from typing import Dict, List, Optional

class DataLoader:
    def __init__(self, file_path: str = 'words.xlsx'):
        self.file_path = file_path
        self.backup_dir = 'backups'
        self.history_file = 'test_history.json'
        self.df = None
        self.test_history = {}
        
    def load_data(self) -> bool:
        """加载单词数据"""
        try:
            self.df = pd.read_excel(self.file_path)
            # 初始化必要列
            for col in ['Times', 'Score', 'LastTested', 'SkipCount']:
                if col not in self.df.columns:
                    self.df[col] = 0 if col != 'LastTested' else ''
            
            # 加载测试历史
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.test_history = json.load(f)
            return True
        except Exception as e:
            print(f"加载文件时出错: {e}")
            return False

    def save_data(self) -> bool:
        """保存数据到文件"""
        try:
            # 创建备份目录
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
            
            # 保存主文件
            self.df.to_excel(self.file_path, index=False)
            
            # 创建带时间戳的备份
            backup_file = os.path.join(
                self.backup_dir,
                f"words_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            self.df.to_excel(backup_file, index=False)
            
            # 保存测试历史
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_history, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception as e:
            print(f"保存文件时出错: {e}")
            return False

    def update_word_data(self, word_idx: int, score: int) -> None:
        """更新单词数据"""
        if self.df is not None:
            self.df.at[word_idx, 'Times'] += 1
            self.df.at[word_idx, 'Score'] += score
            self.df.at[word_idx, 'LastTested'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def record_test_history(self, word_idx: int, score: int) -> None:
        """记录测试历史"""
        if self.df is not None:
            word = self.df.loc[word_idx, 'Words']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if word not in self.test_history:
                self.test_history[word] = []
                
            self.test_history[word].append({
                'timestamp': timestamp,
                'score': score,
                'new_score': self.df.loc[word_idx, 'Score']
            })

    def get_word_info(self, word_idx: int) -> Optional[Dict]:
        """获取单词详细信息"""
        if self.df is None or word_idx >= len(self.df):
            return None
            
        word_row = self.df.loc[word_idx]
        history = self.test_history.get(word_row['Words'], [])
        
        return {
            'word': word_row['Words'],
            'page': word_row['Page'],
            'times': word_row['Times'],
            'score': word_row['Score'],
            'skip_count': word_row['SkipCount'],
            'history': history[-5:] # 最近5次记录
        }