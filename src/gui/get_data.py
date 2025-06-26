

from ast import NameConstant


class Task:
    name = None
    submit_date = None
    due_date = None

    def Task(self, name, submit_date, due_date):
        self.name = name
        self.submit_date = submit_date
        self.due_date = due_date


def gettime():
    return {'year' : 2025, 'month' : 6, 'day' : 25, 'hour' : 14, 'minute' : 49}

def gettasks():
    task_1 = Task('task_1', {'year' : 2025, 'month' : 6, 'day' : 25, 'hour' : 14, 'mintue' : 49}, {'year' : 2025, 'month' : 7, 'day' : 25, 'hour' : 14, 'minute' : 49})
    task_2 = Task('task_2', {'year' : 2025, 'month' : 6, 'day' : 25, 'hour' : 14, 'mintue' : 49}, {'year' : 2025, 'month' : 7, 'day' : 25, 'hour' : 14, 'minute' : 49})
    task_3 = Task('task_3', {'year' : 2025, 'month' : 6, 'day' : 25, 'hour' : 14, 'mintue' : 49}, {'year' : 2025, 'month' : 7, 'day' : 25, 'hour' : 14, 'minute' : 49})
    tasks = []
    tasks.append(task_1)
    tasks.append(task_2)
    tasks.append(task_3)
    
    return tasks