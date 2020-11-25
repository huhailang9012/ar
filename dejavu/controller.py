from fastapi import FastAPI
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
import json

app = FastAPI()
config = {
    "database": {
        "host": "ar.com",
        "user": "postgres",
        "password": "123456",
        "database": "audio_recognition"
    },
    "database_type": "postgres"
}
confidence = 0.1
djv = Dejavu(config)


@app.get("/matched/information/index")
def index(related_key: str):

    infos = djv.find_matched_info(related_key, confidence)
    result = json.dumps(infos, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
    return {"success": True, "code": 0, "msg": "ok", "data": result}


@app.get("/target/audio/recognize")
def recognize_target_audio(audio_id: str, related_key: str, local_audio_path: str):

    FileRecognizer(djv).recognize_file(local_audio_path, related_key, audio_id)
    return {"success": True, "code": 0, "msg": "ok"}


@app.post("/source/audio/import")
def import_source_audio(source_path: str, format: str):

    djv.fingerprint_directory(source_path, ["." + format])
    return {"success": True, "code": 0, "msg": "ok"}


@app.post("/source/audio/query")
def query_source_audio(name: str):
    infos = djv.find_source_audio(name)
    result = json.dumps(infos, default=lambda obj: obj.__dict__, sort_keys=False, indent=4)
    return {"success": True, "code": 0, "msg": "ok", "data": result}