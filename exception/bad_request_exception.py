


from .exception import CustomException 
from typing import List, Dict, Optional



class BadRequestException(CustomException):

    def status_code(self) -> int:
        return 400
    
    def __init__(self,message:str):
        super().__init__(message)


    def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
        return [{"message": self.message, "field": None}]