# CodeAlpha_SocialMedia

An Instagram-style social media platform built with Django — a full-stack web application featuring image uploads, YouTube video embedding, and Instagram URL sharing.

---

## 🔗 Live Demo

**Coming Soon** — Deploying to Render

---

## ✨ Features

### 👤 User Management
- User registration with validation
- Login / Logout functionality
- User profiles with bio and profile picture
- Edit profile (username, email, bio, picture)
- View other users' profiles

### 📝 Post System
- Create posts with three media options:
  - 📷 **Image upload** (stored on Cloudinary)
  - 🎥 **YouTube video** (search & embed via YouTube Data API v3)
  - 📸 **Instagram URL** (preview card with redirect)
- Instagram-style feed (newest first)
- Post grid on profile page
- Delete own posts

### ❤️ Interactions
- Like / Unlike posts (AJAX real-time)
- Comment on posts (AJAX real-time)
- View who liked and commented
- Like count and comment count display

### 🎨 UI/UX
- Instagram-inspired clean design
- Responsive mobile layout with bottom navigation
- Modern gradient accents and smooth animations
- Google Fonts (Inter) typography
- Glassmorphism navbar
- Loading states and error handling

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Django 5.x |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Vanilla JavaScript |
| **Database** | SQLite (development) |
| **Image Storage** | Cloudinary (production) |
| **API** | YouTube Data API v3 |
| **Fonts** | Google Fonts (Inter) |
| **Icons** | Bootstrap Icons |
| **Deployment** | Render |
| **Static Files** | WhiteNoise |

---

## 🚀 Local Setup

### Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** installed
- **Git** installed
- **YouTube Data API v3 key** (from Google Cloud Console)
- **Cloudinary account** (free tier works fine)
- **Code editor** (VS Code recommended)

---

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/praveenraj444/CodeAlpha_SocialMedia.git
cd CodeAlpha_SocialMedia
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Setup Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and add your keys:

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True

YOUTUBE_API_KEY=your_youtube_api_key_here

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your_password
```

#### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Or if using environment variables:

```bash
python manage.py createsuperuser --no-input
```

#### 7. Run Development Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## 📁 Project Structure

```
CodeAlpha_SocialMedia/
│
├── manage.py
├── requirements.txt
├── build.sh                      # Render deployment script
├── .env                          # Environment variables (NOT in git)
├── .env.example                  # Sample env file
├── .gitignore
├── README.md
│
├── CodeAlpha_SocialMedia/        # Project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── social_app/                   # Main application
│   ├── migrations/
│   ├── templates/
│   │   ├── 404.html
│   │   ├── 500.html
│   │   └── social_app/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── profile.html
│   │       ├── edit_profile.html
│   │       ├── create_post.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── delete_post_confirm.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── create_post.js
│   └── images/
│       └── default.png
│
└── media/                        # Local uploads (dev only)
    └── profile_pics/
```

---

## 🗄️ Database Models

### Profile
- `user` (OneToOne → User)
- `bio` (TextField)
- `profile_pic` (ImageField)

### Post
- `user` (ForeignKey → User)
- `image` (ImageField, optional)
- `youtube_video_id` (CharField, optional)
- `youtube_title` (CharField, optional)
- `youtube_thumbnail` (URLField, optional)
- `instagram_url` (URLField, optional)
- `caption` (TextField)
- `created_at` (DateTimeField)

**Rule:** At least one media (image / YouTube / Instagram) required.

### Like
- `user` (ForeignKey)
- `post` (ForeignKey)
- `created_at` (DateTimeField)
- Unique constraint: (user, post)

### Comment
- `user` (ForeignKey)
- `post` (ForeignKey)
- `text` (TextField)
- `created_at` (DateTimeField)

---

## 🔌 API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/` | Home feed |
| GET/POST | `/register/` | User registration |
| GET/POST | `/login/` | Login |
| GET | `/logout/` | Logout |
| GET | `/profile/` | Own profile |
| GET | `/profile/<username>/` | Other user profile |
| GET/POST | `/profile/edit/` | Edit profile |
| GET/POST | `/post/new/` | Create post |
| POST | `/post/<id>/delete/` | Delete post |
| POST | `/post/<id>/like/` | Toggle like (AJAX) |
| POST | `/post/<id>/comment/` | Add comment (AJAX) |
| GET | `/youtube-search/?q=...` | YouTube search (AJAX) |

---

## ☁️ Cloudinary Setup

1. Sign up at [cloudinary.com](https://cloudinary.com) (free tier: 25 GB storage, 25 GB bandwidth/month)
2. Get your **Cloud Name**, **API Key**, **API Secret** from the dashboard
3. Add them to `.env`

**How it works:**
- **Local development** (`DEBUG=True`): images stored in `media/` folder
- **Production** (`DEBUG=False`): images automatically uploaded to Cloudinary

---

## 🎥 YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create **API Key** (restrict to YouTube Data API v3)
5. Add to `.env`

**Free tier:** 10,000 units/day (~100 searches/day)

---

## 🚀 Deployment on Render

### 1. Prepare Files

Ensure these files exist:
- `requirements.txt`
- `build.sh` (executable)
- `.gitignore` (with `.env` excluded)

### 2. Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 3. Create Render Web Service

1. Go to [render.com](https://render.com) → Sign up with GitHub
2. Click **New +** → **Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Name:** `codealpha-socialmedia`
   - **Region:** Singapore (or closest)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn CodeAlpha_SocialMedia.wsgi`

### 4. Add Environment Variables

In Render dashboard → Environment tab → Add:

```
SECRET_KEY=<your_secret_key>
DEBUG=False
YOUTUBE_API_KEY=<your_youtube_key>
CLOUDINARY_CLOUD_NAME=<your_cloud_name>
CLOUDINARY_API_KEY=<your_api_key>
CLOUDINARY_API_SECRET=<your_api_secret>
DJANGO_SUPERUSER_USERNAME=<admin_username>
DJANGO_SUPERUSER_EMAIL=<admin_email>
DJANGO_SUPERUSER_PASSWORD=<admin_password>
PYTHON_VERSION=3.11.9
```

### 5. Deploy

Click **Create Web Service** → wait for build → get your live URL.

### 6. Create Admin User

Build script automatically creates superuser using environment variables (no shell needed).

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `TemplateDoesNotExist` | Check `templates/social_app/` path |
| Static files not loading | Run `python manage.py collectstatic` |
| Images not uploading | Verify Cloudinary credentials |
| YouTube search fails | Check API key restriction |
| `403 CSRF` error | Ensure `{% csrf_token %}` in forms |
| Database errors | Run `python manage.py migrate` |

---

## 📸 Screenshots

*(Add your screenshots here after deployment)*

- Home Feed
- Create Post
- Profile Page
- Mobile View

---

## 🎓 Internship

Built as part of the **CodeAlpha Full Stack Development Internship** — **Task 2: Social Media Platform**.

**Requirements covered:**
- ✅ User profiles
- ✅ Posts & comments
- ✅ Like system
- ✅ Frontend: HTML, CSS, JavaScript
- ✅ Backend: Django
- ✅ Database for users, posts, comments

**Bonus features:**
- YouTube video search & embed
- Instagram URL preview
- Cloudinary image storage
- Real-time like/comment (AJAX)
- Mobile bottom navigation

---

## 📄 License

MIT License — feel free to use this project for learning purposes.

---

## 👨‍💻 Author

**[Your Name]**
- GitHub: [@YOUR_USERNAME](https://github.com/praveenraj444)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

---

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Cloudinary](https://cloudinary.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [CodeAlpha](https://www.codealpha.tech/) for the internship opportunity