import shutil
def disk_free(path='.'): return shutil.disk_usage(path).free
