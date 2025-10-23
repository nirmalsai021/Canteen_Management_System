# TODO: Fix 404 Errors by Making API RESTful

## Backend Changes
- [x] Update `Canteen_Management_System/backend/menu/urls.py` to add RESTful detail endpoint `path('<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-detail')`

## Frontend Changes
- [x] Update `cms_admin_pannel_-_frontend/admin/src/components/ListItems/ListItems.jsx` to change update fetch URL from `/api/menu/${itemId}/update/` to `/api/menu/${itemId}/` (keep PUT method)

## Testing
- [x] Run backend server and frontend admin panel
- [x] Verify update and delete operations work without 404 errors
- [x] Ensure no conflicts with existing endpoints
- [x] Push changes to GitHub
