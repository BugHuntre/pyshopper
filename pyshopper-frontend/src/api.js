import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
});

// 🔐 AUTH APIs
export const loginUser = (email, password, role = 'user') => {
  const endpoint = role === 'admin' ? '/admin/login' : '/login';
  return API.post(endpoint, { email, password });
};

export const registerUser = (name, email, password) => {
  return API.post('/register', { name, email, password });
};

// (keep other API exports like fetchCart, addToCart etc. here)
export const removeItemFromCart = (email, itemName) =>
  API.post('/cart/remove-item', {
    email,
    item_name: itemName,
  });

export const checkoutCart = (email) =>
  API.post('/cart/checkout', { email });

export const getReceiptDownloadUrl = (fileName) =>
  `${process.env.REACT_APP_API_BASE_URL}/receipts/${fileName}`;

export const fetchCatalog = () =>
  API.get('/catalog');

export const fetchUserCart = (email) =>
  API.get(`/cart/${email}`);

export const fetchUserWishlist = (email) =>
  API.get(`/wishlist/${email}`);

export const addItemToCart = (email, item) =>
  API.post('/add-to-cart', {
    email,
    item: { ...item, quantity: item.quantity || 1 },
  });

export const addItemToWishlist = (email, item) =>
  API.post('/wishlist/add', {
    email,
    item: { ...item, quantity: item.quantity || 1 },
  });
export const addManualItemToCart = (email, item) =>
  API.post('/add-to-cart', {
    email,
    item,
  });
export const fetchOrderHistory = (email) =>
  API.get(`/orders/${email}`);
export const moveWishlistItemToCart = (email, itemName) =>
  API.post('/wishlist/move-to-cart', { email, item_name: itemName });

export const removeItemFromWishlist = (email, itemName) =>
  API.post('/wishlist/remove', { email, item_name: itemName });
