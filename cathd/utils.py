import os

from time import strftime
class Help:

    @staticmethod
    def create_dir(paths: str, create: bool = True) -> str:
        try: 
            if create: os.makedirs(paths)
        except Exception as err: ...
        finally: return paths
        ...

    @staticmethod
    def convert_path(path: str) -> str:
        path = path.split('/')
        path[1] = 'data_clean'
        return '/'.join(path)
        ...

    @staticmethod
    def basedir(path: str) -> str:
        return os.path.dirname(path)
        ...
        
    @staticmethod
    def name_file(path: str) -> str:
        return os.path.basename(path).split("?")[0]
        ...
        
    @staticmethod
    def now():
        return strftime('%Y-%m-%d %H:%M:%S')
        ...