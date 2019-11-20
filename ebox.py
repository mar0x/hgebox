# ebox.py - qimport patches from eml files

import email
import re
import os
import subprocess
import tempfile
from mercurial import commands, hg, util, extensions
from mercurial.i18n import gettext, _

def importpatch(ui, repo, patchname, patch):
    """qimport the patch as patchname"""
    try:
        mq = extensions.find('mq')
    except KeyError:
        raise util.Abort(_("'mq' extension not loaded"))

    tmpfd, tmppath = tempfile.mkstemp(prefix='hg-ebox-')
    try:
        try:
            fp = os.fdopen(tmpfd, 'wb')
            fp.write(patch)
            fp.close()
            tmpfd = None
        except IOError:
            if tmpfd:
                os.close(tmpfd)
            raise

        mq.qimport(ui, repo, tmppath, name=patchname, existing=False,
                   force=False, rev=[], git=False)
    finally:
        os.remove(tmppath)

def makepatchname(existing, title):
    """Return a suitable filename for title, adding a suffix to make
    it unique in the existing list"""
    namebase = title.lower()
    namebase = re.sub('\s', '_', namebase)
    namebase = re.sub('\W', '_', namebase)
    namebase = re.sub('_+', '_', namebase)
    name = namebase.strip('_')
    for i in xrange(1, 100):
        if name not in existing:
            return name
        name = '%s__%d' % (namebase, i)
    raise util.Abort(_("can't make patch name for %s") % namebase)

def importpatches(ui, repo, patches):
    """qimport patches in groups in order"""
    imported = []
    # Patches are enumerated backward because qimport prepends them.
    # Groups are enumerated normally because they are already sorted
    # by descending dates, and we want old groups first.
    for p in reversed(patches):
        name = makepatchname(repo.mq.series, p['title'])
        importpatch(ui, repo, name, p['patch'])
        imported.append(name)
    ui.status(_('%d patches imported\n') % len(imported))

re_ispatch = re.compile(r'^(# HG|diff\s)', re.M)

cmdtable = {}

from mercurial import cmdutil
command = cmdutil.command(cmdtable)

@command('eimport',
    [],
    _('hg eimport [FILE ...]'))
def eimport(ui, repo, *patterns, **opts):
    """qimport patches from eml files
    """
    patches = []

    d = None
    if len(patterns) == 1 and patterns[0] == '-':
        d = tempfile.mkdtemp(prefix='hg-ebox-')
        dname = os.path.dirname(os.path.realpath(__file__))
        sc = os.path.join(dname, "ebox.scpt")
        subprocess.call(["osascript", sc, d[1:].replace('/', ':')])
        patterns = os.listdir(d)

    for p in patterns:

        if d:
            p = os.path.join(d, p)

        try:
            f = open(p)
            m = email.message_from_file(f)
            s = m['subject']
            if m.is_multipart():
                for a in m.get_payload():
                    a = a.get_payload(decode=True)
                    if re_ispatch.search(a):
                        break;
            else:
                a = m.get_payload(decode=True)

            if re_ispatch.search(a):
                patch = { 'title': s, 'patch': a }
                ui.status('%s\n' % s)
                patches.append(patch)
            else:
                ui.status('Not a patch: %s\n' % s)

            f.close()

        except IOError:
            if f:
                f.close()

        if d:
            os.remove(p)

    if d:
        os.rmdir(d)

    if len(patches) > 0:
        allowed = _('[Ny]')
        choices = [_('&No'), _('&Yes')]

        # Since hg 2.7
        r = ui.promptchoice(prompt=_('import this group? %s $$ %s'
            % (allowed, '$$'.join(choices))), default=0)

        if r == 1:
            importpatches(ui, repo, patches)

