# -*- coding: utf-8 -*-

import enum
import multiprocessing
import os
import typing


from ..utils import execution


class BuildType(enum.Enum):
    CMake = 0


class SourceType(enum.Enum):
    Git = 0


class BuildDependency:
    def __init__(self, source: str, source_type: SourceType = SourceType.Git,
                 source_tag: str = None, source_branch: str = None, use_latest_source_tag: bool = True,
                 build_type: BuildType = BuildType.CMake, build_options: typing.Dict = None):
        self.name = None
        self.source = source
        self.source_type = source_type
        self.source_tag = source_tag
        self.source_branch = source_branch or 'master'
        self.build_type = build_type
        self.build_options = build_options or {}
        self.use_latest_source_tag = use_latest_source_tag
        if self.source_type == SourceType.Git:
            self.name = self.source.split('/')[-1]

    def fetch(self, source_path: str, verbose: bool = False) -> str:
        if self.source_type == SourceType.Git:
            if not os.path.isdir(source_path):
                execution.run('git', 'clone', self.source, source_path, silent=not verbose)
            else:
                execution.run('git', 'checkout', self.source_branch, path=source_path, silent=not verbose)
                execution.run('git', 'pull', 'origin', self.source_branch, path=source_path, silent=not verbose)
            tag = None
            if self.source_tag:
                tag = self.source_tag
            elif self.use_latest_source_tag:
                tag = execution.run(
                    'git', 'describe', '--tags', '$(git rev-list --tags --max-count=1)', path=source_path,
                    silent=True
                )
            if tag:
                execution.run('git', 'checkout', 'tags/' + tag, path=source_path, silent=not verbose)
        else:
            raise NotImplementedError('Unknown source type {}'.format(self.source_type))
        return source_path

    def prepare(self, source_path: str, verbose: bool = False) -> str:
        build_path = os.path.join(source_path, 'build')
        if not os.path.isdir(build_path):
            os.mkdir(build_path)
        if self.build_type == BuildType.CMake:
            cmake_arguments = ['-D{}={}'.format(o, self.build_options[o]) for o in self.build_options.keys()]
            execution.run('cmake', *cmake_arguments, '..', path=build_path, silent=not verbose)
        else:
            raise NotImplementedError('Unknown build type {}'.format(self.build_type))
        return build_path

    def build(self, build_path: str, verbose: bool = False) -> str:
        if self.build_type == BuildType.CMake:
            execution.run(
                'make', '-j{}'.format(multiprocessing.cpu_count()),
                path=build_path, silent=not verbose
            )
        else:
            raise NotImplementedError('Unknown build type {}'.format(self.build_type))
        return build_path

    def install(self, build_path: str, verbose: bool = False) -> str:
        if self.build_type == BuildType.CMake:
            # Cannot be completely silenced in case a password
            # prompt comes up.
            execution.run(
                'sudo', 'make', 'install', '>/dev/null' if not verbose else '', path=build_path, silent=False
            )
        else:
            raise NotImplementedError('Unknown build type {}'.format(self.build_type))
        return build_path
