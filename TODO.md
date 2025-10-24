# TODO: Fix Authentication and Deploy Backend

## 1. Fix Admin Authentication
- [x] Update simple_admin_auth.py to use real Django Token authentication instead of fake token
- [x] Ensure admin login endpoints return valid tokens that work with TokenAuthentication

## 2. Prepare for Production Deployment
- [x] Verify render.yaml configuration for Render deployment
- [x] Update settings.py for production (DEBUG=False, ALLOWED_HOSTS)
- [x] Ensure CORS allows mobile and web app origins

## 3. Test and Deploy
- [x] Test admin login and menu endpoints locally
- [x] Deploy to Render
- [x] Verify backend works from mobile/web apps

## 4. Final Verification
- [x] Confirm 401 errors are fixed
- [x] Ensure data storage is in cloud (Render)
- [x] Test accessibility from different devices

## 5. Data Management
- [x] Clear all stored data (items, orders, images, cart)
- [x] Start fresh with new menu items (burger, whooper, gulab jamun, maggie, mango)
- [x] Verify new menu items are accessible via API

## 6. Frontend API Refactoring
- [x] Remove hardcoded API_BASE URLs from frontend components
- [x] Use api.js for all API calls to leverage baseURL and interceptors
- [x] Update Menu.jsx, Profile.jsx, App.jsx to use relative URLs
- [x] Ensure image URLs use process.env.REACT_APP_API_URL for fallback
