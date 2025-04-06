#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

import pytest
from easyops import Config
from easyops.config.manager import _config_merge


@pytest.fixture
def test_config_path():
    """Fixture providing the path to the test configuration file."""
    return "tests/resources/test-config.yml"


def test_config_merge():
    """
    Test config merge

    Verify that the config merge function works properly for both
    top-level and nested dictionaries, and for both strings and lists
    """
    a = dict(
        x1="abc",
        x2="abc",
        x3=list(["123", "456"]),
        x4=list(["123", "456"]),
        x5=dict(a="test1"),
        x6=dict(a="test1"),
        x7=dict(a=dict(n="abc")),
        x8=dict(a=dict(n="abc")),
    )
    b = dict(
        x2="def",
        x4=list(["789"]),
        x6=dict(b="test2"),
        x8=dict(a=dict(m="def")),
    )
    mix = _config_merge(a, b)
    assert mix["x1"] == "abc"
    assert mix["x2"] == "def"
    assert len(mix["x3"]) == 2
    assert len(mix["x4"]) == 3
    assert "b" not in mix["x5"]
    assert "b" in mix["x6"]
    assert mix["x6"]["b"] == "test2"
    assert "m" not in mix["x7"]["a"]
    assert "m" in mix["x8"]["a"]
    assert mix["x8"]["a"]["m"] == "def"


def test_config_mgr():
    """
    Test the config manager

    Verify that the config manager parses the configuration file
    correctly and that the data is accessible via the config object
    """
    config = Config(path=test_config_path)

    assert "debian" in config.hosts
    debian = config.hosts["debian"]
    assert "ubuntu" in config.hosts
    ubuntu = config.hosts["ubuntu"]

    assert debian.os == "debian"
    assert ubuntu.os == "ubuntu"

    assert debian.mirror == "auto"
    assert ubuntu.mirror == "auto"

    assert debian.host == "debian-std"
    assert ubuntu.host == "ubuntu-std"

    print(debian.packages)
    print(ubuntu.packages)

    assert "test1" in config.hosts
    test1 = config.hosts["test1"]
    assert "test2" in config.hosts
    test2 = config.hosts["test2"]

    assert test1.username == "test1"
    assert test2.username == "test"
    assert test1.users[test1.username]["key"] == "test1_rsa_2048"
    assert test2.users[test2.username]["key"] == "test_rsa_2048"

    assert "post_scripts" not in test1.data
    assert "post_scripts" in test2.data
