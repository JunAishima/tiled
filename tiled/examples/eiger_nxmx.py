import dxtbx
#from tiled.adapters.dataframe import DataFrameAdapter
from tiled.adapters.mapping import MapAdapter
from tiled.adapters.dataframe import DataFrameAdapter
from tiled.adapters.hdf5 import HDF5Adapter, HDF5DatasetAdapter, MockHDF5Dataset
import pandas as pd
import dask.dataframe

#tree = MapAdapter({"example": EigerNxmxDataFrameAdapter.from_file("lys01_lsdc1_01_1044_master.h5")})

def read_eiger_nxmx(fileobj):
    if isinstance(fileobj, str):
        return _read_nxmx(fileobj)
    print("We must get a string-like object, not a file object!")

def _read_nxmx(filename):
    metadata = {}
    fi = dxtbx.load(filename)
    #print(fi.get_beam())
    # TODO check whether this is of the correct format
    metadata = extract_from_beam(fi.get_beam())
    metadata.update(extract_from_detector(fi.get_detector()))
    # TODO also detector.get_ray_intersection()
    metadata.update(extract_from_goniometer(fi.get_goniometer()))
    data = []
    #for i in range(fi.get_num_images()):
    for i in range(30):
        if not i%10:
            print(f"Processing image {i}")
        data.append(fi.get_raw_data(i).as_numpy_array())
    print("converting to data frame...")
    df = pd.array(data)
    print(f"data: {df} metadata: {metadata}")
    return df, metadata

class EigerNxmxDataFrameAdapter(HDF5Adapter):
    specs = ["nxmx"]
    metadata = {}

    structure_family = "node"

    @classmethod
    def from_file(cls, file):
        df, metadata = read_eiger_nxmx(file)
        return cls(dask.dataframe.from_array(df), metadata=metadata)

    def __init__(self, node, metadata, access_policy=None, principal=None):
        tree = MapAdapter({
            'data':DataFrameAdapter(node),
            'raw':HDF5Adapter.from_file(node)
        })
        super().__init__(tree, access_policy, principal)
        print(f'mynode: {mynode}')
        self.metadata=metadata

    def authenticated_as(self, principal):
        if self._principal is not None:
            raise RuntimeError(f"Already authenticated as {self.principal}")
        if self._access_policy is not None:
            raise NotImplementedError
        tree = type(self)(
            self._node, self.metadata,
            access_policy=self._access_policy,
            principal=principal,
        )
        return tree

    def __getitem__(self, key):
        print(f'getitem key: {key}')
        if self.metadata.get(key):
            value = self.metadata.get(key)
            print(value)
            return value #EigerNxmxDataFrameAdapter(value, self.metadata)
        else:
            value = self._node[key]
            print('else')
            if value.dtype == numpy.dtype("O"):
                warnings.warn(
                    f"The dataset {key} is of object type, using a "
                    "Python-only feature of h5py that is not supported by "
                    "HDF5 in general. Read more about that feature at "
                    "https://docs.h5py.org/en/stable/special.html. "
                    "Consider using a fixed-length field instead. "
                    "Tiled will serve an empty placeholder, unless the "
                    "object is of size 1, where it will attempt to repackage "
                    "the data into a numpy array."
                )

                check_str_dtype = h5py.check_string_dtype(value.dtype)
                if check_str_dtype.length is None:
                    dataset_names = value.file[self._node.name + "/" + key][...][()]
                    if value.size == 1:
                        arr = MockHDF5Dataset(numpy.array(dataset_names), {})
                        return HDF5DatasetAdapter(arr)
                return HDF5DatasetAdapter(MockHDF5Dataset(numpy.array([]), {}))
            return HDF5DatasetAdapter(value)


def extract_from_beam(beam_obj):
    metadata = {}
    metadata['wavelength'] = beam_obj.get_wavelength()
    metadata['transmission'] = beam_obj.get_transmission()
    return metadata

def extract_from_detector(det_obj):
    metadata = {}
    return metadata

def extract_from_goniometer(gon_obj):
    metadata = {}
    return metadata

def write_eiger_nxmx(df, metadata):
    # TODO is this possible with dxtbx? or just do it froms scratch?
    # TODO first check metadata to ensure it complies with what is required for the NXMX format
    pass
