# Task Tracker CLI

A simple command-line task tracking application written in Python. It allows you to add, list, delete, and update the status of your tasks, storing data in a JSON file.

## Features

- Add new tasks with an optional status.
- List all tasks, optionally filtered by status.
- Delete tasks by their task number.
- Update the status of existing tasks.
- Tasks are saved persistently in a `data.json` file.

## Usage

The tool uses subcommands to manage tasks.

### Commands

#### `list`

List all tasks. Optionally filter by status.

```bash
python track.py list
python track.py list -s done
python track.py list --status inprogress

python track.py add "Finish homework"
python track.py list
python track.py mark 1 done
python track.py list -s done
python track.py delete 1