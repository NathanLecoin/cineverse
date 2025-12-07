import { Link } from 'react-router-dom';

function NotFound() {
  return (
    <div style={{
      textAlign: 'center',
      padding: '100px 20px',
      maxWidth: '600px',
      margin: '0 auto'
    }}>
      <h1 style={{ fontSize: '120px', margin: '0', color: '#646cff' }}>404</h1>
      <h2 style={{ marginBottom: '20px' }}>Page non trouvée</h2>
      <p style={{ color: '#888', marginBottom: '30px', lineHeight: '1.6' }}>
        La page que vous recherchez n'existe pas ou a été déplacée.
      </p>
      <Link to="/">
        <button style={{
          padding: '12px 24px',
          backgroundColor: '#646cff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '16px'
        }}>
          🏠 Retour à l'accueil
        </button>
      </Link>
    </div>
  );
}

export default NotFound;
