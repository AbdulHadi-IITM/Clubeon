<template>
          <div class="tab-pane">
            <!-- Aesthetic Club Banner -->
            <div v-if="courtStore.club" class="club-banner glass">
              <div class="club-banner-icon">🏛️</div>
              <div class="club-banner-info">
                <h2>{{ courtStore.club.name }}</h2>
                <p>{{ courtStore.club.address }}</p>
                <div class="club-hours-badge">
                  <span
                    >🕒 {{ courtStore.club.open_time || 'N/A' }} -
                    {{ courtStore.club.close_time || 'N/A' }}</span
                  >
                  <span>⏱️ {{ courtStore.club.slot_duration_minutes || 60 }} min slots</span>
                </div>
              </div>
            </div>
            <div v-else class="club-banner glass-empty">
              <p>Club not set up yet. Add your first court to create your club.</p>
            </div>

            <!-- KPI Grid with Real Stats -->
            <section class="kpi-grid" aria-label="Court Performance Indicators">
              <div class="kpi-card">
                <div class="kpi-header">
                  <div class="kpi-icon-box emerald">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                      />
                    </svg>
                  </div>
                  <span class="trend-badge neutral">• All Facilities</span>
                </div>
                <div class="kpi-body">
                  <span class="kpi-title">Total Courts</span>
                  <h3 class="kpi-value">{{ totalCourts }}</h3>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-header">
                  <div class="kpi-icon-box blue">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                      />
                    </svg>
                  </div>
                  <span class="trend-badge positive">↑ Ready for Booking</span>
                </div>
                <div class="kpi-body">
                  <span class="kpi-title">Available Courts</span>
                  <h3 class="kpi-value">{{ activeCourtsCount }}</h3>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-header">
                  <div class="kpi-icon-box orange">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                      />
                    </svg>
                  </div>
                  <span class="trend-badge neutral">• Inactive / Maintenance</span>
                </div>
                <div class="kpi-body">
                  <span class="kpi-title">Under Maintenance</span>
                  <h3 class="kpi-value">{{ inactiveCourtsCount }}</h3>
                </div>
              </div>

              <div class="kpi-card">
                <div class="kpi-header">
                  <div class="kpi-icon-box purple">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>
                  <span class="trend-badge positive">↑ Peak Occupancy</span>
                </div>
                <div class="kpi-body">
                  <span class="kpi-title">Court Utilization</span>
                  <h3 class="kpi-value">{{ analyticsKpis.utilisation }}</h3>
                </div>
              </div>
            </section>

            <!-- Courts List Section with Date Picker -->
            <section class="section-block">
              <div class="block-header flex-between">
                <div>
                  <h3>Court Status Overview</h3>
                  <span class="subtext">Manage your club's courts and availability</span>
                </div>
                <div style="display: flex; gap: 1rem; align-items: center">
                  <button class="btn-primary-action" @click="openAddCourtModal">+ Add Court</button>
                </div>
              </div>

              <div v-if="courtStore.loading" class="loading-state">Loading courts...</div>
              <div v-else-if="courtStore.courts.length === 0" class="empty-state">
                <p>
                  You haven't created any courts yet. Click "Add Court" to set up your club's first
                  facility!
                </p>
              </div>
              <div v-else class="events-grid">
                <div v-for="court in courtStore.courts" :key="court.id" class="admin-event-card" style="padding: 0; overflow: hidden;">
                  <div style="height: 120px; width: 100%; position: relative; overflow: hidden; background: #0f172a;">
                    <img :src="getSportImage(court.name || court.sport_type)" :alt="court.name" style="width: 100%; height: 100%; object-fit: cover;" />
                    <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(15,23,42,0.6) 100%);"></div>
                    <span
                      class="event-status-pill"
                      :class="court.is_active ? 'status-open' : 'status-scheduled'"
                      style="position: absolute; top: 10px; right: 10px;"
                    >
                      {{ court.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <div style="padding: 1.25rem;">
                    <h4 class="event-card-title">{{ court.name }}</h4>
                    <div class="court-sport-type">{{ sportLabel(court.sport_type) }}</div>

                  <!-- Default/Custom Badge -->
                  <div class="court-settings-badge">
                    <span
                      v-if="
                        court.open_time_override ||
                        court.close_time_override ||
                        court.slot_duration_override
                      "
                      class="badge-custom"
                    >
                      ⚙️ Custom
                    </span>
                    <span v-else class="badge-default"> 🏛️ Default </span>
                  </div>

                  <div class="event-details">
                    <!-- Actions -->
                    <div class="detail-item" style="gap: 1rem; margin-top: 0.5rem">
                      <button @click="openEditCourtModal(court)" class="action-btn view-btn">
                        Edit
                      </button>
                      <button @click="handleDeleteCourt(court.id)" class="action-btn cancel-btn">
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            </section>
          </div>
</template>

<script setup>
import { inject } from 'vue'

const {
  activeCourtsCount,
  courtStore,
  handleDeleteCourt,
  inactiveCourtsCount,
  openAddCourtModal,
  openEditCourtModal,
  sportLabel,
  totalCourts
} = inject('adminContext')
</script>
