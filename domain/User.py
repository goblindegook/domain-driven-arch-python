from pydantic import EmailStr, BaseModel


class User(BaseModel):
    email: EmailStr
    name: str
    password: str
