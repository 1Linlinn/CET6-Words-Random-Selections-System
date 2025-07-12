# 单词测试系统

这是一个用于辅助英语单词学习的命令行工具，支持多种测试模式和进度追踪功能。

## 功能特点

- 多种测试模式：
  - 随机测试：根据综合权重随机选择单词
  - 重点突破：专注于得分较低的单词
  - 复习模式：复习已掌握但需要巩固的单词
- 智能选词算法：
  - 考虑单词得分
  - 考虑测试间隔时间
  - 考虑测试次数
- 数据分析：
  - 学习进度统计
  - 分数分布分析
  - 个人学习曲线
- 自动备份：
  - 定期自动备份
  - 手动备份还原
  - 历史记录追踪

## 安装说明

1. 确保已安装Python 3.7或更高版本
2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 使用说明

1. 准备单词文件：
   - 创建Excel文件（words.xlsx）
   - 包含列：Words（单词）, Page（页码）

2. 启动程序：
```bash
python main.py
```

3. 主菜单选项：
   - 1: 随机测试
   - 2: 重点突破
   - 3: 复习模式
   - 4: 批量测试
   - 5: 查看统计
   - 6: 查看单词详情
   - 7: 管理备份
   - 0: 退出

4. 测试反馈等级：
   - 2: 非常熟悉
   - 1: 熟悉
   - 0: 模糊
   - -1: 不熟悉
   - -2: 完全不知道
   - s: 跳过
   - q: 退出

## 配置说明

系统配置文件位于 `config` 目录：

- `settings.json`: 系统基本设置
  - color_mode: 是否启用彩色显示
  - auto_save: 是否自动保存
  - auto_save_interval: 自动保存间隔
  - weights: 单词选择权重配置

- `feedback_levels.json`: 反馈等级定义
  - 不同分数对应的描述和颜色
  - 特殊操作的定义

## 项目结构

```
word_test_system/
├── config/                 # 配置文件
│   ├── settings.json
│   └── feedback_levels.json
├── core/                   # 核心功能模块
│   ├── data_loader.py
│   ├── word_selector.py
│   ├── tester.py
│   └── analyzer.py
├── utils/                  # 工具函数
│   ├── display.py
│   ├── logger.py
│   └── backup.py
├── models/                 # 数据模型
│   ├── word.py
│   └── test_history.py
├── tests/                  # 单元测试
│   ├── test_data_loader.py
│   └── test_word_selector.py
├── main.py                 # 程序入口
└── requirements.txt        # 依赖列表
```

## 开发说明

1. 运行测试：
```bash
python -m unittest discover tests
```

2. 添加新功能：
   - 在相应模块中添加功能实现
   - 添加单元测试
   - 更新文档

## 注意事项

1. 首次使用前请确保：
   - 已正确安装所有依赖
   - 已准备好单词文件
   - 已配置好系统设置

2. 数据安全：
   - 定期检查备份
   - 重要操作前手动备份
   - 保持足够的磁盘空间

## 常见问题

1. 启动失败：
   - 检查Python版本
   - 检查依赖安装
   - 检查配置文件

2. 数据丢失：
   - 检查备份目录
   - 使用最近的备份恢复
   - 确保磁盘空间充足

## 更新日志

### v1.0.0
- 初始版本发布
- 基本功能实现
- 完整的测试覆盖