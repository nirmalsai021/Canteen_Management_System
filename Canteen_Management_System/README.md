# CMS API Documentation

## Base URL
`http://127.0.0.1:8000` or `http://localhost:8000`

---

## 🔐 Authentication APIs

### 1. Customer Registration
**Purpose**: Register a new customer account

- **Method**: `POST`
- **Endpoint**: `/api/users/register/`
- **Authentication**: Not required
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "username": "student123",           // Required, unique
    "email": "student@example.com",     // Required, valid email
    "password": "securepassword123",    // Required, min 8 characters
    "password_confirm": "securepassword123", // Required, must match password
    "first_name": "John",               // Required
    "last_name": "Doe"                  // Required
}
```

**Success Response** (201):
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "student123",
        "email": "student@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

---

### 2. Customer Login
**Purpose**: Login customer and get authentication tokens

- **Method**: `POST`
- **Endpoint**: `/api/users/login/`
- **Authentication**: Not required
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "username": "student123",           // Required
    "password": "securepassword123"     // Required
}
```

**Success Response** (200):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "student123",
        "email": "student@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_staff": false
    },
    "user_type": "customer",
    "profile": {
        "id": 1,
        "phone": null,
        "roll_number": null,
        "address": null,
        "gender": null,
        "date_of_birth": null
    }
}
```

---

### 3. Admin Login
**Purpose**: Login admin user and get authentication tokens

- **Method**: `POST`
- **Endpoint**: `/api/users/admin/login/`
- **Authentication**: Not required
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "username": "admin123",             // Required
    "password": "adminpassword123"      // Required
}
```

**Success Response** (200):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 2,
        "username": "admin123",
        "email": "admin@canteen.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "is_staff": true
    },
    "user_type": "admin",
    "profile": {
        "id": 2,
        "phone": null,
        "employee_id": null,
        "department": null,
        "position": null
    }
}
```

---

### 4. Logout
**Purpose**: Logout user and invalidate tokens

- **Method**: `POST`
- **Endpoint**: `/api/users/logout/`
- **Authentication**: Required (Bearer Token)
- **Content-Type**: `application/json`
- **Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
    "refresh": "<refresh_token>"        // Required
}
```

**Success Response** (200):
```json
{
    "message": "Successfully logged out"
}
```

---

### 5. Token Refresh
**Purpose**: Get new access token using refresh token

- **Method**: `POST`
- **Endpoint**: `/api/token/refresh/`
- **Authentication**: Not required
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "refresh": "<refresh_token>"        // Required
}
```

**Success Response** (200):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 👤 Profile Management APIs

### 6. Get Current User Profile Info
**Purpose**: Get current logged-in user's basic information

- **Method**: `GET`
- **Endpoint**: `/api/users/profile/info/`
- **Authentication**: Required (Bearer Token)
- **Headers**: `Authorization: Bearer <access_token>`

**Success Response** (200):
```json
{
    "id": 1,
    "username": "student123",
    "email": "student@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "customer",
    "is_staff": false,
    "date_joined": "2025-06-28T10:30:00Z"
}
```

---

### 7. Get Customer Profile
**Purpose**: Get detailed customer profile information

- **Method**: `GET`
- **Endpoint**: `/api/users/profile/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

**Success Response** (200):
```json
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "student123",
        "first_name": "John",
        "last_name": "Doe",
        "email": "student@example.com"
    },
    "phone": "+91-9876543210",
    "roll_number": "CS2021001",
    "address": "Hostel Block A, Room 205",
    "gender": "M",
    "date_of_birth": "2000-05-15",
    "profile_image": null,
    "created_at": "2025-06-28T10:30:00Z",
    "updated_at": "2025-06-28T10:30:00Z"
}
```

---

### 8. Update Customer Profile
**Purpose**: Update customer profile information

- **Method**: `PUT` or `PATCH`
- **Endpoint**: `/api/users/profile/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "phone": "+91-9876543210",          // Optional
    "roll_number": "CS2021001",         // Optional
    "address": "Hostel Block A, Room 205", // Optional
    "gender": "M",                      // Optional (M/F/O)
    "date_of_birth": "2000-05-15",      // Optional (YYYY-MM-DD)
    "first_name": "John",               // Optional
    "last_name": "Doe",                 // Optional
    "email": "john.doe@example.com"     // Optional
}
```

---

### 9. Get Admin Profile
**Purpose**: Get detailed admin profile information

- **Method**: `GET`
- **Endpoint**: `/api/users/admin/profile/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`

---

### 10. Update Admin Profile
**Purpose**: Update admin profile information

- **Method**: `PUT` or `PATCH`
- **Endpoint**: `/api/users/admin/profile/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "phone": "+91-9876543210",          // Optional
    "employee_id": "EMP001",            // Optional
    "department": "KITCHEN",            // Optional
    "position": "Head Chef",            // Optional
    "first_name": "Jane",               // Optional
    "last_name": "Smith",               // Optional
    "email": "jane.smith@canteen.com"   // Optional
}
```

---

## 🍽️ Menu APIs (Customer View)

### 11. Get All Available Menu Items
**Purpose**: Get all available menu items for customers

- **Method**: `GET`
- **Endpoint**: `/api/menu/customer/`
- **Authentication**: Not required
- **Query Parameters**:
  - `category` (optional): Filter by category
  - `available` (optional): Filter by availability (true/false)

**Success Response** (200):
```json
[
    {
        "id": 1,
        "name": "Orange Juice",
        "description": "Fresh orange juice",
        "price": "25.00",
        "available": true,
        "category": "juices",
        "created_at": "2025-06-28T10:30:00Z"
    }
]
```

---

### 12. Search Menu Items
**Purpose**: Search menu items with filters

- **Method**: `GET`
- **Endpoint**: `/api/menu/customer/search/`
- **Authentication**: Not required
- **Query Parameters**:
  - `q` (optional): Search query
  - `category` (optional): Filter by category
  - `min_price` (optional): Minimum price filter
  - `max_price` (optional): Maximum price filter

---

### 13. Get Menu Categories
**Purpose**: Get all available menu categories

- **Method**: `GET`
- **Endpoint**: `/api/menu/customer/categories/`
- **Authentication**: Not required

**Success Response** (200):
```json
[
    {
        "category": "juices",
        "count": 5
    },
    {
        "category": "snacks",
        "count": 8
    }
]
```

---

### 14. Get Specific Menu Item
**Purpose**: Get details of a specific menu item

- **Method**: `GET`
- **Endpoint**: `/api/menu/customer/{menu_item_id}/`
- **Authentication**: Not required

---

## 🛒 Cart Management APIs

### 15. View Cart
**Purpose**: Get current user's cart items

- **Method**: `GET`
- **Endpoint**: `/api/cart/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

**Success Response** (200):
```json
{
    "cart_items": [
        {
            "id": 1,
            "menu_item": 1,
            "menu_item_name": "Orange Juice",
            "menu_item_price": "25.00",
            "menu_item_category": "juices",
            "quantity": 2,
            "total_price": "50.00",
            "added_at": "2025-06-30T10:30:00Z"
        }
    ],
    "total_amount": "50.00",
    "total_items": 2
}
```

---

### 16. Add Item to Cart
**Purpose**: Add menu item to cart

- **Method**: `POST`
- **Endpoint**: `/api/cart/add/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "menu_item_id": 1,                  // Required
    "quantity": 2                       // Required, positive integer
}
```

**Success Response** (201):
```json
{
    "message": "Added Orange Juice to cart",
    "cart_item": {
        "id": 1,
        "menu_item": 1,
        "menu_item_name": "Orange Juice",
        "menu_item_price": "25.00",
        "quantity": 2,
        "total_price": "50.00",
        "added_at": "2025-06-30T10:30:00Z"
    }
}
```

---

### 17. Update Cart Item Quantity
**Purpose**: Update quantity of item in cart

- **Method**: `PUT`
- **Endpoint**: `/api/cart/items/{cart_item_id}/update/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "quantity": 3                       // Required, positive integer
}
```

---

### 18. Remove Item from Cart
**Purpose**: Remove specific item from cart

- **Method**: `DELETE`
- **Endpoint**: `/api/cart/items/{cart_item_id}/remove/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

**Success Response** (200):
```json
{
    "message": "Item removed from cart"
}
```

---

### 19. Get Cart Summary
**Purpose**: Get cart total and item count

- **Method**: `GET`
- **Endpoint**: `/api/cart/summary/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

**Success Response** (200):
```json
{
    "total_amount": "125.00",
    "total_items": 5,
    "item_count": 3
}
```

---

### 20. Clear Cart
**Purpose**: Remove all items from cart

- **Method**: `DELETE`
- **Endpoint**: `/api/cart/clear/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

**Success Response** (200):
```json
{
    "message": "Cart cleared successfully"
}
```

---

## 📋 Order Management APIs (Customer)

### 21. Place Order from Cart
**Purpose**: Convert cart items to order

- **Method**: `POST`
- **Endpoint**: `/api/orders/place/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "notes": "Please make it less spicy"    // Optional
}
```

**Success Response** (201):
```json
{
    "message": "Order placed successfully",
    "order": {
        "id": 1,
        "user": 1,
        "user_username": "student123",
        "status": "PLACED",
        "total_amount": "125.00",
        "total_items": 5,
        "notes": "Please make it less spicy",
        "created_at": "2025-06-30T10:35:00Z",
        "items": [
            {
                "id": 1,
                "menu_item_name": "Orange Juice",
                "menu_item_price": "25.00",
                "quantity": 2,
                "total_price": "50.00"
            }
        ]
    }
}
```

---

### 22. View Customer Orders
**Purpose**: Get all orders for current customer

- **Method**: `GET`
- **Endpoint**: `/api/orders/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`
- **Query Parameters**:
  - `status` (optional): Filter by order status
  - `page` (optional): Page number for pagination

**Success Response** (200):
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/orders/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "status": "PLACED",
            "total_amount": "125.00",
            "total_items": 5,
            "notes": "Please make it less spicy",
            "created_at": "2025-06-30T10:35:00Z",
            "updated_at": "2025-06-30T10:35:00Z"
        }
    ]
}
```

---

### 23. Get Specific Order Details
**Purpose**: Get detailed information about specific order

- **Method**: `GET`
- **Endpoint**: `/api/orders/{order_id}/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

---

### 24. Cancel Order
**Purpose**: Cancel a placed order (if allowed)

- **Method**: `POST`
- **Endpoint**: `/api/orders/{order_id}/cancel/`
- **Authentication**: Required (Customer Token)
- **Headers**: `Authorization: Bearer <customer_access_token>`

**Success Response** (200):
```json
{
    "message": "Order cancelled successfully",
    "order": {
        "id": 1,
        "status": "CANCELLED",
        "total_amount": "125.00"
    }
}
```

---

## 🛠️ Admin APIs

### 25. List All Menu Items (Admin)
**Purpose**: Get all menu items for admin management

- **Method**: `GET`
- **Endpoint**: `/api/menu/admin/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`

---

### 26. Create New Menu Item (Admin)
**Purpose**: Add new menu item to system

- **Method**: `POST`
- **Endpoint**: `/api/menu/admin/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "name": "Masala Dosa",              // Required
    "description": "Crispy dosa with spicy potato filling", // Optional
    "price": 45.00,                     // Required
    "available": true,                  // Required
    "category": "snacks"                // Required
}
```

---

### 27. Update Menu Item (Admin)
**Purpose**: Update existing menu item

- **Method**: `PUT`
- **Endpoint**: `/api/menu/admin/{menu_item_id}/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Content-Type**: `application/json`

---

### 28. Delete Menu Item (Admin)
**Purpose**: Remove menu item from system

- **Method**: `DELETE`
- **Endpoint**: `/api/menu/admin/{menu_item_id}/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`

---

### 29. View All Orders (Admin)
**Purpose**: Get all orders in the system

- **Method**: `GET`
- **Endpoint**: `/api/orders/admin/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Query Parameters**:
  - `status` (optional): Filter by order status
  - `search` (optional): Search by customer username
  - `page` (optional): Page number

---

### 30. Update Order Status (Admin)
**Purpose**: Change order status

- **Method**: `PATCH`
- **Endpoint**: `/api/orders/admin/{order_id}/update-status/`
- **Authentication**: Required (Admin Token)
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Content-Type**: `application/json`

**Request Body**:
```json
{
    "status": "PREPARING"               // Required
}
```

**Valid Status Values**:
- `PLACED`
- `CONFIRMED`
- `PREPARING`
- `READY`
- `DELIVERED`
- `CANCELLED`

---

## ⚠️ Error Responses

### Common Error Status Codes:
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format:
```json
{
    "error": "Error message description"
}
```

### Validation Error Format:
```json
{
    "field_name": ["Error message for this field"],
    "another_field": ["Another error message"]
}
```

---

## 📝 Notes for Frontend Integration

1. **Authentication**: Save `access` and `refresh` tokens from login response
2. **Token Refresh**: Implement automatic token refresh when API returns 401
3. **User Type**: Check `user_type` from login response to determine user permissions
4. **Pagination**: Many list APIs support pagination with `page` parameter
5. **Search & Filters**: Use query parameters for filtering and searching
6. **Error Handling**: Always handle error responses appropriately
7. **Cart Management**: Cart is user-specific and requires authentication
8. **Order Status**: Track order status changes for real-time updates


<!-- happy coading -->