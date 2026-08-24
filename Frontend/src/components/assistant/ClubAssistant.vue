<template>
  <div class="assistant-wrapper" v-if="isVisible">
    <!-- Floating Action Button -->
    <button class="assistant-toggle" @click="toggleChat" :class="{ 'is-open': isOpen }" aria-label="Toggle AI Assistant">
      <div class="icon-box">
        <svg v-if="!isOpen" class="toggle-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2a10 10 0 0 1 10 10c0 5.523-4.477 10-10 10a9.96 9.96 0 0 1-4.587-1.11L3 22l1.11-4.413A9.96 9.96 0 0 1 2 12C2 6.477 6.477 2 12 2z" />
          <path d="m9.5 9.5 5 5" stroke-width="1.5" stroke-dasharray="2 2" />
          <circle cx="12" cy="12" r="1.5" fill="currentColor" />
        </svg>
        <svg v-else class="toggle-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </div>
      <span class="text" v-if="!isOpen">AI Concierge</span>
      <span class="pulse-ring" v-if="!isOpen"></span>
    </button>

    <!-- Chat Panel -->
    <div class="chat-panel" v-if="isOpen">
      <div class="chat-header">
        <div class="header-title-group">
          <div class="bot-avatar">
            <svg class="avatar-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 8V4m0 0a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm0 4a4 4 0 0 0-4 4v4a4 4 0 0 0 8 0v-4a4 4 0 0 0-4-4z" />
              <circle cx="9" cy="13" r="1" fill="currentColor" />
              <circle cx="15" cy="13" r="1" fill="currentColor" />
            </svg>
            <span class="online-indicator"></span>
          </div>
          <div>
            <h3>ClubDash AI</h3>
            <span class="header-subtitle">Concierge & Booking Assistant</span>
          </div>
        </div>
        <div class="header-actions">
          <button class="icon-btn clear-btn" @click="clearChat" title="Clear chat history">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"></path>
              <path d="M21 3v5h-5"></path>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"></path>
              <path d="M8 16H3v5"></path>
            </svg>
          </button>
          <button class="icon-btn close-btn" @click="toggleChat" title="Close Assistant">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
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
            <svg class="tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
            </svg>
            <span>Live Action: {{ msg.tools_used.join(', ') }}</span>
          </div>
          <VMarkdownView v-if="msg.role === 'assistant'" :content="msg.content" class="message-content md-view" mode="light" />
          <div v-else class="message-content">{{ msg.content }}</div>

          <!-- Quick Action Buttons for Booking Confirmation -->
          <div v-if="isBookingDraftReady(msg)" class="booking-actions">
            <button @click="sendMessage('Yes, please confirm and finalize this booking.')" class="action-btn confirm-btn" :disabled="isLoading">
              <svg class="btn-svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>Confirm & Book Now</span>
            </button>
            <button @click="sendMessage('No, please cancel this booking draft.')" class="action-btn cancel-btn" :disabled="isLoading">
              <svg class="btn-svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
              <span>Cancel</span>
            </button>
          </div>
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
          placeholder="Ask a question or book a court..."
          :disabled="isLoading"
        />
        <button class="send-btn" @click="sendMessage(newMessage)" :disabled="isLoading || !newMessage.trim()" aria-label="Send message">
          <svg class="send-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue';
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
  return authStore.isAuthenticated();
});

const welcomeMessage = computed(() => {
  if (authStore.user?.role === 'player') {
    return "Hi! I'm your ClubDash assistant. I can help you find & recommend facilities (by sport, amenities, distance), check bookings, and see court availability.";
  }
  if (authStore.user?.role === 'owner') {
    return "Hello! I can assist with your club analytics, facility bookings, court schedules, attendance, and member reservations.";
  }
  return "Hello! I can assist with today's operational dashboard, staff bookings, attendance, court status, and facility discovery.";
});

const suggestedPrompts = computed(() => {
  if (authStore.user?.role === 'player') {
    return [
      "Book Badminton Court 1 for today at 6 PM",
      "Find a chlorine-free, kid-friendly pool within 5 km",
      "Which courts are available today?",
      "What are my upcoming bookings?"
    ];
  }
  if (authStore.user?.role === 'owner') {
    return [
      "Show today's court status and bookings",
      "Find facilities with parking and cafe",
      "Check today's attendance summary",
      "Which courts are available today?"
    ];
  }
  return [
    "Book a court for a walk-in member",
    "Find facilities with parking and cafe",
    "Show today's attendance summary",
    "Which courts are available today?"
  ];
});

const toggleChat = () => {
  isOpen.value = !isOpen.value;
};

const clearChat = async () => {
  try {
    await api.post('/assistant/clear');
  } catch (e) {
    console.error('Error clearing chat:', e);
  }
  messages.value = [];
};

function isBookingDraftReady(msg) {
  if (msg.role !== 'assistant') return false;
  if (!msg.tools_used || !msg.tools_used.includes('prepare_court_booking')) return false;
  const content = (msg.content || '').toLowerCase();
  if (
    content.includes('already booked') ||
    content.includes('unavailable') ||
    content.includes('already passed') ||
    content.includes('cannot be booked') ||
    content.includes('error') ||
    content.includes('sorry')
  ) {
    return false;
  }
  return true;
}

const scrollToBottom = async () => {
  await nextTick();
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

let cachedLocation = { lat: 12.9716, lon: 77.5946 };
if (typeof navigator !== 'undefined' && navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      cachedLocation = { lat: pos.coords.latitude, lon: pos.coords.longitude };
    },
    () => {},
    { timeout: 3000 }
  );
}

const sendMessage = async (text) => {
  if (!text.trim()) return;
  
  const userText = text;
  messages.value.push({ role: 'user', content: userText });
  newMessage.value = '';
  isLoading.value = true;
  await scrollToBottom();

  try {
    const payload = { 
      message: userText,
      user_lat: cachedLocation.lat,
      user_lon: cachedLocation.lon
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

/* Floating Action Button */
.assistant-toggle {
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: white;
  border: none;
  border-radius: 9999px;
  padding: 10px 18px;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.15) inset;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.assistant-toggle:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 14px 28px -4px rgba(79, 70, 229, 0.55);
}

.assistant-toggle.is-open {
  padding: 12px;
  background: #0f172a;
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.3);
}

.icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-svg {
  width: 19px;
  height: 19px;
}

/* Chat Panel */
.chat-panel {
  width: 410px;
  height: 570px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 24px 48px -12px rgba(15, 23, 42, 0.22), 0 0 0 1px rgba(226, 232, 240, 0.9);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px) scale(0.97); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* Header */
.chat-header {
  background: #ffffff;
  padding: 14px 18px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bot-avatar {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  color: white;
}

.avatar-svg {
  width: 18px;
  height: 18px;
}

.online-indicator {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #10b981;
  border: 2px solid #ffffff;
}

.chat-header h3 {
  margin: 0;
  font-size: 14.5px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
}

.header-subtitle {
  font-size: 11px;
  color: #64748b;
  font-weight: 500;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.icon-btn {
  background: transparent;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.icon-btn svg {
  width: 16px;
  height: 16px;
}

.icon-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

/* Chat Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #f8fafc;
}

.message {
  padding: 12px 15px;
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
  font-size: 12.5px;
}

.tool-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 600;
  color: #4f46e5;
  background: #eef2ff;
  padding: 3px 8px;
  border-radius: 6px;
  margin-bottom: 8px;
  border: 1px solid #e0e7ff;
}

.tool-icon {
  width: 12px;
  height: 12px;
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
  font-size: 14.5px;
  font-weight: 800;
  margin: 10px 0 6px;
  color: #0f172a;
}

:deep(.md-h3),
:deep(.md-h4) {
  font-size: 13.5px;
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

/* Suggested Prompts */
.suggested-prompts {
  padding: 0 16px 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  background: #f8fafc;
}

.prompt-btn {
  background: #ffffff;
  color: #4338ca;
  border: 1px solid #e0e7ff;
  border-radius: 10px;
  padding: 6px 11px;
  font-size: 11.5px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.prompt-btn:hover {
  background: #eef2ff;
  border-color: #c7d2fe;
  transform: translateY(-1px);
}

/* Input Area */
.chat-input-area {
  padding: 12px 16px;
  background: #ffffff;
  border-top: 1px solid #f1f5f9;
  display: flex;
  gap: 8px;
  align-items: center;
}

.chat-input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  outline: none;
  font-size: 13.5px;
  background: #f8fafc;
  transition: all 0.2s;
}

.chat-input-area input:focus {
  background: #ffffff;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.send-btn {
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: white;
  border: none;
  border-radius: 10px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25);
}

.send-svg {
  width: 17px;
  height: 17px;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.35);
}

.send-btn:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

/* Booking Actions Component */
.booking-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-svg {
  width: 14px;
  height: 14px;
}

.confirm-btn {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.25);
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(16, 185, 129, 0.35);
}

.cancel-btn {
  background: #ffffff;
  color: #64748b;
  border: 1px solid #cbd5e1;
}

.cancel-btn:hover:not(:disabled) {
  background: #f1f5f9;
  color: #334155;
  border-color: #94a3b8;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .chat-panel {
    width: calc(100vw - 32px);
    height: 70vh;
  }
}
</style>
