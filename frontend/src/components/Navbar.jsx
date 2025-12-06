import { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

function Navbar() {
  const { user, isAuthenticated, logout } = useContext(AuthContext);

  return (
    <nav style={{
      backgroundColor: '#1a1a1a',
      padding: '15px 30px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '20px'
    }}>
      <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
        <Link to="/" style={{ fontSize: '24px', fontWeight: 'bold', textDecoration: 'none' }}>
          🎬 CineVerse
        </Link>
        
        {isAuthenticated && (
          <>
            <Link to="/" style={{ textDecoration: 'none', color: 'white' }}>Films</Link>
            <Link to="/watchlist" style={{ textDecoration: 'none', color: 'white' }}>Ma Watchlist</Link>
          </>
        )}
      </div>

      <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
        {isAuthenticated ? (
          <>
            <span>👤 {user?.username}</span>
            <button 
              onClick={logout}
              style={{
                padding: '8px 16px',
                backgroundColor: '#f44336',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Déconnexion
            </button>
          </>
        ) : (
          <>
            <Link to="/login">
              <button style={{
                padding: '8px 16px',
                backgroundColor: '#646cff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Connexion
              </button>
            </Link>
            <Link to="/register">
              <button style={{
                padding: '8px 16px',
                backgroundColor: '#4caf50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Inscription
              </button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;