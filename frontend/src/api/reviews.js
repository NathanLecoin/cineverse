import axios from './axios';

// Récupérer les reviews d'un film
export const getMovieReviews = async (movieId) => {
  const response = await axios.get(`/movies/${movieId}/reviews`);
  return response.data;
};

// Créer une review
export const createReview = async (reviewData) => {
  const response = await axios.post('/reviews/', reviewData);
  return response.data;
};

// Supprimer une review
export const deleteReview = async (reviewId) => {
  const response = await axios.delete(`/reviews/${reviewId}`);
  return response.data;
};