#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from os.path import dirname
from os.path import join as path_join
from os.path import sep as path_sep

from .config import Config, Host

__version__ = "1.2.1"

CONF_PATH = path_join("..", "configs")
CONF_APT_PATH = path_join(CONF_PATH, "apt")
CONF_PRESEED_PATH = path_join(CONF_PATH, "boot")

BUILD_PATH = path_join(".", "build")
BUILD_TMP_PATH = path_join(BUILD_PATH, "temp")

DOCKER_PATH = path_join(".", "build", "docker")
CFG_WEB_PATH = path_join(DOCKER_PATH, "cfg-web")

SH_PATH = ".." + path_sep + "scripts"

PKG_PATH = dirname(__file__)
TEMPLATES_PATH = path_join(PKG_PATH, "templates")
TEMPLATES_PRESEED_PATH = path_join(CONF_PATH, "boot")
SCRIPTS_PATH = path_join(PKG_PATH, "scripts")
