"""Basically copied from Illuminator, but tweaks applied."""
import sys
import os
import inspect

# game/Submods/MAICA_ChatSubmod/fecore.exe

def locater():
    """
    Gets the project/container path.
    """
    try:
        is_frozen = sys.frozen
    except Exception:
        try:
            is_frozen = locater.__compiled__
        except Exception:
            is_frozen = None
    
    if is_frozen:
        absolute_path = os.path.abspath(sys.executable)
    else:
        absolute_path = os.path.abspath(inspect.getfile(locater))

    dirname = os.path.dirname(absolute_path)
    if not is_frozen:
        for i in range(2):
            dirname = os.path.dirname(dirname)
    
    return is_frozen, dirname

def get_inner_path(filename):
    frozen, base_path = locater()
    if frozen:
        filepath = os.path.join(base_path, filename)
    else:
        filepath = os.path.join(base_path, 'fecore', filename)
    return filepath

def get_outer_path(filename):
    frozen, base_path = locater()
    return os.path.join(base_path, filename)

frozen, MAS_DIR = locater()
if frozen:
    try:
        _mas_dir = MAS_DIR
        for _ in range(3):
            _mas_dir = os.path.join(_mas_dir, '..')
        MAS_DIR = os.path.abspath(_mas_dir)
    except Exception:
        pass

if __name__ == "__main__":
    print(MAS_DIR)