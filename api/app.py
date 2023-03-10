import functools
import os
import tempfile

import internetarchive as ia

from typing import Optional
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from iacopilot import __main__
from llama_index import GPTSimpleVectorIndex, LLMPredictor, SimpleDirectoryReader
from langchain.llms import OpenAI


app = FastAPI()
copilot = __main__.IaCopilot()


@functools.lru_cache(maxsize=64)
def get_index(item_id: str) -> GPTSimpleVectorIndex:
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

@app.get('/{item_id}')
def query_item(item_id: str, prompt: Optional[str] = Query(default=None)):
    idx = get_index(item_id)
    if isinstance(idx, GPTSimpleVectorIndex):
       if prompt:
        answer = idx.query(prompt).response.strip()
        return JSONResponse(content={'status': 'success', 'answer': answer})
       else:
        return JSONResponse(content={'status': 'success'})      
    else:
        return JSONResponse(content={'status': 'error'})  

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", reload=True, root_path=os.getenv("ROOT_PATH", "/"))