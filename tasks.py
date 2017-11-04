# -*- coding: utf-8 -*-
"""
Base version of package/tasks.py, created by

    package/root/dir> dk-tasklib install

(it should reside in the root directory of your package)

This file defines tasks for the Invoke tool: http://www.pyinvoke.org

Basic usage::

    inv -l               # list all available tasks
    inv build -f         # build everything, forcefully
    inv build --docs     # only build the docs

dk-tasklib is a library of basic tasks that tries to automate common tasks.
dk-tasklib will attempt to install any tools/libraries/etc. that are required,
e.g. when running the task to compile x.less to x.css, it will check that
the lessc compiler is installed (and if not it will attempt to install it).

This file is an initial skeleton, you are supposed to edit and add to it so it
will fit your use case.


"""
# pragma: nocover
from __future__ import print_function
import os
import warnings

from dkfileutils.changed import changed
from dkfileutils.path import Path
from dktasklib.wintask import task
from invoke import Collection

from dktasklib import docs as doctools
from dktasklib import jstools
from dktasklib import lessc
from dktasklib import version, upversion
from dktasklib.manage import collectstatic
from dktasklib.package import Package, package
from dktasklib.watch import Watcher
from dktasklib.publish import publish

#: where tasks.py is located (root of package)
DIRNAME = Path(os.path.dirname(__file__))

# collectstatic
# --------------
# Specify which settings file should be used when running
# `python manage.py collectstatic` (must be on the path or package root
# directory).
DJANGO_SETTINGS_MODULE = ''

# .less
# ------
# there should be a mypkg/mypkg/less/mypkg.less file that imports any other
# needed sources

# .jsx (es6 source)
# ------------------
# list any .jsx files here. Only filename.jsx (don't include the path).
# The files should reside in mypkg/mypkg/js/ directory.
JSX_FILENAMES = []

# ============================================================================
# autodoc is in a separate process, so can't use settings.configure().
HAVE_SETTINGS = bool(DJANGO_SETTINGS_MODULE)
if not HAVE_SETTINGS and (DIRNAME / 'settings.py').exists():
    # look for a dummy settings.py module in the root of the package.
    DJANGO_SETTINGS_MODULE = 'settings'
if DJANGO_SETTINGS_MODULE:
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
WARN_ABOUT_SETTINGS = not bool(DJANGO_SETTINGS_MODULE)


@task
def build_js(ctx, force=False):
    """Build all javascript files.
    """
    for fname in JSX_FILENAMES:
        jstools.babel(
            ctx,
            '{pkg.source_js}/' + fname,
            '{pkg.django_static}/{pkg.name}/js/' + fname + '.js',
            force=force
        )


@task
def build(ctx, less=False, docs=False, js=False, force=False):
    """Build everything and collectstatic.
    """
    specified = any([less, docs, js])
    buildall = not specified

    if buildall or less:
        less_fname = ctx.pkg.source_less / ctx.pkg.name + '.less'
        if less_fname.exists():
            lessc.LessRule(
                ctx,
                src='{pkg.source_less}/{pkg.name}.less',
                dst='{pkg.django_static}/{pkg.name}/css/{pkg.name}-{version}.min.css',
                force=force
            )
        elif less:
            print("WARNING: build --less specified, but no file at:", less_fname)

    if buildall or docs:
        if WARN_ABOUT_SETTINGS:
            warnings.warn(
                "autodoc might need a dummy settings file in the root of "
                "your package. Since it runs in a separate process you cannot"
                "use settings.configure()"
            )
        doctools.build(ctx, force=force)

    if buildall or js:
        build_js(ctx, force)

    if HAVE_SETTINGS and (force or changed(ctx.pkg.django_static)):
        collectstatic(ctx, DJANGO_SETTINGS_MODULE)


@task
def watch(ctx):
    """Automatically run build whenever a relevant file changes.
    """
    watcher = Watcher(ctx)
    watcher.watch_directory(
        path='{pkg.source_less}', ext='.less',
        action=lambda e: build(ctx, less=True)
    )
    watcher.watch_directory(
        path='{pkg.source_js}', ext='.jsx',
        action=lambda e: build(ctx, js=True)
    )
    watcher.watch_directory(
        path='{pkg.docs}', ext='.rst',
        action=lambda e: build(ctx, docs=True)
    )
    watcher.start()


# individual tasks that can be run from this project
ns = Collection(
    build,
    watch,
    build_js,
    lessc,
    doctools,
    version, upversion,
    package,
    collectstatic,
    publish,
)
ns.configure({
    'pkg': Package(),
    'run': {
        'echo': True
    }
})
