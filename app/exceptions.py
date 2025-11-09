#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: exceptions.py
Author: Maria Kevin
Created: 2025-11-09
Description: Exceptions 
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


from fastapi import HTTPException

class FFmpegNotInstalledException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="FFmpeg is not installed on the server.")

class InvalidFFmpegCommandException(HTTPException):
    def __init__(self, detail: str = "Invalid FFmpeg command."):
        super().__init__(status_code=400, detail=detail)

class ProhibitedOperationException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Command contains prohibited operations.")


class CommandExecutionException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=500, detail=f"Command execution failed: {message}")