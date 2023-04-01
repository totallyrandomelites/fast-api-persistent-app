from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List
import os


app = FastAPI()


class FileAppend(BaseModel):
    """Object that contains data to insert to file"""
    lines: List[str]
    """Lines to insert in the file"""


@app.post("/file/create/{filename}")
def create_file(filename: str = Path(..., description="The name of the file to create")):
    """Creates a new empty file."""
    path = f"/run/fast-dir/{filename}"
    try:
        with open(path, "w") as f:
            pass
    except OSError:
        raise HTTPException(status_code=400, detail="File already exists")
    return {"message": f"File {filename} created"}


@app.post("/file/append/{filename}")
def append_to_file(file: FileAppend, filename: str = Path(..., description="The name of the file to append data to")):
    """Appends given lines to the file."""
    path = f"/run/fast-dir/{filename}"
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="File not found")
    with open(path, "a") as f:
        f.writelines([i + '\n' for i in file.lines])
    return {"message": f"Lines added to file {filename}"}


@app.get("/file/contents/{filename}")
def get_file_contents(filename: str = Path(..., description="The name of the file to retrieve")):
    """Gets the contents of the file."""
    path = f"/run/fast-dir/{filename}"
    if not os.path.isfile(path):
        raise HTTPException(status_code=400, detail="File not found")
    with open(path, "r") as f:
        contents = f.read()
    return {"contents": contents}
