#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for debian.py
"""

from unittest.mock import patch

import pytest

from easyops.linux.debian import Debian


@pytest.fixture
def test_values():
    """Fixture for test values"""
    return {
        "hostname": "test-debian",
        "domain": "test.local",
        "password": "testpass123",
    }


def test_gen_preseed_conf(test_values):
    """Test generation of preseed configuration"""
    with patch("easyops.linux.debian.Debian.gen_preseed2") as mock_gen_preseed2:
        mock_gen_preseed2.return_value = "/tmp/preseed.cfg"

        # Test with default version
        result = Debian.gen_preseed_conf(test_values)
        mock_gen_preseed2.assert_called_with("debian", test_values, None)
        assert result == "/tmp/preseed.cfg"

        # Test with specific version
        result = Debian.gen_preseed_conf(test_values, ver_code="bookworm")
        mock_gen_preseed2.assert_called_with("debian", test_values, "bookworm")
        assert result == "/tmp/preseed.cfg"


def test_gen_apt_src_default_params():
    """Test generation of apt sources with default parameters"""
    with patch("easyops.linux.debian.Debian.gen_src_list") as mock_gen_src_list:
        mock_gen_src_list.return_value = (
            "deb http://deb.debian.org/debian bookworm main contrib non-free"
        )

        result = Debian.gen_apt_src()

        expected_values = {
            "mirror": "deb.debian.org",
            "dir_main": "debian",
            "dir_sec": "debian-security",
            "version": "bookworm",
            "repotype": "main contrib non-free",
        }

        mock_gen_src_list.assert_called_with(expected_values, False, True, False, None)
        assert isinstance(result, str)


def test_gen_apt_src_custom_params():
    """Test generation of apt sources with custom parameters"""
    with patch("easyops.linux.debian.Debian.gen_src_list") as mock_gen_src_list:
        mock_gen_src_list.return_value = (
            "deb http://ftp.cn.debian.org/debian bullseye main"
        )

        result = Debian.gen_apt_src(
            mirror="cn",
            version=11,
            contrib=False,
            non_free=False,
            backports=True,
            src=False,
            write=True,
            dst_path="/etc/apt/sources.list",
        )

        expected_values = {
            "mirror": "ftp.cn.debian.org",
            "dir_main": "debian",
            "dir_sec": "debian-security",
            "version": "bullseye",
            "repotype": "main",
        }

        mock_gen_src_list.assert_called_with(
            expected_values, True, False, True, "/etc/apt/sources.list"
        )
        assert isinstance(result, str)
