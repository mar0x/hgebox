Apple Mail Import Mercurial Extension
=====================================

This extension allows you to import patches strait from Apple Mail application.

Get
```
hg clone https://github.com/mar0x/hgebox.git
```

Enable
```
cat <<EOF >> .hg/hgrc
[extensions]
ebox = /path/to/hgebox/ebox.py
EOF
```

Try
```
hg eimport -
```
