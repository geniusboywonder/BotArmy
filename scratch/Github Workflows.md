# GitHub Workflows for Sub-Agent Collaboration

This guide outlines how to set up GitHub to support multiple sub-agents (e.g., automated agents or human developers) that automatically branch, push/pull, develop, and test different aspects of code. It includes a practical tagging convention and keeps the setup simple for beginners. The workflow leverages GitHub Actions, branch protection, Projects, and Codespaces to streamline collaboration.

## 1. Define the Sub-Agent Workflow

To enable multiple sub-agents to work independently, use a modified **GitHub Flow** with automation. Sub-agents are assigned roles to handle specific tasks, ensuring modularity and traceability.

- **Sub-Agent Roles**:
  - **Developer Agents** (Front-End, Back-End, API): Create and push code to feature branches.
  - **Test Agent**: Runs automated tests on pull requests (PRs) or branches.
  - **Review Agent**: Enforces code quality (e.g., linting, style checks).
  - **Deploy Agent**: Manages deployment after successful merges.

- **Workflow Overview**:
  - Each sub-agent works on a dedicated feature branch.
  - GitHub Actions automate branching, pushing/pulling, testing, and tagging.
  - Branch protection ensures code quality and prevents conflicts.
  - A tagging convention tracks contributions and releases.

## 2. Set Up the Repository

Optimize your repository for sub-agent collaboration:

- **Repository Structure**:
  - Maintain a clear structure: `/src` for source code, `/tests` for tests, `/docs` for documentation.
  - Add a `.github/workflows/` directory for GitHub Actions YAML files.
  - Include a `README.md` to describe the project and a `.gitignore` to exclude unnecessary files.

- **Branch Protection Rules**:
  - Navigate to Settings > Branches > Add rule (apply to `main` or `develop`).
  - Enable:
    - **Require pull request reviews before merging**: Ensures code review.
    - **Require status checks to pass**: Ensures tests pass before merging.
    - **Include administrators**: Prevents bypassing rules.
    - **Restrict who can push to matching branches**: Limits direct pushes to `main`.
  - This ensures all changes go through PRs, maintaining code quality.

- **Default Branch**:
  - Use `main` for production-ready code.
  - Optionally, use `develop` for integrating features before release (Git Flow model).

## 3. Automate Branching and Push/Pull with GitHub Actions

GitHub Actions automate repetitive tasks like branching, pushing, and pulling for sub-agents.

### Create Feature Branches Automatically
Automate branch creation when issues are opened to assign tasks to sub-agents.

```yaml
# .github/workflows/create-branch.yml
name: Create Feature Branch
on:
  issues:
    types: [opened]
jobs:
  create-branch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create branch
        run: |
          git checkout -b feature/${{ github.event.issue.title }}-${{ github.event.issue.number }}
          git push origin feature/${{ github.event.issue.title }}-${{ github.event.issue.number }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- **Trigger**: When an issue is created (e.g., “Implement login page”), a branch like `feature/implement-login-page-12` is created.
- **Usage**: Sub-agents work on this branch in isolation.

### Automate Push/Pull for Sub-Agents
Ensure sub-agents’ changes are synchronized with the remote branch.

```yaml
# .github/workflows/sync-agent-changes.yml
name: Sync Agent Changes
on:
  push:
    branches:
      - feature/*
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Pull and push changes
        run: |
          git pull origin feature/${{ github.ref_name }}
          # Sub-agent makes changes (e.g., via script or API)
          git add .
          git commit -m "Changes by ${GITHUB_ACTOR} on ${github.ref_name}"
          git push origin feature/${{ github.ref_name }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- **Purpose**: Keeps branches up-to-date and commits changes automatically.

### Automate Pull Requests
Automatically create PRs when a feature branch is pushed.

```yaml
# .github/workflows/auto-pr.yml
name: Auto Create PR
on:
  push:
    branches:
      - feature/*
jobs:
  create-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Create Pull Request
        uses: repo-sync/pull-request@v2
        with:
          source_branch: ${{ github.ref_name }}
          destination_branch: main
          pr_title: "Changes from ${{ github.ref_name }}"
          pr_body: "Automated PR for changes in ${{ github.ref_name }}"
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

- **Purpose**: Opens a PR for review, ensuring changes are vetted before merging.

## 4. Automate Development and Testing

Each sub-agent can have dedicated workflows to develop and test specific code aspects.

### Development Workflows
Create workflows tailored to each agent’s role (e.g., Front-End, Back-End).

Example for a Front-End agent:

```yaml
# .github/workflows/frontend-dev.yml
name: Front-End Development
on:
  push:
    branches:
      - feature/frontend-*
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
      - name: Install dependencies
        run: npm install
      - name: Build front-end
        run: npm run build
      - name: Commit build artifacts
        run: |
          git add .
          git commit -m "Front-end build by agent"
          git push origin ${{ github.ref_name }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- **Customization**: Create similar workflows for Back-End (`feature/backend-*`) or API (`feature/api-*`) agents, using tools like Python or Postman.

### Testing Workflow
Run tests on pushes or PRs to ensure code quality.

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches:
      - feature/*
  pull_request:
    branches:
      - main
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up environment
        uses: actions/setup-node@v3
        with:
          node-version: '16'
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm test
      - name: Run linter
        run: npm run lint
```

- **Purpose**: Ensures all code is tested and linted before merging.
- **Enhancement**: Use a matrix strategy for multi-environment testing (e.g., different Node.js versions).

### Concurrency Control
Prevent multiple CI runs on the same branch to avoid conflicts.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.repository }}-${{ github.ref_name }}
  cancel-in-progress: false
```

## 5. Tagging Convention

A clear tagging convention ensures traceability of sub-agent contributions and releases.

- **Feature Branch Tags**:
  - Format: `<agent-role>/<task-description>-<issue-number>`
  - Examples:
    - `frontend/login-page-12`: Front-End agent on issue #12.
    - `backend/auth-api-15`: Back-End agent on issue #15.
    - `test/unit-tests-20`: Test agent on issue #20.
  - **Purpose**: Ties branches to roles and tasks for easy tracking.

- **Release Tags**:
  - Format: `v<major>.<minor>.<patch>` (Semantic Versioning)
  - Examples:
    - `v1.0.0`: Initial release.
    - `v1.1.0`: Minor feature update.
    - `v1.1.1`: Bug fix or patch.
  - Create tags on `main` after merging:
    ```bash
    git checkout main
    git tag -a v1.0.0 -m "Release v1.0.0 by Deploy Agent"
    git push origin v1.0.0
    ```

- **Automate Tagging**:
  ```yaml
  # .github/workflows/tag-release.yml
  name: Tag Release
  on:
    push:
      branches:
        - main
  jobs:
    tag:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Create tag
          run: |
            git tag -a v${{ github.run_number }} -m "Release v${{ github.run_number }} by Deploy Agent"
            git push origin v${{ github.run_number }}
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  ```

- **Agent-Specific Commit Tags**:
  - Format: `<ROLE>-<description>`
  - Examples:
    - `FE-Updated UI components`: Front-End agent.
    - `BE-Added database schema`: Back-End agent.
    - `TEST-Wrote unit tests`: Test agent.
  - Example commit: `git commit -m "FE-Added responsive navbar"`

## 6. Using GitHub Codespaces for Sub-Agents

Configure Codespaces for each sub-agent to work in isolated environments.

- **Agent-Specific Codespaces**:
  - Add a `devcontainer.json` for each agent type in `.devcontainer/` (e.g., `frontend.json`, `backend.json`).
  - Example for a Front-End agent:
    ```json
    {
      "name": "Front-End Agent",
      "image": "mcr.microsoft.com/vscode/devcontainers/javascript-node:16",
      "customizations": {
        "vscode": {
          "extensions": ["esbenp.prettier-vscode", "dbaeumer.vscode-eslint"]
        }
      },
      "postCreateCommand": "npm install"
    }
    ```
  - Launch Codespaces from specific branches (e.g., `feature/frontend-12`).

- **Automate Codespace Setup**:
  - Use the GitHub CLI:
    ```bash
    gh codespace create -b feature/frontend-12 -m 2core
    ```

## 7. Keeping It Simple and Practical

To avoid complexity for beginners:

- **Start Small**: Test with one agent (e.g., Front-End) before scaling.
- **Use Templates**: Leverage GitHub’s Action templates (Actions > New workflow).
- **Limit Branch Scope**: One feature branch per agent task to avoid conflicts.
- **Monitor Actions**: Check the Actions tab to debug failures.
- **Regular Pulls**: Agents should pull from `main` before starting:
  ```bash
  git checkout feature/frontend-12
  git pull origin main
  ```

## 8. Example End-to-End Workflow

1. **Issue Created**: A user or orchestrator creates an issue (e.g., “Add user login”).
2. **Branch Created**: `create-branch.yml` creates `feature/frontend-login-12`.
3. **Development**: Front-End agent works in a Codespace, commits, and pushes.
4. **Testing**: `ci.yml` runs tests on push or PR.
5. **PR Created**: `auto-pr.yml` opens a PR to `main`.
6. **Review and Merge**: A Review agent or human checks the PR; tests must pass.
7. **Tagging**: `tag-release.yml` tags the commit (e.g., `v123`).
8. **Deployment**: Deploy agent handles deployment via another Action.

## 9. Troubleshooting and Next Steps

- **Common Issues**:
  - **Merge Conflicts**: Agents should pull regularly (`git pull origin main`) and resolve conflicts in PRs.
  - **Action Failures**: Check Actions tab logs. Ensure `GITHUB_TOKEN` permissions are set (Settings > Actions > General).
  - **Resource Limits**: Monitor Codespaces usage to stay within the free tier (120 core hours/month).

- **Next Steps**:
  - Add a Review agent workflow for coding standards (e.g., ESLint, Pylint).
  - Integrate a Deploy agent with platforms like Vercel or AWS.
  - Use GitHub’s API for programmatic issue/PR management: https://x.ai/api.

This setup ensures a scalable, automated workflow for sub-agents while remaining beginner-friendly.