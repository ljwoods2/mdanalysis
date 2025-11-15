from MDAnalysisTests.datafiles import COORDINATES_H5MD, COORDINATES_TOPOLOGY
import MDAnalysis as mda
import h5py

with h5py.File(COORDINATES_H5MD, "a") as f:
    with h5py.File("testh5md.h5md", 'w') as new_file:  # Open or create the new file in write mode
        # Copy each item from the original file to the new file
        for item in f.keys():
            f.copy(item, new_file)

        del new_file["particles/trajectory/velocity/step"]
        del new_file["particles/trajectory/velocity/time"]
        # step was previously [0, 1, 2, 3 ,4]
        new_file.create_dataset("particles/trajectory/velocity/step", data=[99, 105, 110, 111, 236], dtype=int)
        # time was previously [0, 1, 2, 3, 4]
        new_file.create_dataset("particles/trajectory/velocity/time", data=[99, 105, 110, 111, 236], dtype=float)

        vel = new_file["particles/trajectory/velocity/value"][:]
        del new_file["particles/trajectory/velocity/value"]
        new_file.create_dataset("particles/trajectory/velocity/value", data=vel, dtype=float)
        new_file["particles/trajectory/velocity/value"].attrs["unit"] = "Angstrom ps-1"

u = mda.Universe(COORDINATES_TOPOLOGY, "testh5md.h5md")

for ts in u.trajectory:
    print(ts.frame)
    print(ts.time)
    print(ts.data['step'])
    print(ts.velocities)