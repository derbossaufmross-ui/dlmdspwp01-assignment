# Additional Task 1.3 - Required Git Commands

## Clone repository and check out `develop`

```bash
git clone <repo-url>
cd <repo-folder>
git checkout develop
git pull origin develop
```

## Add a new function and contribute it back to `develop`

```bash
git checkout -b feature/new-function
git add .
git commit -m "Add new function <name> and related tests"
git push -u origin feature/new-function
```

Then open a Pull Request from `feature/new-function` to `develop` and merge after team review.
