from pydantic import BaseModel, EmailStr

# Pydantic схемы
class UserAddSchema(BaseModel):
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str