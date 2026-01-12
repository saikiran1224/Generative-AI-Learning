# if not installed - pip3 install fastapi uvicorn

# 1 - library imports
import uvicorn
from fastapi import FastAPI

# 2 - Create the app object
app = FastAPI()

# 3 - Index route, opens on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message' : 'Hello, world!'}

# 4 - Welcome page creation
@app.get('/welcome')
def get_name(name):
    return {'Welcome to my world!' : f'{name}'}

# 5 - Run the API with uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)

# Command to be used to run the file
# uvicorn main:app --reload

# 'main' means the file name, and inside the 'app' object