import { useState } from 'react';

function StarRating({ rating, onRatingChange, readOnly = false }) {
  const [hover, setHover] = useState(0);

  return (
    <div style={{ display: 'flex', gap: '5px' }}>
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          onClick={() => !readOnly && onRatingChange(star)}
          onMouseEnter={() => !readOnly && setHover(star)}
          onMouseLeave={() => !readOnly && setHover(0)}
          style={{
            background: 'none',
            border: 'none',
            fontSize: '30px',
            cursor: readOnly ? 'default' : 'pointer',
            padding: '0',
            transition: 'transform 0.2s'
          }}
          disabled={readOnly}
          onMouseDown={(e) => !readOnly && (e.currentTarget.style.transform = 'scale(1.2)')}
          onMouseUp={(e) => !readOnly && (e.currentTarget.style.transform = 'scale(1)')}
        >
          <span style={{ 
            color: star <= (hover || rating) ? '#ffd700' : '#444'
          }}>
            ★
          </span>
        </button>
      ))}
      {!readOnly && (
        <span style={{ marginLeft: '10px', color: '#888', alignSelf: 'center' }}>
          {rating > 0 ? `${rating} / 5` : 'Choisissez une note'}
        </span>
      )}
    </div>
  );
}

export default StarRating;
