from datetime import datetime
from typing import List
from src.models import Task  # �������Ľṹ��������·��

class TaskAnalytics:
    """�������ݷ������񣨼�������Ŀ¼�ṹ��"""
    
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def count_by_status(self) -> dict:
        """״̬ͳ�ƣ���������״̬��"""
        return {
            'δ���': sum(1 for t in self.tasks if t.status == 'δ���'),
            '�����': sum(1 for t in self.tasks if t.status == '�����')
        }

    def urgent_tasks(self) -> List[Task]:
        """��ȡ���н�������"""
        return [t for t in self.tasks if t.is_urgent]

    def deadline_report(self) -> dict:
        """��ֹ���ڷ�������"""
        return {
            'total_with_deadline': sum(1 for t in self.tasks if t.deadline),
            'overdue': self._get_overdue_tasks(),
            'upcoming': self._get_upcoming_tasks()
        }

    def _get_overdue_tasks(self) -> List[Task]:
        """�ڲ���������ȡ��������"""
        today = datetime.now().date()
        return [
            t for t in self.tasks 
            if t.deadline and 
            datetime.strptime(t.deadline, '%Y-%m-%d').date() < today and
            t.status == 'δ���'
        ]

    def _get_upcoming_tasks(self) -> List[Task]:
        """�ڲ���������ȡ3���ڵ�������"""
        today = datetime.now().date()
        return [
            t for t in self.tasks 
            if t.deadline and 
            0 <= (datetime.strptime(t.deadline, '%Y-%m-%d').date() - today).days <= 3
        ]