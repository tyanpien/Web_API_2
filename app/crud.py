from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Task

async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

async def create_task(db: AsyncSession, title: str):
    task = Task(title=title)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task: Task):
    await db.delete(task)
    await db.commit()
