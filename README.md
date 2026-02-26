# Nebius Assignment

 Basic GitHub repository information retrieval API


## Installing and running from commandline

``` shell

  pip install virtualenv
  virtualenv -p python3.13 .venv
  .\.venv\Scripts\activate
  pip install --no-cache-dir --upgrade -r requirements.txt

  uvicorn app.main:app --port 7070 --reload

```

## API Endpoints

```

  http://127.0.0.1:7070/docs
  http://127.0.0.1:7070/health

```
