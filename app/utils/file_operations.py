#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: file_operations.py
Author: Maria Kevin
Created: 2025-11-09
Description: File handling and upload operations for FFmpeg API.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

import os


def save_uploaded_file(file_bytes: bytes, destination_path: str) -> None:
    """Save uploaded file bytes to the specified destination path."""
    # Ensure the parent directory exists
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(destination_path, "wb") as f:
        f.write(file_bytes)
