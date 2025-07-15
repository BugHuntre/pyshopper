import React, { useState } from 'react';
import axios from 'axios';
import {
  Container,
  Form,
  Button,
  Alert,
  InputGroup,
  Row,
  Col,
} from 'react-bootstrap';
// import { useNavigate } from 'react-router-dom';

const BASE_URL = 'http://127.0.0.1:5000';

function Login() {
  const [isRegistering, setIsRegistering] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState('user');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  // const navigate = useNavigate();

  const handleLogin = async () => {
    if (!email || !password) {
      return setError('Email and password required.');
    }

    const endpoint = userType === 'admin' ? '/admin/login' : '/login';

    try {
      const res = await axios.post(`${BASE_URL}${endpoint}`, { email, password });

      if (res.status === 200) {
        const name = res.data?.name || 'User';

        localStorage.setItem('logged_in', 'true');
        localStorage.setItem('email', email);
        localStorage.setItem('role', userType);
        localStorage.setItem('password', password);
        localStorage.setItem('name', name);

        window.location.href = '/dashboard';
      }
    } catch (err) {
      const msg = err?.response?.data?.error || 'Login failed';
      setError(msg);
    }
  };

  const handleRegister = async () => {
    if (!name || !email || !password) {
      return setError('All fields required for registration.');
    }

    try {
      const res = await axios.post(`${BASE_URL}/register`, { name, email, password });
      if (res.status === 200) {
        alert('✅ Registered successfully. Please log in.');
        setIsRegistering(false);
        setName('');
        setEmail('');
        setPassword('');
        setError('');
      }
    } catch (err) {
      const msg = err?.response?.data?.error || 'Registration failed';
      setError(msg);
    }
  };

  return (
    <Container className="mt-5" style={{ maxWidth: '500px' }}>
      <h2 className="mb-4 text-center">🛍️ PyShopper {isRegistering ? 'Register' : 'Login'}</h2>

      <Form>
        {isRegistering && (
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
            />
          </Form.Group>
        )}

        <Form.Group className="mb-3">
          <Form.Label>Email address</Form.Label>
          <Form.Control
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter email"
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Password</Form.Label>
          <InputGroup>
            <Form.Control
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
            />
            <Button
              variant="outline-secondary"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? 'Hide' : 'Show'}
            </Button>
          </InputGroup>
        </Form.Group>

        {!isRegistering && (
          <Form.Group className="mb-3">
            <Form.Label>Login as</Form.Label>
            <Form.Select
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
            >
              <option value="user">User</option>
              <option value="admin">Admin</option>
            </Form.Select>
          </Form.Group>
        )}

        {error && <Alert variant="danger">{error}</Alert>}

        <Row className="mt-4">
          <Col>
            <Button
              variant="primary"
              className="w-100"
              onClick={isRegistering ? handleRegister : handleLogin}
            >
              {isRegistering ? 'Register' : 'Login'}
            </Button>
          </Col>
          <Col>
            <Button
              variant="outline-secondary"
              className="w-100"
              onClick={() => {
                setIsRegistering(!isRegistering);
                setError('');
              }}
            >
              {isRegistering ? 'Already have an account? Login' : 'New user? Register'}
            </Button>
          </Col>
        </Row>
      </Form>
    </Container>
  );
}

export default Login; 