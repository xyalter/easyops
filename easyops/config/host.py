#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-01-31 18:36
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""
from enum import Enum
from typing import List

from easyops.filter import flatten


class BootType(Enum):
    """Boot type of the host system.

    Attributes:
        BIOS: BIOS style boot
        EFI: EFI style boot
    """

    BIOS = "bios"
    EFI = "efi"


class Host:
    """A class representing a host system configuration.

    This class encapsulates all configuration settings for a host including network settings,
    system properties, user accounts, installed packages, and post-installation scripts.
    It provides property-based access to all configuration values with appropriate type hints.

    Attributes:
        data (dict): Raw configuration data
        host (str): Hostname
        domain (str): Domain name
        fqdn (str): Fully Qualified Domain Name
        network (dict): Network configuration including ipv4, gateway, and dns
        port (int): Port number
        os (str): Operating system identifier
        mirror (str): Mirror configuration
        proxy (str): Proxy settings
        username (str): Username
        fullname (str): Full name
        users (dict): User accounts configuration
        features (List[str]): Enabled features
        packages (List[str]): Installed packages
        files (list): File configurations
        post_scripts (List[str]): Post-installation scripts
    """

    def __init__(self, config: dict):
        """Initialize a new Host instance.

        Args:
            config (dict): Configuration dictionary containing host settings including
                          host, domain, port, os, mirror, proxy, username, fullname,
                          features, files, users, network, packages, and postScripts.
        """
        self._data = {}
        fields = [
            "boot_type",
            "host",
            "domain",
            "port",
            "os",
            "mirror",
            "proxy",
            "username",
            "fullname",
            "features",
            "files",
        ]
        for field in fields:
            if field in config:
                self._data[field] = config[field]
            else:
                self._data[field] = None
        if self._data["boot_type"] is None:
            self._data["boot_type"] = BootType.BIOS.value
        elif isinstance(self._data["boot_type"], str):
            try:
                self._data["boot_type"] = BootType(self._data["boot_type"]).value
            except ValueError:
                self._data["boot_type"] = BootType.BIOS.value
        if "users" in config:
            self._data["users"] = {}
            users = config["users"]
            for item in users:
                user = users[item]
                self._data["users"][item] = dict(
                    key=user["key"], password=user["password"]
                )
        if "network" in config:
            network = config["network"]
            self._data["network"] = dict(
                ipv4=network["ipv4"], gateway=network["gateway"], dns=network["dns"]
            )
        if "packages" in config:
            self._data["packages"] = flatten(config["packages"])
        if "postScripts" in config:
            self._data["post_scripts"] = config["postScripts"]

    @property
    def data(self):
        """Get the raw configuration data.

        Returns:
            dict: The complete configuration data dictionary.
        """
        return self._data

    @property
    def boot_type(self) -> BootType:
        """Get the boot type.

        Returns:
            BootType: The boot type of this host, either BIOS or EFI.
        """
        return BootType(self._data["boot_type"])

    @property
    def host(self):
        """Get the hostname.

        Returns:
            str: The hostname of this host.
        """
        return self._data["host"]

    @property
    def domain(self):
        """Get the domain name.

        Returns:
            str: The domain name of this host.
        """
        return self._data["domain"]

    @property
    def fqdn(self):
        """Get the Fully Qualified Domain Name (FQDN) of the host.

        Returns:
            str: The FQDN created by joining the host and domain with a dot.
        """
        return ".".join([self.host, self.domain])

    @property
    def network(self):
        """Get the network configuration.

        Returns:
            dict: Network configuration containing ipv4, gateway, and dns settings.
        """
        return self._data["network"]

    @property
    def port(self):
        """Get the port number.

        Returns:
            int: The port number for this host, or None if not set.
        """
        return self._data["port"]

    @property
    def os(self) -> str:
        """Get the operating system.

        Returns:
            str: The operating system identifier.
        """
        return self._data["os"]

    @property
    def mirror(self):
        """Get the mirror configuration.

        Returns:
            str: The mirror URL or configuration, or None if not set.
        """
        return self._data["mirror"]

    @property
    def proxy(self):
        """Get the proxy configuration.

        Returns:
            str: The proxy URL or configuration, or None if not set.
        """
        return self._data["proxy"]

    @property
    def username(self) -> str:
        """Get the username.

        Returns:
            str: The username for this host.
        """
        return self._data["username"]

    @property
    def fullname(self) -> str:
        """Get the full name.

        Returns:
            str: The full name associated with this host.
        """
        return self._data["fullname"]

    @property
    def users(self):
        """Get the users configuration.

        Returns:
            dict: Dictionary of users with their keys and passwords.
        """
        return self._data["users"]

    @property
    def features(self) -> List[str]:
        """Get the list of features.

        Returns:
            List[str]: List of enabled features for this host.
        """
        return self._data["features"]

    @property
    def packages(self) -> List[str]:
        """Get the list of packages.

        Returns:
            List[str]: List of packages to be installed on this host.
        """
        return self._data["packages"]

    @property
    def files(self):
        """Get the files configuration.

        Returns:
            list: List of file configurations for this host, or None if not set.
        """
        return self._data["files"]

    @property
    def post_scripts(self) -> List[str]:
        """Get the list of post scripts.

        Returns:
            List[str]: List of post scripts to be executed on this host.
        """
        return self._data["post_scripts"]
