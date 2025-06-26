class APIError(Exception):
    """基础API异常"""
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)

class TaskNotFoundError(APIError):
    """任务不存在异常"""
    def __init__(self, task_id: int):
        super().__init__(f"Task ID {task_id} not found", 404)

class InvalidStatusError(APIError):
    """无效状态异常"""
    def __init__(self, status: str):
        super().__init__(f"Invalid status: {status}", 422)