#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: command_processing.py
Author: Maria Kevin
Created: 2025-11-09
Description: Command preprocessing and manipulation functions for FFmpeg commands.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


import shlex
from typing_extensions import Annotated
from fastapi import File, UploadFile, Form
from app.config import settings
from app.exceptions import InvalidFFmpegCommandException
from app.utils.file_operations import save_uploaded_file
from app.utils.system import create_temp_folder
from app.utils.validation import input_file_size_within_limit


def preprocess_cmd(
    input_path: Annotated[UploadFile, File()],
    cmd: str = Form(...),
) -> str:
    """Saves the uploaded input file and replaces the input tag in the command.

    Example:
    If cmd is "ffmpeg -i input.mp4 -c:v libx264 output.mp4" and the uploaded file
    is "input.mp4", this function saves the file to the upload directory and replaces
    "input.mp4" with the full path to the saved file.

    """

    # check if multple -i tags exist, if yes raise exception
    if cmd.count(r"-i") != 1:
        raise InvalidFFmpegCommandException(
            detail="Command must contain exactly one input tag '-i'."
        )

    if not input_file_size_within_limit(input_path.size):
        raise InvalidFFmpegCommandException(
            detail=f"Input file size exceeds the maximum allowed limit of {settings.max_upload_size_mb} bytes."
        )

    full_path = f"{create_temp_folder(settings.upload_dir)}/{input_path.filename}"

    save_uploaded_file(input_path.file.read(), full_path)

    new_cmd = replace_input_tag(cmd, full_path)
    new_cmd = replace_output_tag(new_cmd)
    return new_cmd


def replace_input_tag(cmd: str, full_path: str) -> str:
    """Replaces the input tag in the command with the actual local input file path."""
    # get the part after -i
    # replace only the input file name part
    new_cmd = cmd.replace(settings.input_tag_placeholder, f"'{full_path}'", 1)
    return new_cmd


def get_output_path_from_cmd(cmd: str, replace_parent_dir: bool = False) -> str:
    """Extract the output file path safely from an ffmpeg command string."""
    tokens = shlex.split(cmd)
    if not tokens:
        return ""

    output_path = tokens[-1]  # last token is usually output
    if replace_parent_dir:
        # remove first directory level
        parts = output_path.split("/", 1)
        if len(parts) == 2:
            output_path = parts[1]
    return output_path


def replace_output_tag(cmd: str) -> str:
    "Replace the output tag in the command with the actual local output file path."

    # get the part after the last space
    output_file_name_part = get_output_path_from_cmd(cmd)
    # have only the part after last /
    output_file_name_part = output_file_name_part.split("/")[-1]

    local_path = f"{create_temp_folder(settings.output_dir)}/{output_file_name_part}"
    new_cmd = cmd.replace(output_file_name_part, local_path, 1)
    return new_cmd
