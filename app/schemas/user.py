from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    is_active: bool = True

class UserInDB(User):
    hashed_password: str | None = None

class UserCreate(BaseModel):
    username: str
    password: str
