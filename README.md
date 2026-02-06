# git-local-sweep

Clean up local Git branches that no longer exist on remote.

Similar to [git-sweep](https://github.com/arc90/git-sweep), but specifically designed to delete local branches marked as "gone" (i.e., their remote tracking branches have been deleted).

## Why?

After pull requests are merged and remote branches are deleted, your local repository still contains those branches. Over time, this clutter builds up. Running `git branch -vv` shows them with a `[origin/branch: gone]` marker.

`git-local-sweep` makes it easy to identify and delete these orphaned local branches.

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/phassani/git-local-sweep/main/install.sh | bash
```

Or using wget:

```bash
wget -qO- https://raw.githubusercontent.com/phassani/git-local-sweep/main/install.sh | bash
```

### Manual Installation

1. Download the script:
```bash
curl -fsSL https://raw.githubusercontent.com/phassani/git-local-sweep/main/git-local-sweep -o git-local-sweep
```

2. Make it executable:
```bash
chmod +x git-local-sweep
```

3. Move it to a directory in your PATH:
```bash
sudo mv git-local-sweep /usr/local/bin/
```

Or for user-only installation:
```bash
mkdir -p ~/.local/bin
mv git-local-sweep ~/.local/bin/
# Add ~/.local/bin to your PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
```

## Usage

### Preview branches to be deleted

```bash
git-local-sweep preview
```

This shows you which local branches are marked as "gone" from remote without deleting anything.

### Clean up branches

```bash
git-local-sweep cleanup
```

This will show you the branches and prompt for confirmation before deleting them.

### Clean up without confirmation

```bash
git-local-sweep cleanup --force
```

Deletes branches without prompting for confirmation. Use with caution!

## Example

```bash
$ git-local-sweep preview
These local branches are gone from remote:
  feature/old-feature
  bugfix/fixed-bug
  experiment/test-idea

To delete them, run again with `git-local-sweep cleanup`

$ git-local-sweep cleanup
These local branches are gone from remote:
  feature/old-feature
  bugfix/fixed-bug
  experiment/test-idea

Delete these branches? (y/n) y

deleting feature/old-feature (done)
deleting bugfix/fixed-bug (done)
deleting experiment/test-idea (done)

All done!
```

## Requirements

- Python 3.6 or higher
- Git

## How it works

The script:
1. Runs `git branch -vv` to get detailed branch information
2. Identifies branches with the `[origin/...: gone]` marker
3. Uses `git branch -D` to force-delete these branches

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - see LICENSE file for details

## Author

Created by Parsa Hassani ([@phassani](https://github.com/phassani))
