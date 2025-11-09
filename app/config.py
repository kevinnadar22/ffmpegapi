#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: config.py
Author: Maria Kevin
Created: 2025-11-09
Description: Settings for FFmpeg API application.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    upload_dir: str = "uploads"
    output_dir: str = "outputs"

    input_tag_placeholder: str = "<input>"

    allowed_commands: list[str] = ["ffmpeg", "ffprobe"]
    max_upload_size_mb: int = 100  * 1024 * 1024  # 100 MB


settings = Settings()
