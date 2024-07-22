
from rest_framework.views import exception_handler
from rest_framework.response import Response
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class CustomException(Exception, ABC):
    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @abstractmethod
    def __init__(self,message: str):
        super().__init__(message)
        self.message = message
    


    @abstractmethod
    def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
        pass

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomException):
        error_list = exc.serialize_errors()
        custom_response_data = {'errors': error_list}
        return Response(custom_response_data, status=exc.status_code())

    return response
    
    # return Response({'errors':[
    #     {
    #         'message':"Internal server error",
    #         "field":""
    #     }
    # ]}, status = 500)

        



    
    
# class ServerErrorException(CustomException):

#     def status_code(self) -> int:
#         return 500
    
#     def __init__(self,message:str):
#         super().__init__(message)


#     def serialize_errors(self) -> List[Dict[str, Optional[str]]]:
#         return [{"message": self.message, "field": None}]
    

    

    



    
    





