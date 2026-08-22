<template>
  <div class="assistant-wrapper" v-if="isVisible">
    <!-- Floating Button -->
    <button class="assistant-toggle" @click="toggleChat" :class="{ 'is-open': isOpen }">
      <span class="icon">💬</span>
      <span class="text" v-if="!isOpen">ClubDash Assistant</span>
    </button>

    <!-- Chat Panel -->
    <div class="chat-panel" v-if="isOpen">
      <div class="chat-header">
        <h3>AI Assistant</h3>
        <button class="close-btn" @click="toggleChat">✕</button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <!-- Welcome Message -->
        <div class="message system">
          {{ welcomeMessage }}
        </div>

        <!-- Messages -->
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          :class="['message', msg.role]"
        >
          <div v-if="msg.tools_used && msg.tools_used.length" class="tool-badge">
            <span class="tool-dot"></span>
            <span>Live tool: {{ msg.tools_used.join(', ') }}</span>
          </div>
          <VMarkdownView v-if="msg.role === 'assistant'" :content="msg.content" class="message-content md-view" mode="light" />
          <div v-else class="message-content">{{ msg.content }}</div>
        </div>
        
        <div v-if="isLoading" class="message system loading">
          <span class="typing-indicator"></span> Thinking...
        </div>
      </div>

      <!-- Suggested Prompts -->
      <div class="suggested-prompts" v-if="messages.length === 0">
        <button 
          v-for="prompt in suggestedPrompts" 
          :key="prompt"
          @click="sendMessage(prompt)"
          class="prompt-btn"
        >
          {{ prompt }}
        </button>
      </div>

      <div class="chat-input-area">
        <input 
          type="text" 
          v-model="newMessage" 
          @keyup.enter="sendMessage(newMessage)"
          placeholder="Ask a question..."
          :disabled="isLoading"
        />
        <button @click="sendMessage(newMessage)" :disabled="isLoading || !newMessage.trim()">
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/api/axios';
import { VMarkdownView } from 'vue3-markdown';
import 'vue3-markdown/dist/vue3-markdown.css';

const authStore = useAuthStore();
const isOpen = ref(false);
const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(false);
const messagesContainer = ref(null);

const isVisible = computed(() => {
  return authStore.isAuthenticated && (authStore.user?.role === 'player' || authStore.user?.role === 'front-desk');
});

const welcomeMessage = computed(() => {
  if (authStore.user?.role === 'player') {
    return "Hi! I'm your ClubDash assistant. I can help you find & recommend facilities (by sport, amenities, distance), check bookings, and see court availability.";
  }
  return "Hello! I can assist with today's operational dashboard, staff bookings, attendance, court status, and facility discovery.";
});

const suggestedPrompts = computed(() => {
  if (authStore.user?.role === 'player') {
    return [
      "Find a chlorine-free, kid-friendly pool within 5 km",
      "Which indoor badminton courts have parking?",
      "Which courts are available today?",
      "What are my upcoming bookings?"
    ];
  }
  return [
    "Find facilities with parking and cafe",
    "Show me today's dashboard",
    "What is the court status?",
    "Who is currently checked in?"
  ];
});

const toggleChat = () => {
  isOpen.value = !isOpen.value;
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const getUserLocation = async () => {
  return new Promise((resolve) => {
    if (!navigator.geolocation) return resolve(null);
    navigator.geolocation.getCurrentPosition(
      (pos) => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
      () => resolve({ lat: 12.9716, lon: 77.5946 }), // fallback to default center
      { timeout: 3000 }
    );
  });
};

const sendMessage = async (text) => {
  if (!text.trim()) return;
  
  const userText = text;
  messages.value.push({ role: 'user', content: userText });
  newMessage.value = '';
  isLoading.value = true;
  await scrollToBottom();

  try {
    const loc = await getUserLocation();
    const payload = { 
      message: userText,
      user_lat: loc ? loc.lat : 12.9716,
      user_lon: loc ? loc.lon : 77.5946
    };
    
    const response = await api.post('/assistant/chat', payload);
    messages.value.push({ 
      role: 'assistant', 
      content: response.data.assistant_message,
      tools_used: response.data.tools_used || []
    });
  } catch (error) {
    console.error('Chat error:', error);
    messages.value.push({ 
      role: 'system', 
      content: 'Sorry, I encountered an error while processing your request.' 
    });
  } finally {
    isLoading.value = false;
    await scrollToBottom();
  }
};
</script>

<style scoped>
.assistant-wrapper {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.assistant-toggle {
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: white;
  border: none;
  border-radius: 9999px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.assistant-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 28px -4px rgba(79, 70, 229, 0.5);
}

.assistant-toggle.is-open {
  padding: 12px;
  background: #1e293b;
}

.chat-panel {
  width: 400px;
  height: 560px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.2), 0 0 0 1px rgba(226, 232, 240, 0.8);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.25s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.chat-header {
  background: #f8fafc;
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-header h3::before {
  content: '';
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #94a3b8;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #0f172a;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: #fafafa;
}

.message {
  padding: 12px 16px;
  border-radius: 14px;
  max-width: 88%;
  font-size: 13.5px;
  line-height: 1.6;
  word-break: break-word;
}

.message.user {
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.message.assistant {
  background: #ffffff;
  color: #1e293b;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.message.system {
  background: #eff6ff;
  color: #1e40af;
  align-self: flex-start;
  border: 1px solid #dbeafe;
  font-size: 13px;
}

.tool-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: #6366f1;
  background: #eef2ff;
  padding: 2px 8px;
  border-radius: 999px;
  margin-bottom: 8px;
  border: 1px solid #e0e7ff;
}

.tool-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #6366f1;
}

/* Markdown typography styling */
:deep(.message-content) {
  font-size: 13.5px;
  line-height: 1.6;
}

:deep(.md-bold) {
  font-weight: 700;
  color: inherit;
}

:deep(.md-h2) {
  font-size: 15px;
  font-weight: 800;
  margin: 10px 0 6px;
  color: #0f172a;
}

:deep(.md-h3),
:deep(.md-h4) {
  font-size: 14px;
  font-weight: 700;
  margin: 8px 0 4px;
  color: #0f172a;
}

:deep(.md-ul),
:deep(.md-ol) {
  margin: 6px 0;
  padding-left: 18px;
}

:deep(.md-li),
:deep(.md-oli) {
  margin-bottom: 3px;
}

:deep(.md-spacer) {
  height: 8px;
}

:deep(.inline-code) {
  background: #f1f5f9;
  color: #0f172a;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
}

:deep(.code-block) {
  background: #0f172a;
  color: #f8fafc;
  padding: 10px 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
  font-family: monospace;
  font-size: 12px;
}

.suggested-prompts {
  padding: 0 16px 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  background: #fafafa;
}

.prompt-btn {
  background: #ffffff;
  color: #4f46e5;
  border: 1px solid #e0e7ff;
  border-radius: 12px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.prompt-btn:hover {
  background: #eef2ff;
  border-color: #c7d2fe;
  transform: translateY(-1px);
}

.chat-input-area {
  padding: 14px 16px;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  display: flex;
  gap: 8px;
  align-items: center;
}

.chat-input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  outline: none;
  font-size: 13.5px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.chat-input-area input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.chat-input-area button {
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 18px;
  cursor: pointer;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.2s;
}

.chat-input-area button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .chat-panel {
    width: calc(100vw - 32px);
    height: 70vh;
  }
}
</style>
