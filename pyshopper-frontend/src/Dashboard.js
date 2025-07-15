import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import Catalog from './Catalog1';
import Cart from './Cart';
import Wishlist from './Wishlist';
import ManualAdd from './ManualAdd';

import {
  fetchCatalog,
  fetchUserCart,
  fetchUserWishlist
} from './api';

function Dashboard() {
  const navigate = useNavigate();
  const email = localStorage.getItem('email');
  const role = localStorage.getItem('role');
  const name = localStorage.getItem('name');

  const [catalog, setCatalog] = useState([]);
  const [cart, setCart] = useState([]);
  const [wishlist, setWishlist] = useState([]);

  useEffect(() => {
    if (!email || !role) {
      navigate('/');
    }
  }, [email, role, navigate]);

 const fetchCatalogData = useCallback(async () => {
  try {
    const res = await fetchCatalog();
    setCatalog(res.data);
  } catch {
    alert('❌ Error fetching catalog');
  }
}, []);


  const fetchCartData = useCallback(async () => {
  try {
    const res = await fetchUserCart(email);
    setCart(res.data.cart || []);
  } catch {
    alert('❌ Error fetching cart');
  }
}, [email]);

const fetchWishlistData = useCallback(async () => {
  try {
    const res = await fetchUserWishlist(email);
    setWishlist(res.data.wishlist || []);
  } catch {
    alert('❌ Error fetching wishlist');
  }
}, [email]);

  useEffect(() => {
    fetchCatalogData();
  fetchCartData();
  fetchWishlistData();

  }, [fetchCatalog, fetchCartData, fetchWishlistData]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  return (
    <Container className="py-4">
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>👋 Welcome {role === 'admin' ? `Admin ${name}` : name || 'User'}</Card.Title>
          <Card.Text>
            <strong>Email:</strong> {email}
          </Card.Text>
          <Button variant="danger" onClick={handleLogout}>🚪 Logout</Button>
        </Card.Body>
      </Card>

      <Row className="mb-4">
        <Col>
          <Catalog
            email={email}
            catalog={catalog}
            refreshCart={fetchCartData}
            refreshWishlist={fetchWishlistData}
          />
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <Cart
            email={email}
            cart={cart}
            refreshCart={fetchCartData}
          />
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <Wishlist
            email={email}
            wishlist={wishlist}
            refreshCart={fetchCartData}
            refreshWishlist={fetchWishlistData}
          />
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <ManualAdd
            email={email}
            refreshCart={fetchCartData}
          />
        </Col>
      </Row>

      <Row>
        <Col>
          <Button
            variant="outline-dark"
            className="w-100"
            onClick={() => navigate('/orders')}
          >
            📜 View Order History
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;
