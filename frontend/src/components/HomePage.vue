// Home.vue
<template>
  <div class="home">
    <h1>Welcome to Whatsapp Assistants</h1>
    <p>Empowering your organization with intelligent knowledge management</p>
    <button @click="startChatting">Start Chatting</button>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    startChatting() {
      this.$router.push('/chat')
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

h2 {
  color: #4285F4;
}
</style>