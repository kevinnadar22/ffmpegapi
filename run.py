#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: run.py
Author: Maria Kevin
Created: 2025-11-09
Description: Main EntryPoint module for FFmpeg API application.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
