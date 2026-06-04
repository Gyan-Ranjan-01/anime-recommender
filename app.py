from fastapi import FastAPI, HTTPException, Request
from recommender import recommend

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(title = "Anime Recommender")

#static files
app.mount('/static', StaticFiles(directory='static'), name = 'static')

#for template
templates = Jinja2Templates(directory = 'templates')


@app.get('/', response_class=HTMLResponse)
def home(request : Request):
    return templates.TemplateResponse(
        request=request,
        name='index.html'
        )


@app.get("/recommend/{title}")
def get_recommendations(title : str, k : int = 5):
    query_name, results = recommend(title,k)
    if query_name is None:
        raise HTTPException (status_code = 404, detail = f'No match found for the {title}')
    return {
        'query': query_name,
        'recommendations': results
    }
