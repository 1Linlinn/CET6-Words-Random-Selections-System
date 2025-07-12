import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    def __init__(self, log_dir: str = 'logs', log_level: int = logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = None
        self.setup_logger()
    
    def setup_logger(self) -> None:
        """设置日志记录器"""
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 创建日志文件名
        log_file = os.path.join(
            self.log_dir,
            f"word_test_{datetime.now().strftime('%Y%m%d')}.log"
        )
        
        # 配置日志记录器
        self.logger = logging.getLogger('WordTestSystem')
        self.logger.setLevel(self.log_level)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # 控制台只显示警告及以上级别
        
        # 设置格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str) -> None:
        """记录信息级别的日志"""
        if self.logger:
            self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录警告级别的日志"""
        if self.logger:
            self.logger.warning(message)
    
    def error(self, message: str, exc: Optional[Exception] = None) -> None:
        """记录错误级别的日志"""
        if self.logger:
            if exc:
                self.logger.error(f"{message}: {str(exc)}")
            else:
                self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """记录调试级别的日志"""
        if self.logger:
            self.logger.debug(message)
    
    def log_test_result(self, word: str, score: Optional[int], action: str) -> None:
        """记录测试结果"""
        if self.logger:
            if action == 'continue':
                self.info(f"测试单词 '{word}', 得分: {score}")
            elif action == 'skip':
                self.info(f"跳过单词 '{word}'")
            elif action == 'quit':
                self.info("退出测试")
    
    def log_data_operation(self, operation: str, success: bool,
                          details: Optional[str] = None) -> None:
        """记录数据操作"""
        if self.logger:
            status = "成功" if success else "失败"
            message = f"{operation}{status}"
            if details:
                message += f": {details}"
            
            if success:
                self.info(message)
            else:
                self.error(message)
    
    def log_system_event(self, event: str, details: Optional[str] = None) -> None:
        """记录系统事件"""
        if self.logger:
            message = event
            if details:
                message += f": {details}"
            self.info(message)