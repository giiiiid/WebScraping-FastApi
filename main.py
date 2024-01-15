from fastapi import FastAPI, Body
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class WebUrl(BaseModel):
    url: HttpUrl


class SchemaExample(WebUrl):
    name: str | None = None
    desc: str | None = None
    image: str | None = None

    class Config:
        json_schema_extra = {
            "example":{
            "url":"https://www.github.com",
            "name":"Github",
            "desc":"A platform to build public",
            "image":"new.png"
        }
    }

@app.post("/scrape-web", response_model=SchemaExample)
async def web_scrape(url: WebUrl= Body(..., embed=True)):

    # import pdb
    # pdb.set_trace()
    
    page = requests.get(str(url.url))

    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.head.title.text

    return {
        "name":title
    }