# AuraLink — Event Management (Django)

Quick starter scaffold for AuraLink using Django + MySQL (optional) and Bootstrap.

## Setup (local)

1. Create and activate venv (Windows):
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy env file and edit values:
   ```powershell
   copy .env.example .env
   # edit .env with your MySQL credentials or leave DB_ENGINE blank to use sqlite
   ```

3. Make migrations and create superuser:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Seed sample events (optional):
   ```powershell
   python manage.py seed
   ```
- Email & payments (dev):
  - Emails in development are printed to the console (console backend). Configure `EMAIL_BACKEND` in `.env` for production.
  - A simple payment **placeholder** was added: paid events use a demo checkout flow at `/events/<slug>/checkout/`. Integrate Stripe or PayPal to replace this demo flow.

- Assets & branding:
  - Hero image: place your image at `/static/images/hero.jpg` (or set `HERO_IMAGE_URL` in `.env` to point to another asset).
  - Logo: place `logo.png` at `/static/images/logo.png` (or set `LOGO_URL` in `.env` to a custom path). If the logo isn't found, the site will display the `SITE_NAME` text instead.
  - Favicon: add `/static/favicon.ico` if you want it to appear in browsers.
5. Run the dev server:
   - Automatic (recommended): Open the project folder in VS Code and accept the task prompt to run "Start Dev Server (auto)" (this will run migrations, collect static, seed sample data, start the server in a new window, and open http://127.0.0.1:8000).
   - Manual: ```powershell
   python manage.py runserver
   ```

If you don't want the server to start on folder open, disable the task in `.vscode/tasks.json` or change/remove the `runOn` setting.

Desktop shortcut
- To create a desktop shortcut that launches the site start script, run (once):
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts\create_shortcut.ps1
  ```
- Or double-click `scripts\create_shortcut.ps1` in File Explorer. This will create "AuraLink - Start.lnk" on your Windows desktop so you can start the site with a double-click.

Admin: http://127.0.0.1:8000/admin/  
Home: http://127.0.0.1:8000/

Notes:
- To use MySQL, install MySQL server and create the DB and user, then set environment variables in `.env`.
- Media files (uploaded event images) are stored in `/media/` by default.

Enjoy! 🎉
