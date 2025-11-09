#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: test_root.py
Author: Maria Kevin
Created: 2025-11-09
Description: Test Modules for /
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "use /run to execute the main functionality"}
