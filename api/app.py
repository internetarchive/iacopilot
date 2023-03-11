import functools
import os
import tempfile
import yaml

import internetarchive as ia

from typing import Union
from enum import Enum
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from iacopilot import __main__
from llama_index import GPTSimpleVectorIndex, LLMPredictor, SimpleDirectoryReader
from langchain.llms import OpenAI
from pydantic import BaseModel



class ApiVersion(str, Enum):
    v1 = "1.0.0"

app = FastAPI(
    version=list(ApiVersion)[-1],
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["GET", "HEAD", "POST", "OPTIONS"],
#     allow_headers=["*"],
#     expose_headers=["link", "x-resume-token", "x-api-version"]
# )

# @app.middleware("http")
# async def add_api_version_header(req: Request, call_next):
#     res = await call_next(req)
#     res.headers["x-api-version"] = f"{req.app.version}"
#     return res

class Query(BaseModel):
    q: Union[str, None]


class PromptQuery(Query):
    prompt: Union[str, None] = None

copilot = __main__.IaCopilot()


@functools.lru_cache(maxsize=64)
def _get_index(item_id: str) -> GPTSimpleVectorIndex:
    index_json_dump = f"{item_id}.json"
    if os.path.isfile(index_json_dump):
        return GPTSimpleVectorIndex.load_from_disk(index_json_dump)
    tmploc = tempfile.mkdtemp()
    ia.download(item_id, destdir=tmploc, no_directory=True, formats="DjVuTXT")
    if not os.listdir(tmploc):
      return "Item was not loaded!"
    docs = SimpleDirectoryReader(tmploc).load_data()
    idx = GPTSimpleVectorIndex(docs, llm_predictor=LLMPredictor(llm=OpenAI(max_tokens=1024, model_name="text-davinci-003")))
    idx.save_to_disk(index_json_dump)
    return idx

def _load_and_query_item(item_id: str, prompt: Union[str, None] = None):
    idx = _get_index(item_id)
    if isinstance(idx, GPTSimpleVectorIndex):
       if prompt:
        answer = idx.query(prompt).response.strip()
        return JSONResponse(content={"status": "success", "answer": answer})
       else:
        return JSONResponse(content={"status": "success"})      
    else:
        return JSONResponse(content={"status": "error"})  

@app.get("/{item_id}", tags=["prompt"])
def query_item_via_query_params(item_id: str, q: Union[str, None] = None):
    return _load_and_query_item(item_id, q)

@app.post("/{item_id}", tags=["prompt"])
def query_item_via_payload(item_id: str, payload: PromptQuery):
    return _load_and_query_item(item_id, payload.prompt)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", reload=True, root_path=os.getenv("ROOT_PATH", "/"))