from fastapi import FastAPI, Request, status
from database import engine, Base
from routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
app = FastAPI()

Base.metadata.create_all(bind=engine)


app.mount("/static", StaticFiles(directory="static"), name='static')


@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
async def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
