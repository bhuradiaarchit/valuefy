import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { TextField, Button, CircularProgress } from '@mui/material';
import { toast } from 'react-hot-toast';
import { setUser, setLoading, setError } from '../store/slices/authSlice';
import { loginUser } from '../services/api';
import { RootState } from '../store/store';
import { LineChart } from 'lucide-react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { isLoading } = useSelector((state: RootState) => state.auth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      toast.error('Please fill in all fields');
      return;
    }

    dispatch(setLoading(true));
    try {
      const user = await loginUser(username, password);
      dispatch(setUser(user));
      toast.success('Welcome back!');
      navigate('/');
    } catch (error) {
      dispatch(setError((error as Error).message));
      toast.error('Login failed');
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full"
      >
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center justify-center mb-8">
            <LineChart size={40} className="text-blue-600" />
            <h1 className="text-3xl font-bold ml-2">Valuefy</h1>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <TextField
              fullWidth
              label="Username"
              variant="outlined"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isLoading}
            />
            <TextField
              fullWidth
              label="Password"
              type="password"
              variant="outlined"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
            />
            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="large"
              disabled={isLoading}
            >
              {isLoading ? <CircularProgress size={24} /> : 'Login'}
            </Button>
          </form>

          <p className="mt-4 text-center text-gray-600">
            Don't have an account?{' '}
            <Link to="/signup" className="text-blue-600 hover:text-blue-800">
              Sign up now
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;