from pydantic import BaseModel, EmailStr


class RegisterDTO(BaseModel):
    register_username: str
    register_password: str
    register_firstname: str
    register_lastname: str
    register_email: EmailStr
    register_gender: str
    register_phone: str


class UpdateRegisterDTO(BaseModel):
    id: int
    register_username: str
    register_password: str
    register_login_vo: int
    register_firstname: str
    register_lastname: str
    register_email: EmailStr
    register_gender: str
    register_phone: str

    class Config:
        from_attributes = True
