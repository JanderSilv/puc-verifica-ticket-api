from pydantic import BaseModel


class ResponseException(BaseModel):
  message: str
