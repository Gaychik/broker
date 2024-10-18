from pydantic import BaseModel

class MessageRequest(BaseModel):
    command:str
    device_id:str
    status:str
    target_host: str
    target_port: str
    result:str = ""