from pydantic import BaseModel


class LoginDTO(BaseModel):
    login_username: str
    login_password: str


class UpdateLoginDTO(BaseModel):
    id: int
    login_username: str
    login_password: str

    class Config:
        from_attributes = True
