#!/usr/bin/env python3
# main.py
from todo import add_task, list_tasks, update_status, delete_task, filter_tasks

def main():
    while True:
        print("\n欢迎使用 To-Do List ")
        print("1. 添加任务")
        print("2. 列出所有任务")
        print("3. 更新任务状态")
        print("4. 删除任务")
        print("5. 筛选任务")
        print("0. 退出程序")
        choice = input("请选择操作 (0-5): ").strip()

        if choice == '1':
            name = input("任务名称: ").strip()
            desc = input("任务描述 (可留空): ").strip()
            deadline = input("截止日期 (YYYY-MM-DD，可留空): ").strip() or None
            is_urgent = input("是否紧急? (y/n): ").lower() == 'y'
            prio = input("重要程度 (1=高,2=中,3=低，默认3): ").strip()
            priority = int(prio) if prio in ('1','2','3') else 3
            add_task(name, desc, deadline, is_urgent, priority)

        elif choice == '2':
            list_tasks()

        elif choice == '3':
            tid = input("任务 ID: ").strip()
            status = input("新状态 (未完成/已完成): ").strip()
            if tid.isdigit() and status in ('未完成','已完成'):
                update_status(int(tid), status)
            else:
                print("输入无效。")

        elif choice == '4':
            tid = input("任务 ID: ").strip()
            if tid.isdigit():
                delete_task(int(tid))
            else:
                print("输入无效。")

        elif choice == '5':
            iu = input("筛选是否紧急? (y/n/留空跳过): ").lower()
            is_urgent = True if iu=='y' else False if iu=='n' else None
            pr = input("筛选重要程度 (1/2/3/留空跳过): ").strip()
            priority = int(pr) if pr in ('1','2','3') else None
            st = input("筛选状态 (未完成/已完成/留空跳过): ").strip() or None
            db = input("截止日期前筛选 (YYYY-MM-DD/留空跳过): ").strip() or None
            filter_tasks(is_urgent=is_urgent, priority=priority, status=st, deadline_before=db)

        elif choice == '0':
            print("程序已退出。")
            break
        else:
            print("无效选择，请重试。")

if __name__ == '__main__':
    main()