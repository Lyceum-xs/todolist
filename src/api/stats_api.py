from typing import Dict
from ..models import Task
from ..database import load_tasks

class StatsAPI:
    """统计分析API"""
    
    @staticmethod
    def get_completion_rate() -> Dict[str, float]:
        """获取任务完成率"""
        tasks = load_tasks()
        if not tasks:
            return {"rate": 0.0}
            
        completed = sum(1 for t in tasks if t.status == "已完成")
        return {"rate": round(completed / len(tasks), 2)}

    @staticmethod
    def get_priority_distribution() -> Dict[int, int]:
        """获取优先级分布"""
        tasks = load_tasks()
        dist = {1: 0, 2: 0, 3: 0}
        for t in tasks:
            dist[t.priority] += 1
        return dist

    @staticmethod
    def get_overdue_tasks() -> Dict[str, list]:
        """获取逾期任务"""
        from datetime import datetime
        tasks = [
            t for t in load_tasks()
            if t.deadline and 
            datetime.strptime(t.deadline, '%Y-%m-%d').date() < datetime.now().date() and
            t.status == "未完成"
        ]
        return {"count": len(tasks), "tasks": tasks}