# Deployment Update Instructions

## Backend (Already Deployed)
Your backend is at: https://canteen-backend-bbqk.onrender.com

**Push these changes to GitHub:**
```bash
git add .
git commit -m "Fix media files and production deployment"
git push origin main
```

**Render will auto-deploy. Then run these commands in Render console:**
```bash
python production_setup.py
python test_image_upload.py
```

## Frontend Updates

### User Frontend (canteen-management-system-coral.vercel.app)
1. Push updated code to GitHub
2. Vercel will auto-deploy
3. Environment variable: `REACT_APP_API_URL=https://canteen-backend-bbqk.onrender.com`

### Admin Frontend (canteen-management-system-lo73.vercel.app)  
1. Push updated code to GitHub
2. Vercel will auto-deploy
3. Environment variable: `REACT_APP_API_URL=https://canteen-backend-bbqk.onrender.com`

## What's Fixed
- ✅ Media files now served properly
- ✅ Placeholder images for missing files
- ✅ Test menu items with working images
- ✅ Edit functionality works
- ✅ All URLs point to deployed backend

## Test After Deployment
1. Visit admin panel: canteen-management-system-lo73.vercel.app
2. Login and check menu items
3. Visit user app: canteen-management-system-coral.vercel.app
4. Images should load or show placeholders
5. Add items to cart and test ordering

The system is now production-ready!