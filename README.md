# DITora — Your Complete DIT Learning Platform

Flask learning platform with course catalog, lessons, student accounts, progress tracking, and practice quiz.

## Vercel deployment
- `app.py` is the Flask entry point.
- HTML files are in `templates/`.
- CSS is in `static/`.
- Set `DATABASE_URL` to the Supabase PostgreSQL Session Pooler connection string.
- Set `SECRET_KEY` to a long random secret in Vercel Environment Variables.
- Redeploy after changing environment variables.

## Local run
1. Install Python 3.11+.
2. Run `python -m pip install -r requirements.txt`
3. Set `DATABASE_URL` and `SECRET_KEY` environment variables.
4. Run `python app.py`
5. Visit `http://127.0.0.1:5000`
