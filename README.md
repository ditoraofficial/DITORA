# DITora — Your Complete DIT Learning Platform

A responsive Flask learning platform starter with course catalog, lessons, student accounts, progress tracking, and practice quiz.

## Run locally
1. Install Python 3.11+.
2. Open terminal in this folder.
3. Run `python -m pip install -r requirements.txt`
4. Run `python app.py`
5. Visit `http://127.0.0.1:5000`

## Hosting
This project is prepared for deployment to a Python web host. ChatGPT cannot itself provide an always-on public server. Before public production use, configure a strong `SECRET_KEY`, persistent database storage, HTTPS, backups, and appropriate privacy/security policies.

## Customizing
- Course data and lessons: edit `COURSES` and `LESSONS` in `app.py`.
- Page templates: `templates/`
- Styles: `static/style.css`
