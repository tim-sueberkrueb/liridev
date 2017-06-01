# -*- coding: utf-8 -*-

import typing

from .ubuntu import Ubuntu


_platform_map = {
    'Ubuntu': Ubuntu
}

supported_processors = ('x86_64',)
supported_distro_names = _platform_map.keys()
supported_distro_versions = {
    p: _platform_map[p].supported_platform_versions for p in _platform_map.keys()
}


def by_platform_name(platform_name: str):
    return _platform_map[platform_name]


def click_options(platform_name: str, platform_version: str):
    if platform_name in _platform_map:
        config = _platform_map[platform_name]
        config.platform_version = platform_version

        def decorator(f: typing.Callable):
            for option in config.options:
                f = option(f)
            return f

        return decorator
    return lambda f: f
