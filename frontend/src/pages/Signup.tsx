import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { TextField, Button, CircularProgress } from '@mui/material';
import { toast } from 'react-hot-toast';
import { setUser, setLoading, setError } from '../store/slices/authSlice';
import { registerUser } from '../services/api';
import { RootState } from '../store/store';
import { LineChart } from 'lucide-react';
import { FcGoogle } from 'react-icons/fc';
import { getAuth, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { app } from '../firebase';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [authLoading,setAuthLoading] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
    const { isLoading,error:authError } = useSelector((state: RootState) => state.auth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      toast.error('Please fill in all fields');
      return;
    }

    dispatch(setLoading(true));
    try {
      const user = await registerUser(username, password);
      dispatch(setUser(user));
      toast.success(`Heyy ${username}!`);
      navigate('/');
    } catch (error) {
      dispatch(setError((error as Error).message));
      toast.error('Registration failed');
    } finally {
      dispatch(setLoading(false));
    }
  };

   const handleGoogleSignup = async () => {
      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({ prompt: "select_account" });
  
      const auth = getAuth(app);
  
      setAuthLoading(true);
      try {
        const result = await signInWithPopup(auth, provider);
        const username = result.user.displayName || "User";
        const password = result.user.uid || "abc123";
        const user = await registerUser(username, password);
        dispatch(setUser(user));
        toast.success(`Heyy ${username}!`);
        navigate('/');
      } catch (error) {
        dispatch(setError((error as Error).message));
        toast.error(authError || 'Login failed');
      } finally {
        setAuthLoading(false);
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
            <h1 className="text-3xl font-bold ml-2">Stock AI</h1>
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
              {isLoading ? <CircularProgress size={24} /> : 'Sign Up'}
            </Button>
          </form>

          <div className="my-2 text-center text-gray-500 text-xs md:text-sm">OR</div>

          <Button
                      fullWidth
                      variant="outlined"
                      size="large"
                      className="flex items-center justify-center space-x-2 border-gray-300"
                      onClick={handleGoogleSignup}
                      disabled={authLoading}
                    >
                      {authLoading ? (
                        <CircularProgress size={24} />
                      ) : (
                        <div className="flex items-center space-x-2">
                          <FcGoogle size={24} />
                          <span>Signup with Google</span>
                        </div>
                      )}
                    </Button>

          <p className="mt-4 text-center text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-600 hover:text-blue-800">
              Login now
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Signup;