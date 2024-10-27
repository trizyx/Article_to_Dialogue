import aiohttp  # для асинхронного HTTP-запроса к внешним ссылкам
import shutil
from copy import copy
import os

from fastapi import FastAPI, UploadFile, File, Query, HTTPException, APIRouter
from fastapi.responses import FileResponse
from typing import Optional

from src.services.parser import pdf_to_txt, url_to_txt
from src.services.gpt_api import send_request_to_gpt4_mini, ssml_promt
from src.services.llama_api import send_article_and_get_dialogue
from src.services.voice_synth import voice_synth, AUDIO_DIR
from config.config import config


def delete_everything_in_folder(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)


router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@router.post("/gpt/file_input")
async def api(
    file: Optional[UploadFile] = File(None)
):
    if not file:
        raise HTTPException(status_code=400, detail="Either file or URL must be provided.")
    save_path_out = f"{BASE_DIR}/files_out/save_path_out.txt"

    if not ".txt" in file.filename and not ".pdf" in file.filename:
        raise HTTPException(status_code=400, detail="File is not normal format")
    
    save_path_in = f"{BASE_DIR}/files_input/{file.filename}"
    

    os.makedirs(os.path.dirname(save_path_in), exist_ok=True)
    os.makedirs(os.path.dirname(save_path_out), exist_ok=True)

    with open(save_path_in, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        pdf_to_txt(save_path_in, save_path_out)
    
    if file.filename.endswith(".txt"):
        shutil.copy(save_path_in, save_path_out)
    
    # result = article2dialogue(model, save_path_out, examples)
    result = send_request_to_gpt4_mini(ssml_promt ,save_path_out)
    print(result)
    voice_synth(result, config.api_synth)
    
    
    if not os.path.isfile(AUDIO_DIR):
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(AUDIO_DIR)
    response.headers["Content-Disposition"] = f"attachment; filename={AUDIO_DIR}"  # Указываем имя файла
    
    delete_everything_in_folder(f"{BASE_DIR}/files_out")
    delete_everything_in_folder(f"{BASE_DIR}/files_input")
    return response


@router.post("/gpt/url_input")
async def api(
    url: Optional[str] = Query(None)
):
    if not url:
        raise HTTPException(status_code=400, detail="Either file or URL must be provided.")
    save_path_out = f"{BASE_DIR}/files_out/save_path_out.txt"
    url_to_txt(url, save_path_out)
    # result = article2dialogue(model, save_path_out, examples)
    result = send_request_to_gpt4_mini(ssml_promt ,save_path_out)
    voice_synth(result, config.api_synth)
    
    if not os.path.isfile(AUDIO_DIR):
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(AUDIO_DIR)
    response.headers["Content-Disposition"] = f"attachment; filename={AUDIO_DIR}"  # Указываем имя файла
    
    delete_everything_in_folder(f"{BASE_DIR}/files_out")
    delete_everything_in_folder(f"{BASE_DIR}/files_input")

    return response


@router.post("/llama/file_input")
async def api(
    file: Optional[UploadFile] = File(None)
):
    if not file:
        raise HTTPException(status_code=400, detail="Either file or URL must be provided.")
    save_path_out = f"{BASE_DIR}/files_out/save_path_out.txt"

    if not ".txt" in file.filename and not ".pdf" in file.filename:
        raise HTTPException(status_code=400, detail="File is not normal format")
    
    save_path_in = f"{BASE_DIR}/files_input/{file.filename}"
    

    os.makedirs(os.path.dirname(save_path_in), exist_ok=True)
    os.makedirs(os.path.dirname(save_path_out), exist_ok=True)

    with open(save_path_in, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        pdf_to_txt(save_path_in, save_path_out)
    
    if file.filename.endswith(".txt"):
        shutil.copy(save_path_in, save_path_out)
    
    # result = article2dialogue(model, save_path_out, examples)
    result = send_article_and_get_dialogue(save_path_out)
    print(result)
    try:
        voice_synth(result, config.api_synth)
    except:
        raise HTTPException(status_code=400, detail="анлак бро")
    
    
    if not os.path.isfile(AUDIO_DIR):
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(AUDIO_DIR)
    response.headers["Content-Disposition"] = f"attachment; filename={AUDIO_DIR}"  # Указываем имя файла
    
    delete_everything_in_folder(f"{BASE_DIR}/files_out")
    delete_everything_in_folder(f"{BASE_DIR}/files_input")
    return response


@router.post("/llama/url_input")
async def api(
    url: Optional[str] = Query(None)
):
    if not url:
        raise HTTPException(status_code=400, detail="Either file or URL must be provided.")
    save_path_out = f"{BASE_DIR}/files_out/save_path_out.txt"
    url_to_txt(url, save_path_out)
    # result = article2dialogue(model, save_path_out, examples)
    result = send_article_and_get_dialogue(save_path_out)
    try:
        voice_synth(result, config.api_synth)
    except:
        raise HTTPException(status_code=400, detail="анлак бро")
    
    if not os.path.isfile(AUDIO_DIR):
        raise HTTPException(status_code=404, detail="File not found")

    response = FileResponse(AUDIO_DIR)
    response.headers["Content-Disposition"] = f"attachment; filename={AUDIO_DIR}"  # Указываем имя файла
    
    delete_everything_in_folder(f"{BASE_DIR}/files_out")
    delete_everything_in_folder(f"{BASE_DIR}/files_input")

    return response