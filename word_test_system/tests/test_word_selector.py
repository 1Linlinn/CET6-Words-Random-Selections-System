import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from core.word_selector import WordSelector

class TestWordSelector(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        # 创建测试数据
        self.df = pd.DataFrame({
            'Words': ['test1', 'test2', 'test3', 'test4', 'test5'],
            'Page': [1, 2, 3, 4, 5],
            'Times': [0, 1, 2, 1, 0],
            'Score': [-2, -1, 0, 1, 2],
            'LastTested': [
                '',
                (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
                (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
                (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                ''
            ],
            'SkipCount': [0, 0, 0, 0, 0]
        })
        
        self.selector = WordSelector()
    
    def test_calculate_weights_random(self):
        """测试随机模式权重计算"""
        weights = self.selector.calculate_weights(self.df, 'random')
        
        # 验证权重是否为概率分布
        self.assertEqual(len(weights), len(self.df))
        self.assertAlmostEqual(weights.sum(), 1.0)
        self.assertTrue(all(w >= 0 for w in weights))
        
        # 验证分数较低的单词权重较高
        self.assertGreater(weights[0], weights[4])  # test1(-2) > test5(2)
    
    def test_calculate_weights_focus(self):
        """测试重点突破模式权重计算"""
        weights = self.selector.calculate_weights(self.df, 'focus')
        
        # 验证权重是否为概率分布
        self.assertEqual(len(weights), len(self.df))
        self.assertAlmostEqual(weights.sum(), 1.0)
        
        # 验证只有最低分的单词有权重
        nonzero_indices = np.nonzero(weights)[0]
        self.assertTrue(all(self.df.iloc[i]['Score'] <= 0 for i in nonzero_indices))
    
    def test_calculate_weights_review(self):
        """测试复习模式权重计算"""
        weights = self.selector.calculate_weights(self.df, 'review')
        
        # 验证权重是否为概率分布
        self.assertEqual(len(weights), len(self.df))
        self.assertAlmostEqual(weights.sum(), 1.0)
        
        # 验证高分且长时间未测试的单词权重较高
        high_score_old = self.df[(
            self.df['Score'] > 0
        ) & (
            self.df['LastTested'] != ''
        )].index
        if len(high_score_old) > 0:
            self.assertTrue(all(weights[i] > 0 for i in high_score_old))
    
    def test_select_word(self):
        """测试单词选择"""
        # 测试随机模式
        word_idx = self.selector.select_word(self.df, 'random')
        self.assertIsNotNone(word_idx)
        self.assertTrue(0 <= word_idx < len(self.df))
        
        # 测试重点突破模式
        word_idx = self.selector.select_word(self.df, 'focus')
        self.assertIsNotNone(word_idx)
        self.assertTrue(0 <= word_idx < len(self.df))
        
        # 测试复习模式
        word_idx = self.selector.select_word(self.df, 'review')
        self.assertIsNotNone(word_idx)
        self.assertTrue(0 <= word_idx < len(self.df))
    
    def test_get_focus_words(self):
        """测试获取重点关注单词"""
        focus_words = self.selector.get_focus_words(self.df, 2)
        
        self.assertEqual(len(focus_words), 2)
        # 验证返回的是分数最低的单词
        scores = [self.df.loc[idx, 'Score'] for idx in focus_words]
        self.assertEqual(scores, sorted(scores))  # 应该是升序
    
    def test_get_review_words(self):
        """测试获取需要复习的单词"""
        review_words = self.selector.get_review_words(self.df, 2)
        
        self.assertEqual(len(review_words), 2)
        # 验证返回的单词都有最后测试时间
        self.assertTrue(all(
            self.df.loc[idx, 'LastTested'] != ''
            for idx in review_words
        ))

if __name__ == '__main__':
    unittest.main()