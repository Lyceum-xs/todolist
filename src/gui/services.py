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
    def create_datetime(year, month, day):
        return datetime(year, month, day)


class TaskServices:
    @staticmethod
    def gettasks():
        url = f'{BASE_URL}/tasks'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
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

    @staticmethod
    def sort_treetasks(tasks):
        return sorted(tasks, key = lambda x : x['id'])




