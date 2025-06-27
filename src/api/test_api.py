import pytest
from task_api import TaskAPI
from stats_api import StatsAPI
from exceptions import TaskNotFound

def test_get_task_not_found():
    with pytest.raises(TaskNotFound):
        TaskAPI.get_task(999)  # ¼ÙÉè ID 999 ²»´æÔÚ

def test_completion_rate():
    result = StatsAPI.get_completion_rate()
    assert "rate" in result
    assert 0 <= result["rate"] <= 100