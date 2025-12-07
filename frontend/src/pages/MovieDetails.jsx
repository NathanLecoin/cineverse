import { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { AuthContext } from '../context/AuthContext';
import { getMovieById } from '../api/movies';
import { getMovieReviews, deleteReview } from '../api/reviews';
import { addToWatchlist, checkInWatchlist } from '../api/watchlist';
import ReviewList from '../components/ReviewList';
import ReviewForm from '../components/ReviewForm';
import StarRating from '../components/StarRating';

function MovieDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useContext(AuthContext);

  const [movie, setMovie] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [inWatchlist, setInWatchlist] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMovieData = async () => {
    try {
      setLoading(true);
      
      // Récupérer le film
      const movieData = await getMovieById(id);
      setMovie(movieData);

      // Récupérer les reviews
      const reviewsData = await getMovieReviews(id);
      setReviews(reviewsData);

      // Vérifier si dans la watchlist
      if (isAuthenticated && user) {
        try {
          const watchlistCheck = await checkInWatchlist(user.id, id);
          setInWatchlist(watchlistCheck.in_watchlist);
        } catch (err) {
          console.log('Erreur check watchlist:', err);
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement du film');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMovieData();
  }, [id, isAuthenticated, user]);

  const handleAddToWatchlist = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      await addToWatchlist(user.id, id);
      setInWatchlist(true);
      toast.success('Film ajouté à votre watchlist !');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Erreur lors de l\'ajout à la watchlist');
    }
  };

  const handleDeleteReview = async (reviewId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette review ?')) {
      return;
    }

    try {
      await deleteReview(reviewId);
      // Rafraîchir les reviews
      const reviewsData = await getMovieReviews(id);
      setReviews(reviewsData);
      toast.success('Review supprimée');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Erreur lors de la suppression');
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>🎬 Chargement...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2 style={{ color: 'red' }}>❌ {error}</h2>
        <button onClick={() => navigate('/')} style={{ marginTop: '20px', padding: '10px 20px' }}>
          ← Retour à la liste
        </button>
      </div>
    );
  }

  if (!movie) {
    return null;
  }

  // Calculer la moyenne des notes
  const averageRating = reviews.length > 0
    ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)
    : null;

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
      {/* Header */}
      <button
        onClick={() => navigate('/')}
        style={{
          marginBottom: '20px',
          padding: '8px 16px',
          backgroundColor: '#333',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        ← Retour
      </button>

      {/* Détails du film */}
      <div style={{ 
        backgroundColor: '#1e1e1e', 
        padding: '30px', 
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <h1 style={{ fontSize: '36px', marginBottom: '15px', color: '#646cff' }}>
          {movie.title}
        </h1>

        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px', flexWrap: 'wrap' }}>
          <span style={{ color: '#888' }}>📅 {movie.release_year}</span>
          {movie.genre && <span style={{ color: '#888' }}>🎭 {movie.genre}</span>}
          {averageRating && (
            <span style={{ color: '#ffd700' }}>⭐ {averageRating} / 5</span>
          )}
          <span style={{ color: '#888' }}>💬 {reviews.length} reviews</span>
        </div>

        <p style={{ 
          color: '#ccc', 
          lineHeight: '1.8', 
          fontSize: '16px',
          marginBottom: '20px'
        }}>
          {movie.description || 'Pas de description disponible'}
        </p>

        {isAuthenticated && !inWatchlist && (
          <button
            onClick={handleAddToWatchlist}
            style={{
              padding: '12px 24px',
              backgroundColor: '#4caf50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            ➕ Ajouter à ma watchlist
          </button>
        )}

        {inWatchlist && (
          <p style={{ color: '#4caf50', fontWeight: 'bold' }}>
            ✅ Dans votre watchlist
          </p>
        )}
      </div>

      {/* Formulaire de review */}
      <ReviewForm movieId={parseInt(id)} onReviewCreated={fetchMovieData} />

      {/* Liste des reviews */}
      <ReviewList reviews={reviews} onDeleteReview={handleDeleteReview} />
    </div>
  );
}

export default MovieDetails;