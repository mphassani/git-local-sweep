# git-local-sweep

Clean up local Git branches that no longer exist on remote.

Similar to [git-sweep](https://github.com/arc90/git-sweep), but specifically designed to delete local branches marked as "gone" (i.e., their remote tracking branches have been deleted).

## Why?

After pull requests are merged and remote branches are deleted, your local repository still contains those branches. Over time, this clutter builds up. Running `git branch -vv` shows them with a `[origin/branch: gone]` marker.

`git-local-sweep` makes it easy to identify and delete these orphaned local branches.

The package exposes a short alias: `gls`.

## Installation

### npm Global Install (Recommended)

```bash
npm install -g @cryterion/git-local-sweep
```

This installs both commands:
- `git-local-sweep`
- `gls`

### Shell Installer (Alternative)

```bash
curl -fsSL https://raw.githubusercontent.com/mphassani/git-local-sweep/main/install.sh | bash
```

Or using wget:

```bash
wget -qO- https://raw.githubusercontent.com/mphassani/git-local-sweep/main/install.sh | bash
```

### Manual Installation

1. Download the script:
```bash
curl -fsSL https://raw.githubusercontent.com/mphassani/git-local-sweep/main/git-local-sweep -o git-local-sweep
```

2. Make it executable:
```bash
chmod +x git-local-sweep
```

3. Move it to a directory in your PATH:
```bash
sudo mv git-local-sweep /usr/local/bin/
sudo ln -sf /usr/local/bin/git-local-sweep /usr/local/bin/gls
```

Or for user-only installation:
```bash
mkdir -p ~/.local/bin
mv git-local-sweep ~/.local/bin/
ln -sf ~/.local/bin/git-local-sweep ~/.local/bin/gls
# Add ~/.local/bin to your PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
```

## Updating

### npm Installation

If installed via npm, update with:

```bash
npm install -g @cryterion/git-local-sweep@latest
```

If you run `git-local-sweep update` (or `gls update`) from an npm-managed install, the command guides you to the npm update flow.

### Shell/Manual Installation

If installed via `install.sh` or manual copy, run:

```bash
git-local-sweep update
```

Or re-run the installer:

```bash
curl -fsSL https://raw.githubusercontent.com/mphassani/git-local-sweep/main/install.sh | bash
```

## Usage

### Preview branches to be deleted

```bash
git-local-sweep preview
# or
gls preview
```

This shows you which local branches are marked as "gone" from remote without deleting anything.
Before listing branches, the tool refreshes remote tracking data with a `git fetch --all --prune` check.

### Clean up branches

```bash
git-local-sweep cleanup
# or
gls cleanup
```

This will show you the branches and prompt for confirmation before deleting them.
At the prompt, `y` or just pressing Enter confirms deletion.

### Clean up without confirmation

```bash
git-local-sweep cleanup --force
# or
gls cleanup --force
```

Deletes branches without prompting for confirmation. Use with caution!

### Check version

```bash
git-local-sweep --version
# or
gls --version
```

Shows the currently installed version.

### Update to latest version

```bash
git-local-sweep update
# or
gls update
```

For npm-managed installs, this recommends the npm global update command.
For shell/manual installs, this checks for and applies script updates.

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

Delete these branches? ([Y]/n)

deleting feature/old-feature (done)
deleting bugfix/fixed-bug (done)
deleting experiment/test-idea (done)

All done!
```

## Requirements

- Python 3.6 or higher
- Git
- npm (only required for npm install/update/release flows)

## Release Process

### Version bump workflow

Use Bun scripts to keep `package.json` and the CLI script version in sync:

```bash
bun run check:version-sync
bun run version:patch
# or: bun run version:minor
# or: bun run version:major
```

After bumping, commit and merge to `main`. The release workflow then:
1. Confirms version sync
2. Checks whether version increased from the previous `main` commit
3. Creates GitHub Release `vX.Y.Z` if missing
4. Publishes `@cryterion/git-local-sweep@X.Y.Z` to npm if not already published

### One-time setup for automated npm publish

1. Configure npm Trusted Publishing (OIDC) for this repository:
   - npm package: `@cryterion/git-local-sweep`
   - GitHub repo: `mphassani/git-local-sweep`
   - Workflow file: `.github/workflows/release.yml`
2. Ensure the `@cryterion` npm scope allows public packages.

### First manual npm publish bootstrap

Run once from the repository root (after version sync check):

```bash
npm publish --access public
```

The release workflow is idempotent, so if this version is already on npm it will skip publishing and continue safely.

## How it works

The script:
1. Runs `git branch -vv` to get detailed branch information
2. Identifies branches with the `[origin/...: gone]` marker
3. Uses `git branch -D` to force-delete these branches

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

MIT License - see LICENSE file for details.

## Author

Created by Parsa Hassani ([@mphassani](https://github.com/mphassani))
