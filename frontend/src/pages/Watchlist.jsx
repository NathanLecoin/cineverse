import { useState, useEffect, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { AuthContext } from '../context/AuthContext';
import { getUserWatchlist, removeFromWatchlist } from '../api/watchlist';
import MovieGrid from '../components/MovieGrid';

function Watchlist() {
  const { user, isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();

  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    fetchWatchlist();
  }, [isAuthenticated, user]);

  const fetchWatchlist = async () => {
    try {
      setLoading(true);
      const data = await getUserWatchlist(user.id);
      setWatchlist(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement de la watchlist');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveFromWatchlist = async (movieId) => {
    if (!window.confirm('Retirer ce film de votre watchlist ?')) {
      return;
    }

    try {
      await removeFromWatchlist(user.id, movieId);
      // Rafraîchir la watchlist
      await fetchWatchlist();
      toast.success('Film retiré de votre watchlist');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Erreur lors de la suppression');
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>📚 Chargement de votre watchlist...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2 style={{ color: 'red' }}>❌ {error}</h2>
      </div>
    );
  }

  if (!watchlist || watchlist.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: '100px 20px',
        maxWidth: '600px',
        margin: '0 auto'
      }}>
        <h1 style={{ fontSize: '48px', marginBottom: '20px' }}>📭</h1>
        <h2 style={{ marginBottom: '15px' }}>Votre watchlist est vide</h2>
        <p style={{ color: '#888', marginBottom: '30px', lineHeight: '1.6' }}>
          Parcourez notre catalogue et ajoutez des films à votre liste pour les retrouver facilement plus tard !
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
            🎬 Découvrir des films
          </button>
        </Link>
      </div>
    );
  }

  // Transformer les entrées de watchlist en format "films"
  const moviesInWatchlist = watchlist.map(entry => ({
    ...entry.movie,
    watchlistId: entry.id  // Garder l'ID de la watchlist pour pouvoir supprimer
  }));

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      <div style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '36px', marginBottom: '10px' }}>
          📚 Ma Watchlist
        </h1>
        <p style={{ color: '#888', fontSize: '18px' }}>
          {watchlist.length} film{watchlist.length > 1 ? 's' : ''} à regarder
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '20px',
        padding: '20px'
      }}>
        {moviesInWatchlist.map((movie) => (
          <div key={movie.id} style={{ position: 'relative' }}>
            {/* Carte du film */}
            <Link to={`/movies/${movie.id}`} style={{ textDecoration: 'none' }}>
              <div style={{
                backgroundColor: '#1e1e1e',
                borderRadius: '8px',
                padding: '20px',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                border: '1px solid #333',
                height: '100%'
              }}>
                <h3 style={{ color: '#646cff', marginBottom: '10px', fontSize: '18px' }}>
                  {movie.title}
                </h3>
                
                <p style={{ color: '#888', fontSize: '14px', marginBottom: '10px' }}>
                  📅 {movie.release_year}
                </p>
                
                {movie.genre && (
                  <p style={{ color: '#999', fontSize: '12px', marginBottom: '10px' }}>
                    🎭 {movie.genre}
                  </p>
                )}
                
                <p style={{ 
                  color: '#ccc', 
                  fontSize: '14px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical',
                  lineHeight: '1.4'
                }}>
                  {movie.description || 'Pas de description disponible'}
                </p>
              </div>
            </Link>

            <button
              onClick={() => handleRemoveFromWatchlist(movie.id)}
              style={{
                position: 'absolute',
                top: '10px',
                right: '10px',
                padding: '8px 12px',
                backgroundColor: '#f44336',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold',
                zIndex: 10
              }}
            >
              ✕ Retirer
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Watchlist;