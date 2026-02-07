from fastapi import FastAPI, HTTPException
from fastapi import Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from models.services import get_user, create_user
from auth.dependency import get_current_user_id
from auth.security import hash_password, verify_password, create_access_token
from db.databse import get_connection
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Add CORS middleware to allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "https://frontend-personal-time-management-app.onrender.com"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserSignupModel(BaseModel):
    useremail: str
    password: str


class UserLoginModel(BaseModel):
    useremail: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TaskCreateModel(BaseModel):
    title: str
    description: str
    is_completed: int = 0


class TaskUpdateModel(BaseModel):
    title: str = None
    description: str = None
    is_completed: int = None


@app.get('/')
async def root():
    return {"message": "Connection Established"}


@app.post('/signup', response_model=dict)
async def sign_up(user_req: UserSignupModel):
    # Check if user already exists
    existing_user = get_user(user_req.useremail)
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    # Hash password and create user
    password_hash = hash_password(user_req.password)
    user_id = create_user(user_req.useremail, password_hash)
    
    return {
        "message": "User created successfully",
        "user_id": user_id,
        "useremail": user_req.useremail
    }


@app.post('/login', response_model=TokenResponse)
async def login(user_req: UserLoginModel):
    # Get user from database
    user = get_user(user_req.useremail)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(user_req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create JWT token
    access_token = create_access_token(data={"user_id": user["id"], "email": user["email"]})
    
    return TokenResponse(access_token=access_token)




@app.get("/tasks")
def get_tasks(user_id: int = Depends(get_current_user_id)):
    conn = get_connection()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()

    return [dict(t) for t in tasks]


@app.get("/tasks/{task_id}")
def get_task(task_id: int, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()
    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, user_id)
    ).fetchone()
    conn.close()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return dict(task)


@app.post("/tasks")
def create_task(task: TaskCreateModel, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO tasks (title, description, user_id, is_completed) VALUES (?, ?, ?, ?)",
            (task.title, task.description, user_id, task.is_completed)
        )
        conn.commit()
        task_id = cursor.lastrowid
        
        # Fetch the created task
        created_task = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return dict(created_task)
    finally:
        conn.close()


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdateModel, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()
    try:
        # Check if task exists and belongs to user
        existing = conn.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()
        
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Build update query dynamically based on provided fields
        updates = []
        values = []
        
        if task.title is not None:
            updates.append("title = ?")
            values.append(task.title)
        if task.description is not None:
            updates.append("description = ?")
            values.append(task.description)
        if task.is_completed is not None:
            updates.append("is_completed = ?")
            values.append(task.is_completed)
        
        if not updates:
            # No updates provided, return existing task
            return dict(existing)
        
        values.extend([task_id, user_id])
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
        
        conn.execute(query, values)
        conn.commit()
        
        # Fetch updated task
        updated_task = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return dict(updated_task)
    finally:
        conn.close()


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user_id)):
    conn = get_connection()
    try:
        # Check if task exists and belongs to user
        existing = conn.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        ).fetchone()
        
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found")
        
        conn.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
        conn.commit()
        return {"message": "Task deleted successfully"}
    finally:
        conn.close()

