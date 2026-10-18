## CI/CD Workflow

1. **Pull Requests** to `dev`, `staging`, or `main` trigger the `build-and-test` job (Lint, Pytest, Docker Build). PRs cannot be merged if CI fails.
2. **Merge to `staging`**: Triggers `deploy-staging`. Injects `STAGING_ENV` secrets and builds the staging image.
3. **Merge to `main`**: Triggers `deploy-prod`. Injects `PROD_ENV` secrets and builds the production image.