"""Command line interface for task_tree project."""
import sys
import argparse
from core import Task
from store import JsonStore, store

shift_step = 4

def tree_printer(root, shift):
    if shift != 0:
        print(f"└{shift*'-'}", end='')
    print(root.title)

    for child in root.childs:
        print(' ' * (shift + 1), end='')
        print(f"└{shift*'-'}{child.title}")
        if child.childs:
            tree_printer(child, shift + shift_step)

def find_task(root, title):
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
            with store:
                root = store.get_tree(id=0)
                tree_printer(root, 0)

        elif arg == 'del':
            try:
                title = args[pos + 1]
            except Exception:
                return "No title for taske deletion provided. Abort deletion!"

            with store:
                root = store.get_tree(id =0)
                task  = find_task(root, title)





if __name__ == "__main__":
    print("Can't execute package directly")
else:
    arg_parser()
