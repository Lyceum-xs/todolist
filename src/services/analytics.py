from datetime import datetime
from typing import List
from src.models import Task  # 根据您的结构调整导入路径

class TaskAnalytics:
    """任务数据分析服务（兼容您的目录结构）"""
    
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def count_by_status(self) -> dict:
        """状态统计（适配中文状态）"""
        return {
            '未完成': sum(1 for t in self.tasks if t.status == '未完成'),
            '已完成': sum(1 for t in self.tasks if t.status == '已完成')
        }

    def urgent_tasks(self) -> List[Task]:
        """获取所有紧急任务"""
        return [t for t in self.tasks if t.is_urgent]

    def deadline_report(self) -> dict:
        """截止日期分析报告"""
        return {
            'total_with_deadline': sum(1 for t in self.tasks if t.deadline),
            'overdue': self._get_overdue_tasks(),
            'upcoming': self._get_upcoming_tasks()
        }

    def _get_overdue_tasks(self) -> List[Task]:
        """内部方法：获取逾期任务"""
        today = datetime.now().date()
        return [
            t for t in self.tasks 
            if t.deadline and 
            datetime.strptime(t.deadline, '%Y-%m-%d').date() < today and
            t.status == '未完成'
        ]

    def _get_upcoming_tasks(self) -> List[Task]:
        """内部方法：获取3天内到期任务"""
        today = datetime.now().date()
        return [
            t for t in self.tasks 
            if t.deadline and 
            0 <= (datetime.strptime(t.deadline, '%Y-%m-%d').date() - today).days <= 3
        ]