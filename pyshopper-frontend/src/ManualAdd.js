import React, { useState } from 'react';
import { Card, Form, Button, Alert } from 'react-bootstrap';
import { addManualItemToCart } from './api';



function ManualAdd({ email, refreshCart }) {
  const [item, setItem] = useState({
    name: '',
    price: '',
    quantity: '',
    type: 'generic',
    shipping_weight: '',
    file_size_mb: '',
  });
  const [message, setMessage] = useState('');

  const handleAdd = async () => {
    const payload = {
      name: item.name,
      price: parseFloat(item.price),
      quantity: parseInt(item.quantity),
      type: item.type,
    };

    if (item.type === 'physical') {
      payload.shipping_weight = parseFloat(item.shipping_weight);
    } else if (item.type === 'digital') {
      payload.file_size_mb = parseFloat(item.file_size_mb);
    }

    try {
      await addManualItemToCart(email, payload);

      refreshCart();
      setItem({
        name: '',
        price: '',
        quantity: '',
        type: 'generic',
        shipping_weight: '',
        file_size_mb: '',
      });
      setMessage('✅ Item added to cart!');
    } catch (err) {
      setMessage(err?.response?.data?.error || '❌ Failed to add item');
    }

    setTimeout(() => setMessage(''), 3000); // auto-clear after 3s
  };

  return (
    <Card className="mt-4 shadow-sm">
      <Card.Body>
        <Card.Title>🧾 Manually Add Item to Cart</Card.Title>

        {message && <Alert variant={message.startsWith('✅') ? 'success' : 'danger'}>{message}</Alert>}

        <Form>
          <Form.Control
            className="mb-2"
            placeholder="Item Name"
            value={item.name}
            onChange={(e) => setItem({ ...item, name: e.target.value })}
          />

          <Form.Control
            type="number"
            className="mb-2"
            placeholder="Price"
            value={item.price}
            onChange={(e) => setItem({ ...item, price: e.target.value })}
          />

          <Form.Control
            type="number"
            className="mb-2"
            placeholder="Quantity"
            value={item.quantity}
            onChange={(e) => setItem({ ...item, quantity: e.target.value })}
          />

          <Form.Select
            className="mb-2"
            value={item.type}
            onChange={(e) => setItem({ ...item, type: e.target.value })}
          >
            <option value="generic">Generic</option>
            <option value="physical">Physical (requires shipping weight)</option>
            <option value="digital">Digital (requires file size)</option>
          </Form.Select>

          {item.type === 'physical' && (
            <Form.Control
              type="number"
              className="mb-2"
              placeholder="Shipping Weight (kg)"
              value={item.shipping_weight}
              onChange={(e) => setItem({ ...item, shipping_weight: e.target.value })}
            />
          )}

          {item.type === 'digital' && (
            <Form.Control
              type="number"
              className="mb-2"
              placeholder="File Size (MB)"
              value={item.file_size_mb}
              onChange={(e) => setItem({ ...item, file_size_mb: e.target.value })}
            />
          )}

          <Button variant="success" onClick={handleAdd}>
            ➕ Add to Cart
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
}

export default ManualAdd;
