import unittest
import pandas as pd
import os
import json
from datetime import datetime
from core.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.test_file = 'test_words.xlsx'
        self.test_history_file = 'test_history.json'
        
        # 创建测试用Excel文件
        df = pd.DataFrame({
            'Words': ['test1', 'test2', 'test3'],
            'Page': [1, 2, 3],
            'Times': [0, 0, 0],
            'Score': [0, 0, 0],
            'LastTested': ['', '', ''],
            'SkipCount': [0, 0, 0]
        })
        df.to_excel(self.test_file, index=False)
        
        self.loader = DataLoader(self.test_file)
    
    def tearDown(self):
        """测试后清理"""
        # 删除测试文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_history_file):
            os.remove(self.test_history_file)
        if os.path.exists('backups'):
            for file in os.listdir('backups'):
                os.remove(os.path.join('backups', file))
            os.rmdir('backups')
    
    def test_load_data(self):
        """测试数据加载"""
        self.assertTrue(self.loader.load_data())
        self.assertIsNotNone(self.loader.df)
        self.assertEqual(len(self.loader.df), 3)
        
        # 检查必要列是否存在
        required_columns = ['Times', 'Score', 'LastTested', 'SkipCount']
        for col in required_columns:
            self.assertIn(col, self.loader.df.columns)
    
    def test_save_data(self):
        """测试数据保存"""
        self.loader.load_data()
        
        # 修改数据
        self.loader.df.at[0, 'Score'] = 1
        self.loader.df.at[0, 'Times'] = 1
        
        # 保存数据
        self.assertTrue(self.loader.save_data())
        
        # 重新加载验证
        new_loader = DataLoader(self.test_file)
        new_loader.load_data()
        self.assertEqual(new_loader.df.at[0, 'Score'], 1)
        self.assertEqual(new_loader.df.at[0, 'Times'], 1)
    
    def test_update_word_data(self):
        """测试单词数据更新"""
        self.loader.load_data()
        
        # 更新第一个单词的数据
        self.loader.update_word_data(0, 1)
        
        self.assertEqual(self.loader.df.at[0, 'Times'], 1)
        self.assertEqual(self.loader.df.at[0, 'Score'], 1)
        self.assertNotEqual(self.loader.df.at[0, 'LastTested'], '')
    
    def test_record_test_history(self):
        """测试历史记录"""
        self.loader.load_data()
        
        # 记录测试历史
        self.loader.record_test_history(0, 1)
        
        # 验证历史记录
        word = self.loader.df.at[0, 'Words']
        self.assertIn(word, self.loader.test_history)
        self.assertEqual(len(self.loader.test_history[word]), 1)
        self.assertEqual(self.loader.test_history[word][0]['score'], 1)
    
    def test_get_word_info(self):
        """测试获取单词信息"""
        self.loader.load_data()
        
        # 获取第一个单词的信息
        info = self.loader.get_word_info(0)
        
        self.assertIsNotNone(info)
        self.assertEqual(info['word'], 'test1')
        self.assertEqual(info['page'], 1)
        self.assertEqual(info['times'], 0)
        self.assertEqual(info['score'], 0)
        self.assertEqual(info['skip_count'], 0)

if __name__ == '__main__':
    unittest.main()