# AI-Powered Task & Knowledge Management MVP

A minimal full-stack system where admins upload knowledge documents, assign tasks, and users search the knowledge base with an embedding-style semantic search flow before completing their assigned work.

## Features

- JWT authentication with admin and user roles
- Relational schema for users, roles, tasks, documents, and activity logs
- Document upload for .txt and .pdf files with stored metadata and text content
- Local embedding-based semantic search over indexed document content
- Task filtering by status and assignee
- Analytics for task totals, completion state, and the most searched query

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic, JWT, SQLite/MySQL-ready
- Frontend: React + Vite + Axios
- Search: lightweight local vector store built in Python

## Project Structure

```text
project/
├── backend/
│   ├── app/
│   │   ├── api/v1/routers/
│   │   ├── core/
│   │   ├── db/
│   │   ├── exceptions/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── components/
    │   ├── context/
    │   └── pages/
```

## Setup

### Backend
```bash
cd backend
C:/Users/Meghana/AppData/Local/Python/pythoncore-3.14-64/python.exe -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Frontend
```bash
cd frontend
npm install
```

## Run

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
npm run dev
```

Open http://localhost:5173 and use the seeded admin account:
- Email: admin@example.com
- Password: Admin123!

## Auth / Swagger Login

The backend supports two login flows:

- `POST /api/v1/auth/login` — JSON body login for the frontend
- `POST /api/v1/auth/login/form` — OAuth2 password form login for Swagger

### JSON login request body

```json
{
  "email": "admin@example.com",
  "password": "Admin123!"
}
```

### Swagger OAuth2 login

In Swagger UI, use the following when authorizing:
- Token URL: `/api/v1/auth/login/form`
- Flow: password
- username: your email
- password: your password
- client credentials location: Authorization header
- client_id: leave blank
- client_secret: leave blank

After authorization, Swagger will use the bearer token in the `Authorization` header for protected requests.

## API Summary

- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me
- GET /api/v1/tasks
- POST /api/v1/tasks
- PATCH /api/v1/tasks/{id}
- GET /api/v1/documents
- POST /api/v1/documents
- POST /api/v1/search
- GET /api/v1/analytics

## Screenshots

Screenshots from the running app are available after launch in the browser and can be captured from the UI.
