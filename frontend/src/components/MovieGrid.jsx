import MovieCard from './MovieCard';

function MovieGrid({ movies }) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
      gap: '20px',
      padding: '20px',
      maxWidth: '1400px',
      margin: '0 auto'
    }}>
      {movies.map((movie) => (
        <MovieCard key={movie.id} movie={movie} />
      ))}
    </div>
  );
}

export default MovieGrid;