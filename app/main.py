from fastapi import FastAPI, Depends, WebSocket, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .db import engine, Base, get_db
from .schemas import TaskCreate, TaskUpdate, TaskOut
from .crud import get_tasks, get_task, create_task, delete_task
from .websocket import manager
from .task_generator import generate_task, start_background_task
import asyncio

app = FastAPI(title="TODO API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    asyncio.create_task(start_background_task())

@app.get("/tasks", response_model=list[TaskOut])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await get_tasks(db)

@app.get("/tasks/{task_id}", response_model=TaskOut)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(404)
    return task

@app.post("/tasks", response_model=TaskOut)
async def add_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = await create_task(db, task.title)
    await manager.broadcast(f"Создана новая задача: {task.title}")
    return new_task

@app.patch("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(404)
    if data.title is not None:
        task.title = data.title
    if data.completed is not None:
        task.completed = data.completed
    await db.commit()
    await db.refresh(task)
    await manager.broadcast(f"Задача обновлена: {task.title}")
    return task

@app.delete("/tasks/{task_id}")
async def remove_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(404)
    await delete_task(db, task)
    await manager.broadcast(f"Задача удалена: {task.title}")
    return {"status": "deleted"}

@app.post("/task-generator/run")
async def run_generator(db: AsyncSession = Depends(get_db)):
    await generate_task(db)
    await manager.broadcast("Сгенерированы новые задачи")
    return {"status": "task generated"}

@app.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)
