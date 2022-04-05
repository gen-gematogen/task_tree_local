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

    for child in root.children:
        res = find_task(child, title)

        if res:
            return res
 
    return None


def arg_parser():
    """Look through all given arguments, check it's correctness
    and if posslible execute given request"""

    parser = argparse.ArgumentParser()
    parser.add_argument('prog')
    parser.add_argument('comand')
    parser.add_argument('title_')
    parser.add_argument(['--parent', '-p'], nargs='?')
    parser.add_argument(['--status', '-s'], nargs='?')
    parser.add_argument(['--title', '-t'], nargs='?')
    
    try:
        args = parser.parse_args()
    except Exception:
        print("Wrong arguments provided. See help for better understanding.")

    match args.comand:
        case 'shell':
            # change execution mode to shell
            return
        case 'tree':
            # display existing tree in terminal
            tree_printer(store.store)
        case 'del':
            with store:
                root = store.get_tree(id=0)
                task = find_task(root, args.title_)

                if not task:
                    print("Can't find task with provided title")
                    return
                if task.parent:
                    parent = task.parent
                    parent.remove_child_by_id(task.id)
                else:
                    root = None
            
                store.save_tree(root)
        
        case 'edit':
            with store:
                root = store.get_tree(id=0)
                task = find_task(root, args.title_)

                if args.parent:
                    task.parent.children = tuple(i for i  in task.parent.children if i != task)
                    task.parent = find_task(root, args.parent)
                    task.parent.children = tuple(list(task.parent.children).append(task))
                if args.status:
                    task.status = args.status
                if args.title:
                    task.title = args.title

                store.save_tree(root)

        case 'add':
            with store:
                root = store.get_tree(id=0)
                new_task = Task(args.title_)

                if args.parent:
                    new_task.parent = find_task(root, args.parent)
                    new_task.parent.children = tuple(list(new_task.parent.children).append(new_task))
                if args.status:
                    new_task.status = args.status

                store.save_tree(root)




if __name__ == "__main__":
    print("Can't execute package directly")
else:
    arg_parser()
