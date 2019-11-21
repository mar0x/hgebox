Apple Mail Import Mercurial Extension
=====================================

This extension allows you to import patches straight from Apple Mail.

Get
---
```
git clone https://github.com/mar0x/hgebox.git
```

Enable
------
```
cat <<EOF >> .hg/hgrc
[extensions]
ebox = /path/to/hgebox/ebox.py
EOF
```

Try
---
In Apple Mail select email(s) with patches and
```
hg eimport -
```
