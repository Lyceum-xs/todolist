from fastapi import APIRouter, HTTPException
from .. import services, schemas

router = APIRouter(prefix="/pomodoros", tags=["番茄钟"])

@router.post("/", response_model=schemas.PomodoroOut, status_code=201, summary="开始番茄钟")
def start_pomodoro(data: schemas.PomodoroStart):
    return services.PomodoroService.start(data)

@router.patch("/{session_id}/stop", response_model=schemas.PomodoroOut, summary="结束番茄钟")
def stop_pomodoro(session_id: int):
    try:
        return services.PomodoroService.stop(session_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Pomodoro not found")

@router.get("/", response_model=list[schemas.PomodoroOut], summary="番茄钟列表")
def list_pomodoros():
    return services.PomodoroService.list_all()