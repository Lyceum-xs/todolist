from fastapi import HTTPException
from starlette import status

class APIError(HTTPException):
    """基础API异常"""
    def __init__(self, detail: str = "API处理错误"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class TaskNotFound(HTTPException):
    """任务不存在异常"""
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务ID {task_id} 不存在"
        )

class InvalidTaskData(HTTPException):
    """无效任务数据异常"""
    def __init__(self, field: str, reason: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"字段 {field} 无效: {reason}"
        )