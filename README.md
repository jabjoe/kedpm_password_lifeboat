This was just knocked together to get passwords out of kedpm and into keepass.

Kedpm is Python2 and GTK2 and is not going to be updated. It's no longer in Debian. Time to get the passwords out!
This requires kedpm to be installed (old-stable) as it uses some of it's Python libraries.

The exporter options in kedpm didn't seam to work, so I wrote one.

It dumps the passwords out, unencrypted, as a JSON file. Then you can just knock together an importer for your password manager of choice.

The one here is for keepass as that has multiple implementations and is probably "the winner" format in this space.
It needs pykeepass, which isn't packaged in Debian right now (pip3 install pykeepass).
It also requires an existing keepass file.


Very basic:


    ./kedpm_exporter.py
    ./keepass_import.py my_db.kdbx
