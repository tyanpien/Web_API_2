import asyncio
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from .crud import create_task

API_URL = "https://dummyjson.com/todos"

async def generate_task(db: AsyncSession):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            data = response.json()
            tasks_data = data["todos"]
            for item in tasks_data[:5]:
                await create_task(db, title=item["todo"])
    except Exception as e:
        print("Ошибка при генерации задачи:", e)
        await create_task(db, title="Тестовая задача")

async def start_background_task():
    from .db import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        while True:
            await generate_task(db)
            await asyncio.sleep(30)
