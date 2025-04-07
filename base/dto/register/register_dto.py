from pydantic import BaseModel


class RegisterDTO(BaseModel):
    register_username: str
    register_password: str
    register_firstname: str
    register_lastname: str
    register_email: str
    register_gender: str
    register_phone: str

    class Config:
        from_attributes = True
