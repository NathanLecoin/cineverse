import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import StarRating from './StarRating';

function ReviewList({ reviews, onDeleteReview }) {
  const { user } = useContext(AuthContext);

  if (!reviews || reviews.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '30px', color: '#888' }}>
        <p>📭 Aucune review pour ce film</p>
        <p style={{ fontSize: '14px', marginTop: '10px' }}>
          Soyez le premier à donner votre avis !
        </p>
      </div>
    );
  }

  return (
    <div style={{ marginTop: '20px' }}>
      <h3 style={{ marginBottom: '20px' }}>💬 Reviews ({reviews.length})</h3>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        {reviews.map((review) => (
          <div
            key={review.id}
            style={{
              padding: '15px',
              backgroundColor: '#1e1e1e',
              borderRadius: '8px',
              border: '1px solid #333'
            }}
          >
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              marginBottom: '10px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                <span style={{ color: '#646cff', fontWeight: 'bold' }}>
                  👤 {review.user?.username || 'Utilisateur'}
                </span>
                <StarRating rating={review.rating} readOnly />
              </div>

              {user && user.id === review.user_id && (
                <button
                  onClick={() => onDeleteReview(review.id)}
                  style={{
                    padding: '5px 10px',
                    backgroundColor: '#f44336',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '12px'
                  }}
                >
                  🗑️ Supprimer
                </button>
              )}
            </div>

            {review.comment && (
              <p style={{ color: '#ccc', lineHeight: '1.5', marginTop: '10px' }}>
                {review.comment}
              </p>
            )}

            {review.created_at && (
              <p style={{ 
                color: '#666', 
                fontSize: '12px', 
                marginTop: '10px' 
              }}>
                📅 {new Date(review.created_at).toLocaleDateString('fr-FR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ReviewList;