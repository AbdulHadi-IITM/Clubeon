<template>
          <div class="tab-pane">
            <section class="section-block">
              <div class="block-header flex-between flex-wrap gap-4">
                <div>
                  <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.5rem;">📢</span>
                    <h3 style="margin: 0;">Broadcast & Announcements Hub</h3>
                  </div>
                  <span class="subtext">Facility updates, tournament schedules, policy notices, and court maintenance</span>
                </div>
                <div class="header-action-buttons" style="display: flex; gap: 0.75rem; align-items: center;">
                  <button
                    class="btn-secondary-action"
                    title="Refresh Announcements"
                    @click="refreshAnnouncements"
                    :disabled="notificationStore.isLoading"
                    style="display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.55rem 0.95rem;"
                  >
                    <svg :class="{ 'spin-animate': notificationStore.isLoading }" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>Refresh</span>
                  </button>
                  <button
                    class="btn-primary-action"
                    @click="handleCreateAnnouncement"
                    style="display: inline-flex; align-items: center; gap: 0.4rem; background: linear-gradient(135deg, #2563eb, #4f46e5); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                    </svg>
                    <span>+ Create Announcement</span>
                  </button>
                </div>
              </div>

              <!-- Filter & Search Toolbar -->
              <div class="announcements-toolbar" style="margin-bottom: 1.25rem; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; background: #ffffff; padding: 1rem 1.25rem; border-radius: 1rem; border: 1px solid #e2e8f0; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);">
                <!-- Category Filter Pills -->
                <div class="filter-pills-group" style="display: flex; flex-wrap: wrap; gap: 0.45rem;">
                  <button
                    v-for="cat in [
                      { name: 'All', icon: '✨' },
                      { name: 'General', icon: '📢' },
                      { name: 'Broadcast', icon: '📣' },
                      { name: 'Tournament', icon: '🏆' },
                      { name: 'Policy', icon: '📜' },
                      { name: 'Maintenance', icon: '🛠️' }
                    ]"
                    :key="cat.name"
                    class="filter-pill-btn"
                    :class="{ active: announcementsCategoryFilter === cat.name }"
                    @click="announcementsCategoryFilter = cat.name"
                  >
                    <span>{{ cat.icon }} {{ cat.name }}</span>
                    <span v-if="cat.name === 'All'" class="pill-count">({{ announcements.length }})</span>
                    <span v-else class="pill-count">({{ announcements.filter(a => a.category.toLowerCase() === cat.name.toLowerCase()).length }})</span>
                  </button>
                </div>

                <!-- Search Input -->
                <div class="search-input-wrapper" style="position: relative; min-width: 280px;">
                  <svg style="position: absolute; left: 0.85rem; top: 50%; transform: translateY(-50%); color: #94a3b8;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  <input
                    v-model="announcementsSearchQuery"
                    type="text"
                    placeholder="Search announcements..."
                    class="announcement-search-input"
                    style="width: 100%; padding: 0.55rem 0.85rem 0.55rem 2.4rem; border: 1px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.88rem; outline: none; transition: border-color 0.2s;"
                  />
                  <button
                    v-if="announcementsSearchQuery"
                    @click="announcementsSearchQuery = ''"
                    style="position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%); background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 0.9rem;"
                  >✕</button>
                </div>
              </div>

              <div class="card-box" style="padding: 1.25rem;">
                <!-- Loading State -->
                <div v-if="notificationStore.isLoading && announcements.length === 0" class="announcements-loading" style="padding: 3.5rem; text-align: center; color: #64748b;">
                  <div class="spinner-sm" style="margin: 0 auto 1rem;"></div>
                  <p style="font-weight: 500;">Fetching facility announcements...</p>
                </div>

                <!-- Empty State -->
                <div v-else-if="filteredAnnouncements.length === 0" class="empty-announcements-state" style="padding: 3.5rem 2rem; text-align: center;">
                  <div style="width: 64px; height: 64px; margin: 0 auto 1.25rem; border-radius: 999px; background: linear-gradient(135deg, #eff6ff, #dbeafe); color: #2563eb; display: grid; place-items: center; font-size: 1.8rem; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);">
                    📢
                  </div>
                  <h4 style="font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 0.35rem;">No Announcements Found</h4>
                  <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 1.5rem; max-width: 420px; margin-left: auto; margin-right: auto; line-height: 1.5;">
                    {{ announcementsSearchQuery || announcementsCategoryFilter !== 'All' ? 'No announcements match your search or filter criteria. Try changing filters or clearing search.' : 'Keep your players and club members informed by broadcasting your first facility announcement.' }}
                  </p>
                  <button class="btn-primary-action" @click="handleCreateAnnouncement" style="padding: 0.65rem 1.25rem;">
                    + Create First Announcement
                  </button>
                </div>

                <!-- Announcements List -->
                <div v-else class="announcements-list-rich">
                  <div
                    v-for="item in filteredAnnouncements"
                    :key="item.id"
                    class="announcement-item-rich"
                    :style="{
                      borderLeftWidth: '5px',
                      borderLeftColor: item.category === 'Maintenance' ? '#ef4444' : item.category === 'Policy' ? '#f59e0b' : item.category === 'Tournament' ? '#10b981' : item.category === 'Broadcast' ? '#8b5cf6' : '#2563eb'
                    }"
                    @click="openAnnouncementDetails(item)"
                  >
                    <div class="announcement-item-main">
                      <div class="announcement-top" style="display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span class="announcement-badge" :class="item.categoryClass">
                          {{ item.icon }} {{ item.category }}
                        </span>
                        <span class="announcement-date" style="font-size: 0.82rem; color: #64748b; font-weight: 500;">
                          {{ item.date }}
                        </span>
                      </div>
                      <h4 class="announcement-title" style="font-size: 1.05rem; font-weight: 700; color: #0f172a; margin: 0 0 0.4rem; line-height: 1.35;">
                        {{ item.title }}
                      </h4>
                      <p v-if="item.body" class="announcement-body-preview" style="font-size: 0.88rem; color: #475569; line-height: 1.55; margin: 0;">
                        {{ item.body }}
                      </p>
                    </div>

                    <div class="announcement-item-actions" style="display: flex; align-items: center; gap: 0.5rem;" @click.stop>
                      <button
                        class="btn-view-announcement"
                        @click="openAnnouncementDetails(item)"
                        style="display: inline-flex; align-items: center; gap: 0.35rem;"
                      >
                        <span>View Details</span>
                        <span>→</span>
                      </button>
                      <button
                        class="btn-icon-trash"
                        title="Delete Announcement"
                        @click="handleDeleteAnnouncement(item)"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
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
  announcements,
  announcementsCategoryFilter,
  announcementsSearchQuery,
  filteredAnnouncements,
  handleCreateAnnouncement,
  handleDeleteAnnouncement,
  notificationStore,
  openAnnouncementDetails,
  refreshAnnouncements
} = inject('adminContext')
</script>
