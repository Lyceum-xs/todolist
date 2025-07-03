from asyncio import exceptions
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from urllib import response
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

class TimeServices:
    @staticmethod
    def gettime():
        nowtime = datetime.now()
        return {'year' : nowtime.year, 'month' : nowtime.month, 'day' : nowtime.day, 'hour' : nowtime.hour, 'minute' : nowtime.minute}

    @staticmethod
    def getcalendar(year, month):
        calendar = {}

        max_day = 0
        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                max_day = 29
            else:
                max_day = 28
        elif month == 4 or month == 6 or month == 9 or month == 11:
            max_day = 30
        else:
            max_day = 31

        for day in range(1, max_day + 1):
            week = datetime(year, month, day).isoweekday()
            calendar.update({day : week})
    
        return calendar

    @staticmethod
    def create_datetime(year, month, day, hour, minute):
        return datetime(year, month, day, hour, minute)

    @staticmethod
    def turn_datetime_strf(time):
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S'
            ]

        for fmt in formats:
            try:
                return datetime.strptime(time, fmt).strftime('%Y-%m-%d %H:%M')
            except ValueError:
                continue

    @staticmethod
    def turn_datetime_strp(time):
        formats = [
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S'
            ]

        for fmt in formats:
            try:
                return datetime.strptime(time, fmt)
            except ValueError:
                continue


class TaskServices:
    @staticmethod
    def gettasks(sort):
        url = f'{BASE_URL}/tasks'

        try:
            response = requests.get(url, {'sort_by' : 'id'})
            if response.status_code == 200:
                tasks = response.json()

                # Create mapping from task ID to task object
                task_map = {task['id']: task for task in tasks}
                
                # Build parent-child relationship structure
                children_map = {}
                for task in tasks:
                    parent_id = task['parent_id']
                    if parent_id not in children_map:
                        children_map[parent_id] = []
                    children_map[parent_id].append(task)
                
                # Define sorting key function
                def get_sort_key(task):
                    if sort == 'Urgency':
                        # True comes before False
                        return (0 if task['urgent'] else 1, task['id'])
                    elif sort == 'Importance':
                        # True comes before False
                        return (0 if task['importance'] else 1, task['id'])
                    elif sort == 'Due Date':
                        # Handle None values (put at end)
                        due_date = task['due_date'] or '9999-12-31'
                        return (due_date, task['id'])
                    else:  # Default case
                        return task['id']
                
                # Collect sorted tasks (ensuring parents come before children)
                sorted_tasks = []
                
                def collect_sorted(parent_id):
                    # Get children for current parent
                    children = children_map.get(parent_id, [])
                    
                    # Sort siblings by the specified criteria
                    children.sort(key=get_sort_key)
                    
                    for child in children:
                        # Add parent task first
                        sorted_tasks.append(child)
                        # Recursively process children
                        collect_sorted(child['id'])
                
                # Start processing from root tasks (parent_id = None)
                collect_sorted(None)
                
                return sorted_tasks
            else:
                print(f'get tasks failed: {response.status_code} - {response.text}')
                return []
        except Exception as e:
            print(f'request failed: {str(e)}')
            return []

    @staticmethod
    def addtask(task):
        url = f'{BASE_URL}/tasks'

        try:
            if not task['name']:
                print('Error: the task must have a name')
                return {'error' : 'task name is None'}
            
            task.setdefault('description', 'test')
            
            response = requests.post(url, json = task)

            if response.status_code == 201:
                print(f'add task successfully: {response.json()}')
                return response.json()
            else:
                error_message = f'add task failed: {response.status_code} - {response.text}'
                print(error_message)
                return {'error' : error_message}
        except requests.exceptions.RequestException as e:
            error_message = f'the network request failed {str(e)}'
            print(error_message)
            return {'error' : error_message}
        except Exception as e:
            error_message = f"unkonwn error: {str(e)}"
            print(error_message)
            return {"error": error_message}

    @staticmethod
    def deltask(task_id):
        url = f'{BASE_URL}/tasks/{task_id}'

        try:
            response = requests.delete(url)

            if response.status_code == 204:
                print(f'delete task {task_id} successfully')
                return True
            else:
                print(f'delete task failed: {response.status_code} - {response.text}')
                return False
        except Exception as e:
            print(f'request failed: {str(e)}')
            return False

    @staticmethod
    def updatetask(task_id, up_dict):
        url = f'{BASE_URL}/tasks/{task_id}'

        try:
            response = requests.patch(url, json = up_dict)

            if response.status_code == 200:
                print(f'update {task_id} successfully: {response.json()}')
                return response.json()
            else:
                print(f'update {task_id} failed: {response.status_code} - {response.text}')
                return {'error' : response.text}
        except Exception as e:
            print(f'request failed: {str(e)}')
            return {'error' : str(e)}

    @staticmethod
    def gettask(task_id):
        url = f'{BASE_URL}/tasks/{task_id}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'get {task_id} failed: {response.status_code} - {response.text}')
                return None
        except Exception as e:
            print(f'request failed: {str(e)}')
            return None

    @staticmethod
    def getchildren(task_id):
        url = f'{BASE_URL}/tasks/{task_id}/children'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f'request failed: {str(e)}')
            return []

class HabitServices:
    @staticmethod
    def create_habit(habit):
        url = f'{BASE_URL}/habits'

        try:
            response = requests.post(url, json = habit)
            if response.status_code == 201:
                print(f'create habit successfully: {response.json()}')
                return response.json()
            else:
                error_message = f'create habit failed: {response.status_code} - {response.text}'
                print(error_message)
                return {'error' : error_message}
        except requests.exceptions.RequestException as e:
            error_message = f'the network request failed {str(e)}'
            print(error_message)
            return {'error' : error_message}
        except Exception as e:
            error_message = f"unkonwn error: {str(e)}"
            print(error_message)
            return {"error": error_message}

    @staticmethod
    def clockin_habit(habit_id):
        url = f'{BASE_URL}/habits/{habit_id}/logs'

        try:
            response = requests.post(url, json = {})

            if response.status_code == 201:
                print(f'clockin {habit_id} successfully')
                return True
            else:
                print(f'clockin {habit_id} failed: {response.status_code} - {response.text}')
                return False
        except Exception as e:
            print(f'request failed: {str(e)}')
            return False
    
    @staticmethod
    def delete_habit(habit_id):
        url = f'{BASE_URL}/habits/{habit_id}'

        try:
            response = requests.delete(url)

            if response.status_code == 204:
                print(f'delete {habit_id} successfully')
                return True
            else:
                print(f'delete {habit_id} failed: {response.status_code} - {response.text}')
                return False
        except Exception as e:
            print(f'request failed: {str(e)}')
            return False

    @staticmethod
    def get_habits():
        url = f'{BASE_URL}/habits'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()
            else:
                print(f'get habits failed: {response.status_code} - {response.text}')
                return []
        except Exception as e:
            print(f'request failed: {str(e)}')
            return []

    @staticmethod
    def get_consecutive_clockin_days(habit_id):
        url = f'{BASE_URL}/habits/{habit_id}/streak'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.json()
            else:
                print(f'get {habit_id} consecutive clockin days failed: {response.status_code} - {response.text}')
                return 0
        except Exception as e:
            print(f'request failed: {str(e)}')
            return 0





