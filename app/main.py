"""
uvicorn app.main:app --port 7070 --reload

http://127.0.0.1:7070/docs
http://127.0.0.1:7070/health

"""

from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi

from datetime import datetime

import logging as log
import httpx

API_TITLE = 'Repository Info API'
API_VERSION = '1.0.0'
API_DESCRIPTION = 'Retrieves repository information from GitHub.'
API_LOGO = '/static/images/koweg.png'

HTTP_CODE_ACCEPTED = '202'
HTTP_CODE_NOT_FOUND = '404'

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title = API_TITLE,
        version = API_VERSION,
        description = API_DESCRIPTION,
        routes=app.routes,
    )
    openapi_schema['info']['x-logo'] = {
        'url': API_LOGO
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(title=API_TITLE)
app.openapi = custom_openapi

GITHUB_API_URL = 'https://api.github.com'
GITHUB_ACCEPT_HEADER = 'application/vnd.github+json'
GITHUB_API_VERSION = '2022-11-28'

# ---------- Endpoints -------------------

@app.get('/health', include_in_schema=False )
async def health_check():
    return {'status': 'OK', 'time': datetime.now().strftime('%Y-%m-%d, %H:%M:%S')} 


@app.get("/api/repo/user/{username}",response_description="User repository information summary", status_code=200)
async def get_github_repos(username: str):
    """
    Retrieves summary information about a GitHub repository, including number of public repositories and their names. <br/>
    The repository information is fetched from GitHub using the provided user name. <br/>
    """
    call_header = {
            'Accept': GITHUB_ACCEPT_HEADER,
            'X-GitHub-Api-Version': GITHUB_API_VERSION
        }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_URL}/users/{username}/repos", headers=call_header)

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="GitHub API error"
            )

        repos = response.json()
        return {
            "username": username,
            "repository_count": len(repos),
            "repository_names": [repo["name"] for repo in repos],
        }
