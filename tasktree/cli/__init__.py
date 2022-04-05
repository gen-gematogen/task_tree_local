"""Command line interface for task_tree project."""
import sys
import argparse
from anytree.importer import JsonImporter
from anytree import RenderTree

from core import Task
from store import JsonStore, store

shift_step = 4

def tree_printer(path):
    with open(path, 'r') as f:
        data = f.read()
        importer = JsonImporter()
        root = importer.import_(data)
        print(RenderTree(root))

def find_task(root, title):
    if not root:
        return None

    if root.title == title:
        return root

    for child in root.childs:
        res = find_task(child, title)

        if res:
            return res
 
    return None


def arg_parser():
    """Look through all given arguments, check it's correctness
    and if posslible execute given request"""

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    for pos, arg in enumerate(args):
        if arg == 'shell':
            # change execution mode to shell
            
            break
        elif arg == 'tree':
            # display existing tree in terminal
            tree_printer(store.store)

        elif arg == 'del':
            try:
                title = args[pos + 1]
            except Exception:
                print("No title for taske deletion provided. Abort deletion!")
                return

            with store:
                root = store.get_tree(id =0)
                task  = find_task(root, title)

                if not task:
                    print("Can't find task with provided title")
                    return

                






if __name__ == "__main__":
    print("Can't execute package directly")
else:
    arg_parser()
