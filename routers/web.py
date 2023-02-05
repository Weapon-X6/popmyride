from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Carsharing Demo</title>
        </head>
        <body>
            <h1>Welcome to this new Car Sharing service!</h1>
            <p>Don't fake this</p>
        </body>
    </html>
    """