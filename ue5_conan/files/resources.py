import os.path


def get_resource_file(filename: str):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename))

def read_resource_file(filename: str):
    with open(get_resource_file(filename), "r", encoding='utf-8') as f:
        return f.read()