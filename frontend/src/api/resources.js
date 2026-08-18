import client from './client';

export const getMyProfile = () => client.get('/identity/me/');
export const submitVerification = (data) => client.post('/identity/verify/', data);

export const listProviders = () => client.get('/providers/');
export const getProvider = (id) => client.get(`/providers/${id}/`);
export const postReview = (providerId, data) => client.post(`/providers/${providerId}/reviews/`, data);

export const listItineraries = () => client.get('/itineraries/');
export const generateItinerary = (data) => client.post('/itineraries/generate/', data);

export const listThreads = () => client.get('/assistant/threads/');
export const sendMessage = (data) => client.post('/assistant/message/', data);

export const listOrders = () => client.get('/payments/orders/');
export const createOrder = (data) => client.post('/payments/orders/', data);
export const payOrder = (id) => client.post(`/payments/orders/${id}/pay/`);
export const requestRefund = (id, data) => client.post(`/payments/orders/${id}/refund/`, data);

export const searchMarketplace = (params) => client.get('/marketplace/search/', { params });
export const getRates = () => client.get('/rates/');

export const getAdminDashboard = () => client.get('/admin/dashboard/');
export const getRemittanceQuote = (data) => client.post('/remittance/quote/', data);
export const listRemittances = () => client.get('/remittance/');
export const createRemittance = (data) => client.post('/remittance/', data);
