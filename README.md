# 🍽️ Canteen Management System

A complete full-stack canteen management system with Django REST API backend and dual React frontends (customer app + admin panel).

## 📁 Project Structure

```
ASAR_CMS_Project/
├── Canteen_Management_System/          # Django Backend
│   └── backend/
│       ├── canteen_cms/               # Main Django project
│       ├── users/                     # User authentication
│       ├── menu/                      # Menu management
│       ├── cart/                      # Shopping cart
│       ├── orders/                    # Order processing
│       └── core/                      # Core functionality
└── cms_admin_pannel_-_frontend/       # React Frontends
    ├── frontend/                      # Customer React App (Mobile-Responsive)
    └── admin/                         # Admin Panel React App
```

## 🚀 Quick Start

### Backend Setup (Django)

1. **Navigate to backend directory:**
   ```bash
   cd Canteen_Management_System/backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start Django server:**
   ```bash
   python manage.py runserver
   ```
   Backend will run on: `http://localhost:8000`

### Frontend Setup (Customer App)

1. **Navigate to frontend directory:**
   ```bash
   cd cms_admin_pannel_-_frontend/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   Customer app will run on: `http://localhost:3000`

### Admin Panel Setup

1. **Navigate to admin directory:**
   ```bash
   cd cms_admin_pannel_-_frontend/admin
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   Admin panel will run on: `http://localhost:3001`

## 🌐 Deployment Options

### Option 1: Vercel + Railway (Recommended)

#### Backend (Railway):
1. Connect your GitHub repo to Railway
2. Deploy the `Canteen_Management_System/backend` folder
3. Add environment variables in Railway dashboard
4. Railway will auto-deploy on git push

#### Frontend (Vercel):
1. Connect GitHub repo to Vercel
2. Set build settings:
   - **Customer App**: Root directory: `cms_admin_pannel_-_frontend/frontend`
   - **Admin Panel**: Root directory: `cms_admin_pannel_-_frontend/admin`
3. Update API endpoints in React apps to Railway backend URL

### Option 2: Heroku

#### Backend:
```bash
# In backend directory
heroku create your-canteen-backend
git subtree push --prefix=Canteen_Management_System/backend heroku main
```

#### Frontend:
```bash
# Deploy each frontend separately
heroku create your-canteen-frontend
heroku create your-canteen-admin
```

### Option 3: DigitalOcean/AWS

1. **Backend**: Deploy Django on DigitalOcean App Platform or AWS Elastic Beanstalk
2. **Frontend**: Deploy React apps on DigitalOcean Static Sites or AWS S3 + CloudFront
3. **Database**: Use managed PostgreSQL service

## 🔧 Environment Configuration

### Backend (.env):
```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com,localhost
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend:
Update API base URL in both React apps:
```javascript
const API_BASE = 'https://your-backend-domain.com';
```

## 📱 Features

### Customer App (Mobile-Responsive):
- ✅ User registration & authentication
- ✅ Browse menu by categories
- ✅ Add/remove items from cart
- ✅ Place orders
- ✅ View order history
- ✅ User profile management
- ✅ Perfect mobile responsiveness

### Admin Panel:
- ✅ Menu item management (CRUD)
- ✅ Order management
- ✅ User management
- ✅ Dashboard analytics
- ✅ Category management

### Backend API:
- ✅ JWT Authentication
- ✅ RESTful API endpoints
- ✅ File upload for menu images
- ✅ Order processing
- ✅ Cart management

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework, SQLite/PostgreSQL
- **Frontend**: React, React Router, Axios
- **Authentication**: JWT tokens
- **Styling**: CSS3, Mobile-first responsive design
- **Deployment**: Vercel, Railway, Heroku compatible

## 📞 API Endpoints

```
POST /api/users/register/          # User registration
POST /api/users/login/             # User login
GET  /api/menu/                    # Get menu items
POST /api/cart/add/                # Add to cart
GET  /api/cart/                    # Get cart items
POST /api/orders/                  # Place order
GET  /api/orders/                  # Get user orders
```

## 🚀 Production Deployment Checklist

- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure production database (PostgreSQL)
- [ ] Set up static file serving (WhiteNoise/CloudFront)
- [ ] Configure CORS for frontend domains
- [ ] Set up SSL certificates
- [ ] Configure environment variables
- [ ] Test all API endpoints
- [ ] Test mobile responsiveness

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Developer

Created by [Nirmal Sai](https://github.com/nirmalsai021)

---

**Ready for deployment! 🚀**