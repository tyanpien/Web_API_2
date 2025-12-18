## TODO API + WebSocket + Фоновая задача

### Описание:

- **CRUD для задач** (`/tasks`): создание, получение, обновление и удаление задач
- **Фоновая задача**, которая каждые 30 секунд автоматически добавляет новые задачи из внешнего API
- **Ручной запуск генератора задач** через HTTP POST `/task-generator/run`
- **WebSocket** (`/ws/tasks`) для уведомлений о создании/обновлении/удалении задач
- Полностью **асинхронная работа** с базой данных и внешним API
- Фронтенд может получать уведомления в реальном времени через WebSocket

### Установка

```bash
git clone https://github.com/tyanpien/Web_API_2.git
cd WebAPI_2
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

### Запуск

```bash
uvicorn app.main:app --reload --port 9000
```



#### После запуска API документация доступна по адресу http://127.0.0.1:9000/docs