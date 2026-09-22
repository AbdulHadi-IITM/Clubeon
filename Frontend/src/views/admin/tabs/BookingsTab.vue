<template>
          <div class="tab-pane">
            <!-- Dynamic KPI Cards -->
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Bookings</span>
                <h3 class="kpi-value">{{ bookingKpis.total }}</h3>
                <span class="trend-badge positive">All recorded slots</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Active / Confirmed</span>
                <h3 class="kpi-value">{{ bookingKpis.confirmed }}</h3>
                <span class="trend-badge positive">↑ High Occupancy</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Completed (Auto & Manual)</span>
                <h3 class="kpi-value">{{ bookingKpis.completed }}</h3>
                <span class="trend-badge neutral">• {{ bookingKpis.autoCompleted }} time-completed</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Cancellations</span>
                <h3 class="kpi-value">{{ bookingKpis.cancelled }}</h3>
                <span class="trend-badge neutral">• {{ bookingKpis.cancelled }} refunded</span>
              </div>
            </section>

            <!-- Bookings Toolbar & Management Section -->
            <section class="section-block">
              <div class="block-header bookings-toolbar-header">
                <div>
                  <h3>Bookings & Reservations</h3>
                  <span class="subtext">Real-time schedule of court bookings • Time-based completion enabled</span>
                </div>
                <div class="header-action-buttons">
                  <button class="export-csv-btn" @click="exportBookingsCSV" title="Export to CSV">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 15px; height: 15px; margin-right: 6px;"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                    Export CSV
                  </button>
                  <button class="add-booking-btn" @click="openNewBookingModal">
                    + New Booking
                  </button>
                </div>
              </div>

              <!-- Filter & Search Controls Bar (Decluttered & Spacious) -->
              <div class="card-box bookings-filter-box">
                <div class="filter-controls-row">
                  <!-- Search Input -->
                  <div class="search-input-wrapper">
                    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    <input
                      type="text"
                      v-model="bookingSearchQuery"
                      placeholder="Search player, email, court, ID..."
                      class="booking-search-input"
                    />
                    <button v-if="bookingSearchQuery" class="clear-search-btn" @click="bookingSearchQuery = ''">×</button>
                  </div>

                  <div class="filter-dropdowns-group">
                    <!-- Status Filter -->
                    <div class="filter-select-group">
                      <select v-model="bookingStatusFilter" class="filter-select">
                        <option value="All">All Statuses</option>
                        <option value="Confirmed">Confirmed</option>
                        <option value="Completed">Completed</option>
                        <option value="Pending">Pending</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </div>

                    <!-- Facility/Sport Filter -->
                    <div class="filter-select-group">
                      <select v-model="bookingFacilityFilter" class="filter-select">
                        <option value="All">All Sports</option>
                        <option value="Tennis">Tennis</option>
                        <option value="Badminton">Badminton</option>
                        <option value="Squash">Squash</option>
                        <option value="Swimming">Swimming</option>
                      </select>
                    </div>

                    <!-- Timeframe Filter -->
                    <div class="filter-select-group">
                      <select v-model="bookingDateFilter" class="filter-select">
                        <option value="All">All Time</option>
                        <option value="Today">Today</option>
                        <option value="Upcoming">Upcoming</option>
                        <option value="Past">Past / Completed</option>
                      </select>
                    </div>

                    <!-- Sort By -->
                    <div class="filter-select-group">
                      <select v-model="bookingSortBy" class="filter-select">
                        <option value="newest">Sort: Newest First</option>
                        <option value="oldest">Sort: Oldest First</option>
                        <option value="name">Sort: Player A-Z</option>
                        <option value="amount">Sort: Fee High-Low</option>
                      </select>
                    </div>

                    <button
                      v-if="bookingSearchQuery || bookingStatusFilter !== 'All' || bookingFacilityFilter !== 'All' || bookingDateFilter !== 'All'"
                      class="reset-filters-btn"
                      @click="resetBookingFilters"
                      title="Reset Filters"
                    >
                      Reset
                    </button>
                  </div>
                </div>
              </div>

              <!-- Bookings Table Display (Clean, Spacious & Modern) -->
              <div class="card-box" style="margin-top: 1rem; overflow-x: auto;">
                <div v-if="bookingsLoading" class="no-bookings-empty">
                  <p class="empty-title">Loading bookings…</p>
                </div>

                <div v-else-if="filteredBookings.length === 0" class="no-bookings-empty">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width: 48px; height: 48px; color: #94a3b8; margin-bottom: 1rem;"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  <p class="empty-title">
                    {{ bookingsList.length ? 'No bookings match your filter' : 'No bookings yet' }}
                  </p>
                  <p class="empty-sub">
                    {{
                      bookingsList.length
                        ? 'Try adjusting your search query or dropdown filters.'
                        : 'Bookings made by members will appear here.'
                    }}
                  </p>
                </div>

                <table v-else class="admin-bookings-table">
                  <thead>
                    <tr>
                      <th>PLAYER & ID</th>
                      <th>COURT & SCHEDULE</th>
                      <th>FEE & PAYMENT</th>
                      <th>STATUS</th>
                      <th style="text-align: right;">ACTIONS</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="b in filteredBookings" :key="b.id" class="booking-table-row">
                      <!-- Player & ID -->
                      <td>
                        <div class="user-cell">
                          <div class="user-avatar-sm">{{ b.initials }}</div>
                          <div class="player-info-meta">
                            <div class="player-name-line">
                              <span class="user-name-txt">{{ b.player }}</span>
                              <span class="booking-ref-tag">{{ b.id }}</span>
                            </div>
                            <span class="user-email-txt">{{ b.email }} • <span class="usertype-tag">{{ b.userType }}</span></span>
                          </div>
                        </div>
                      </td>

                      <!-- Court & Schedule -->
                      <td>
                        <div class="court-info-cell">
                          <div class="facility-head-line">
                            <span class="court-name-txt">{{ b.facility }}</span>
                            <span class="sport-badge-pill" :class="'sport-' + b.sport.toLowerCase()">{{ b.sport }}</span>
                          </div>
                          <span class="time-subtxt">{{ b.dateDisplay }} ({{ b.date }}) • {{ b.time }}</span>
                        </div>
                      </td>

                      <!-- Fee & Payment -->
                      <td>
                        <div class="payment-cell">
                          <span class="amount-txt">₹{{ b.amount }}</span>
                          <span class="pay-status-tag" :class="'pay-' + b.paymentStatus.toLowerCase()">{{ b.paymentStatus }}</span>
                        </div>
                      </td>

                      <!-- Booking Status -->
                      <td>
                        <div style="display: flex; flex-direction: column; gap: 0.15rem; align-items: flex-start;">
                          <span class="booking-status-badge" :class="'bstatus-' + getEffectiveStatus(b).toLowerCase()">
                            {{ getEffectiveStatus(b) }}
                          </span>
                          <span v-if="isTimeCompleted(b)" class="auto-completed-hint">⏱ Time completed</span>
                        </div>
                      </td>

                      <!-- Clean Actions Column -->
                      <td style="text-align: right;">
                        <div class="table-actions-group">
                          <button class="action-icon-btn view-btn" title="View Full Details" @click="openBookingDetails(b)">
                            Details
                          </button>

                          <button
                            v-if="getEffectiveStatus(b) === 'Confirmed' || getEffectiveStatus(b) === 'Pending'"
                            class="action-icon-btn cancel-btn"
                            title="Cancel Booking"
                            @click="requestCancelBooking(b)"
                          >
                            Cancel
                          </button>

                          <button
                            v-if="getEffectiveStatus(b) === 'Confirmed'"
                            class="action-icon-btn complete-btn"
                            title="Mark Completed"
                            @click="markBookingCompleted(b)"
                          >
                            ✓
                          </button>
                        </div>
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
  bookingDateFilter,
  bookingFacilityFilter,
  bookingKpis,
  bookingSearchQuery,
  bookingSortBy,
  bookingStatusFilter,
  bookingsList,
  bookingsLoading,
  exportBookingsCSV,
  filteredBookings,
  getEffectiveStatus,
  isTimeCompleted,
  markBookingCompleted,
  openBookingDetails,
  openNewBookingModal,
  requestCancelBooking,
  resetBookingFilters
} = inject('adminContext')
</script>
