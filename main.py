from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


app = FastAPI()

@app.get("/")
def home():
    return{"message": "Hello, FastAPI"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}

class item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

Base = declarative_base()
engine = create_engine("sqlite:///./test.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    Base.metadata.create_all(bind=engine)

@app.post("/items/")
def create_item(item: item):
    return{"item":item}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    if token != "secrettoken":
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return {"user": "authenticated"}
