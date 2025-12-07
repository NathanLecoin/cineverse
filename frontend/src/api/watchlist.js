import axios from './axios';

// Récupérer la watchlist d'un utilisateur
export const getUserWatchlist = async (userId) => {
  const response = await axios.get(`/watchlist/${userId}`);
  return response.data;
};

// Ajouter un film à la watchlist
export const addToWatchlist = async (userId, movieId) => {
  const response = await axios.post('/watchlist/', {
    user_id: userId,
    movie_id: movieId
  });
  return response.data;
};

// Retirer un film de la watchlist
export const removeFromWatchlist = async (userId, movieId) => {
  const response = await axios.delete(`/watchlist/${userId}/${movieId}`);
  return response.data;
};

// Vérifier si un film est dans la watchlist
export const checkInWatchlist = async (userId, movieId) => {
  const response = await axios.get(`/watchlist/${userId}/${movieId}`);
  return response.data;
};