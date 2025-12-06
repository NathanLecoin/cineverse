import { Link } from 'react-router-dom';

function MovieCard({ movie }) {
  return (
    <Link to={`/movies/${movie.id}`} style={{ textDecoration: 'none' }}>
      <div style={{
        backgroundColor: '#1e1e1e',
        borderRadius: '8px',
        padding: '20px',
        cursor: 'pointer',
        transition: 'transform 0.2s',
        border: '1px solid #333',
        height: '100%'
      }}
      onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
      onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
      >
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

        {movie.average_rating && (
          <p style={{ color: '#ffd700', marginTop: '10px', fontSize: '14px' }}>
            ⭐ {movie.average_rating.toFixed(1)} / 5
          </p>
        )}
      </div>
    </Link>
  );
}

export default MovieCard;