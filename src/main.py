from todo import add_task, list_tasks, update_status, update_status_by_name, delete_task, filter_tasks, search_tasks, delete_tasks_by_name

def main():
    while True:
        print("\n欢迎使用 To-Do List ")
        print("1. 添加任务")
        print("2. 列出所有任务")
        print("3. 根据任务名称更新状态")
        print("4. 删除任务")
        print("5. 筛选任务")
        print("6. 搜索任务")
        print("0. 退出程序")
        choice = input("请选择操作 (0-6): ").strip()

        if choice == '1':
            name = input("任务名称: ").strip()
            desc = input("任务描述 (可留空): ").strip()
            deadline = input("截止日期 (YYYY-MM-DD,可留空): ").strip() or None
            is_urgent = input("是否紧急? (y/n): ").lower() == 'y'
            prio = input("重要程度 (1=高,2=中,3=低,默认3): ").strip()
            priority = int(prio) if prio in ('1','2','3') else 3
            add_task(name, desc, deadline, is_urgent, priority)

        elif choice == '2':
            list_tasks()

        elif choice == '3':
            keyword = input("请输入要更新状态的任务名称:").strip()
            new_status = input("请输入新的状态 (未完成/已完成):").strip()
            if new_status in ('未完成','已完成'):
                update_status_by_name(keyword, new_status)
            else:
                print("状态输入无效。")

        elif choice == '4':
            keyword = input("请输入要删除的任务名称:").strip()
            delete_tasks_by_name(keyword)

        elif choice == '5':
            iu = input("筛选是否紧急? (y/n/留空跳过): ").lower()
            is_urgent = True if iu=='y' else False if iu=='n' else None
            pr = input("筛选重要程度 (1/2/3/留空跳过): ").strip()
            priority = int(pr) if pr in ('1','2','3') else None
            st = input("筛选状态 (未完成/已完成/留空跳过): ").strip() or None
            db = input("截止日期前筛选 (YYYY-MM-DD/留空跳过): ").strip() or None
            filter_tasks(is_urgent=is_urgent, priority=priority, status=st, deadline_before=db)

        elif choice == '6':
            keyword = input("请输入搜索关键字:").strip()
            search_tasks(keyword)

        elif choice == '0':
            print("程序已退出")
            break
        else:
            print("无效选择，请重试")

if __name__ == '__main__':
    main()