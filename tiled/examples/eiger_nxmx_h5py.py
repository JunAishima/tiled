import h5py
import hdf5plugin

def read_eiger_nxmx(fileobj):
    if isinstance(fileobj, str):
        return _read_nxmx(fileobj)
    print("We must get a string-like object, not a file object!")

def _read_nxmx(filename):
    with h5py.File(filename, 'r') as f:
        print(f)
        data = f['/entry/data/data_000001'][0:10]
        cc000 = f['/entry/instrument/detector/detectorSpecific/detectorModule_000/countrate_correction_table'][:]
        wavelength = f['/entry/instrument/beam/incident_wavelength'][()]
        return {'data':data, 'cc000':cc000, 'metadata':{'wavelength':wavelength}}
