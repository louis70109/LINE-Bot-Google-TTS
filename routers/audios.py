import os
from typing import List

from fastapi import APIRouter

from utils.firebase import get_all_collection, get_collection

router = APIRouter(
    prefix="/audios",
    tags=["audios"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_audios():
    audios = []
    for audio in get_all_collection('audios'):
        audios.append(audio.to_dict())
    return audios


@router.get("/{audio_name}")
def get_specific_audio(audio_name: str) -> list:
    audio = get_collection('audios', f"{os.getenv('GOOGLE_BUCKET')}_{audio_name}")
    return audio

#
# @router.post("/", response_model=schemas.User)
# def create_audio(audio: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_audio = crud.get_audio_by_uid(db, audio_id=audio.uid)
#     if db_audio:
#         raise HTTPException(status_code=400, detail="User already registered")
#     return crud.create_audio(db=db, audio=audio)
#
#
# @router.post("/{audio_id}/projects/", response_model=schemas.Project)
# def create_audio_projects(audio_id: str, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
#     db_audio = crud.get_audio_by_uid(db, audio_id=audio_id)
#     if not db_audio:
#         raise HTTPException(status_code=400, detail="User not registered")
#     project = crud.create_audio_project(db, project=project, audio_id=audio_id)
#     return project
#
#
# @router.get("/{audio_id}/projects/", response_model=List[schemas.Project])
# def read_audio_projects(audio_id: str, db: Session = Depends(get_db)):
#     db_audio = crud.get_audio_by_uid(db, audio_id=audio_id)
#     if not db_audio:
#         raise HTTPException(status_code=400, detail="User not registered")
#     audio_projects = crud.get_audio_projects(db, audio_id=audio_id)
#     return audio_projects