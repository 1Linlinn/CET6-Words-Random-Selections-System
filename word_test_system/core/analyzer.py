import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class Analyzer:
    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df
    
    def set_data(self, df: pd.DataFrame) -> None:
        """设置数据源"""
        self.df = df
    
    def get_basic_stats(self) -> Dict:
        """获取基本统计信息"""
        if self.df is None:
            return {}
            
        total_words = len(self.df)
        tested_words = len(self.df[self.df['Times'] > 0])
        avg_score = self.df['Score'].mean()
        low_score_words = len(self.df[self.df['Score'] < 0])
        
        return {
            'total_words': total_words,
            'tested_words': tested_words,
            'tested_percentage': tested_words/total_words if total_words > 0 else 0,
            'avg_score': avg_score,
            'low_score_words': low_score_words
        }
    
    def get_score_distribution(self) -> Dict[str, int]:
        """获取分数分布"""
        if self.df is None:
            return {}
            
        bins = [-float('inf'), -2, -1, 0, 1, 2, float('inf')]
        labels = ['<-2', '-2~-1', '-1~0', '0~1', '1~2', '>2']
        score_dist = pd.cut(self.df['Score'], bins=bins, labels=labels).value_counts().sort_index()
        
        return score_dist.to_dict()
    
    def get_learning_progress(self, days: int = 30) -> Dict:
        """获取学习进度统计"""
        if self.df is None:
            return {}
            
        now = datetime.now()
        start_date = now - timedelta(days=days)
        
        # 转换LastTested为datetime类型
        self.df['LastTested'] = pd.to_datetime(self.df['LastTested'], errors='coerce')
        
        # 按日期统计
        daily_stats = self.df[self.df['LastTested'] >= start_date].groupby(
            self.df['LastTested'].dt.date
        ).agg({
            'Times': 'count',
            'Score': ['mean', 'min', 'max']
        }).reset_index()
        
        # 转换为字典格式
        progress_data = {
            'dates': daily_stats['LastTested'].dt.strftime('%Y-%m-%d').tolist(),
            'counts': daily_stats['Times']['count'].tolist(),
            'avg_scores': daily_stats['Score']['mean'].tolist(),
            'min_scores': daily_stats['Score']['min'].tolist(),
            'max_scores': daily_stats['Score']['max'].tolist()
        }
        
        return progress_data
    
    def get_weak_words(self, limit: int = 20) -> List[Dict]:
        """获取需要加强的单词列表"""
        if self.df is None:
            return []
            
        weak_words = self.df.nsmallest(limit, 'Score')
        
        return [{
            'word': row['Words'],
            'page': row['Page'],
            'score': row['Score'],
            'times': row['Times'],
            'last_tested': row['LastTested']
        } for _, row in weak_words.iterrows()]
    
    def get_review_suggestions(self, limit: int = 20) -> List[Dict]:
        """获取建议复习的单词列表"""
        if self.df is None:
            return []
            
        # 计算复习优先级
        df_copy = self.df.copy()
        df_copy['LastTested'] = pd.to_datetime(df_copy['LastTested'], errors='coerce')
        df_copy['DaysSinceTested'] = (datetime.now() - df_copy['LastTested']).dt.days.fillna(100)
        df_copy['ReviewPriority'] = df_copy['Score'] * df_copy['DaysSinceTested']
        
        review_words = df_copy.nlargest(limit, 'ReviewPriority')
        
        return [{
            'word': row['Words'],
            'page': row['Page'],
            'score': row['Score'],
            'days_since_tested': row['DaysSinceTested'],
            'priority': row['ReviewPriority']
        } for _, row in review_words.iterrows()]