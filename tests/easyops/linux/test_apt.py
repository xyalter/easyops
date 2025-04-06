#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-02 00:02
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

import json
from typing import List

import pytest

from easyops.linux.apt2 import SourceConfigSet


@pytest.fixture
def config_set():
    """Load and return test configurations from sources.json"""
    with open("./sources.json", "r", encoding="utf-8") as f:
        src_list = json.load(f)
    return SourceConfigSet(src_list)


def test_config_set_get_mirror():
    """Verify retrieval of default mirror configuration from sources.json"""
    config = config_set.get_mirror()
    assert config.name == "aly"


def test_config_set_get_by_name():
    """Test getting mirror configuration by specific mirror name (163)"""
    config = config_set.get_mirror(name="163")
    assert config.host == "mirrors.163.com"
    config = config_set.get_by_name(os="common", name="163")
    assert config.host == "mirrors.163.com"


def test_config_set_location_filter():
    """Validate filtering of mirrors by OS (debian) and location (Hong Kong)"""
    config = config_set.get_mirror(os="debian", location="hk")
    assert config.name == "auto"
    assert config.os == "debian"


def test_config_set_scheme_filter():
    """Test scheme filtering functionality with allowed schemes (http, https)"""
    def scheme_filter(schemes: List[str]):
        return "mirror" not in schemes

    config = config_set.get_mirror(os="ubuntu", scheme=scheme_filter)
    assert config.name == "aly"
    assert scheme_filter(config.scheme)
