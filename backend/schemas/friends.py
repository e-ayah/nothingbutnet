from pydantic import BaseModel
from typing import Optional

class FriendRequestIn(BaseModel):
    username: str

class FriendUserDetail(BaseModel):
    user_id: str
    name: str
    username: Optional[str]

class AcceptFriendResponse(BaseModel):
    friend: FriendUserDetail