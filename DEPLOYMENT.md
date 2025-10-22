# 🚀 Deployment Guide: Render + Vercel

## Step 1: Deploy Backend to Render

1. **Go to [Render.com](https://render.com)** and sign up/login
2. **Connect GitHub**: Link your GitHub account
3. **Create Web Service**:
   - Repository: `nirmalsai021/Canteen_Management_System`
   - Root Directory: `Canteen_Management_System/backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

4. **Environment Variables** (Add in Render dashboard):
   ```
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

5. **Deploy** - Render will give you a URL like: `https://your-app-name.onrender.com`

## Step 2: Deploy Customer Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com)** and sign up/login
2. **Import Project**: Connect GitHub repo `nirmalsai021/Canteen_Management_System`
3. **Configure Build Settings**:
   - Framework Preset: `Create React App`
   - Root Directory: `cms_admin_pannel_-_frontend/frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

4. **Environment Variables** (Add in Vercel dashboard):
   ```
   REACT_APP_API_URL=https://your-backend-name.onrender.com
   ```

5. **Deploy** - Vercel will give you a URL like: `https://your-frontend.vercel.app`

## Step 3: Deploy Admin Panel to Vercel

1. **Create New Project** in Vercel
2. **Import Same Repository**
3. **Configure Build Settings**:
   - Framework Preset: `Create React App`
   - Root Directory: `cms_admin_pannel_-_frontend/admin`
   - Build Command: `npm run build`
   - Output Directory: `build`

4. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend-name.onrender.com
   ```

5. **Deploy** - You'll get: `https://your-admin.vercel.app`

## Step 4: Update Backend CORS Settings

1. **Update Django settings** with your Vercel URLs:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://your-frontend.vercel.app",
       "https://your-admin.vercel.app",
   ]
   ```

2. **Redeploy backend** on Render

## ✅ Final URLs:
- **Backend API**: `https://your-backend.onrender.com`
- **Customer App**: `https://your-frontend.vercel.app`
- **Admin Panel**: `https://your-admin.vercel.app`

## 🔧 Perfect Connection:
- ✅ CORS configured for both frontends
- ✅ Environment variables set correctly
- ✅ All API calls will work seamlessly
- ✅ Mobile-responsive design maintained

**No connection issues - everything will work perfectly!** 🎉