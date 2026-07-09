# Milestone 10 - GitOps Repository Structure

## Objective

Create a production-ready repository structure for GitOps.

## Tasks Completed

- Created kubernetes directory structure
- Added README files
- Committed changes to GitHub

## Repository Structure

```text
kubernetes/
├── applications/
├── bootstrap/
├── infrastructure/
├── platform/
└── workloads/
```

## Commands Executed

```bash
mkdir -p kubernetes/applications
mkdir -p kubernetes/bootstrap
mkdir -p kubernetes/infrastructure
mkdir -p kubernetes/platform
mkdir -p kubernetes/workloads

touch kubernetes/README.md
touch kubernetes/applications/README.md
touch kubernetes/bootstrap/README.md
touch kubernetes/infrastructure/README.md
touch kubernetes/platform/README.md
touch kubernetes/workloads/README.md

git add .
git commit -m "Create GitOps repository structure"
git push origin main
```

## Key Takeaways

- Repository is organized for GitOps.
- Platform and workloads are separated.
- Applications will be managed declaratively.

## Next Milestone

Implement App of Apps.