# Deployment Guide

## Environment Variables
We use GitHub Secrets to inject environment configurations.
- `STAGING_ENV`: Contains config for staging (e.g., `DB_HOST=staging.db`).
- `PROD_ENV`: Contains config for production (e.g., `DB_HOST=prod.db`).

## Build Process
- **Staging image**: Automatically built when code is pushed (merged) to the `staging` branch; `STAGING_ENV` secret is written to `.env` before build.
- **Production image**: Automatically built when code is pushed (merged) to the `main` branch; `PROD_ENV` secret is written to `.env` before build.