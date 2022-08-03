"""
Use this examples like:

tiled serve pyobject --public tiled.examples.eiger:tree

To serve a different URL from the example hard-coded here, use the config:

```
# config.yml
authentication:
    allow_anonymous_access: true
trees:
    - path: /
      tree: tiled.examples.nexus:MapAdapter
      args:
          url: YOUR_URL_HERE
```

tiled serve config config.yml
"""
import io

import h5py

from tiled.examples.eiger_nxmx import EigerNxmxDataFrameAdapter


def build_tree(filename):
    # Download a Nexus file into a memory buffer.
    return EigerNxmxDataFrameAdapter.from_file(filename)


EXAMPLE_FILENAME = "examples/lys01_lsdc1_01_1044_master.h5"  # noqa
tree = build_tree(EXAMPLE_FILENAME)
