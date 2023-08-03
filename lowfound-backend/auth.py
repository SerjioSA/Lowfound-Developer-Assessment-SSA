from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext

app = FastAPI()

# Secret key for signing JWT tokens
SECRET_KEY = "mysecretkey"

# Algorithm used for signing JWT tokens
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# User database (for demonstration purposes only)
users_db = {}

class User(BaseModel):
    username: str
    password: str

def get_user(username: str):
    """Get user from database"""
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)

def authenticate_user(username: str, password: str):
    """Authenticate user"""
    user = get_user(username)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

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

@app.post("/register")
async def register(user: User):
    """Register new user"""
    # Check if username already exists
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password before storing in database
    hashed_password = pwd_context.hash(user.password)
    
    # Store new user in database
    users_db[user.username] = {"username": user.username, "password": hashed_password}
    print(users_db)
    return {"message": "User created successfully"}

@app.post("/token")
async def login(form_data: User):
    """Login route"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Protected route for authenticated users"""
    return current_user
