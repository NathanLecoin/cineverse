import { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import StarRating from './StarRating';

function ReviewForm({ movieId, onReviewCreated }) {
  const { user, isAuthenticated } = useContext(AuthContext);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (rating === 0) {
      setError('Veuillez choisir une note');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const { createReview } = await import('../api/reviews');
      await createReview({
        user_id: user.id,
        movie_id: movieId,
        rating,
        comment
      });

      // Reset le formulaire
      setRating(0);
      setComment('');
      
      // Notifie le parent
      if (onReviewCreated) {
        onReviewCreated();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de la création de la review');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div style={{ 
        padding: '20px', 
        backgroundColor: '#1e1e1e', 
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <p style={{ color: '#888' }}>
          Vous devez être connecté pour laisser une review
        </p>
      </div>
    );
  }

  return (
    <div style={{ 
      padding: '20px', 
      backgroundColor: '#1e1e1e', 
      borderRadius: '8px',
      marginTop: '20px'
    }}>
      <h3 style={{ marginBottom: '15px' }}>✍️ Laisser une review</h3>
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '10px', color: '#ccc' }}>
            Votre note :
          </label>
          <StarRating rating={rating} onRatingChange={setRating} />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px', color: '#ccc' }}>
            Votre commentaire :
          </label>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Partagez votre avis sur ce film..."
            rows="4"
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#2a2a2a',
              border: '1px solid #444',
              borderRadius: '4px',
              color: 'white',
              fontSize: '14px',
              resize: 'vertical'
            }}
          />
        </div>

        {error && <p style={{ color: 'red', marginBottom: '10px' }}>{error}</p>}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#555' : '#646cff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px'
          }}
        >
          {loading ? 'Envoi...' : 'Publier la review'}
        </button>
      </form>
    </div>
  );
}

export default ReviewForm;