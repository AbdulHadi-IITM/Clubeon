<template>
  <div class="settings-card">
    <div class="card-header">
      <div class="header-title-group">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <h2>Account Settings</h2>
      </div>
    </div>

    <!-- Settings List -->
    <div class="settings-list" role="navigation" aria-label="Account Settings Menu">
      <!-- Edit Profile -->
      <button @click="$emit('action', 'edit-profile')" class="settings-item" aria-label="Edit Profile Details">
        <div class="item-left">
          <div class="item-icon-box edit-profile">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <div class="item-meta">
            <span class="item-title">Edit Profile</span>
            <span class="item-desc">Change your personal and address info</span>
          </div>
        </div>
        <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Change Password -->
      <button @click="$emit('action', 'change-password')" class="settings-item" aria-label="Change Password">
        <div class="item-left">
          <div class="item-icon-box change-password">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div class="item-meta">
            <span class="item-title">Change Password</span>
            <span class="item-desc">Update your login security credentials</span>
          </div>
        </div>
        <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Notification Preferences -->
      <button @click="$emit('action', 'notifications')" class="settings-item" aria-label="Notification Preferences">
        <div class="item-left">
          <div class="item-icon-box notifications">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
          <div class="item-meta">
            <span class="item-title">Notification Preferences</span>
            <span class="item-desc">Manage booking email and push alerts</span>
          </div>
        </div>
        <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Privacy Settings -->
      <button @click="$emit('action', 'privacy')" class="settings-item" aria-label="Privacy Settings">
        <div class="item-left">
          <div class="item-icon-box privacy">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div class="item-meta">
            <span class="item-title">Privacy Settings</span>
            <span class="item-desc">Control visibility and active login sessions</span>
          </div>
        </div>
        <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['action'])
</script>

<script>
export default {
  name: 'SettingsPanel'
}
</script>

<style scoped>
.settings-card {
  background: #ffffff;
  border-radius: 1.5rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
  padding: 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.settings-card:hover {
  border-color: rgba(79, 70, 229, 0.12);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.75rem;
  padding-bottom: 1.15rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

.header-title-group {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.header-icon {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 0.75rem;
  background: rgba(79, 70, 229, 0.08);
  color: #4f46e5;
  display: grid;
  place-items: center;
}

h2 {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.settings-item {
  width: 100%;
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.5);
  border-radius: 1rem;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  text-align: left;
  transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

.settings-item:hover {
  transform: translateY(-2px);
  background: rgba(248, 250, 252, 0.8);
  border-color: rgba(79, 70, 229, 0.15);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.02);
}

.settings-item:active {
  transform: translateY(0);
}

.item-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.item-icon-box {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.item-icon-box.edit-profile {
  background: rgba(59, 130, 246, 0.08);
  color: #2563eb;
}

.item-icon-box.change-password {
  background: rgba(16, 185, 129, 0.08);
  color: #059669;
}

.item-icon-box.notifications {
  background: rgba(249, 115, 22, 0.08);
  color: #ea580c;
}

.item-icon-box.privacy {
  background: rgba(139, 92, 246, 0.08);
  color: #7c3aed;
}

.item-meta {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.item-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
}

.item-desc {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 500;
}

.chevron-icon {
  color: #94a3b8;
  transition: transform 0.2s ease, color 0.2s ease;
}

.settings-item:hover .chevron-icon {
  color: #4f46e5;
  transform: translateX(3px);
}

@media (max-width: 576px) {
  .settings-card {
    padding: 1.5rem;
  }
  .settings-item {
    padding: 0.85rem 1rem;
  }
}
</style>
