#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from functools import wraps
from os import makedirs
from os.path import dirname, exists, isfile


def singleton(cls):
    """
    A decorator to make a class a singleton.

    The decorated class will maintain a single instance of itself, and all
    subsequent calls to the constructor will return that instance.

    Parameters
    ----------
    cls : type
        The class to be decorated.

    Returns
    -------
    The decorated class, now a singleton.

    """
    _instances = {}

    @wraps(cls)
    def _singleton(*args, **kwargs):
        key = repr(cls) + repr(frozenset(kwargs.items()))
        if key not in _instances:
            _instances[key] = cls(*args, **kwargs)
        return _instances[key]

    return _singleton


def sudo(ctx, path, command):
    """
    Execute a command in a context with sudo privileges, after changing to a directory.

    Parameters
    ----------
    ctx : Context
        The context to use for the command execution.
    path : str
        The path to which the command's working directory should be changed.
    command : str
        The command to execute.
    """
    cmd = 'bash -c "cd ' + path + " && "
    cmd += command
    cmd += '"'
    ctx.sudo(cmd)


def mkdir(path, f=False):
    """
    Make a directory.

    Parameters
    ----------
    path : str
        The path of the directory.
    f : bool
        If the path is a file, set to True. Defaults to False.

    Returns
    -------
    None

    Notes
    -----
    If the path is a file and not a directory, set the path to the parent directory of the file.
    If the directory does not exist, create it.
    """
    if not f and exists(path) and isfile(path):
        f = True
    if f:
        path = dirname(path)
    if not exists(path):
        makedirs(path)


def read_text(path):
    """
    Read a text file.

    Parameters
    ----------
    path : str
        The path of the text file.

    Returns
    -------
    str
        The content of the text file.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return text


def write_text(text: str, path: str):
    """
    Write a text to a file.

    Parameters
    ----------
    text : str
        The text to be written.
    path : str
        The path of the file.

    Notes
    -----
    The parent directory of ``path`` will be created if it does not exist.
    """
    mkdir(path, True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
