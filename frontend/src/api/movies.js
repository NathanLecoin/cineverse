import axios from './axios';

// Récupérer tous les films
export const getAllMovies = async () => {
  const response = await axios.get('/movies?limit=100');  
  return response.data;
};

// Récupérer un film par ID
export const getMovieById = async (id) => {
  const response = await axios.get(`/movies/${id}`);
  return response.data;
};

// Récupérer les reviews d'un film
export const getMovieReviews = async (movieId) => {
  const response = await axios.get(`/movies/${movieId}/reviews`);
  return response.data;
};