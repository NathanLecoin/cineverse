import { useState, useEffect } from 'react';
import { getAllMovies } from '../api/movies';
import MovieGrid from '../components/MovieGrid';

function Home() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true);
        const data = await getAllMovies();
        setMovies(data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Erreur lors du chargement des films');
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>🎬 Chargement des films...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2 style={{ color: 'red' }}>❌ {error}</h2>
        <p style={{ color: '#888' }}>Vérifiez que le backend est bien démarré</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ 
        textAlign: 'center', 
        padding: '30px 20px 10px',
        maxWidth: '1400px',
        margin: '0 auto'
      }}>
        <h1 style={{ fontSize: '36px', marginBottom: '10px' }}>🎬 Catalogue CineVerse</h1>
        <p style={{ color: '#888', fontSize: '18px' }}>
          {movies.length} films disponibles
        </p>
      </div>

      {movies.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <h2>📭 Aucun film disponible</h2>
          <p style={{ color: '#888' }}>La base de données est vide</p>
        </div>
      ) : (
        <MovieGrid movies={movies} />
      )}
    </div>
  );
}

export default Home;