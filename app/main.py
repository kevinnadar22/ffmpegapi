#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: main.py
Author: Maria Kevin
Created: 2025-11-09
Description: FFmpeg command execution via FastAPI endpoint.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

import shlex
import subprocess
from contextlib import asynccontextmanager
from typing import Dict, Tuple, Union
from typing_extensions import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.models import CommandResult
from app.utils import (
    allow_command,
    ensure_directories_exist,
    preprocess_cmd,
    get_output_path_from_cmd,
)
from app.task import periodic_cleanup
import asyncio
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories_exist()
    task = asyncio.create_task(periodic_cleanup())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)

ensure_directories_exist()  # need to ensure directories exist before mounting static files
app.mount("/static", StaticFiles(directory=settings.output_dir), name="static")


@app.get("/")
async def read_root():
    return {"message": "use /run to execute the main functionality"}


@app.post("/run", response_model=CommandResult)
async def ffmpeg_run(
    request: Request,
    _: Annotated[bool, Depends(allow_command)],
    cmd: Annotated[str, Depends(preprocess_cmd)],
    return_file: bool = Form(
        False, description="If true, returns the output file itself."
    ),
) -> Union[CommandResult, Tuple[Dict[str, str], int], RedirectResponse]:
    """Executes the provided FFmpeg command after validation and preprocessing."""
    try:
        # Tokenize and execute
        result = subprocess.run(
            shlex.split(cmd), capture_output=True, text=True, timeout=30
        )

        output_url = request.url_for(
            "static", path=get_output_path_from_cmd(cmd, replace_parent_dir=True)
        )

        if return_file:
            return RedirectResponse(output_url, status_code=302)

        return CommandResult(
            cmd=cmd,
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            output_url=str(output_url),
        )
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out"}, 408
    except Exception as e:
        return {"error": str(e)}, 500
