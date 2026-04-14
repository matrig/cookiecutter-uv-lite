# GitHub Actions CI/CD

When you enable GitHub Actions during project creation (`github_actions: y`), your project automatically includes enterprise-grade continuous integration and deployment workflows. These workflows run automatically on every push and pull request to ensure code quality, test coverage, and security.

## Overview

The template includes three workflows in `.github/workflows/`:

| Workflow                       | Triggers                   | Purpose                                   |
| ------------------------------ | -------------------------- | ----------------------------------------- |
| **CI** (`ci.yml`)              | Push to main, PRs          | Testing, linting, type checking           |
| **Security** (`security.yml`)  | Push, PRs, weekly schedule | CodeQL analysis, dependency scanning      |
| **Documentation** (`docs.yml`) | Push to main, PRs          | Build and deploy MkDocs docs (if enabled) |

## Continuous Integration (CI)

The CI workflow runs on every push to `main` and every pull request.

### Code Quality Job

Runs linting, formatting checks, and type checking on the latest Python version:

```yaml
- Run ruff linting: ruff check .
- Run ruff formatting: ruff format --check .
- Run type checking: mypy .
```

This job fails if:

- Ruff finds style violations
- Code is not properly formatted
- MyPy detects type errors

### Testing Job

Runs your test suite across multiple Python versions and operating systems:

**Matrix:**

- **Python versions**: 3.9, 3.10, 3.11, 3.12, 3.13
- **Operating systems**: Ubuntu, macOS, Windows

Each combination runs independently:

```bash
uv run pytest --cov --cov-report=xml --cov-report=term
```

This means:

- A total of 15 separate test jobs (5 Python versions × 3 OSs)
- Tests run in parallel across GitHub's runners
- Faster feedback: if one OS/version fails, others continue
- Coverage reports are generated for each run

**Key features:**

- **Fast test execution**: Uses `pytest-xdist` for parallel test execution within each job
- **Coverage reporting**: Generates coverage reports in both XML and terminal formats
- **Cross-platform validation**: Ensures your package works on all major operating systems

## Codecov Integration

When you enable Codecov (`codecov: y`) alongside GitHub Actions, coverage reports are automatically uploaded to Codecov:

```yaml
- Upload coverage to Codecov (on Ubuntu, Python 3.11 only)
  - Uses: codecov/codecov-action@v4
  - Requires: CODECOV_TOKEN secret (see below)
```

**Why only Python 3.11 on Ubuntu?**

To optimize CI run time, coverage is only uploaded once using a consistent baseline (Python 3.11 on Ubuntu). This avoids redundant uploads and keeps Codecov reports clean.

**Setup required:**

1. Visit https://codecov.io/ and sign in with your GitHub account
2. Grant Codecov access to your repository
3. Add your `CODECOV_TOKEN` as a GitHub secret:
   - Go to your repo settings → Secrets and variables → Actions
   - Create new secret: `CODECOV_TOKEN` with your token from Codecov
4. Codecov will automatically start processing coverage reports from your CI

Once set up, Codecov will:

- Display coverage percentages on pull requests
- Show coverage trends over time
- Highlight changed files with coverage gaps

## Security Scanning

The Security workflow runs on every push, pull request, and on a weekly schedule (Mondays at 6 AM UTC) to catch vulnerabilities early.

### CodeQL Analysis

GitHub's native security analysis tool scans your Python code for security vulnerabilities:

- Analyzes code patterns for common security issues
- Checks for CWE (Common Weakness Enumeration) violations
- Results appear in your repository's "Security" tab
- Can be configured to fail on critical vulnerabilities

### Dependency Scanning

Scans your project dependencies for known vulnerabilities using the Safety tool:

```bash
uv tool run safety check --json
```

This checks against a database of known security vulnerabilities and reports:

- Vulnerable packages in your dependencies
- Severity levels (critical, high, medium, low)
- Suggested fixed versions

The workflow continues even if vulnerabilities are found (doesn't fail CI), allowing you to review and address them deliberately.

## Documentation Deployment

When you enable MkDocs (`mkdocs: y`) alongside GitHub Actions, the Documentation workflow automatically builds and deploys your docs:

**Build Job:**

- Runs on every push to main and PRs
- Builds documentation: `mkdocs build --clean --strict`
- `--strict` mode fails if there are any documentation warnings
- Uploads the `site/` directory as a GitHub Pages artifact

**Deploy Job:**

- Runs after the build job succeeds
- Only deploys on pushes to `main` (not on PRs)
- Uses GitHub's official Pages deployment action
- Your docs are live at `https://username.github.io/repo-name/`

**Deployment permissions:**

The workflow includes GitHub Pages permissions:

```yaml
permissions:
  contents: read # Read repository contents
  pages: write # Write to GitHub Pages
  id-token: write # For OIDC authentication
```

These permissions are automatically managed by GitHub and don't require additional secrets.

## Enterprise GitHub Support

The workflows support GitHub Enterprise deployments through environment variables:

```yaml
env:
  GH_HOST: "{{cookiecutter.git_server}}"
```

This allows the generated workflows to work with:

- `github.com` (public GitHub)
- Private GitHub Enterprise instances
- GitHub Enterprise Cloud

The `git_server` value you provided during project creation is automatically used in the workflows.

## Workflow Behavior

### When Workflows Run

| Trigger         | Workflows                | Behavior                             |
| --------------- | ------------------------ | ------------------------------------ |
| Push to `main`  | All (CI, Security, Docs) | Full suite runs                      |
| Pull Request    | CI, Security, Docs       | Full suite runs, doesn't deploy docs |
| Weekly schedule | Security only            | Runs Mondays at 6 AM UTC             |

### GitHub Pages Deployment

- Docs deploy **only** on successful builds pushed to `main`
- PRs generate docs artifacts for preview but don't deploy
- Deployment history is visible in your repository's "Deployments" tab

### Concurrency Control

The Documentation workflow uses concurrency management:

```yaml
concurrency:
  group: "pages"
  cancel-in-progress: false
```

This ensures:

- Only one documentation deployment runs at a time
- In-progress deployments aren't cancelled by newer pushes
- Prevents race conditions when multiple commits are pushed quickly

## Customizing Workflows

You can customize the workflows to fit your needs:

### Change Python Versions

Edit `.github/workflows/ci.yml` to test different Python versions:

```yaml
matrix:
  python-version: ["3.11", "3.12", "3.13"] # Test only these versions
```

### Skip Documentation Deployment

If you don't need automatic docs deployment, you can:

1. Delete `.github/workflows/docs.yml`
2. Or set `if: false` on the deploy job

### Add Custom Jobs

Add new jobs to any workflow for custom checks (e.g., security audits, integration tests):

```yaml
jobs:
  custom-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Your custom check
        run: your-command-here
```

### Disable Workflows Temporarily

To temporarily disable a workflow without deleting it:

1. Rename the file: `ci.yml` → `ci.yml.disabled`
2. Or add `.disabled` to any workflow file

Workflows in `.github/workflows/*.yml` are automatically discovered and run.

## Workflow Status and Logs

### View Workflow Status

- **On GitHub**: Go to your repo → "Actions" tab
- **In PRs**: Workflow status appears as a check at the bottom
- **Status badge**: Add this to your README:
  ```markdown
  [![CI](https://img.shields.io/github/actions/workflow/status/owner/repo/ci.yml?branch=main)](https://github.com/owner/repo/actions/workflows/ci.yml)
  ```

### Debug Workflow Failures

1. Click the failed workflow in the Actions tab
2. Click the job that failed
3. Expand the step to see full logs
4. Look for error messages and stack traces

**Common issues:**

- **MyPy errors**: Type annotations needed or configuration too strict
- **Ruff failures**: Code style violations (fix with `make check`)
- **Test failures**: Cross-platform or version-specific issues
- **CodeQL alerts**: Security patterns that need review

### Re-run Failed Workflows

You can re-run a failed workflow from the Actions tab without making new commits. This is useful for transient failures (network issues, timeouts, etc.).

## Performance Optimization

The workflows are optimized for speed:

- **Parallel execution**: Tests run across Python versions and OSs simultaneously
- **Caching**: Dependencies are cached to avoid re-downloading
- **Minimal redundancy**: Coverage is uploaded once, not 15 times
- **Fast uv**: Dependency installation is blazingly fast with `uv`

## Disabling GitHub Actions

If you want to disable workflows after project creation:

```bash
# Temporarily disable all workflows
mv .github .github.disabled

# Re-enable
mv .github.disabled .github
```

Or permanently remove the workflows:

```bash
rm -rf .github
```

GitHub will no longer run any automated checks. You can still use local checks (`make check`).

## Related Documentation

- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [Codecov documentation](https://docs.codecov.io/)
- [CodeQL documentation](https://codeql.github.com/)
- [uv GitHub integration](https://docs.astral.sh/uv/guides/integration/github/)
