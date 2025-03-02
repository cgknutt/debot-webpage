import { defineStore } from 'pinia'
import axios from 'axios'

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
        const response = await axios.get('/api/items')
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
      
      try {
        const response = await axios.post('/api/items', item)
        this.items.push(response.data)
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