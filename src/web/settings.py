import fastapi, os
DEBUG_MODE = os.environ.get("DEBUG_MODE", True)
application = fastapi.FastAPI(debug=DEBUG_MODE) 

