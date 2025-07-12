import os
import shutil
from datetime import datetime
from typing import List, Optional, Tuple
import json

class Backup:
    def __init__(self, backup_dir: str = 'backups'):
        self.backup_dir = backup_dir
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self) -> None:
        """确保备份目录存在"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, file_path: str, backup_type: str = 'auto') -> Tuple[bool, str]:
        """创建文件备份
        
        Args:
            file_path: 需要备份的文件路径
            backup_type: 备份类型 ('auto' 或 'manual')
            
        Returns:
            Tuple[bool, str]: (是否成功, 备份文件路径或错误信息)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"源文件不存在: {file_path}"
            
            # 生成备份文件名
            file_name = os.path.basename(file_path)
            name, ext = os.path.splitext(file_name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{name}_{backup_type}_{timestamp}{ext}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # 复制文件
            shutil.copy2(file_path, backup_path)
            
            return True, backup_path
        except Exception as e:
            return False, str(e)
    
    def restore_backup(self, backup_path: str, target_path: str) -> Tuple[bool, str]:
        """从备份恢复文件
        
        Args:
            backup_path: 备份文件路径
            target_path: 目标恢复路径
            
        Returns:
            Tuple[bool, str]: (是否成功, 成功或错误信息)
        """
        try:
            if not os.path.exists(backup_path):
                return False, f"备份文件不存在: {backup_path}"
            
            # 如果目标文件存在，先创建一个临时备份
            if os.path.exists(target_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                temp_backup = f"{target_path}.{timestamp}.temp"
                shutil.copy2(target_path, temp_backup)
                
                try:
                    # 复制备份文件到目标位置
                    shutil.copy2(backup_path, target_path)
                    # 恢复成功，删除临时备份
                    os.remove(temp_backup)
                except Exception as e:
                    # 恢复失败，还原原文件
                    if os.path.exists(temp_backup):
                        shutil.copy2(temp_backup, target_path)
                        os.remove(temp_backup)
                    raise e
            else:
                # 目标文件不存在，直接复制
                shutil.copy2(backup_path, target_path)
            
            return True, "恢复成功"
        except Exception as e:
            return False, str(e)
    
    def list_backups(self, file_name: Optional[str] = None) -> List[dict]:
        """列出备份文件
        
        Args:
            file_name: 可选，指定文件名筛选备份
            
        Returns:
            List[dict]: 备份文件信息列表
        """
        backups = []
        
        try:
            for item in os.listdir(self.backup_dir):
                if file_name and not item.startswith(file_name):
                    continue
                    
                item_path = os.path.join(self.backup_dir, item)
                if os.path.isfile(item_path):
                    stat = os.stat(item_path)
                    backups.append({
                        'name': item,
                        'path': item_path,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime)
                            .strftime('%Y-%m-%d %H:%M:%S')
                    })
        except Exception as e:
            print(f"列出备份文件时出错: {e}")
        
        # 按创建时间排序
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def clean_old_backups(self, max_backups: int = 10,
                         file_name: Optional[str] = None) -> Tuple[bool, str]:
        """清理旧的备份文件
        
        Args:
            max_backups: 保留的最大备份数量
            file_name: 可选，指定文件名筛选备份
            
        Returns:
            Tuple[bool, str]: (是否成功, 成功或错误信息)
        """
        try:
            backups = self.list_backups(file_name)
            
            if len(backups) <= max_backups:
                return True, "无需清理"
            
            # 删除超出数量的旧备份
            for backup in backups[max_backups:]:
                try:
                    os.remove(backup['path'])
                except Exception as e:
                    print(f"删除备份文件失败: {backup['name']} - {e}")
            
            return True, f"已清理 {len(backups) - max_backups} 个旧备份"
        except Exception as e:
            return False, str(e)