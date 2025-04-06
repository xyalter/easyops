#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time    : 2020-02-01 23:59
@Author  : xxy1991
@Email   : xxy@lesscode.dev
"""

from typing import List, Set, Callable


class SourceConfigItem:
    """
    A class representing a source configuration item for a mirror.

    This class encapsulates the details of a mirror configuration, including its
    name, host, location, and applicable operating system. It provides property-based
    access to all configuration values with appropriate type hints.

    Attributes:
        os (str): The operating system identifier this mirror is applicable to.
        item (dict): Raw configuration data for the mirror.
    """

    def __init__(self, os: str, item):
        self.__os = os
        self.__item = item

    @property
    def name(self) -> str:
        """
        The name of the mirror.

        Returns:
            str: The name of the mirror.
        """
        return self.__item["name"]

    @property
    def scheme(self) -> List[str]:
        """
        The scheme(s) used by the mirror, defaulting to 'http' if not specified.

        Returns:
            List[str]: A list of schemes such as 'http' or 'https'.
        """
        if "scheme" in self.__item:
            return self.__item["scheme"]
        return ["http"]

    @property
    def host(self) -> str:
        """
        The hostname of the mirror.

        Returns:
            str: The hostname of the mirror.
        """
        return self.__item["host"]

    @property
    def location(self) -> str or None:
        """
        The location of the mirror, None if not specified.

        Returns:
            str or None: The location of the mirror.
        """
        if "location" in self.__item:
            return self.__item["location"]
        return None

    @property
    def is_location_default(self) -> bool:
        """
        Whether the mirror is the default mirror for its location.

        Returns:
            bool: True if the mirror is the default mirror for its location, False
                otherwise.
        """
        if "location-default" in self.__item:
            return self.__item["location-default"]
        return False

    @property
    def os(self) -> str:
        """
        The operating system identifier this mirror is applicable to.

        Returns:
            str: The operating system identifier.
        """
        return self.__os

    @property
    def is_default(self) -> bool:
        """
        Whether the mirror is the default mirror for its OS.

        Returns:
            bool: True if the mirror is the default mirror for its OS, False
                otherwise.
        """
        if "default" in self.__item:
            return self.__item["default"]
        return False

    def __repr__(self) -> str:
        return repr(
            dict(
                name=self.name,
                scheme=self.scheme,
                host=self.host,
                location=self.location,
                location_default=self.is_location_default,
                os=self.os,
                default=self.is_default,
            )
        )


class SourceConfigSet:
    """Represents a collection of mirror configuration items.

    This class manages a set of mirror configurations, allowing for efficient
    querying and management of repository mirrors.
    
    Parameters
    ----------
    data : iterable
        Initial data to populate the configuration set.
    """
    def __init__(self, data):
        self.__set = set()
        for os in data:
            for item in data[os]:
                config = SourceConfigItem(os, item)
                self.__set.add(config)

    def get_by_name(self, os: str, name: str) -> SourceConfigItem or None:
        """
        Get a SourceConfigItem by its name, first searching within the given
        operating system, then in the global set of configurations.

        Args:
            os (str): The operating system identifier.
            name (str): The name of the mirror to search for.

        Returns:
            SourceConfigItem or None: The SourceConfigItem object with the
                matching name, or None if not found.
        """
        result = set(filter(lambda item: item.name == name, self.get_by_os(os)))
        if len(result) > 0:
            return result.pop()
        result = set(filter(lambda item: item.name == name, self.__set))
        if len(result) > 0:
            return result.pop()
        return None

    @staticmethod
    def filter(
        filter_func: Callable[[SourceConfigItem], bool], configs: set
    ) -> Set[SourceConfigItem]:
        """
        Filter a set of SourceConfigItem objects by a given filter function.

        Args:
            filter_func (Callable[[SourceConfigItem], bool]): A filter function
                that takes a SourceConfigItem object as input and returns a
                boolean indicating whether the object should be included or
                excluded.
            configs (set): The set of SourceConfigItem objects to filter.

        Returns:
            Set[SourceConfigItem]: A set of SourceConfigItem objects that
                satisfy the given filter function.
        """
        return set(filter(filter_func, configs))

    @staticmethod
    def filter_by_scheme(
        scheme: Callable[[List[str]], bool] or None, configs: set
    ) -> Set[SourceConfigItem]:
        """
        Filter a set of SourceConfigItem objects by a given scheme filter.

        Args:
            scheme (Callable[[List[str]], bool] or None): A filter function
                that takes a list of strings (i.e., schemes) as input and
                returns a boolean indicating whether the schemes should be
                included or excluded. If None, the original set of
                SourceConfigItem objects is returned.
            configs (set): The set of SourceConfigItem objects to filter.

        Returns:
            Set[SourceConfigItem]: A set of SourceConfigItem objects that
                satisfy the given scheme filter.
        """
        if scheme is None:
            return configs
        return set(filter(lambda item: scheme(item.scheme), configs))

    def get_by_os(self, os: str) -> Set[SourceConfigItem]:
        """
        Get all mirrors for the given operating system.

        Args:
            os (str): The operating system identifier.

        Returns:
            Set[SourceConfigItem]: A set of SourceConfigItem objects representing
                all mirrors for the given operating system.
        """
        return self.filter(lambda item: item.os == os, self.__set)

    def get_by_location(self, location: str) -> Set[SourceConfigItem]:
        """
        Get all mirrors for the given location.

        Args:
            location (str): The location identifier.

        Returns:
            Set[SourceConfigItem]: A set of SourceConfigItem objects representing
                all mirrors for the given location.
        """
        return self.filter(lambda item: item.location == location, self.__set)

    def get_by_default(
        self, os, location=None, scheme=None
    ) -> SourceConfigItem or None:
        """
        Get a default mirror for the given operating system and location.

        Args:
            os (str): The operating system identifier.
            location (str or None): The location identifier. If None, the
                location is not considered when selecting the default mirror.
            scheme (Callable[[List[str]], bool] or None): A filter function
                that takes a list of strings (i.e., schemes) as input and
                returns a boolean indicating whether the schemes should be
                included or excluded. If None, the original set of
                SourceConfigItem objects is returned.

        Returns:
            SourceConfigItem or None: A default mirror for the given
                operating system and location, or None if no default mirror is
                found.
        """
        result = self.get_by_os(os)

        if location is not None:
            result = set(result).intersection(self.get_by_location(location))
            result = set(filter(lambda item: item.is_location_default, result))
        if scheme is not None:
            result = set(filter(lambda item: scheme(item.scheme), result))
        return result

    def get_mirror(
        self, os="common", name=None, location=None, scheme=None
    ) -> SourceConfigItem or None:
        """Retrieve a mirror configuration based on specified criteria.

        Args:
            os (str, optional): Target operating system. Defaults to "common".
            name (str, optional): Mirror name to filter by.
            location (str, optional): Geographical location constraint.
            scheme (str, optional): URI scheme (http/https) requirement.

        Returns:
            SourceConfigItem or None: Matching configuration item or None if not found.
        """
        # priority level
        # name-os > name >
        # os-location-default > os-default >
        # common-location-default > common-default
        if name is not None:
            config = self.get_by_name(os, name)
            if scheme is not None and scheme(config.scheme):
                return config

        os_set = self.get_by_os(os)
        loc_set = self.get_by_location(location)
        result = self.filter_by_scheme(scheme, os_set.intersection(loc_set))
        if len(result) > 0:
            configs = set(self.filter(lambda item: item.is_location_default, result))
            if len(configs) > 0:
                return result.pop()
            return result.pop()

        result = self.filter_by_scheme(
            scheme, set(self.filter(lambda item: item.is_default, os_set))
        )
        if len(result) > 0:
            return result.pop()

        if os != "common":
            return self.get_mirror(location=location, scheme=scheme)

        return None
