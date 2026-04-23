# Fixes for the stage 2 devops

### Fix 1: Redis connection misconfiguration
- file: api/main.py
- line: 8
- issue: redis was hardcoded to "localhost", which fails in the containerized environment
- fix: replaced with environment variable, , and included a fallback

### Fix 2: Frontend API URL hardcoded
- file: frontend/app.js
- line: 6
- issue: api url was hardcoded
- fix: replaced with environment variable, and included a fallback

### Fix 3: Worker Redis connection
- file: worker/worker.py
- line: 6
- issue: redis was hardcoded to "localhost", which fails in the containerized environment
- fix: replaced with environment variable