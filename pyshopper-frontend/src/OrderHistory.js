import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Spinner, Alert, Card, Button } from 'react-bootstrap';

const BASE_URL = 'http://127.0.0.1:5000';

function OrderHistory() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const email = localStorage.getItem('email');

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await axios.get(`${BASE_URL}/orders/${email}`);
        setOrders(res.data.orders || []);
      } catch (err) {
        console.error('Failed to fetch orders:', err);
        alert('Failed to load order history.');
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [email]);

  return (
    <Container className="py-4">
      <h3 className="mb-4">📦 Your Past Orders</h3>

      {loading ? (
        <div className="text-center mt-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-2">Loading orders...</p>
        </div>
      ) : orders.length === 0 ? (
        <Alert variant="info">No past orders found.</Alert>
      ) : (
        orders.map((order) => (
          <Card className="mb-3" key={order.id}>
            <Card.Header>
              <strong>🧾 Order #{order.id}</strong> <span className="text-muted float-end">📅 {order.timestamp}</span>
            </Card.Header>
            <Card.Body>
              <ul className="mb-3">
                {order.items.map((item, idx) => (
                  <li key={idx}>
                    {item.name} — ₹{item.price} × {item.quantity}
                  </li>
                ))}
              </ul>
              <p><strong>Total:</strong> ₹{order.total}</p>
              <Button
                variant="outline-primary"
                size="sm"
                onClick={() => window.open(`${BASE_URL}/receipts/${order.receipt_file}`, '_blank')}
              >
                📥 Download Receipt
              </Button>
            </Card.Body>
          </Card>
        ))
      )}
    </Container>
  );
}

export default OrderHistory;
