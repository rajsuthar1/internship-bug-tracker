import axios from 'axios';

const API_URL = "http://127.0.0.1:8000/api/v1/projects/";

export const projectService = {
    // Get all projects for a dropdown selector
    getAll: async () => {
        const response = await axios.get(API_URL);
        return response.data;
    },
    // Get a single project's details
    getById: async (id) => {
        const response = await axios.get(`${API_URL}${id}`);
        return response.data;
    }
};