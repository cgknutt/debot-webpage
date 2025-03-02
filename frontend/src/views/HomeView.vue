<template>
  <div class="home">
    <h2>Add Item</h2>
    <form @submit.prevent="submitItem" class="item-form">
      <div class="form-group">
        <input 
          v-model="newItem" 
          placeholder="Enter item text..." 
          :disabled="itemsStore.loading"
          required
          class="text-input"
        />
        <button 
          type="submit" 
          class="submit-button"
          :disabled="itemsStore.loading || !newItem.trim()"
        >
          {{ itemsStore.loading ? 'Adding...' : 'Add Item' }}
        </button>
      </div>
      <div v-if="itemsStore.error" class="error-message">
        {{ itemsStore.error }}
      </div>
    </form>

    <h2>Items from Database</h2>
    <div v-if="itemsStore.loading && !itemsStore.items.length" class="loading">
      Loading items...
    </div>
    <div v-else-if="itemsStore.items.length === 0" class="no-items">
      No items found. Add some items above!
    </div>
    <ul v-else class="items-list">
      <li v-for="item in itemsStore.items" :key="item._id" class="item">
        {{ item.text }}
        <span class="timestamp">Created: {{ new Date(item.created_at).toLocaleString() }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useItemsStore } from '../store/items'

const itemsStore = useItemsStore()
const newItem = ref('')

onMounted(() => {
  itemsStore.fetchItems()
})

const submitItem = async () => {
  if (!newItem.value.trim()) return

  try {
    await itemsStore.addItem({ text: newItem.value.trim() })
    newItem.value = '' // Clear the input after successful submission
  } catch (error) {
    // Error is already handled in the store
  }
}
</script>

<style scoped>
.home {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.item-form {
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.text-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-button {
  padding: 0.75rem 1.5rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.submit-button:hover:not(:disabled) {
  background-color: #3aa876;
}

.submit-button:disabled {
  background-color: #9dc5b6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  margin-top: 0.5rem;
}

.items-list {
  list-style: none;
  padding: 0;
}

.item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item:last-child {
  border-bottom: none;
}

.timestamp {
  font-size: 0.8rem;
  color: #999;
}

.loading, .no-items {
  text-align: center;
  padding: 2rem;
  color: #777;
}
</style> 