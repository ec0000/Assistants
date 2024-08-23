// AssistantAdmin.vue
<template>
  <div class="admin">
    <h1>Whatsapp Assistants Admin</h1>
    <div class="section assistants">
      <h2>Assistants</h2>
      <div class="button-group">
        <button class="create" @click="openCreateModal">Create Assistant</button>
        <button class="edit" @click="openEditModal" :disabled="!selectedAssistant">Edit Assistant</button>
        <button class="delete" @click="deleteAssistant" :disabled="!selectedAssistant">Delete Assistant</button>
      </div>
      <div class="assistant-list-container">
        <ul class="assistant-list">
          <li v-for="assistant in assistants" :key="assistant.assistant_id" @click="selectAssistant(assistant)" :class="{ selected: selectedAssistant && selectedAssistant.assistant_id === assistant.assistant_id }">
            <h3>{{ assistant.assistant_name }}</h3>
            <p>{{ assistant.role }}</p>
          </li>
        </ul>
      </div>
    </div>

  <div class="section knowledge-base">
    <h2>Knowledge Base</h2>
    <div class="button-group">
      <button class="upload" @click="openUploadModal" :disabled="!selectedAssistant">Upload File</button>
      <button class="delete" @click="deleteKnowledgeBase" :disabled="!selectedKnowledgeBase">Delete File</button>
    </div>
    <div 
      class="upload-area" 
      @drop.prevent="handleFileDrop" 
      @dragover.prevent="dragover = true"
      @dragleave.prevent="dragover = false"
      :class="{ 'dragover': dragover }"
    >
      <p>{{ dragover ? 'Drop file here' : 'Drag and drop files here or click "Upload File" button' }}</p>
    </div>
    <ul class="knowledge-base-list">
      <li v-for="kb in knowledgeBase" :key="kb.kb_id" @click="selectKnowledgeBase(kb)" :class="{ selected: selectedKnowledgeBase && selectedKnowledgeBase.kb_id === kb.kb_id }">
        {{ kb.file_name }}
      </li>
    </ul>
    <p v-if="knowledgeBase.length === 0">No files added yet. Add PDFs or other documents to the knowledge base that the assistant will reference in every conversation.</p>
  </div>

    <!-- Create Assistant Modal -->
    <div v-if="showCreateModal" class="modal">
      <div class="modal-content">
        <h2>Create New Assistant</h2>
        <form @submit.prevent="createAssistant">
          <label for="create-assistant-name">Name:</label>
          <input id="create-assistant-name" v-model="newAssistant.assistant_name" required>
          
          <label for="create-assistant-role">Role:</label>
          <input id="create-assistant-role" v-model="newAssistant.role" required>
          
          <label for="create-assistant-prompt">System Prompt:</label>
          <textarea id="create-assistant-prompt" v-model="newAssistant.system_prompt" required></textarea>
          
          <div class="button-group">
            <button type="submit">Create</button>
            <button type="button" @click="closeCreateModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Assistant Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h2>Edit Assistant</h2>
        <form @submit.prevent="updateAssistant">
          <label for="edit-assistant-name">Name:</label>
          <input id="edit-assistant-name" v-model="editingAssistant.assistant_name" required>
          
          <label for="edit-assistant-role">Role:</label>
          <input id="edit-assistant-role" v-model="editingAssistant.role" required>
          
          <label for="edit-assistant-prompt">System Prompt:</label>
          <textarea id="edit-assistant-prompt" v-model="editingAssistant.system_prompt" required></textarea>
          
          <div class="button-group">
            <button type="submit">Save</button>
            <button type="button" @click="closeEditModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Upload File Modal -->
    <div v-if="showUploadModal" class="modal">
      <div class="modal-content">
        <h2>Upload Knowledge Base File</h2>
        <form @submit.prevent="uploadFile">
          <input type="file" @change="handleFileChange" accept=".pdf,.doc,.docx,.txt" required>
          <div class="button-group">
            <button type="submit">Upload</button>
            <button type="button" @click="closeUploadModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const API_BASE_URL = 'http://localhost:8000';

export default {
  name: 'AssistantAdmin',
  setup() {
    const assistants = ref([]);
    const selectedAssistant = ref(null);
    const knowledgeBase = ref([]);
    const selectedKnowledgeBase = ref(null);
    const showCreateModal = ref(false);
    const showEditModal = ref(false);
    const showUploadModal = ref(false);
    const newAssistant = ref({
      assistant_name: '',
      role: '',
      system_prompt: ''
    });
    const editingAssistant = ref({
      assistant_id: '',
      assistant_name: '',
      role: '',
      system_prompt: ''
    });
    const fileToUpload = ref(null);

    const fetchAssistants = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/assistants/`);
        assistants.value = response.data;
      } catch (error) {
        console.error('Error fetching assistants:', error);
      }
    };

    const createAssistant = async () => {
      try {
        const response = await axios.post(`${API_BASE_URL}/assistants/`, newAssistant.value);
        assistants.value.push(response.data);
        closeCreateModal();
      } catch (error) {
        console.error('Error creating assistant:', error);
      }
    };

    const updateAssistant = async () => {
      try {
        const response = await axios.put(`${API_BASE_URL}/assistants/${editingAssistant.value.assistant_id}`, editingAssistant.value);
        const index = assistants.value.findIndex(a => a.assistant_id === editingAssistant.value.assistant_id);
        if (index !== -1) {
          assistants.value[index] = response.data;
        }
        closeEditModal();
      } catch (error) {
        console.error('Error updating assistant:', error);
      }
    };

    const deleteAssistant = async () => {
      if (!selectedAssistant.value) return;
      try {
        await axios.delete(`${API_BASE_URL}/assistants/${selectedAssistant.value.assistant_id}`);
        assistants.value = assistants.value.filter(a => a.assistant_id !== selectedAssistant.value.assistant_id);
        selectedAssistant.value = null;
        knowledgeBase.value = [];
      } catch (error) {
        console.error('Error deleting assistant:', error);
      }
    };

    const fetchKnowledgeBase = async (assistantId) => {
      try {
        const response = await axios.get(`${API_BASE_URL}/knowledge-base/${assistantId}`);
        knowledgeBase.value = response.data;
      } catch (error) {
        console.error('Error fetching knowledge base:', error);
      }
    };

    const uploadFile = async () => {
      if (!fileToUpload.value || !selectedAssistant.value) return;

      const formData = new FormData();
      formData.append('file', fileToUpload.value);

      try {
        const response = await axios.post(
          `${API_BASE_URL}/knowledge-base/?assistant_id=${selectedAssistant.value.assistant_id}&file_name=${fileToUpload.value.name}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        knowledgeBase.value.push(response.data);
        closeUploadModal();
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    };

    const deleteKnowledgeBase = async () => {
      if (!selectedKnowledgeBase.value) return;
      try {
        await axios.delete(`${API_BASE_URL}/knowledge-base/${selectedKnowledgeBase.value.kb_id}`);
        knowledgeBase.value = knowledgeBase.value.filter(kb => kb.kb_id !== selectedKnowledgeBase.value.kb_id);
        selectedKnowledgeBase.value = null;
      } catch (error) {
        console.error('Error deleting knowledge base file:', error);
      }
    };

    const selectAssistant = (assistant) => {
      selectedAssistant.value = assistant;
      fetchKnowledgeBase(assistant.assistant_id);
    };

    const selectKnowledgeBase = (kb) => {
      selectedKnowledgeBase.value = kb;
    };

    const handleFileChange = (event) => {
      fileToUpload.value = event.target.files[0];
    };

    const handleFileDrop = (event) => {
      fileToUpload.value = event.dataTransfer.files[0];
      openUploadModal();
    };

    const openCreateModal = () => {
      showCreateModal.value = true;
    };

    const closeCreateModal = () => {
      showCreateModal.value = false;
      newAssistant.value = { assistant_name: '', role: '', system_prompt: '' };
    };

    const openEditModal = () => {
      if (selectedAssistant.value) {
        editingAssistant.value = { ...selectedAssistant.value };
        showEditModal.value = true;
      }
    };

    const closeEditModal = () => {
      showEditModal.value = false;
      editingAssistant.value = { assistant_id: '', assistant_name: '', role: '', system_prompt: '' };
    };

    const openUploadModal = () => {
      showUploadModal.value = true;
    };

    const closeUploadModal = () => {
      showUploadModal.value = false;
      fileToUpload.value = null;
    };

    onMounted(() => {
      fetchAssistants();
    });

    return {
      assistants,
      selectedAssistant,
      knowledgeBase,
      selectedKnowledgeBase,
      showCreateModal,
      showEditModal,
      showUploadModal,
      newAssistant,
      editingAssistant,
      selectAssistant,
      selectKnowledgeBase,
      createAssistant,
      updateAssistant,
      deleteAssistant,
      uploadFile,
      deleteKnowledgeBase,
      handleFileChange,
      handleFileDrop,
      openCreateModal,
      closeCreateModal,
      openEditModal,
      closeEditModal,
      openUploadModal,
      closeUploadModal
    };
  }
};
</script>

<style scoped>
.admin {
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1, h2 {
  color: #4285F4;
}

.section {
  background-color: #f0f0f0;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

button.create, button.upload {
  background-color: #4285F4;
  color: white;
}

button.edit {
  background-color: #FBBC05;
  color: black;
}

button.delete {
  background-color: #EA4335;
  color: white;
}

button:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}

.assistant-list-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.assistant-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.assistant-list li {
  background-color: white;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
  cursor: pointer;
}

.assistant-list li:last-child {
  border-bottom: none;
}

.assistant-list li.selected {
  background-color: #e0e0e0;
}

.assistant-list h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.assistant-list p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.assistant-list li, .knowledge-base-list li {
  background-color: white;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.assistant-list li.selected, .knowledge-base-list li.selected {
  background-color: #e0e0e0;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  margin-top: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.upload-area.dragover {
  background-color: #e0e0e0;
  border-color: #4285F4;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 80%;
  max-width: 500px;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-top: 1rem;
}

input, textarea {
  margin-top: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  height: 100px;
}
</style>