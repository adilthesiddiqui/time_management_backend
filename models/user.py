from pydantic import BaseModel
from pydantic import EmailStr
import datetime

class UserDbModel(BaseModel):
    id : int
    user_email : str
    password_hash : str
    created_at : datetime.datetime