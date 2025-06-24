# models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    name: str
    description: Optional[str] = ''
    deadline: Optional[str] = None  # 格式 'YYYY-MM-DD'
    status: str = '未完成'
    is_urgent: bool = False
    priority: int = 3

    def __post_init__(self):
        # 校验优先级
        if self.priority not in (1, 2, 3):
            raise ValueError("priority must be 1, 2, or 3")
        # 校验状态
        if self.status not in ('未完成', '已完成'):
            raise ValueError("status must be '未完成' or '已完成'")
        # 校验日期格式
        if self.deadline:
            try:
                datetime.strptime(self.deadline, '%Y-%m-%d')
            except ValueError:
                raise ValueError("deadline format must be YYYY-MM-DD")