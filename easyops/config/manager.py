#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""
from copy import deepcopy
from typing import Dict

from invoke import Config as InvCfg, Context as InvCtx
from invoke.config import DataProxy

from .host import Host
from ..filter import flatten
from ..util import singleton


def _data_proxy_to_dict(origin: DataProxy) -> dict:
    result = {}
    for key in origin:
        if isinstance(origin[key], DataProxy):
            result[key] = _data_proxy_to_dict(origin[key])
        else:
            result[key] = origin[key]
    return result


def _config_merge(origin: dict, target: dict) -> dict:
    for key in target:
        if isinstance(target[key], str):
            item = target[key]
        else:
            item = deepcopy(target[key])
        if key not in origin:
            origin[key] = item
        else:
            if key == "users":
                print(type(item))
            if isinstance(item, str):
                origin[key] = item
            elif isinstance(item, list):
                if len(item) > 0 and isinstance(item[0], list):
                    that = flatten(item)
                else:
                    that = item
                merged = list(origin[key]) + that
                origin[key] = sorted(set(merged), key=merged.index)
            elif isinstance(item, dict):
                if key == "users":
                    print(item)
                origin[key] = _config_merge(deepcopy(origin[key]), deepcopy(item))
    return origin


@singleton
class Config:
    """
    Represents a collection of host configuration items.

    This class manages a set of host configurations, allowing for efficient
    querying and management of host configurations.

    Parameters
    ----------
    ctx : InvCtx
        The Invoke context.
    path : str
        The path to load the configuration from.

    Attributes
    ----------
    hosts : Dict[str, Host]
        A dictionary of host configurations mapped by host identifier.
    context : InvCtx
        The Invoke context.
    config : InvCfg
        The Invoke configuration.
    """

    def __init__(self, ctx=None, path=None):
        if ctx is None and path is None:
            pass
        if ctx is None:
            # cfg = InvCfg(project_location='../configs')
            # cfg.load_project()
            if path is not None:
                cfg = InvCfg(runtime_path=path)
                cfg.load_runtime()
                self.__context = InvCtx(cfg)
            else:
                self.__context = InvCtx()
        else:
            self.__context = ctx

        self.__hosts = {}
        if "Hosts" in self.config:
            hosts = self.config.Hosts
            default = _data_proxy_to_dict(hosts["default"])
            if "packages" in default:
                default["packages"] = flatten(default["packages"])

            for key in hosts:
                if key == "default":
                    continue
                host = Host(
                    _config_merge(deepcopy(default), _data_proxy_to_dict(hosts[key]))
                )
                self.__hosts[key] = host

    @property
    def hosts(self) -> Dict[str, Host]:
        """
        Get the dictionary of hosts mapped by host identifier.

        Returns:
            Dict[str, Host]: A dictionary of host configurations mapped by host
            identifier.
        """
        return self.__hosts

    @property
    def context(self) -> InvCtx:
        """
        Get the Invoke context.

        Returns:
            InvCtx: The Invoke context.
        """
        return self.__context

    @property
    def config(self) -> InvCfg:
        """
        Get the Invoke configuration.

        Returns:
            InvCfg: The Invoke configuration.
        """
        return self.context.config
