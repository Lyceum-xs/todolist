from datetime import datetime
from typing import List, Tuple
from src.models import Task  # 根据您的结构调整导入路径

class TaskNotifier:
    """任务提醒服务（适配您的目录结构）"""
    
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def check_reminders(self) -> List[Tuple[Task, str]]:
        """生成提醒消息列表"""
        reminders = []
        
        # 紧急任务提醒
        reminders.extend(
            (task, "紧急任务待处理") 
            for task in self.tasks 
            if task.is_urgent and task.status == '未完成'
        )
        
        # 逾期提醒
        reminders.extend(
            (task, f"任务已逾期 {self._days_overdue(task)} 天") 
            for task in self._get_overdue_tasks()
        )
        
        # 临近截止提醒
        reminders.extend(
            (task, f"剩余 {self._days_remaining(task)} 天") 
            for task in self._get_upcoming_tasks()
        )
        
        return reminders

    def _get_overdue_tasks(self) -> List[Task]:
        """获取逾期任务"""
        today = datetime.now().date()
        return [
            t for t in self.tasks 
            if t.deadline and 
            self._parse_date(t.deadline) < today and
            t.status == '未完成'
        ]

    def _get_upcoming_tasks(self, days: int = 3) -> List[Task]:
        """获取临近任务（默认3天内）"""
        today = datetime.now().date()
        return [
            t for t in self.tasks 
            if t.deadline and 
            0 <= (self._parse_date(t.deadline) - today).days <= days
        ]

    @staticmethod
    def _parse_date(date_str: str) -> datetime.date:
        """日期解析辅助方法"""
        return datetime.strptime(date_str, '%Y-%m-%d').date()

    @staticmethod
    def _days_remaining(task: Task) -> int:
        """计算剩余天数"""
        return (TaskNotifier._parse_date(task.deadline) - datetime.now().date()).days

    @staticmethod
    def _days_overdue(task: Task) -> int:
        """计算逾期天数"""
        return (datetime.now().date() - TaskNotifier._parse_date(task.deadline)).days