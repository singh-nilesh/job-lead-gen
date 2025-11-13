import React from 'react';
import { useAuth } from '@/core/AuthContext';


const Home: React.FC = () => {
  const { user } = useAuth();
  
  return (
    <div className='text-center font-bold'>
      <h1>Welcome to the Home Page</h1>
    </div>
  );
};

export default Home;