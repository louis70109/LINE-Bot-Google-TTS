from fastapi import APIRouter, HTTPException

from utils.common import contents_dict_to_vtt
from utils.firebase import get_all_collection, get_collection, update_subtitle, create_subtitle, \
    remove_subtitle, get_audios_collection

router = APIRouter(
    prefix="/subtitles",
    tags=["subtitles"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{vid}")
def get_subtitles(vid: str, vtt: str = '0') -> list:
    subtitles = []
    for subtitle in get_audios_collection('subtitles', vid):
        subtitles.append(subtitle.to_dict())

    if vtt != "0":
        return contents_dict_to_vtt(subtitles)
    return subtitles


@router.get("/{vid}/{id}")
def get_specific_subtitle(vid: str, id: str) -> dict:
    subtitle = get_collection('subtitles', f"{vid}_{id}")
    return subtitle


@router.post("/{vid}")
def post_subtitle(vid: str, subtitle: dict):
    # {"id":9,"start_time":"0:08:59.800",
    # "vid":"UUID","description":"一個",
    # end_time":"0:09:59.700"}
    sub_dict = {'vid': vid, **subtitle}
    db_subtitle = get_collection('subtitles', f"{vid}_{sub_dict.get('id')}")
    if db_subtitle:
        raise HTTPException(status_code=400, detail="Subtitle created")
    result = create_subtitle(sub_dict)
    if result != {}:
        raise HTTPException(status_code=400, detail="Subtitle create fail, please check body.")
    return get_collection('subtitles', f"{vid}_{sub_dict.get('id')}")


@router.put("/{vid}")
def put_subtitle(vid: str, subtitle: dict):
    # {"id":9,"start_time":"0:08:59.800",
    # "vid":"UUID","description":"一個",
    # end_time":"0:09:59.700"}
    sub_dict = {'vid': vid, **subtitle}
    db_subtitle = get_collection('subtitles', f"{vid}_{sub_dict.get('id')}")
    if db_subtitle is None:
        raise HTTPException(status_code=404, detail="Subtitle not found")
    result = update_subtitle(sub_dict)
    if result != {}:
        raise HTTPException(status_code=400, detail="Subtitle update fail, please check body.")
    return get_collection('subtitles', f"{vid}_{sub_dict.get('id')}")


@router.delete("/{vid}/{id}")
def delete_subtitle(vid: str, id: str):
    db_subtitle = get_collection('subtitles', f"{vid}_{id}")
    if db_subtitle is None:
        raise HTTPException(status_code=404, detail="Subtitle not found")
    result = remove_subtitle(vid, id)
    if result != {}:
        raise HTTPException(status_code=400, detail="Subtitle remove fail, please check body.")
    return {}
