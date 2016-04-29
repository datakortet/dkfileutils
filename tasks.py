from invoke import Collection
from dktasklib import version
from dktasklib import upversion
from dktasklib import publish
from dktasklib import docs as doctools
from dktasklib.package import Package
from invoke import ctask as task


@task
def build(ctx, less=False, docs=False, js=False, force=False):
    """Build everything and collectstatic.
    """
    specified = any([less, docs, js])
    buildall = not specified

    if buildall or less:
        pass

    if buildall or docs:
        doctools.build(ctx, force=force)

    if buildall or js:
        pass


ns = Collection(build, version, upversion, publish)
ns.configure({
    'pkg': Package()
})
