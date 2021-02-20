import os
import re
import gzip
import shutil
import subprocess


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

def particulas():
    p = subprocess.run("paraFoam", cwd="CFD_DEM")

class Particulas():
    def __init__(self, t = (0.5,30)):
        #Ejecutar
        root =  os.getcwd() + '/'
        command = "gmshToFoam " + file
        os.chdir("CFD_DEM")
        os.system(command)
        os.chdir("..")