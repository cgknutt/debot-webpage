import { defineStore } from 'pinia'
import axios from 'axios'

// Create a base API instance with relative URL
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchItems() {
      this.loading = true
      this.error = null
      
      try {
        // Use the api instance with relative path and trailing slash
        const response = await api.get('/items/')
        this.items = response.data
      } catch (err) {
        this.error = err.message || 'Failed to fetch items'
        console.error('Error fetching items:', err)
      } finally {
        this.loading = false
      }
    },
    
    async addItem(item) {
      this.loading = true
      this.error = null
      
      // Generate a unique ID if not provided
      if (!item.id) {
        item.id = 'frontend-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9)
      }
      
      try {
        // Use the api instance with relative path and trailing slash
        const response = await api.post('/items/', item)
        // Add the new item to the beginning of the array
        this.items.unshift(response.data)
        return response.data
      } catch (err) {
        this.error = err.message || 'Failed to add item'
        console.error('Error adding item:', err)
        throw err
      } finally {
        this.loading = false
      }
    }
  }
}) 