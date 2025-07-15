from fastapi import APIRouter, HTTPException, Path
from dependency import db_dependency, user_dependency
from starlette import status
from models import Todos
router = APIRouter(
    prefix="/admin",
    tags=['admin']
)


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.delete(todo_model)
    db.commit()
