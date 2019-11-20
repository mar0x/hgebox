Apple Mail Import Mercurial Extension
=====================================

This extension allows you to import patches straight from Apple Mail.

Get
---
```
hg clone https://github.com/mar0x/hgebox.git
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
Select email(s) with patches and
```
hg eimport -
```
