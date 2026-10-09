# Sri Iyyanar Catering Service - Django website

## Folder map

```
iyyanar_catering/
  manage.py                  <- Django command tool (you run commands with this)
  requirements.txt           <- Python packages (just Django)
  config/                    <- project settings
    settings.py              <- settings (database, static, media, time zone)
    urls.py                  <- /admin/ + the website urls
    wsgi.py                  <- used by the hosting server
  catering/                  <- the website app
    models.py                <- database tables: GalleryItem, Review, Booking
    views.py                 <- Python code: home page, booking save, review, gallery add/delete
    urls.py                  <- page addresses
    admin.py                 <- admin panel setup
  templates/index.html       <- the HTML page
  static/css/style.css       <- the CSS (design)
  static/js/app.js           <- the JavaScript (booking message, WhatsApp/SMS links, stars...)
  static/img/                <- veg.jpg, nonveg.jpg, deva.webp
  media/                     <- photos and videos that admins upload (created automatically)
  db.sqlite3                 <- the database file (created by "migrate")
```

## Run it on your own computer (step by step)

1. Install Python 3.10 or newer from python.org. Tick "Add Python to PATH" on Windows.
2. Open a terminal (Command Prompt / PowerShell / Terminal) inside the `iyyanar_catering` folder.
3. Make a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install Django: `pip install -r requirements.txt`
5. Create the database tables (run both):
   ```
   python manage.py makemigrations catering
   python manage.py migrate
   ```
6. Create the first admin (it asks for a name, email and password):
   ```
   python manage.py createsuperuser
   ```
   Use the admin ID you want (for example `deva1112`) and a strong password of your own.
7. Start the website: `python manage.py runserver`
8. Open http://127.0.0.1:8000 in the browser.

## The 3 admins

1. Open http://127.0.0.1:8000/admin/ and log in with the admin from step 6.
2. Click **Users** -> **Add user**. Type the ID and password, Save.
3. On the next page tick **Staff status** (and **Superuser status** if the person should manage everything). Save.
4. Do this for each of the 3 people. Each person has their own ID and password.

## What admins can do (after login)

- On the website top bar click **Admin**, log in. The site then shows **Admin mode**:
  - **+ Add photo or video** (upload files or paste a YouTube / Facebook link) and **Delete** under each item.
  - Reviews waiting for approval appear with **Approve** and **Delete** buttons. Approved reviews have **Delete**.
- The same things can be done in the admin panel (`/admin/`): Gallery, Reviews, and **Bookings** (every booking typed on the website is saved here).
- Visitors (not logged in) cannot add or delete anything. The server checks this, not only the page.

## Where the data is stored

- Photos and videos: files in the `media/gallery/` folder.
- Gallery list, reviews, bookings, admin logins: `db.sqlite3` (one file).
- Back up both `db.sqlite3` and `media/` regularly.

## Do I create a new project?

Easiest: use this folder as it is (it already is a complete Django project).

If you want to create your own project and copy the files in:
1. `django-admin startproject config .`  then  `python manage.py startapp catering`
2. Copy `models.py`, `views.py`, `urls.py`, `admin.py` into `catering/`.
3. Copy `templates/`, `static/` into the project root.
4. Replace `config/settings.py` and `config/urls.py` with the ones here.
5. Run the steps 5 to 8 above.

## Put it online (free option: PythonAnywhere)

PythonAnywhere has a free plan that can run a Django site at `yourname.pythonanywhere.com`. Check their current free-plan limits first. A custom domain needs a paid plan.

1. Make a free account at pythonanywhere.com.
2. Upload the `iyyanar_catering` folder (Files tab, or a zip and unzip it in a Bash console).
3. In a Bash console: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`, then run steps 5 and 6 above.
4. Web tab -> Add a new web app -> Manual configuration (pick your Python version).
5. Set Source code and Working directory to your project folder, and the Virtualenv path to `.../venv`.
6. Edit the WSGI file so it points to `config.settings` and the project folder (the PythonAnywhere help page "How to use Django" shows the exact lines).
7. In the Web tab add Static files: URL `/static/` -> `<project>/staticfiles` and URL `/media/` -> `<project>/media`.
8. In a console run `python manage.py collectstatic`.
9. Set environment variables (or edit settings.py): `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS=yourname.pythonanywhere.com`, and a long random `DJANGO_SECRET_KEY`.
10. Click **Reload**.

Before going live: change SECRET_KEY, set DEBUG to 0, and use strong admin passwords.
