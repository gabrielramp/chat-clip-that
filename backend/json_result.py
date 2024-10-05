from pydantic import BaseModel
from typing import List

class json_result(BaseModel):
    meme_token: str
    timestamp: str

class json_result_array(BaseModel):
    results: List[json_result]