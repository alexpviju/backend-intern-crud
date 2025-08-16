# LawVriksh Blog API - Backend Intern Assignment

A simple **FastAPI** based backend project for a blogging system with **CRUD operations**, **authentication**, **likes**, and **comments**.

---

## 📂 Project Structure

backend-intern-crud/
│
├── src/
│ ├── routes/
│ │ ├── comments.py
│ │ ├── likes.py
│ │ ├── posts.py
│ │ └── users.py
│ │
│ ├── auth.py
│ ├── database.py
│ ├── main.py
│ ├── models.py
│ └── schemas.py
│
├── uploads/
└── blog.db

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/backend-intern-crud.git
cd backend-intern-crud
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
.
env\Scripts ctivate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
uvicorn src.main:app --reload
```
Access the API at 👉 http://localhost:8000  
Interactive Docs 👉 http://localhost:8000/docs

---

## 📚 API Documentation

### 🔑 Authentication

#### Register User  
**Request**
```http
POST /auth/register
Content-Type: application/json
```
```json
{
  "username": "law_user",
  "email": "user@lawvriksh.com",
  "password": "secure123"
}
```

**Response (201 Created)**
```json
{
  "message": "User registered successfully"
}
```

#### Login  
**Request**
```http
POST /auth/login
Content-Type: application/json
```
```json
{
  "email": "user@lawvriksh.com",
  "password": "secure123"
}
```

**Response (200 OK)**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

---

### 📝 Posts

#### Create Post  
**Request**
```http
POST /posts/
Authorization: Bearer <token>
Content-Type: multipart/form-data
```
**Form Data**
- title: "New Legal Guidelines"
- content: "Summary of recent changes..."
- image: [upload file]

**Response (201 Created)**
```json
{
  "id": 1,
  "title": "New Legal Guidelines",
  "content": "Summary of recent changes...",
  "image": "/uploads/legal.jpg",
  "like_count": 0,
  "comment_count": 0,
  "created_at": "2023-08-16T10:30:00",
  "author": {
    "id": 1,
    "username": "law_user"
  }
}
```

#### Get All Posts  
**Request**
```http
GET /posts/
```
**Response (200 OK)**
```json
[
  {
    "id": 1,
    "title": "New Legal Guidelines",
    "content": "Summary of recent changes...",
    "like_count": 3,
    "comment_count": 2,
    "created_at": "2023-08-16T10:30:00",
    "author": {
      "id": 1,
      "username": "law_user"
    }
  }
]
```

---

### ❤️ Likes

#### Like/Unlike Post  
**Request**
```http
POST /likes/1
Authorization: Bearer <token>
```
**Response (200 OK)**
```json
{
  "message": "Post liked"
}
```
(or `"Like removed"` on second call)

#### Get Post Likes  
**Request**
```http
GET /likes/post/1
```
**Response (200 OK)**
```json
[
  {
    "id": 1,
    "created_at": "2023-08-16T10:35:00",
    "user": {
      "id": 2,
      "username": "client_user"
    }
  }
]
```

---

### 💬 Comments

#### Add Comment  
**Request**
```http
POST /comments/1
Authorization: Bearer <token>
Content-Type: application/json
```
```json
{
  "content": "This is very informative!"
}
```

**Response (201 Created)**
```json
{
  "id": 1,
  "content": "This is very informative!",
  "created_at": "2023-08-16T10:40:00",
  "user": {
    "id": 2,
    "username": "client_user"
  }
}
```

#### Get Post Comments  
**Request**
```http
GET /comments/post/1
```
**Response (200 OK)**
```json
[
  {
    "id": 1,
    "content": "This is very informative!",
    "created_at": "2023-08-16T10:40:00",
    "user": {
      "id": 2,
      "username": "client_user"
    }
  }
]
```

---

## 🧪 Testing

Import the Postman collection from repository root  

**Test workflow:**  
Register → Login → Create Post → Like Post → Add Comment  

Verify responses match the examples above ✅

---

## ⚙️ Configuration

- **Database**: Auto-created at `blog.db` on first run  
- **Uploads**: Files saved in `uploads/` directory  
- **API Docs**: Available at http://localhost:8000/docs

---

## 📁 .gitignore
```
venv/
__pycache__/
uploads/
*.db
*.db-journal
.env
```

---

## 🛠️ Development Notes

- Route handlers → `src/routes/`
- Database models → `src/models.py`
- JWT Authentication → `src/auth.py`
- Token expires after 30 minutes
