<template>
          <div class="tab-pane">
            <section class="section-block">
              <div class="block-header">
                <h3>System & Club Settings</h3>
                <span class="subtext"
                  >Manage facility parameters, operating hours, and default slot duration</span
                >
              </div>

              <div class="analytics-grid">
                <!-- CASE 1: CLUB EXISTS -> Update Mode -->
                <div v-if="courtStore.club" class="card-box">
                  <h4 class="settings-card-title">Club Information</h4>
                  <div class="setting-row">
                    <span class="setting-label">Club Name</span>
                    <input type="text" v-model="clubForm.name" class="settings-input" />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Club Address</span>
                    <input type="text" v-model="clubForm.address" class="settings-input" />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Contact Email</span>
                    <span class="setting-val">{{ adminProfile.email || 'Not set' }}</span>
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Contact Phone</span>
                    <span class="setting-val">{{ adminProfile.phone || 'Not set' }}</span>
                  </div>
                </div>

                <!-- CASE 2: NO CLUB -> Create Mode -->
                <div v-else class="card-box">
                  <h4 class="settings-card-title">Create Your Club</h4>
                  <p class="subtext" style="margin-bottom: 1rem">
                    You don't have a club yet. Create one to start adding courts.
                  </p>
                  <div class="setting-row">
                    <span class="setting-label">Club Name</span>
                    <input
                      type="text"
                      v-model="clubForm.name"
                      class="settings-input"
                      placeholder="e.g. Apex Sports Arena"
                    />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Club Address</span>
                    <input
                      type="text"
                      v-model="clubForm.address"
                      class="settings-input"
                      placeholder="Full physical address"
                    />
                  </div>
                </div>

                <!-- Operating Hours Card (Shared by both Create and Update) -->
                <div class="card-box">
                  <h4 class="settings-card-title">Operating Hours (Default)</h4>
                  <div class="setting-row">
                    <span class="setting-label">Open Time</span>
                    <input type="time" v-model="clubForm.open_time" class="settings-input" />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Close Time</span>
                    <input type="time" v-model="clubForm.close_time" class="settings-input" />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Slot Duration (mins)</span>
                    <input
                      type="number"
                      v-model="clubForm.slot_duration_minutes"
                      class="settings-input"
                      min="15"
                      step="15"
                    />
                  </div>

                  <!-- Dynamic Button -->
                  <button
                    class="btn-primary-action"
                    style="margin-top: 1rem; width: 100%"
                    @click="saveOrCreateClub"
                  >
                    {{ courtStore.club ? 'Save Default Settings' : 'Create Club' }}
                  </button>
                </div>
              </div>
            </section>
          </div>
</template>

<script setup>
import { inject } from 'vue'

const {
  adminProfile,
  clubForm,
  courtStore,
  saveOrCreateClub
} = inject('adminContext')
</script>
