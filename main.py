import argparse
import json

def read_json(filename='data.json', verbose=True):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        if verbose:
            print('No database found. Starting with an empty task list.')
        return []
    except json.JSONDecodeError:
        if verbose:
            print('Database is empty or corrupted. Starting with an empty task list.')
        return []

def write_json(data, filename='data.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print('Tasks saved successfully.')
    except Exception as e:
        print(f'Error writing to database: {e}')

def main():
    parser = argparse.ArgumentParser(prog="track", description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-s", "--status", choices=["done", "notdone", "inprogress"], help="Filter tasks by status")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task", type=str, help="Task description")
    add_parser.add_argument("-s", "--status", choices=["done", "notdone", "inprogress"], default="notdone", help="Set status of the new task")

    delete_parser = subparsers.add_parser("delete", help="Delete a task by number")
    delete_parser.add_argument("task_number", type=int, help="Task number to delete (from list)")

    mark_parser = subparsers.add_parser("mark", help="Update status of a task")
    mark_parser.add_argument("task_number", type=int, help="Task number to update")
    mark_parser.add_argument("status", choices=["done", "notdone", "inprogress"], help="New status for the task")

    args = parser.parse_args()

    if args.command == "list":
        tasks = read_json()
        filtered = []
        for t in tasks:
            if isinstance(t, dict):
                if not args.status or t.get("status") == args.status:
                    filtered.append(t)
            else:
                if not args.status or args.status == "notdone":
                    filtered.append({"description": t, "status": "notdone"})
        if filtered:
            print(f"Your Tasks{' (' + args.status + ')' if args.status else ''}:")
            for i, task in enumerate(filtered, 1):
                desc = task.get("description", "<no description>")
                status = task.get("status", "notdone")
                print(f"{i}. [{status}] {desc}")
        else:
            print("No tasks found.")

    elif args.command == "add":
        tasks = read_json(verbose=False)
        tasks.append({"description": args.task, "status": args.status})
        write_json(tasks)

    elif args.command == "delete":
        tasks = read_json(verbose=False)
        index = args.task_number - 1
        if 0 <= index < len(tasks):
            removed_task = tasks.pop(index)
            write_json(tasks)
            desc = removed_task["description"] if isinstance(removed_task, dict) else removed_task
            print(f"Deleted task #{args.task_number}: {desc}")
        else:
            print(f"Task number {args.task_number} does not exist.")

    elif args.command == "mark":
        tasks = read_json(verbose=False)
        index = args.task_number - 1
        if 0 <= index < len(tasks):
            if isinstance(tasks[index], dict):
                tasks[index]["status"] = args.status
            else:
                tasks[index] = {"description": tasks[index], "status": args.status}
            write_json(tasks)
            print(f"Task #{args.task_number} marked as {args.status}.")
        else:
            print(f"Task number {args.task_number} does not exist.")

if __name__ == "__main__":
    main()
