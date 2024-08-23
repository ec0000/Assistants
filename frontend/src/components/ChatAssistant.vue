// ChatAssistant.vue
// ChatAssistant.vue
<template>
  <div class="chat-container">
    <div class="chat-list">
      <h3>Chats</h3>
      <ul>
        <li v-for="chat in chats" :key="chat.id" @click="selectChat(chat.id)" :class="{ active: currentChat && currentChat.id === chat.id }">
          {{ chat.name }}
        </li>
      </ul>
    </div>
    <div class="chat-window" v-if="currentChat">
      <div class="chat-header">
        <h3>{{ currentChat.name }}</h3>
      </div>
      <div class="message-list" ref="messageList">
        <div v-for="message in currentChat.messages" :key="message.id" :class="['message', message.sender === 'user' ? 'user-message' : 'assistant-message']">
          <strong>{{ message.sender }}</strong>: {{ message.text }}
        </div>
      </div>
      <div class="message-input">
        <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message...">
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatAssistant',
  data() {
    return {
      chats: [
        { id: 1, name: 'General Chat', messages: [] },
        { id: 2, name: 'Tech Support', messages: [] },
        { id: 3, name: 'Project Alpha', messages: [] },
      ],
      currentChat: null,
      newMessage: '',
    }
  },
  created() {
    // Select the first chat by default when the component is created
    this.selectChat(1);
  },
  methods: {
    selectChat(chatId) {
      this.currentChat = this.chats.find(chat => chat.id === chatId);
    },
    sendMessage() {
      if (this.newMessage.trim() && this.currentChat) {
        this.currentChat.messages.push({
          id: Date.now(),
          sender: 'user',
          text: this.newMessage
        });
        this.newMessage = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
        // Simulate assistant response
        setTimeout(() => {
          this.currentChat.messages.push({
            id: Date.now(),
            sender: 'assistant',
            text: "I'm an AI assistant. How can I help you today?"
          });
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }, 1000);
      }
    },
    scrollToBottom() {
      const messageList = this.$refs.messageList;
      if (messageList) {
        messageList.scrollTop = messageList.scrollHeight;
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 60px); /* Adjust based on your header height */
  border: 1px solid #ccc;
}

.chat-list {
  width: 200px;
  border-right: 1px solid #ccc;
  overflow-y: auto;
}

.chat-list ul {
  list-style-type: none;
  padding: 0;
}

.chat-list li {
  padding: 10px;
  cursor: pointer;
}

.chat-list li.active {
  background-color: #e0e0e0;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 10px;
  background-color: #f0f0f0;
  border-bottom: 1px solid #ccc;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.message {
  margin-bottom: 10px;
  padding: 5px;
  border-radius: 5px;
}

.user-message {
  background-color: #e3f2fd;
  text-align: right;
}

.assistant-message {
  background-color: #f0f0f0;
}

.message-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
}

.message-input input {
  flex: 1;
  padding: 5px;
  margin-right: 10px;
}

.message-input button {
  padding: 5px 10px;
  background-color: #4285F4;
  color: white;
  border: none;
  cursor: pointer;
}
</style>