#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: models.py
Author: Maria Kevin
Created: 2025-11-09
Description: Pydantic models for FFmpeg command input and output.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


from pydantic import BaseModel


class FFmpegCommand(BaseModel):
    cmd: str


class CommandResult(BaseModel):
    cmd: str
    stdout: str
    stderr: str
    returncode: int
    output_url: str
