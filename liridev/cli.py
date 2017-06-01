# -*- coding: utf-8

import typing
import platform
import click
import sys

from liridev.utils import linux_platform
from liridev.utils import console
from liridev.utils import execution
from liridev.environment import platform as env_platform
from liridev import repo as repotools

_distro_name, _distro_version, _ = linux_platform.linux_distribution()

report_bug_url = 'https://github.com/tim-sueberkrueb/liridev/issues/new'


def check_platform():
    proc = platform.processor()
    if proc not in 'x86_64':
        console.error('Your processor "{}" is not supported.'.format(proc))
        return False
    if _distro_name not in env_platform.supported_distro_names:
        console.error(
            'You are not running a Linux distribution or your Linux distribution "{}" is not supported.'.format(
                _distro_name
            )
        )
        return False
    if _distro_version not in env_platform.supported_distro_versions[_distro_name]:
        console.error('Your {} version "{}" is not supported.'.format(_distro_name, _distro_version))
        return False
    return True


def require_programs(*programs: tuple):
    not_found = []
    for p in programs:
        if not execution.find_program(p[0]):
            not_found.append(p)
    if len(not_found) > 0:
        console.error('Missing required programs:')
        for p in not_found:
            console.warning('- {} ({})'.format(p[0], p[1]))
        console.log('Make sure they are installed and can be found in $PATH.')
        abort()


def abort():
    console.error('Aborting.')
    sys.exit(1)


def error_information(e: Exception):
    console.log()
    console.error('An error ({}) has occurred.'.format(type(e).__name__))
    console.error('Please check your configuration.')
    console.log()
    console.log('If you think this is a bug in this program, please report it here:')
    console.log(report_bug_url)
    console.log('Please include relevant parts of the previous console output' +
                ' as well as the following information in your report.')
    console.log()
    console.info("System: {}".format(platform.platform()))
    console.info("Python: {}".format(sys.version))
    console.log()


def call_safe(f: typing.Callable):
    try:
        f()
    except Exception as e:
        error_information(e)
        raise e


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output.')
@click.pass_context
def cli(ctx: click.Context, verbose: bool):
    ctx.obj['verbose'] = verbose


@cli.group(help='Get, install and setup dependencies.')
def deps():
    pass


@deps.command('setup', help='Setup dependencies. This option may require build steps depending on your platform.')
@env_platform.click_options(_distro_name, _distro_version)
@click.pass_context
def deps_setup(ctx: click.Context, **options):
    verbose = ctx.obj['verbose']
    if not check_platform():
        abort()
    console.heading('Setting up environment ...')
    config = env_platform.by_platform_name(_distro_name)()
    config.verbose = verbose
    config.platform_version = _distro_version
    config.configure(options)
    call_safe(config.create_paths)
    call_safe(config.install_packages)
    call_safe(config.setup_build_dependencies)
    console.success('Done.')


@cli.group(help='Manage source code repository.')
def repo():
    require_programs(
        ('repo', 'Google repo tool'),
        ('git', 'Version control system')
    )


@repo.command('setup', help='Setup a clone of the source repository.')
@click.option('--path', '-p', type=click.Path(file_okay=False, writable=True),
              required=True, help='Path to repository clone (e.g. <project-path>/repo)')
@click.pass_context
def repo_setup(ctx: click.Context, path: str=None):
    call_safe(
        lambda: repotools.setup(path, silent=not ctx.obj['verbose'])
    )


@repo.command('update', help='Update a clone of the source repository.')
@click.option('--path', '-p', type=click.Path(file_okay=False, writable=True, exists=True),
              required=False, help='Path to repository clone (e.g <project-path>/repo)')
@click.pass_context
def repo_update(ctx: click.Context, path: str=None):
    call_safe(
        lambda: repotools.update(path, silent=not ctx.obj['verbose'])
    )
