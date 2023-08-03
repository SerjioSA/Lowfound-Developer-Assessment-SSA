from fastapi import FastAPI, WebSocket,Request,Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ai_api
import uvicorn
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine


# Load .env
load_dotenv()

# Init FastAPI
app = FastAPI()

#DB stuff 
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Secret key for signing JWT tokens
SECRET_KEY = os.getenv('SECRET_KEY')

# Algorithm used for signing JWT tokens
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# User database (for demonstration purposes only)
users_db = {}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = []

# Add questions
@app.post("/ask-question", tags=["questions"])
async def add_question(card: dict) -> dict:
    
    last_id = 1
    if (len(questions) != 0):
        last_id = questions[ len(questions) - 1]['id'] 
        
    questions.append({ 
        "id": last_id + 1,
        "date":card['date'],
        "question":card['question'],
        "answer":ai_api.send_question(card['question'])}) 
    
    return { "data": questions[-1] }

# Get all questions
@app.get("/questions", tags=["todos"])
async def get_questions() -> dict:
    return { "data": questions }

# # Get last question 
# @app.get("/questions/last", tags=["todos"])
# async def get_questions() -> dict:
#     if (len(questions) > 0):
#         return { "data": questions[-1] }

# Delete all questions
@app.delete("/questions")
async def delete_item():
    # Your code to delete the item with the given item_id
    questions.clear()
    return {"message": f"DB has been deleted"}


class User(BaseModel):
    email: str
    username: str
    password: str





def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    return user




@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Protected route for authenticated users"""
    return current_user


# Stuff with db
# Registation in DB
# works
@app.post("/register",response_model=schemas.User)
async def register(user: User, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if username already exists
    # Check if username already exists
    db_user = crud.get_user(db, username = user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    
    
    # Hash password before storing in database
    user.password = pwd_context.hash(user.password)
    
    # Store new user in database    
    return crud.create_user(db=db, user=user)


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: User, db: Session = Depends(get_db)):
#     """Register new user"""
    
#     # Check if username already exists
#     db_user = crud.get_user(db, username = user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
    
    
#     return crud.create_user(db=db, user=user)

# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_user(username: str,db: Session = Depends(get_db)):
    """Get user from database"""
    db_user = crud.get_user(db, username=username)
    if db_user:
        user_dict = db_user
        return user_dict

def authenticate_user(username: str, password: str,db: Session = Depends(get_db)):
    """Authenticate user"""
    user = get_user(username = username,db=db)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

# Works
@app.post("/token")
async def login(form_data: User,db: Session = Depends(get_db)):
    """Login route"""
    

    user = authenticate_user(username = form_data.username, password=form_data.password,db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/users/{user_id}/items/", response_model=list[schemas.Item])
def read_items_froom_id( user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items_from_id(db,owner_id=user_id, skip=skip, limit=limit)
    return items

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items



if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port = 8000)