from pydantic import BaseModel

class Source(BaseModel):
  name: str
  url: str

class NewsResult(BaseModel):
  headline: str
  description: str
  source: list[Source]

class NewsResults(BaseModel):
  results: list[NewsResult]