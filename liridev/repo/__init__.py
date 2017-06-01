# -*- coding: utf-8

import os

from ..utils import execution
from ..utils import console


repo_url = 'https://github.com/lirios/lirios.git'
repo_branch = 'develop'


def setup(repo_path: str=None, silent: bool=False):
    console.heading('Setting up repository at "{}" ...'.format(repo_path))
    os.makedirs(repo_path, exist_ok=True)
    execution.run('repo', 'init', '-q' if silent else '', '-u', repo_url, '-b', repo_branch, path=repo_path)
    console.success('Repository setup successfully.')


def update(repo_path: str=None, silent: bool=False):
    console.heading('Updating repository at "{}" ...'.format(repo_path))
    execution.run('repo', 'sync', path=repo_path, silent=silent)
    execution.run('repo', 'forall', '-c', "'git checkout $REPO_RREV'", path=repo_path, silent=silent)
    execution.run('repo', 'forall', '-c', "'git submodule update --init --recursive'", path=repo_path, silent=silent)
    execution.run(
        'ROOTDIR=$(pwd)', 'repo', 'forall', '-c', "'git config commit.template $ROOTDIR/.commit-template'",
        path=repo_path, silent=silent
    )
    console.success('Repository updated successfully.')
