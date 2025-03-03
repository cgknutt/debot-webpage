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
      
      // We don't need to generate an ID anymore, as the backend will handle this
      // Just send the text directly
      const itemData = { text: item.text }
      
      try {
        // Use the api instance with relative path and trailing slash
        const response = await api.post('/items/', itemData)
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