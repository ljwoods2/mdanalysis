import MDAnalysis as mda
from MDAnalysisTests.datafiles import PSF, PDB_small
import s3fs


s3_fs = s3fs.S3FileSystem(
    # anon must be false to allow authentication
    anon=False,
    # use profiles defined in a .aws/credentials file to store secret keys
    # docs: 
    profile='sample_profile',
    client_kwargs=dict(
        region_name='us-west-1',
    )
)
store = s3fs.S3File(path=f'zarrtraj-test-data/pdb_small.pdb',
                   s3=s3_fs)
#
#u = mda.Universe(PSF, store, format="PDB")
#
#for ts in u.trajectory:
#    print(u.atoms)
store.close()