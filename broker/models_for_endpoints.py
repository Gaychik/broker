from pydantic import BaseModel

class MessageRequest(BaseModel):
    message_id:str
    command:str
    device_id:str
    status:str
    result:str
    target_host: str
    target_port: str