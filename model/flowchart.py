from pydantic import BaseModel
from typing import Optional, List, Dict

class Flowchart(BaseModel):
    id: int
    name: str
    graph: Dict[str, List[str]]

class updated_flowchart(BaseModel):
    name: Optional[str] = None
    graph: Optional[dict] = None
