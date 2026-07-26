# MIL Reality Check Bangladesh

A complete multipage Media and Information Literacy awareness website built entirely with Python and Streamlit.

## Main features
- Public homepage, initiative information, Reality vs Reality Wall, activities, weekly archive, team, social media, resources, suspicious-news submissions, and contact form.
- Session-based public voting with permanent SQLite storage.
- SQLAlchemy ORM models and seeded sample data.
- Secure administrator authentication with Werkzeug password hashing.
- Admin dashboard for content management, publishing controls, review workflow, messages, settings, uploads, and password changes.
- Pandas tables, Plotly charts, Pillow image validation, Streamlit forms, and responsive Streamlit layouts.

## Technology stack
Python, Streamlit, SQLite, SQLAlchemy, Pandas, Plotly, Pillow, Werkzeug, python-dotenv, and validators.

## Folder structure
The project follows the requested `pages`, `components`, `services`, `data`, `uploads`, and `assets` structure.

## Installation
Install Python 3.10 or newer.

### Create a virtual environment
macOS or Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bat
python -m venv venv
venv\Scripts\activate
```

### Install packages
```bash
pip install -r requirements.txt
```

## Environment setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
On Windows, create `.env` manually or run:
```bat
copy .env.example .env
```
Replace `SECRET_KEY` with a long random value before deployment.

## Database creation and sample data
```bash
python3 seed_data.py
```
Windows may use:
```bat
python seed_data.py
```
The script creates database tables and inserts sample records only when their tables are empty.

## Development administrator
- Username: `admin`
- Password: `admin123`

**Security warning: Change this default password immediately before deployment.**  
Open Admin Dashboard → Security after logging in. The database stores only the password hash, never the plain-text password.

## Run in Visual Studio Code
1. Open the `mil_reality_check` folder in VS Code.
2. Select the virtual-environment Python interpreter.
3. Open the integrated terminal.
4. Activate the environment.
5. Run:
```bash
streamlit run app.py
```
Open:
`http://localhost:8501`

## Replacing images
Use the Admin Dashboard upload controls. Uploaded images are validated, renamed with UUID values, and stored in category-specific folders. Supported formats are PNG, JPG, JPEG, and WEBP. The default maximum size is 5 MB.

## Changing the website name
Admin Dashboard → Website Settings → Website name. No source-code edit is required.

## Updating team members
Admin Dashboard → Team. Select one of the ten fixed profile slots, edit all fields, upload a photograph, and save.

## Changing the admin password
Admin Dashboard → Security. Enter the current password and a new password containing at least eight characters.

## Streamlit Community Cloud deployment
1. Push the project to a private or public GitHub repository.
2. Do not commit `.env`, uploaded private submissions, or the local SQLite database.
3. In Streamlit Community Cloud, choose `app.py` as the main file.
4. Add secrets through the Streamlit Cloud settings.
5. For a small demonstration, SQLite can run on the app filesystem, but its data may reset when the app is rebuilt. Use a persistent external database for production-grade deployment.
6. Change the default admin password immediately.

## Editing content
Most public content is database-driven. Use the Admin Dashboard for Reality Wall posts, archives, activities, team profiles, social records, resources, submissions, messages, and website settings.

## Common errors and solutions
- **Module not found:** activate the virtual environment and rerun `pip install -r requirements.txt`.
- **Database not found or empty:** run `python3 seed_data.py`.
- **Permission error:** ensure the project folder is writable.
- **Image rejected:** use PNG, JPG, JPEG, or WEBP below the configured size limit.
- **Port 8501 busy:** run `streamlit run app.py --server.port 8502`.
- **SQLite locked:** stop duplicate Streamlit processes and restart the app.
- **Admin login fails:** confirm `seed_data.py` ran and use the development credentials once.
- **Broken page navigation:** run from the project root using `streamlit run app.py`, not from inside the `pages` folder.

## Notes
- Custom CSS is embedded only through Streamlit `st.markdown`.
- No Flask, Django, React, Node.js, or separate HTML/CSS/JavaScript frontend is used.
- Replace sample URLs, placeholders, and seeded content before public launch.
