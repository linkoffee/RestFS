from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.file_service import (
    create_file,
    get_file_with_content,
    update_file,
    delete_file,
    list_files
)
from app.schemas.file import FileCreate, FileGet, FileUpdate

router_v1 = APIRouter()


@router_v1.post('/', response_model=FileGet)
def create_file_route(file: FileCreate, db: Session = Depends(get_db)):
    try:
        new_file = create_file(db, file)
        return FileGet.from_orm(new_file)
    except FileExistsError as err:
        raise HTTPException(status_code=400, detail=f'{err}')


@router_v1.get('/{file_id}', response_model=FileGet)
def get_file_route(file_id: int, db: Session = Depends(get_db)):
    file = get_file_with_content(db, file_id)
    if not file:
        raise HTTPException(
            status_code=404,
            detail=f'Error 404. File №{file_id} not found.'
        )
    return file


@router_v1.put('/{file_id}', response_model=FileGet)
def update_file_route(file_id: int, file_data: FileUpdate,
                      db: Session = Depends(get_db)):
    updated_file = update_file(db, file_id, file_data)
    if updated_file is None:
        raise HTTPException(
            status_code=404,
            detail=f'Error 404. File №{file_id} not found.'
        )
    return FileGet.from_orm(updated_file)


@ router_v1.delete('/{file_id}', response_model=dict)
def delete_file_route(file_id: int, db: Session = Depends(get_db)):
    deleted_file = delete_file(db, file_id)
    if not deleted_file:
        raise HTTPException(
            status_code=404,
            detail=f'Error 404. File №{file_id} not found.'
        )
    return {'message': f'File №{file_id} was deleted successfully.'}


@ router_v1.get('/', response_model=List[FileGet])
def list_files_route(db: Session = Depends(get_db)):
    files = list_files(db)
    return [FileGet.from_orm(file) for file in files]
