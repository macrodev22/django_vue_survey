import axios from 'axios'

// const URL = import.meta.env.BACKEND_API_BASE
const URL = 'http://localhost:8000'

const apiClient = axios.create({
    baseURL: `${URL}/api`
})


export default apiClient