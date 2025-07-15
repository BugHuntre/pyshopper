import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import Catalog from './Catalog1';
import Cart from './Cart';
import Wishlist from './Wishlist';
import ManualAdd from './ManualAdd';

const BASE_URL = 'http://127.0.0.1:5000';

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

  const fetchCatalog = useCallback(async () => {
    try {
      const res = await axios.get(`${BASE_URL}/catalog`);
      setCatalog(res.data);
    } catch {
      alert('❌ Error fetching catalog');
    }
  }, []);

  const fetchCart = useCallback(async () => {
    try {
      const res = await axios.get(`${BASE_URL}/cart/${email}`);
      setCart(res.data.cart || []);
    } catch {
      alert('❌ Error fetching cart');
    }
  }, [email]);

  const fetchWishlist = useCallback(async () => {
    try {
      const res = await axios.get(`${BASE_URL}/wishlist/${email}`);
      setWishlist(res.data.wishlist || []);
    } catch {
      alert('❌ Error fetching wishlist');
    }
  }, [email]);

  useEffect(() => {
    fetchCatalog();
    fetchCart();
    fetchWishlist();
  }, [fetchCatalog, fetchCart, fetchWishlist]);

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
            refreshCart={fetchCart}
            refreshWishlist={fetchWishlist}
          />
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <Cart
            email={email}
            cart={cart}
            refreshCart={fetchCart}
          />
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <Wishlist
            email={email}
            wishlist={wishlist}
            refreshCart={fetchCart}
            refreshWishlist={fetchWishlist}
          />
        </Col>
      </Row>

      <Row className="mb-4">
        <Col>
          <ManualAdd
            email={email}
            refreshCart={fetchCart}
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
