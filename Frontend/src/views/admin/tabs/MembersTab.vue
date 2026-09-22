<template>
          <div class="tab-pane">
            <!-- Members Executive KPI Cards -->
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Registered Members</span>
                <h3 class="kpi-value">{{ totalMembers }}</h3>
                <span class="trend-badge neutral">• All members</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Active Memberships</span>
                <h3 class="kpi-value">{{ activeMembers }}</h3>
                <span class="trend-badge positive">↑ Active plans</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Total Bookings</span>
                <h3 class="kpi-value">{{ totalBookingsAll }}</h3>
                <span class="trend-badge neutral">• All time</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Recent Signups</span>
                <h3 class="kpi-value">{{ totalMembers }}</h3>
                <span class="trend-badge positive">↑ This month</span>
              </div>
            </section>

            <!-- Club Members Directory Table -->
            <section class="section-block">
              <div class="block-header bookings-toolbar-header">
                <div>
                  <h3>Club Members Directory</h3>
                  <span class="subtext">View registered members, membership plans, and booking activity</span>
                </div>
                <div class="header-action-buttons">
                  <button class="export-csv-btn" @click="exportMembersCSV">📥 Export CSV</button>
                </div>
              </div>

              <!-- Filter & Search Controls Bar -->
              <div class="card-box bookings-filter-box" style="margin-top: 1rem;">
                <div class="filter-controls-row">
                  <div class="search-input-wrapper">
                    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    <input
                      type="text"
                      v-model="memberSearchQuery"
                      placeholder="Search member name, email, or plan..."
                      class="booking-search-input"
                    />
                    <button v-if="memberSearchQuery" class="clear-search-btn" @click="memberSearchQuery = ''">×</button>
                  </div>

                  <!-- Plan Filter Pills -->
                  <div class="view-toggle-group">
                    <button
                      v-for="planFilter in ['All', 'Premium', 'Standard']"
                      :key="planFilter"
                      class="view-toggle-btn"
                      :class="{ active: selectedMemberPlanFilter === planFilter }"
                      @click="selectedMemberPlanFilter = planFilter"
                    >
                      {{ planFilter }}
                    </button>
                  </div>
                </div>
              </div>

              <!-- Members Table Card -->
              <div class="card-box" style="margin-top: 1rem; padding: 0; overflow: hidden;">
                <div v-if="filteredMembersList.length === 0" class="no-bookings-empty" style="padding: 3rem;">
                  <p class="empty-title">No members found</p>
                  <p class="empty-sub">Try adjusting your search or filter.</p>
                </div>
                <table v-else class="analytics-table">
                  <thead>
                  <tr>
                    <th>Member Details</th>
                    <th>Membership Plan</th>
                    <th>Date Joined</th>
                    <th>Total Bookings</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="m in filteredMembersList" :key="m.id">
                    <td>
                      <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div class="user-avatar-sm" style="background: linear-gradient(135deg, #2563eb, #4f46e5); color: #fff; font-weight: 700; display: grid; place-items: center; border-radius: 999px; width: 32px; height: 32px; font-size: 0.8rem;">{{ m.initials }}</div>
                        <div>
                          <strong style="color: #0f172a; font-size: 0.88rem; display: block;">{{ m.name }}</strong>
                          <span style="font-size: 0.78rem; color: #64748b;">{{ m.email }}</span>
                        </div>
                      </div>
                    </td>
                    <td>
              <span
                class="plan-badge"
                :style="{
                  background: m.plan.includes('VIP') ? '#fef3c7' : (m.plan.includes('Permanent') ? '#eff6ff' : '#f1f5f9'),
                  color: m.plan.includes('VIP') ? '#b45309' : (m.plan.includes('Permanent') ? '#1d4ed8' : '#475569'),
                  border: '1px solid ' + (m.plan.includes('VIP') ? '#fde68a' : (m.plan.includes('Permanent') ? '#bfdbfe' : '#e2e8f0')),
                  padding: '0.25rem 0.65rem',
                  borderRadius: '999px',
                  fontSize: '0.78rem',
                  fontWeight: '700'
                }"
              >
                {{ m.plan }}
              </span>
                    </td>
                    <td style="font-weight: 600; color: #334155; font-size: 0.82rem;">{{ m.dateJoined }}</td>
                    <td style="font-weight: 700; color: #0f172a; font-size: 0.84rem;">{{ m.totalBookings }} bookings</td>
                    <td>
              <span class="status-badge-chip" :class="m.membership_status === 'active' ? 'status-active' : 'status-completed'">
                {{ m.membership_status === 'active' ? 'Active' : 'Inactive' }}
              </span>
                    </td>
                    <td>
                      <button class="action-icon-btn view-btn" @click="viewMemberDetails(m)" title="View Member Profile">View Profile</button>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </section>
          </div>
</template>

<script setup>
import { inject } from 'vue'

const {
  activeMembers,
  exportMembersCSV,
  filteredMembersList,
  memberSearchQuery,
  members,
  selectedMemberPlanFilter,
  totalBookingsAll,
  totalMembers,
  viewMemberDetails
} = inject('adminContext')
</script>
