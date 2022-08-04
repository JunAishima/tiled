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

from tiled.adapters.hdf5 import HDF5DatasetAdapter
from tiled.adapters.mapping import MapAdapter
from tiled.examples.eiger_nxmx_h5py import read_eiger_nxmx


def build_tree(filename):
    data = read_eiger_nxmx(filename)
    return MapAdapter({'data': HDF5DatasetAdapter(data['data']),
                   'cc000':HDF5DatasetAdapter(data['cc000']),
                   })


EXAMPLE_FILENAME = "examples/lys01_lsdc1_01_1044_master.h5"  # noqa
tree = build_tree(EXAMPLE_FILENAME)
