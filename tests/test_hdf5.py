import time

import numpy as np
import os

from simrecorder import Recorder, HDF5DataStore


class Timer:
    def __init__(self):
        self._startime = None
        self._endtime = None
        self.difftime = None

    def __enter__(self):
        self._startime = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._endtime = time.time()
        self.difftime = self._endtime - self._startime


def main():
    n_arrays = 10

    arrays = np.random.rand(n_arrays, 10, 500, 20, 600)
    # arrays = (np.random.rand(n_arrays, 10, 500, 20, 600) > 0.5).astype(np.float)
    # arrays = np.random.rand(n_arrays, 10, 5, 2, 6)

    data_dir = os.path.expanduser('~/output/tmp/hdf5-test')
    os.makedirs(data_dir, exist_ok=True)
    file_pth = os.path.join(data_dir, 'data.h5')
    if os.path.exists(file_pth):
        os.remove(file_pth)
    key = 'train/what'

    ## WRITE
    hdf5_datastore = HDF5DataStore(file_pth)
    recorder = Recorder(hdf5_datastore)

    for i in range(n_arrays):
        array = arrays[i]
        with Timer() as st:
            recorder.record(key, array)
        print("Storing took %.2fs" % st.difftime)
    recorder.close()
    ## END WRITE

    print("File size after write is %d MiB" % (int(os.path.getsize(file_pth)) / 1024 / 1024))

    ## READ
    hdf5_datastore = HDF5DataStore(file_pth)
    recorder = Recorder(hdf5_datastore)

    with Timer() as rt:
        l = recorder.get_all(key)
    print("Reading took %.2fs" % rt.difftime)
    with Timer() as rrt:
        l = np.array(l)
    print("Into array took %.2f" % rrt.difftime)
    print("Mean is", np.mean(l), l.shape)

    recorder.close()
    ## END READ

    # os.remove(file_pth)


if __name__ == "__main__":
    from ipdb import launch_ipdb_on_exception

    with launch_ipdb_on_exception():
        main()