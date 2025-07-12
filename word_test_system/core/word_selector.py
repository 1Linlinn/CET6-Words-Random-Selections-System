import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

class WordSelector:
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            'score_weight': 0.7,
            'time_weight': 0.2,
            'count_weight': 0.1
        }
    
    def calculate_weights(self, df: pd.DataFrame, mode: str = 'random') -> np.ndarray:
        """计算单词权重"""
        now = datetime.now()
        
        # 基础权重基于分数
        df_copy = df.copy()
        df_copy['ScoreWeight'] = 1 / (df_copy['Score'] + 5)  # 加5避免极端值
        
        # 时间权重 - 最近测试过的权重降低
        if 'LastTested' in df.columns and pd.api.types.is_string_dtype(df['LastTested']):
            df_copy['LastTested'] = pd.to_datetime(df_copy['LastTested'], errors='coerce')
            df_copy['DaysSinceTested'] = (now - df_copy['LastTested']).dt.days.fillna(100)
            df_copy['TimeWeight'] = np.log(df_copy['DaysSinceTested'] + 1)
        else:
            df_copy['TimeWeight'] = 1
            
        # 测试次数权重 - 测试次数少的权重高
        df_copy['CountWeight'] = 1 / (df_copy['Times'] + 1)
        
        # 根据不同模式调整权重
        if mode == 'focus':
            # 重点突破模式: 只关注最低分的20个单词
            focus_words = df_copy.nsmallest(20, 'Score').index
            weights = np.zeros(len(df_copy))
            weights[focus_words] = 1
            return weights / weights.sum() if weights.sum() > 0 else np.ones(len(df_copy)) / len(df_copy)
            
        elif mode == 'review':
            # 复习模式: 高分但久未复习的单词
            df_copy['ReviewWeight'] = df_copy['Score'] * df_copy['DaysSinceTested']
            weights = df_copy['ReviewWeight'].values
            
        else:  # random mode
            # 随机模式: 综合权重
            weights = (
                self.weights['score_weight'] * df_copy['ScoreWeight'] +
                self.weights['time_weight'] * df_copy['TimeWeight'] +
                self.weights['count_weight'] * df_copy['CountWeight']
            )
        
        # 归一化
        weights = weights / weights.sum() if weights.sum() > 0 else np.ones(len(df_copy)) / len(df_copy)
        return weights
    
    def select_word(self, df: pd.DataFrame, mode: str = 'random') -> int:
        """根据模式选择单词"""
        if df is None or len(df) == 0:
            return None
            
        weights = self.calculate_weights(df, mode)
        return np.random.choice(df.index, p=weights)
    
    def get_focus_words(self, df: pd.DataFrame, num: int = 20) -> List[int]:
        """获取需要重点关注的单词"""
        if df is None or len(df) == 0:
            return []
            
        return df.nsmallest(num, 'Score').index.tolist()
    
    def get_review_words(self, df: pd.DataFrame, num: int = 20) -> List[int]:
        """获取需要复习的单词"""
        if df is None or len(df) == 0:
            return []
            
        df_copy = df.copy()
        df_copy['LastTested'] = pd.to_datetime(df_copy['LastTested'], errors='coerce')
        df_copy['DaysSinceTested'] = (datetime.now() - df_copy['LastTested']).dt.days.fillna(100)
        df_copy['ReviewPriority'] = df_copy['Score'] * df_copy['DaysSinceTested']
        
        return df_copy.nlargest(num, 'ReviewPriority').index.tolist()