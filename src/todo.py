from database import load_tasks, save_tasks, generate_id
from models import Task
from datetime import datetime

# 打印单个任务
def print_task(t):
    dl = t.deadline if t.deadline else '无'
    info = "[" + str(t.id) + "] " + t.name + " | 状态:" + t.status \
           + " | 截止:" + dl + " | 紧急:" + str(t.is_urgent) \
           + " | 优先级:" + str(t.priority)
    print(info)

def add_task(name, description = '', deadline = None,
             is_urgent = False, priority = 3):
    try:
        tasks = load_tasks()
    except:
        print("任务加载失败，无法添加")
        return
    task_id = generate_id(tasks)
    task = Task(id=task_id, name=name, description=description,
                deadline=deadline, status='未完成',
                is_urgent=is_urgent, priority=priority)
    tasks.append(task)
    try:
        save_tasks(tasks)
        print("任务已添加:" + str(task))
    except:
        print("任务保存失败")

def list_tasks(tasks = None):
    if tasks is None:
        try:
            tasks = load_tasks()
        except:
            print("任务加载失败")
            return
    if not tasks:
        print("当前没有任何任务")
        return
    for t in tasks:
        print_task(t)

def update_status(task_name, new_status):
    try:
        tasks = load_tasks()
    except:
        print("任务加载失败，无法更新状态")
        return
    updated = False
    for t in tasks:
        if t.name == task_name:
            t.status = new_status
            updated = True
    if not updated:
        print("未找到任务 名称:" + task_name)
        return
    try:
        save_tasks(tasks)
        print("任务名 " + task_name + " 状态已更新为 " + new_status)
    except:
        print("任务保存失败")

def delete_task(task_name):
    try:
        tasks = load_tasks()
    except:
        print("任务加载失败，无法删除")
        return
    new_tasks = [t for t in tasks if t.name != task_name]
    if len(new_tasks) == len(tasks):
        print("未找到任务 名称:" + task_name)
        return
    try:
        save_tasks(new_tasks)
        print("任务 " + task_name + " 已删除")
    except:
        print("任务保存失败。")

def filter_tasks(is_urgent = None,
                 priority = None,
                 status = None,
                 deadline_before = None):
    try:
        task_list = load_tasks()
    except:
        print("任务加载失败，无法筛选")
        return
    filtered = task_list
    if is_urgent is not None:
        filtered = [t for t in filtered if t.is_urgent == is_urgent]
    if priority is not None:
        filtered = [t for t in filtered if t.priority == priority]
    if status is not None:
        filtered = [t for t in filtered if t.status == status]
    if deadline_before:
        try:
            cutoff = datetime.strptime(deadline_before, '%Y-%m-%d').date()
            filtered = [t for t in filtered
                        if t.deadline and datetime.strptime(t.deadline, '%Y-%m-%d').date() <= cutoff]
        except ValueError:
            print("截止日期格式错误，应为 YYYY-MM-DD")
    print("筛选结果（共 " + str(len(filtered)) + " 条）:")
    for t in filtered:
        print_task(t)

# 根据任务名称搜索任务
def search_tasks(keyword):
    try:
        task_list = load_tasks()
    except:
        print("任务加载失败，无法搜索")
        return
    results = [t for t in task_list if keyword in t.name]
    print("搜索完成，共找到 " + str(len(results)) + " 条任务:")
    for t in results:
        print_task(t)

# 根据任务名称删除任务
def delete_tasks_by_name(keyword):
    try:
        task_list = load_tasks()
    except:
        print("任务加载失败，无法删除")
        return
    remaining = [t for t in task_list if keyword not in t.name]
    count = len(task_list) - len(remaining)
    if count == 0:
        print("未找到匹配的任务，关键字：" + keyword)
    else:
        save_tasks(remaining)
        print("已删除 " + str(count) + " 条任务，关键字:" + keyword)

# 根据任务名称更新任务状态
def update_status_by_name(keyword, new_status):
    try:
        task_list = load_tasks()
    except:
        print("任务加载失败，无法更新状态")
        return
    matched = [t for t in task_list if keyword in t.name]
    if not matched:
        print("未找到匹配的任务，关键字:" + keyword)
        return
    for t in matched:
        t.status = new_status
    save_tasks(task_list)
    print("已更新 " + str(len(matched)) + " 条任务状态为 " + new_status)

# 重要度与ddl量化函数