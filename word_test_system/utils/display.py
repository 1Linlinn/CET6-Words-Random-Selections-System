from colorama import Fore, Style, init
from typing import Dict, List, Any, Optional
from datetime import datetime

# 初始化彩色输出
init(autoreset=True)

class Display:
    def __init__(self, color_mode: bool = True):
        self.color_mode = color_mode
    
    def print_color(self, color: str, text: str) -> None:
        """彩色打印"""
        if self.color_mode:
            print(color + text)
        else:
            print(text)
    
    def print_title(self, title: str) -> None:
        """打印标题"""
        self.print_color(Fore.CYAN, f"\n=== {title} ===")
    
    def print_menu(self, options: Dict[str, str]) -> None:
        """打印菜单选项"""
        for key, value in options.items():
            print(f"{key}. {value}")
    
    def print_word_test(self, word: str, page: int, feedback_levels: Dict[str, str]) -> None:
        """打印单词测试界面"""
        self.print_color(Fore.YELLOW, f"\n单词: {word} (页码: {page})")
        print("请选择熟悉程度:")
        for score, desc in feedback_levels.items():
            print(f"{score}. {desc}")
        print("s. 跳过")
        print("q. 退出")
        print("e. 查看例句(如果存在)")
    
    def print_test_result(self, score: int, total_score: float) -> None:
        """打印测试结果"""
        color = Fore.GREEN if score > 0 else Fore.RED
        self.print_color(
            color,
            f"当前分数: {total_score:.1f} (本次: {'+' if score > 0 else ''}{score})"
        )
    
    def print_stats(self, stats: Dict[str, Any]) -> None:
        """打印统计信息"""
        self.print_title("学习统计")
        print(f"总单词数: {stats.get('total_words', 0)}")
        print(f"已测试单词: {stats.get('tested_words', 0)} "
              f"({stats.get('tested_percentage', 0):.1%})")
        print(f"平均分数: {stats.get('avg_score', 0):.2f}")
        print(f"低分单词(分数<0): {stats.get('low_score_words', 0)}")
        
        # 分数分布
        if 'score_distribution' in stats:
            self.print_color(Fore.CYAN, "\n分数分布:")
            for range_label, count in stats['score_distribution'].items():
                print(f"{range_label}: {count}")
    
    def print_word_info(self, word_info: Dict[str, Any]) -> None:
        """打印单词详细信息"""
        self.print_title("单词详情")
        print(f"单词: {word_info.get('word', '')}")
        print(f"页码: {word_info.get('page', '')}")
        print(f"测试次数: {word_info.get('times', 0)}")
        print(f"当前分数: {word_info.get('score', 0)}")
        print(f"跳过次数: {word_info.get('skip_count', 0)}")
        
        # 测试历史
        history = word_info.get('history', [])
        if history:
            self.print_color(Fore.CYAN, "\n测试历史:")
            for record in history:
                print(
                    f"{record['timestamp']}: "
                    f"得分 {record['score']} → "
                    f"新分数 {record['new_score']}"
                )
    
    def print_progress(self, progress: Dict[str, List]) -> None:
        """打印学习进度"""
        self.print_title("学习进度")
        for date, count, avg_score in zip(
            progress['dates'],
            progress['counts'],
            progress['avg_scores']
        ):
            print(f"{date}: 测试{count}个单词, 平均分数{avg_score:.2f}")
    
    def print_weak_words(self, words: List[Dict[str, Any]]) -> None:
        """打印需要加强的单词"""
        self.print_title("需要加强的单词")
        for word in words:
            self.print_color(
                Fore.RED,
                f"{word['word']} (页码: {word['page']}, "
                f"分数: {word['score']}, 测试次数: {word['times']})"
            )
    
    def print_review_suggestions(self, words: List[Dict[str, Any]]) -> None:
        """打印建议复习的单词"""
        self.print_title("建议复习的单词")
        for word in words:
            days = word['days_since_tested']
            self.print_color(
                Fore.YELLOW,
                f"{word['word']} (页码: {word['page']}, "
                f"分数: {word['score']}, 上次测试: {days}天前)"
            )