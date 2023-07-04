import fastapi, os
APPLICATION_HOST = os.environ.get("APPLICATION_HOST", "localhost")
application = fastapi.FastAPI() 
application.host = APPLICATION_HOST