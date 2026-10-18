# Deployment Guide

## Environment Variables
We use GitHub Secrets to inject environment configurations.
- `STAGING_ENV`: Contains config for staging (e.g., `DB_HOST=staging.db`).
- `PROD_ENV`: Contains config for production (e.g., `DB_HOST=prod.db`).

## Build Process
- **Staging image**: Automatically built upon PR merge to the `staging` branch.
- **Production image**: Automatically built upon PR merge to the `main` branch.