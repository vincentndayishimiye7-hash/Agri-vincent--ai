# Agri-Vincent AI

A starter Flask web app for maize-farming questions in Rwanda, with Kinyarwanda, English, and French UI options.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Deploy to Render
1. Push these files to the root of your GitHub repository.
2. In Render, create a new Web Service and select this repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add `MISTRAL_API_KEY` in Render's Environment settings. Create the key in your Mistral account; do not put the key in GitHub or in source code.
6. Deploy, then open `/health` on the deployed URL; it should return JSON with status `ok`.

## Important
- The app uses Mistral API only if `MISTRAL_API_KEY` is configured.
- Without a key, the web app still loads but shows setup guidance instead of a generated AI answer.
- Weather and market-price integrations, MCP tools, farmer profiles, and reminders are not implemented in this starter.
- Agricultural advice is informational; follow local extension guidance and product labels.
