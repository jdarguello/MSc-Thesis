import os
import re
import gzip
import shutil


def gunzip_something(gzipped_file_name, work_dir):
    "gunzip the given gzipped file"

    # see warning about filename
    filename = os.path.split(gzipped_file_name)[-1]
    filename = re.sub(r"\.gz$", "", filename, flags=re.IGNORECASE)

    with gzip.open(gzipped_file_name, 'rb') as f_in:  # <<========== extraction happens here
        with open(os.path.join(work_dir, filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def unzip(file="nParticle.gz"):
    try:
        shutil.register_unpack_format('gz',
                                      ['.gz', ],
                                      gunzip_something)
    except:
        pass

    shutil.unpack_archive(file,
                          os.curdir,
                          'gz')

class particulas():
    def __init__(self, t = (0.5,30)):
        #Leer información
        self.read(t)
        
    
    def read(self, t, root="CFD_DEM/"):
        subpath = "/lagrangian/kinematicCloud/"
        file = "nParticle.gz"
        suma = t[0]
        for tt in range(round(t[1]/t[0])):
            path = root + str(suma) + subpath
            unzip(path + file)
            suma += t[0]