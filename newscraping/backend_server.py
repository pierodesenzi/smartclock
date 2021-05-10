from fastapi import FastAPI
import uvicorn, requests, ast, charfixer
from fastapi.middleware.cors import CORSMiddleware
from scraper import *

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/weather')
async def weather():
    data = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=-23.658&lon=-46.6827&appid=d7ac1f99b520b6521c21eb7775399347",
        headers = { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'}).content.decode()

    parsed = ast.literal_eval(data)
    return int(parsed['main']['temp'] - 273.15)


@app.get('/news')
async def newsfeed():
    whole_feed = []
    whole_feed.extend(estadao_internacional())
    whole_feed.extend(globo_politica()[:15])
    #whole_feed.extend(uol_reinaldo_azevedo()[:8])
    for i in range(len(whole_feed)):
        whole_feed[i]['title'] = charfixer.stringToConvert(whole_feed[i]['title'])

    # The following snippet couldn't have been any more copy pasted.
    # I don't have time to reinvent the wheel.
    seen = set()
    new_l = []
    for d in whole_feed:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)

    return new_l


if __name__=='__main__':
    uvicorn.run('backend_server:app', reload=True, port=8000)