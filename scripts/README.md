Archive unused files helper

This folder contains a small PowerShell helper to safely archive suspected unused files from the project root.

Usage

From PowerShell (run from the project root):

    .\scripts\archive_unused.ps1

By default the script will move:
- Cycleoflife.html
- Self Mastery and Fate With the Cycles of Life - H. Spencer Lewis.pdf
- package-lock.json
- package.json
- package-lock.yaml

It will skip large folders like `venv`, `.venv`, and `node_modules` unless you pass the `-IncludeVenv` flag.

Example (include venv/node_modules):

    .\scripts\archive_unused.ps1 -IncludeVenv

Restoring files

Open the `archive_unused_<timestamp>` folder created in the repo root and move files back to the project root to restore.

Safety notes

- The script moves files (not deletes) so everything is reversible.
- Inspect the archive folder before committing or removing files permanently.
- If you use source control (git), prefer to remove tracked files via `git rm` and commit the change rather than moving them manually.
