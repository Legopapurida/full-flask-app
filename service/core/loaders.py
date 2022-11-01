from dataclasses import KW_ONLY, dataclass, field
from typing import Any, Dict, Optional


@dataclass
class UserModel:
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLoader:

    user: UserModel = None

    def set_user(self, new_user: Any):
        self.user = new_user

    def delete_user(self):
        self.user = None
