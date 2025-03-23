import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Divider,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  BarChart,
  Settings,
  LogOut,
  Menu,
} from 'lucide-react';
import { logout } from '../store/slices/authSlice';
import { RootState } from '../store/store';

const Layout = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { currentUser } = useSelector((state: RootState) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  const drawerItems = [
    { text: 'Top Gainers', icon: <TrendingUp size={24} /> },
    { text: 'Top Losers', icon: <TrendingDown size={24} /> },
    { text: 'High Volume', icon: <BarChart size={24} /> },
    { text: 'Settings', icon: <Settings size={24} /> },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <IconButton
        className="fixed top-4 left-4 z-50"
        onClick={() => setDrawerOpen(true)}
      >
        <Menu />
      </IconButton>

      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <div className="w-64 p-4">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold">Stock AI</h2>
          </div>
          <Divider />
          <List>
            {drawerItems.map((item) => (
              <ListItem button key={item.text}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
            <Divider className="my-2" />
            <ListItem button onClick={handleLogout}>
              <ListItemIcon>
                <LogOut size={24} />
              </ListItemIcon>
              <ListItemText primary="Logout" />
            </ListItem>
          </List>
        </div>
      </Drawer>

      <AnimatePresence mode="wait">
        <motion.main
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ duration: 0.3 }}
          className="container mx-auto px-4 py-8"
        >
          <Outlet />
        </motion.main>
      </AnimatePresence>
    </div>
  );
};

export default Layout;