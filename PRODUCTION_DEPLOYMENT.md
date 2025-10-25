# Production Deployment Guide

## Media Files Issue Fix

The 404 error for images occurs because media files uploaded locally don't exist on the production server (Render). Here's how to fix it:

### 1. Backend Deployment (Render)

```bash
# In your Render deployment, add these commands to your build script:
python production_setup.py
python manage.py collectstatic --noinput
```

### 2. Environment Variables (Render Dashboard)

Add these environment variables in Render:
```
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
```

### 3. Media Files Solution

**Option A: Re-upload Images via Admin Panel**
1. Login to admin panel on production
2. Re-upload all menu item images
3. Images will be stored on Render's filesystem

**Option B: Use Cloud Storage (Recommended)**
1. Set up Cloudinary or AWS S3
2. Update Django settings to use cloud storage
3. Images persist across deployments

### 4. Quick Fix for Testing

The system now includes:
- ✅ Placeholder images for missing files
- ✅ Proper error handling in frontend
- ✅ Automatic media directory creation
- ✅ Test menu items with images

### 5. Deployment Commands

```bash
# Backend
cd Canteen_Management_System/backend
python production_setup.py
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver

# Frontend (Customer)
cd cms_admin_pannel_-_frontend/frontend
npm install
npm run build
npm start

# Admin Panel
cd cms_admin_pannel_-_frontend/admin
npm install
npm run build
npm start
```

### 6. Verification Steps

1. ✅ Backend serves placeholder images
2. ✅ Admin can upload new images
3. ✅ Frontend displays images or placeholders
4. ✅ Edit functionality works
5. ✅ Cart and orders work properly

### 7. Production URLs

- Backend API: `https://your-app.onrender.com`
- Media Files: `https://your-app.onrender.com/media/menu_images/`
- Admin Panel: Deploy separately on Vercel
- Customer App: Deploy separately on Vercel

The system is now production-ready with proper image handling!