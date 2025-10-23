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
- [ ] Deploy to Render
- [ ] Verify backend works from mobile/web apps

## 4. Final Verification
- [x] Confirm 401 errors are fixed
- [ ] Ensure data storage is in cloud (Render)
- [ ] Test accessibility from different devices
