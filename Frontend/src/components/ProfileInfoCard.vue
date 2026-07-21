<template>
  <div class="info-card">
    <div class="card-header">
      <div class="header-title-group">
        <div class="header-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h2>Personal Information</h2>
      </div>
      <button @click="$emit('edit')" class="edit-btn" aria-label="Edit personal information">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
        Edit
      </button>
    </div>

    <div class="info-grid">
      <!-- Full Name -->
      <div class="info-item">
        <span class="info-label">Full Name</span>
        <span class="info-value">{{ info.name }}</span>
      </div>

      <!-- Email Address -->
      <div class="info-item">
        <span class="info-label">Email Address</span>
        <span class="info-value">{{ info.email }}</span>
      </div>

      <!-- Phone Number -->
      <div class="info-item">
        <span class="info-label">Phone Number</span>
        <span class="info-value">{{ info.phone }}</span>
      </div>

      <!-- Date of Birth -->
      <div class="info-item">
        <span class="info-label">Date of Birth</span>
        <span class="info-value">{{ info.dob }}</span>
      </div>

      <!-- Gender -->
      <div class="info-item">
        <span class="info-label">Gender</span>
        <span class="info-value">{{ info.gender }}</span>
      </div>

      <!-- Full Address -->
      <div class="info-item full-width">
        <span class="info-label">Address</span>
        <span class="info-value">{{ info.address }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  info: {
    type: Object,
    required: true,
    default: () => ({
      name: 'Varun Karthik',
      email: 'varun.karthik@example.com',
      phone: '+91 98765 43210',
      dob: 'June 15, 2000',
      gender: 'Male',
      address: '123 Playmaker Avenue, Sports District, Chennai, 600001'
    })
  }
})

defineEmits(['edit'])
</script>

<script>
export default {
  name: 'ProfileInfoCard'
}
</script>

<style scoped>
.info-card {
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

.info-card:hover {
  border-color: rgba(79, 70, 229, 0.12);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
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

.edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.55rem 1rem;
  border-radius: 999px;
  background: #ffffff;
  border: 1.5px solid rgba(226, 232, 240, 0.8);
  color: #475569;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

.edit-btn:hover {
  border-color: rgba(79, 70, 229, 0.25);
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.02);
  transform: translateY(-1px);
}

.edit-btn:active {
  transform: translateY(0);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.info-item.full-width {
  grid-column: span 2;
}

.info-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 0.98rem;
  font-weight: 600;
  color: #334155;
  word-break: break-word;
  line-height: 1.5;
}

@media (max-width: 576px) {
  .info-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .info-item.full-width {
    grid-column: span 1;
  }

  .info-card {
    padding: 1.5rem;
  }

  .card-header {
    margin-bottom: 1.5rem;
  }
}
</style>
