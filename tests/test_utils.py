#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: test_utils.py
Author: Maria Kevin
Created: 2025-11-09
Description: tests for utils functions
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


from app.utils.command_processing import preprocess_cmd
from fastapi import UploadFile
from unittest.mock import MagicMock, patch
import pytest


@patch(
    "app.utils.command_processing.create_temp_folder",
    return_value="/tmp",
)
def test_preprocess_cmd(mock_create_temp_folder):
    # Mock an UploadFile
    mock_file = MagicMock(
        spec=UploadFile,
        filename="all the stars.mp3",
        size=5 * 1024 * 1024,
        file=MagicMock(read=MagicMock(return_value=b"dummy data")),
    )

    cmd = "ffmpeg -i <input> -c:v libx264 output.mp4"
    processed_cmd = preprocess_cmd(input_file=mock_file, cmd=cmd)
    assert "/tmp/all the stars.mp3" in processed_cmd
    assert (
        "ffmpeg -i '/tmp/all the stars.mp3' -c:v libx264 '/tmp/output.mp4'"
        == processed_cmd
    )

    # test


@patch(
    "app.utils.command_processing.create_temp_folder",
    return_value="/tmp",
)
def test_replace_output_tag(mock_create_temp_folder):
    from app.utils.command_processing import replace_output_tag

    cmd = "ffmpeg -i input.mp3 -c:v libx264 'output video.mp4'"
    new_cmd = replace_output_tag(cmd)

    assert "ffmpeg -i input.mp3 -c:v libx264 '/tmp/output video.mp4'" == new_cmd

    cmd = "ffmpeg -i input.mp3 -c:v libx264 video.mp4"
    new_cmd = replace_output_tag(cmd)
    assert "ffmpeg -i input.mp3 -c:v libx264 '/tmp/video.mp4'" == new_cmd


def test_get_output_path_from_cmd():
    from app.utils.command_processing import get_output_path_from_cmd

    # test with quotes
    cmd = "ffmpeg -i input.mp3 -c:v libx264 'output video.mp4'"
    output_path = get_output_path_from_cmd(cmd)
    assert output_path == "output video.mp4"

    cmd = "ffmpeg -i input.mp3 -c:v libx264 video.mp4"
    output_path = get_output_path_from_cmd(cmd)
    assert output_path == "video.mp4"

    cmd = 'ffmpeg -i input.mp3 -c:v libx264 "output video.mp4"'
    output_path = get_output_path_from_cmd(cmd)
    assert output_path == "output video.mp4"


def test_replace_input_tag():
    from app.utils.command_processing import replace_input_tag

    cmd = "ffmpeg -i <input> -c:v libx264 output.mp4"
    full_path = "/tmp/all the stars.mp4"
    new_cmd = replace_input_tag(cmd, full_path)
    expected_cmd = f"ffmpeg -i '{full_path}' -c:v libx264 output.mp4"
    assert new_cmd == expected_cmd


@patch("subprocess.run")
def test_allow_command(mock_subprocess_run):
    from app.utils.validation import allow_command
    from app.exceptions import (
        FFmpegNotInstalledException,
        InvalidFFmpegCommandException,
        ProhibitedOperationException,
    )

    cmd = "ffmpeg -i <input> -c:v libx264 output.mp4"

    allow_command(cmd)  # Should not raise any exception

    mock_subprocess_run.side_effect = FileNotFoundError()
    with pytest.raises(FFmpegNotInstalledException):
        allow_command(cmd)

    mock_subprocess_run.side_effect = None
    invalid_cmd = "invalid_command -i <input> -c:v libx264 output   .mp4"
    with pytest.raises(InvalidFFmpegCommandException):
        allow_command(invalid_cmd)

    prohibited_cmd = "ffmpeg -i <input> -c:v libx264; rm -rf /"
    with pytest.raises(ProhibitedOperationException):
        allow_command(prohibited_cmd)

    cmd_missing_input = "ffmpeg -c:v libx264 output.mp4"
    from app.config import settings

    settings.input_tag_placeholder = "<input>"
    with pytest.raises(InvalidFFmpegCommandException):
        allow_command(cmd_missing_input)

    cmd_invalid_input_tag = "ffmpeg -i somefile.mp4 -c:v libx264 output.mp4"
    with pytest.raises(InvalidFFmpegCommandException):
        allow_command(cmd_invalid_input_tag)


def test_input_file_size_within_limit():
    from app.utils.validation import input_file_size_within_limit
    from app.config import settings

    assert input_file_size_within_limit(1 * 1024 * 1024)  # 1MB
    assert input_file_size_within_limit(settings.max_upload_size_mb)  # max limit
    assert not input_file_size_within_limit(0)  # zero size
    assert not input_file_size_within_limit(
        settings.max_upload_size_mb + 1
    )  # exceed limit
