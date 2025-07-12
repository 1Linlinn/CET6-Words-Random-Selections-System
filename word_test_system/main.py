import json
import os
from core.data_loader import DataLoader
from core.word_selector import WordSelector
from core.tester import Tester
from core.analyzer import Analyzer
from utils.display import Display
from utils.logger import Logger
from utils.backup import Backup

class WordTestSystem:
    def __init__(self):
        # 加载配置
        self.load_config()
        
        # 初始化组件
        self.logger = Logger(self.settings['log_dir'], self.settings['log_level'])
        self.display = Display(self.settings['color_mode'])
        self.backup = Backup(self.settings['backup_dir'])
        
        # 初始化核心组件
        self.data_loader = DataLoader(self.settings['data_file'])
        self.word_selector = WordSelector(self.settings['weights'])
        self.tester = Tester(self.data_loader, self.word_selector)
        self.analyzer = Analyzer()
        
        # 加载数据
        self.load_data()
    
    def load_config(self):
        """加载配置文件"""
        try:
            # 使用os.path来处理路径
            config_dir = os.path.join(os.path.dirname(__file__), 'config')
            settings_path = os.path.join(config_dir, 'settings.json')
            feedback_path = os.path.join(config_dir, 'feedback_levels.json')
            
            # 确保配置目录存在
            os.makedirs(config_dir, exist_ok=True)
            
            with open(settings_path, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            with open(feedback_path, 'r', encoding='utf-8') as f:
                self.feedback_levels = json.load(f)
                
            # 确保必要的目录存在
            os.makedirs(self.settings['log_dir'], exist_ok=True)
            os.makedirs(self.settings['backup_dir'], exist_ok=True)
                
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            # 提供默认配置
            self.settings = {
                "color_mode": True,
                "auto_save": True,
                "auto_save_interval": 5,
                "max_backups": 10,
                "log_level": "INFO",
                "weights": {
                    "score_weight": 0.7,
                    "time_weight": 0.2,
                    "count_weight": 0.1
                },
                "test_modes": ["随机测试", "重点突破", "复习模式"],
                "data_file": "words.xlsx",
                "backup_dir": "backups",
                "log_dir": "logs"
            }
            self.feedback_levels = {}
    
    def load_data(self):
        """加载数据"""
        if self.data_loader.load_data():
            self.analyzer.set_data(self.data_loader.df)
            self.logger.info("数据加载成功")
            self.display.print_color("GREEN", "数据加载成功!")
        else:
            self.logger.error("数据加载失败")
            self.display.print_color("RED", "数据加载失败!")
    
    def show_menu(self):
        """显示主菜单"""
        self.display.print_title("主菜单")
        options = {
            '1': '随机测试',
            '2': '重点突破(低分单词)',
            '3': '复习模式(高分久未复习)',
            '4': '批量测试',
            '5': '查看统计',
            '6': '查看单词详情',
            '7': '管理备份',
            '8': '系统设置',
            '0': '退出'
        }
        self.display.print_menu(options)
    
    def run_test(self, mode='random'):
        """运行测试"""
        word_idx = self.word_selector.select_word(self.data_loader.df, mode)
        if word_idx is not None:
            result, score = self.tester.test_word(word_idx)
            if result == 'continue':
                self.logger.log_test_result(
                    self.data_loader.df.loc[word_idx, 'Words'],
                    score,
                    result
                )
            if self.settings['auto_save']:
                self.data_loader.save_data()
    
    def batch_test(self):
        """批量测试"""
        try:
            num = int(input("输入要测试的单词数量(默认10): ").strip() or "10")
            mode = input("选择测试模式(random/focus/review, 默认random): ").strip() or "random"
            
            stats = self.tester.batch_test(
                num,
                mode,
                self.settings['auto_save']
            )
            
            self.display.print_title("测试统计")
            print(f"总计测试: {stats['total']}个单词")
            print(f"完成: {stats['completed']}个")
            print(f"跳过: {stats['skipped']}个")
            print(f"平均分: {stats['avg_score']:.2f}")
            
        except ValueError:
            self.display.print_color("RED", "请输入有效数字")
    
    def show_stats(self):
        """显示统计信息"""
        stats = self.analyzer.get_basic_stats()
        score_dist = self.analyzer.get_score_distribution()
        stats['score_distribution'] = score_dist
        self.display.print_stats(stats)
    
    def show_word_info(self):
        """显示单词详情"""
        word = input("输入要查询的单词: ").strip()
        matches = self.data_loader.df[self.data_loader.df['Words'].str.contains(word, case=False)]
        
        if len(matches) > 0:
            for idx, _ in matches.iterrows():
                word_info = self.data_loader.get_word_info(idx)
                if word_info:
                    self.display.print_word_info(word_info)
        else:
            self.display.print_color("RED", "未找到匹配的单词")
    
    def manage_backups(self):
        """管理备份"""
        self.display.print_title("备份管理")
        options = {
            '1': '创建备份',
            '2': '查看备份',
            '3': '恢复备份',
            '4': '清理旧备份',
            '0': '返回'
        }
        
        while True:
            self.display.print_menu(options)
            choice = input("请选择: ").strip()
            
            if choice == '1':
                success, msg = self.backup.create_backup(
                    self.settings['data_file'],
                    'manual'
                )
                self.display.print_color(
                    "GREEN" if success else "RED",
                    msg
                )
                
            elif choice == '2':
                backups = self.backup.list_backups()
                if backups:
                    self.display.print_title("备份列表")
                    for b in backups:
                        print(f"{b['name']} - {b['created']} ({b['size']}字节)")
                else:
                    self.display.print_color("YELLOW", "没有找到备份文件")
                    
            elif choice == '3':
                backups = self.backup.list_backups()
                if not backups:
                    self.display.print_color("RED", "没有可用的备份")
                    continue
                    
                print("\n可用备份:")
                for i, b in enumerate(backups, 1):
                    print(f"{i}. {b['name']} - {b['created']}")
                    
                try:
                    idx = int(input("\n选择要恢复的备份编号: ").strip()) - 1
                    if 0 <= idx < len(backups):
                        success, msg = self.backup.restore_backup(
                            backups[idx]['path'],
                            self.settings['data_file']
                        )
                        self.display.print_color(
                            "GREEN" if success else "RED",
                            msg
                        )
                        if success:
                            self.load_data()
                    else:
                        self.display.print_color("RED", "无效的选择")
                except ValueError:
                    self.display.print_color("RED", "请输入有效数字")
                    
            elif choice == '4':
                success, msg = self.backup.clean_old_backups(
                    self.settings['max_backups']
                )
                self.display.print_color(
                    "GREEN" if success else "RED",
                    msg
                )
                
            elif choice == '0':
                break
    
    def run(self):
        """主运行循环"""
        while True:
            self.show_menu()
            choice = input("请选择: ").strip()
            
            if choice == '1':
                self.run_test('random')
            elif choice == '2':
                self.run_test('focus')
            elif choice == '3':
                self.run_test('review')
            elif choice == '4':
                self.batch_test()
            elif choice == '5':
                self.show_stats()
            elif choice == '6':
                self.show_word_info()
            elif choice == '7':
                self.manage_backups()
            elif choice == '0':
                self.data_loader.save_data()
                self.display.print_color("GREEN", "感谢使用，再见!")
                break
            else:
                self.display.print_color("RED", "无效选择，请重新输入")

if __name__ == "__main__":
    system = WordTestSystem()
    system.run()