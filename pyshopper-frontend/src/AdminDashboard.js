import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card, Button, Form, Spinner, Alert, ListGroup } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const BASE_URL = 'http://127.0.0.1:5000';

function AdminDashboard() {
  const navigate = useNavigate();
  const email = localStorage.getItem('email');
  const password = localStorage.getItem('password');
  const role = localStorage.getItem('role');
  

  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [userCart, setUserCart] = useState([]);
  const [userOrders, setUserOrders] = useState([]);
  const [catalog, setCatalog] = useState([]);
  const [newItem, setNewItem] = useState({ name: '', price: 0, quantity: 1 });
  const [loading, setLoading] = useState(false);
// eslint-disable-next-line react-hooks/exhaustive-deps
useEffect(() => {
  if (!email || role !== 'admin') {
    navigate('/');
  } else {
    fetchAllUsers();
    fetchCatalog();
  }
}, [email, role, navigate]);


  const fetchAllUsers = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${BASE_URL}/admin/users/`, { email, password });
      setUsers(res.data.users);
    } catch {
      alert('❌ Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const fetchCatalog = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${BASE_URL}/catalog`);
      setCatalog(res.data);
    } catch {
      alert('❌ Failed to load catalog');
    } finally {
      setLoading(false);
    }
  };

  const fetchUserDetails = async (userEmail) => {
    setSelectedUser(userEmail);
    setLoading(true);
    try {
      const res = await axios.get(`${BASE_URL}/admin/users/${userEmail}`);
      setUserCart(res.data.cart);
      setUserOrders(res.data.orders);
    } catch {
      alert('❌ Failed to fetch user details');
    } finally {
      setLoading(false);
    }
  };

  const handleAddCatalogItem = async () => {
    try {
      await axios.post(`${BASE_URL}/admin/catalog/add`, {
        email,
        password,
        item: newItem,
      });
      setNewItem({ name: '', price: 0, quantity: 1 });
      fetchCatalog();
    } catch (e) {
      alert(e.response?.data?.error || '❌ Failed to add item');
    }
  };

  const handleDeleteItem = async (itemName) => {
    try {
      await axios.post(`${BASE_URL}/admin/catalog/delete`, {
        email,
        password,
        item_name: itemName,
      });
      fetchCatalog();
    } catch {
      alert('❌ Failed to delete item');
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  return (
    
    <Container className="py-4">
      <Row className="mb-3">
        <Col>
          <h2>👑 Admin Dashboard</h2>
          <p><strong>Email:</strong> {email}</p>
          <Button variant="danger" onClick={handleLogout}>Logout</Button>
        </Col>
      </Row>

      <Row>
        <Col md={4}>
          <h4>👥 Users</h4>
          {loading ? <Spinner animation="border" /> : (
            users.length ? users.map((u, i) => (
              <Button
                key={i}
                variant="outline-primary"
                className="w-100 mb-2"
                onClick={() => fetchUserDetails(u.email)}
              >
                {u.name} ({u.email})
              </Button>
            )) : <Alert variant="info">No users found</Alert>
          )}
        </Col>

        <Col md={8}>
          {selectedUser && (
            <>
              <Card className="mb-3">
                <Card.Header>🛒 Cart of {selectedUser}</Card.Header>
                <Card.Body>
                  {userCart.length ? (
                    <ListGroup>
                      {userCart.map((item, idx) => (
                        <ListGroup.Item key={idx}>
                          {item.name} - ₹{item.price} × {item.quantity}
                        </ListGroup.Item>
                      ))}
                    </ListGroup>
                  ) : <Alert variant="secondary">Cart is empty</Alert>}
                </Card.Body>
              </Card>

              <Card className="mb-3">
                <Card.Header>🧾 Orders of {selectedUser}</Card.Header>
                <Card.Body>
                  {userOrders.length ? userOrders.map((o, idx) => (
                    <Card key={idx} className="mb-2">
                      <Card.Body>
                        <strong>Order {idx + 1}</strong>
                        <ul>
                          {o.items.map((item, i) => (
                            <li key={i}>{item.name} - ₹{item.price} × {item.quantity}</li>
                          ))}
                        </ul>
                      </Card.Body>
                    </Card>
                  )) : <Alert variant="secondary">No orders found</Alert>}
                </Card.Body>
              </Card>
            </>
          )}
        </Col>
      </Row>

      <hr />
      <Row>
        <Col md={6}>
          <h4>📦 Catalog</h4>
          {catalog.length ? catalog.map((item, idx) => (
            <Card key={idx} className="mb-2">
              <Card.Body className="d-flex justify-content-between">
                <span>{item.name} — ₹{item.price} × {item.quantity}</span>
                <Button variant="outline-danger" size="sm" onClick={() => handleDeleteItem(item.name)}>Delete</Button>
              </Card.Body>
            </Card>
          )) : <Alert variant="info">Catalog is empty</Alert>}
        </Col>

        <Col md={6}>
          <h4>➕ Add Item</h4>
          <Form>
            <Form.Control
              className="mb-2"
              placeholder="Item name"
              value={newItem.name}
              onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
            />
            <Form.Control
              type="number"
              className="mb-2"
              placeholder="Price"
              value={newItem.price}
              onChange={(e) => setNewItem({ ...newItem, price: parseFloat(e.target.value || 0) })}
            />
            <Form.Control
              type="number"
              className="mb-2"
              placeholder="Quantity"
              value={newItem.quantity}
              onChange={(e) => setNewItem({ ...newItem, quantity: parseInt(e.target.value || 1) })}
            />
            <Button variant="success" onClick={handleAddCatalogItem}>Add to Catalog</Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default AdminDashboard;
