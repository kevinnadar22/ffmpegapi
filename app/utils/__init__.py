#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: Maria Kevin
Created: 2025-11-09
Description: Utility functions for FFmpeg API.
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


# Import all functions from submodules
from app.utils.validation import (
    check_if_ffmpeg_installed,
    validate_ffmpeg_command,
    contains_prohibited_operations,
    check_if_input_tag_exists,
    input_file_size_within_limit,
    allow_command,
)

from app.utils.file_operations import (
    save_uploaded_file,
)

from app.utils.command_processing import (
    preprocess_cmd,
    replace_input_tag,
    get_output_path_from_cmd,
    replace_output_tag,
)

from app.utils.system import (
    create_temp_folder,
    ensure_directories_exist,
)


# Define what should be available when using "from app.utils import *"
__all__ = [
    # Validation functions
    "check_if_ffmpeg_installed",
    "validate_ffmpeg_command",
    "contains_prohibited_operations",
    "check_if_input_tag_exists",
    "input_file_size_within_limit",
    "allow_command",
    # File operations
    "save_uploaded_file",
    # Command processing
    "preprocess_cmd",
    "replace_input_tag",
    "get_output_path_from_cmd",
    "replace_output_tag",
    # System operations
    "create_temp_folder",
    "ensure_directories_exist",
]
