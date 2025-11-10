import React, { PureComponent } from 'react';
import { useNavigate } from 'react-router-dom';

interface LandingProps {
    
}

const Landing: React.FC<LandingProps> = () => {
    const navigate = useNavigate();
    return (
        <div>
            <h1>Landing Page</h1>
            <button onClick={() => navigate('/Auth')}>Go to Auth</button>
        </div>
    );
}

export default Landing;