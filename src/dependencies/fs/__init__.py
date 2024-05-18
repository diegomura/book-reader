import os
import sys

class Namespace():
    def __init__(self, namespace):
        root_path = os.path.dirname(sys.modules['__main__'].__file__)
        self.base_path = os.path.join(root_path, 'outputs', namespace)

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def get_path_for(self, file_name):
        return os.path.join(self.base_path, file_name)
    

class FS():
    def namespace(self, namespace):
        return Namespace(namespace)


fs = FS()