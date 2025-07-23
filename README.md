# goit-pythonweb-hw-10

---

## Запуск

### 1. Заповнити `.env`

```env
# Database Configuration
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=...

#JWT
JWT_SECRET=...

#CLOUDINARY
CLOUDINARY_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```
### 2. Запусти проєкт:

```bash
docker-compose up --build
```
### При першому запуску:

Застосуються міграції Alembic

Запуститься FastAPI на http://localhost:8000/docs

