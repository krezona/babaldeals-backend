from .exception import CustomException 
from typing import List, Dict

class NotAuthorized(CustomException):
    def status_code(self) -> int:
        return 401
    
    def __init__(self,message:str):
        super().__init__(message)

    def serialize_errors(self) -> List[Dict[str, str | None]]:
        return [{"message": self.message, "field": None}]