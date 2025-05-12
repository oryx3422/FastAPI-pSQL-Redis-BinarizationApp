from pydantic import BaseModel, EmailStr

class UserAddSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
