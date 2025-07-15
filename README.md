# 🛍️ PyShopper – Full-Stack E-Commerce App

PyShopper is a lightweight, full-stack e-commerce platform built with **React** (frontend) and **Flask** (backend). It allows users to browse a product catalog, manage cart/wishlist, checkout with receipt generation, and view past orders.

### 🚀 Live Demo

🌐 Frontend: [https://pyshopper.vercel.app](https://pyshopper.vercel.app)  
🔧 Backend: [https://pyshopper.onrender.com](https://pyshopper.onrender.com)

---

## 🧠 Features

- ✅ User Registration & Login (User/Admin)
- 🛍️ Browse product catalog
- 🛒 Add/remove items from cart
- 💖 Wishlist system with move-to-cart
- ✍️ Manual item add form (for custom items)
- 📦 Checkout with receipt generation & download
- 📜 Order history page
- 🧑 Admin mode (customizable)
- 🔐 Session persistence using `localStorage`

---

## 🛠️ Tech Stack

| Layer       | Technology                 |
|-------------|----------------------------|
| Frontend    | React, React Bootstrap     |
| Backend     | Flask, Flask-CORS          |
| Hosting     | Vercel (Frontend), Render (Backend) |
| Styling     | Bootstrap 5                |
| State Mgmt  | React Hooks & Context      |
| Data Store  | In-memory (for demo)       |

---

## 🏗️ Folder Structure

---
frontend/
├── public/
├── src/
│ ├── api.js # Centralized Axios instance
│ ├── Login.js
│ ├── Dashboard.js
│ ├── Cart.js
│ ├── Wishlist.js
│ ├── ManualAdd.js
│ ├── Checkout.js
│ ├── OrderHistory.js
│ └── ...
└── .env

## 📦 Backend API Endpoints

Some sample endpoints from the Flask backend:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/login` | POST | User login |
| `/register` | POST | Register new user |
| `/catalog` | GET | Fetch all items |
| `/add-to-cart` | POST | Add item to cart |
| `/wishlist/add` | POST | Add item to wishlist |
| `/cart/checkout` | POST | Checkout and get receipt |
| `/orders/<email>` | GET | Get past orders |

> Full API hosted at: `https://pyshopper.onrender.com`

---

## 🧪 Run Locally (Dev Setup)

### Frontend:

```bash
cd frontend
npm install
npm start


