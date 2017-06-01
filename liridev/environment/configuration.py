# -*- coding: utf-8 -*-

import typing
import abc
import os
import click

from ..utils import console


class ValidationError(Exception):
    pass


class NotConfiguredError(Exception):
    pass


class Configuration(abc.ABC):
    platform_name = 'Unknown'
    supported_platform_versions = tuple()

    options = [
        click.option(
            '--path', '-p',
            type=click.Path(file_okay=False, writable=True), required=True,
            help='Path to install dependency sources (e.g. <project-path>/deps)'
        )
    ]

    def __init__(self):
        self.verbose = False
        self.platform_version = None
        self.build_dependencies = []
        self.path = None
        self.is_configured = False

    def assert_configured(self):
        if not self.is_configured:
            raise NotConfiguredError('Configuration not setup with required options')

    def configure(self, options: typing.Dict = None):
        options = options or {}
        self.path = options['path']
        self._configure(options)
        self.is_configured = True

    def create_paths(self):
        self.assert_configured()
        console.heading('Creating structure ...')
        os.makedirs(self.path, exist_ok=True)
        console.success('Finished creating structure.')

    def setup_build_dependencies(self):
        self.assert_configured()
        console.heading('Installing dependencies')
        for dep in self.build_dependencies:
            console.heading('Setting up dependency {} ...'.format(dep.name))
            source_path = os.path.join(self.path, dep.source.split('/')[-1])
            console.info('Fetching {} to {} ...'.format(dep.name, source_path))
            dep.fetch(source_path, verbose=self.verbose)
            console.info('Preparing to build {} ...'.format(dep.name))
            build_path = dep.prepare(source_path, verbose=self.verbose)
            console.info('Building {} in {} ...'.format(dep.name, build_path))
            dep.build(build_path, verbose=self.verbose)
            console.info('Installing {} ...'.format(dep.name))
            dep.install(build_path, verbose=self.verbose)
            console.success('Finished setting up {}.'.format(dep.name))

    @abc.abstractmethod
    def install_packages(self, *packages):
        pass

    @abc.abstractmethod
    def _configure(self, options: typing.Dict):
        pass
