from .datastore import InMemoryDataStore
from .hdf_datastore import HDF5DataStore
from .recorder import Recorder
from .zarr_datastore import ZarrDataStore, DatastoreType, CompressionType
from .redis_datastore import RedisDataStore, RedisServer
from .serialization import Serialization

__all__ = ['Recorder', 'InMemoryDataStore', 'HDF5DataStore', 'ZarrDataStore', 'RedisDataStore', 'RedisServer', 'Serialization', 'DatastoreType', 'CompressionType']

def record_dict(recorder, prefix, d):
    for k, v in d.items():
        recorder.record(f'{prefix}/{k}', v)
