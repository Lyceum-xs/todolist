#!/usr/bin/env python3
# todo.py
from database import load_tasks, save_tasks, generate_id
from models import Task
from datetime import datetime
from typing import List, Optional

def add_task(name: str, description: str = '', deadline: Optional[str] = None,
             is_urgent: bool = False, priority: int = 3):
    tasks = load_tasks()
    task_id = generate_id(tasks)
    task = Task(id=task_id, name=name, description=description,
                deadline=deadline, status='未完成',
                is_urgent=is_urgent, priority=priority)
    tasks.append(task)
    save_tasks(tasks)
    print(f"任务已添加：{task}")

def list_tasks(tasks: List[Task] = None):
    if tasks is None:
        tasks = load_tasks()
    if not tasks:
        print("当前没有任何任务。")
        return
    for t in tasks:
        dl = t.deadline or '无'
        print(f"[{t.id}] {t.name} - {t.status} - 截止: {dl} - 紧急: {t.is_urgent} - 优先级: {t.priority}")

def update_status(task_id: int, new_status: str):
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.status = new_status
            save_tasks(tasks)
            print(f"任务 ID {task_id} 状态已更新为 {new_status}")
            return
    print(f"未找到任务 ID：{task_id}")

def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        print(f"未找到任务 ID：{task_id}")
    else:
        save_tasks(new_tasks)
        print(f"任务 ID {task_id} 已删除")

def filter_tasks(is_urgent: Optional[bool] = None,
                 priority: Optional[int] = None,
                 status: Optional[str] = None,
                 deadline_before: Optional[str] = None):
    tasks = load_tasks()
    result = tasks
    if is_urgent is not None:
        result = [t for t in result if t.is_urgent == is_urgent]
    if priority is not None:
        result = [t for t in result if t.priority == priority]
    if status is not None:
        result = [t for t in result if t.status == status]
    if deadline_before:
        try:
            cutoff = datetime.strptime(deadline_before, '%Y-%m-%d').date()
            result = [t for t in result
                      if t.deadline and datetime.strptime(t.deadline, '%Y-%m-%d').date() <= cutoff]
        except ValueError:
            print("截止日期格式错误，应为 YYYY-MM-DD。")
    print(f"筛选结果（共 {len(result)} 条）：")
    list_tasks(result)