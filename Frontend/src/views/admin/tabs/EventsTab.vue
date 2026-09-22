<template>
          <div class="tab-pane">
            <!-- Dynamic KPI Cards for Events -->
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Events</span>
                <h3 class="kpi-value">{{ eventsKpis.total }}</h3>
                <span class="trend-badge neutral">• All scheduled events</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Upcoming & Active</span>
                <h3 class="kpi-value">{{ eventsKpis.upcoming }}</h3>
                <span class="trend-badge positive">↑ Active registration</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Total Attendees</span>
                <h3 class="kpi-value">{{ eventsKpis.totalRegistered }} / {{ eventsKpis.totalCapacity }}</h3>
                <span class="trend-badge positive">↑ High participation</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Event Revenue</span>
                <h3 class="kpi-value">₹{{ eventsKpis.totalRevenue.toLocaleString() }}</h3>
                <span class="trend-badge positive">• Collected entry fees</span>
              </div>
            </section>

            <!-- Events Toolbar & Section Header -->
            <section class="section-block">
              <div class="block-header bookings-toolbar-header">
                <div>
                  <h3>Club Events & Tournaments</h3>
                  <span class="subtext">Organize, schedule, edit, and manage club competitions & coaching clinics</span>
                </div>
                <div class="header-action-buttons">
                  <div class="view-toggle-group">
                    <button
                      class="view-toggle-btn"
                      :class="{ active: eventViewMode === 'grid' }"
                      @click="eventViewMode = 'grid'"
                      title="Grid View"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
                    </button>
                    <button
                      class="view-toggle-btn"
                      :class="{ active: eventViewMode === 'table' }"
                      @click="eventViewMode = 'table'"
                      title="Table View"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>
                    </button>
                  </div>
                  <button class="add-booking-btn" @click="openCreateEventModal">
                    + Create Event
                  </button>
                </div>
              </div>

              <!-- Filter & Search Bar -->
              <div class="card-box bookings-filter-box">
                <div class="filter-controls-row">
                  <div class="search-input-wrapper">
                    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    <input
                      type="text"
                      v-model="eventSearchQuery"
                      placeholder="Search event title, venue, organizer..."
                      class="booking-search-input"
                    />
                    <button v-if="eventSearchQuery" class="clear-search-btn" @click="eventSearchQuery = ''">×</button>
                  </div>

                  <div class="filter-dropdowns-group">
                    <div class="filter-select-group">
                      <select v-model="eventStatusFilter" class="filter-select">
                        <option value="All">All Statuses</option>
                        <option value="Upcoming">Upcoming</option>
                        <option value="Ongoing">Ongoing</option>
                        <option value="Completed">Completed</option>
                        <option value="Cancelled">Cancelled</option>
                      </select>
                    </div>

                    <div class="filter-select-group">
                      <select v-model="eventSportFilter" class="filter-select">
                        <option value="All">All Sports</option>
                        <option value="Tennis">Tennis</option>
                        <option value="Badminton">Badminton</option>
                        <option value="Squash">Squash</option>
                        <option value="Swimming">Swimming</option>
                        <option value="Social">Social</option>
                      </select>
                    </div>

                    <div class="filter-select-group">
                      <select v-model="eventTypeFilter" class="filter-select">
                        <option value="All">All Types</option>
                        <option value="Tournament">Tournament</option>
                        <option value="Coaching Clinic">Coaching Clinic</option>
                        <option value="Social League">Social League</option>
                      </select>
                    </div>

                    <div class="filter-select-group">
                      <select v-model="eventSortBy" class="filter-select">
                        <option value="date">Sort: Date (Soonest)</option>
                        <option value="title">Sort: Title (A-Z)</option>
                        <option value="registered">Sort: Most Filled</option>
                        <option value="fee">Sort: Fee (High-Low)</option>
                      </select>
                    </div>

                    <button
                      v-if="eventSearchQuery || eventStatusFilter !== 'All' || eventSportFilter !== 'All' || eventTypeFilter !== 'All'"
                      class="reset-filters-btn"
                      @click="resetEventFilters"
                    >
                      Reset
                    </button>
                  </div>
                </div>
              </div>

              <!-- Events Container Display -->
              <div v-if="filteredEvents.length === 0" class="card-box no-bookings-empty" style="margin-top: 1rem;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width: 48px; height: 48px; color: #94a3b8; margin-bottom: 1rem;"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                <p class="empty-title">No events found matching your criteria</p>
                <p class="empty-sub">Try resetting your search query or filters, or create a new event.</p>
              </div>

              <!-- Grid View -->
              <div v-else-if="eventViewMode === 'grid'" class="admin-events-grid-container" style="margin-top: 1rem;">
                <div v-for="evt in filteredEvents" :key="evt.id" class="event-card-rich" style="padding: 0; overflow: hidden;">
                  <div style="height: 130px; width: 100%; position: relative; overflow: hidden; background: #0f172a;">
                    <img :src="getSportImage(evt.title || evt.sport)" :alt="evt.title" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.9;" />
                    <div style="position: absolute; inset: 0; background: linear-gradient(180deg, transparent 40%, rgba(15,23,42,0.7) 100%);"></div>
                    <span class="sport-badge-pill" :class="'sport-' + evt.sport.toLowerCase()" style="position: absolute; top: 10px; left: 10px;">{{ evt.sport }}</span>
                    <span class="booking-status-badge" :class="'estatus-' + evt.status.toLowerCase()" style="position: absolute; top: 10px; right: 10px;">{{ evt.status }}</span>
                  </div>

                  <div class="event-card-rich-body">
                    <h4 class="event-rich-title">{{ evt.title }}</h4>
                    <span class="event-type-subtag">{{ evt.type }}</span>

                    <p class="event-rich-desc">{{ evt.description }}</p>

                    <div class="event-meta-list">
                      <div class="meta-row">
                        <svg class="meta-icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                        <span>{{ evt.dateDisplay }} • {{ evt.time }}</span>
                      </div>
                      <div class="meta-row">
                        <svg class="meta-icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                        <span>{{ evt.venue }}</span>
                      </div>
                      <div class="meta-row">
                        <svg class="meta-icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                        <span>{{ evt.registered }} / {{ evt.capacity }} Players Registered</span>
                      </div>
                      <div class="meta-row">
                        <svg class="meta-icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        <span class="font-semibold" style="color: #0f172a;">Entry Fee: {{ evt.fee > 0 ? '₹' + evt.fee : 'Free' }}</span>
                      </div>
                    </div>

                    <!-- Capacity Progress Bar -->
                    <div class="capacity-progress-wrapper">
                      <div class="capacity-progress-bar">
                        <div
                          class="capacity-progress-fill"
                          :style="{ width: Math.min(100, Math.round((evt.registered / evt.capacity) * 100)) + '%' }"
                          :class="{ full: evt.registered >= evt.capacity }"
                        ></div>
                      </div>
                    </div>
                  </div>

                  <div class="event-card-rich-footer">
                    <button class="action-icon-btn view-btn" @click="openEventDetails(evt)">
                      View Details
                    </button>
                    <div style="display: flex; gap: 0.35rem;">
                      <button class="action-icon-btn complete-btn" @click="openEditEventModal(evt)" title="Edit Event">
                        ✎ Edit
                      </button>
                      <button class="action-icon-btn cancel-btn" @click="requestDeleteEvent(evt)" title="Delete Event">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Table View -->
              <div v-else-if="eventViewMode === 'table'" class="card-box" style="margin-top: 1rem; overflow-x: auto;">
                <table class="admin-bookings-table">
                  <thead>
                    <tr>
                      <th>EVENT TITLE & TYPE</th>
                      <th>SPORT & VENUE</th>
                      <th>DATE & TIME</th>
                      <th>ATTENDEES & CAPACITY</th>
                      <th>FEE</th>
                      <th>STATUS</th>
                      <th style="text-align: right;">ACTIONS</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="evt in filteredEvents" :key="evt.id" class="booking-table-row">
                      <td>
                        <div class="player-info-meta">
                          <span class="user-name-txt" style="font-size: 0.95rem;">{{ evt.title }}</span>
                          <span class="user-email-txt">{{ evt.type }} • Organizer: {{ evt.organizer }}</span>
                        </div>
                      </td>
                      <td>
                        <div class="court-info-cell">
                          <span class="court-name-txt">{{ evt.venue }}</span>
                          <span class="sport-badge-pill" :class="'sport-' + evt.sport.toLowerCase()">{{ evt.sport }}</span>
                        </div>
                      </td>
                      <td>
                        <div class="court-info-cell">
                          <span class="font-semibold">{{ evt.dateDisplay }}</span>
                          <span class="time-subtxt">{{ evt.time }}</span>
                        </div>
                      </td>
                      <td>
                        <div class="court-info-cell">
                          <span class="font-bold" style="color: #2563eb;">{{ evt.registered }} / {{ evt.capacity }}</span>
                          <span class="time-subtxt">{{ evt.registered >= evt.capacity ? 'Fully Booked' : (evt.capacity - evt.registered) + ' spots left' }}</span>
                        </div>
                      </td>
                      <td>
                        <span class="amount-txt">{{ evt.fee > 0 ? '₹' + evt.fee : 'Free' }}</span>
                      </td>
                      <td>
                        <span class="booking-status-badge" :class="'estatus-' + evt.status.toLowerCase()">
                          {{ evt.status }}
                        </span>
                      </td>
                      <td style="text-align: right;">
                        <div class="table-actions-group">
                          <button class="action-icon-btn view-btn" @click="openEventDetails(evt)" title="View Details">Details</button>
                          <button class="action-icon-btn complete-btn" @click="openEditEventModal(evt)" title="Edit Event">Edit</button>
                          <button class="action-icon-btn cancel-btn" @click="requestDeleteEvent(evt)" title="Delete Event">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
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
  eventSearchQuery,
  eventSortBy,
  eventSportFilter,
  eventStatusFilter,
  eventTypeFilter,
  eventViewMode,
  eventsKpis,
  filteredEvents,
  openCreateEventModal,
  openEditEventModal,
  openEventDetails,
  requestDeleteEvent,
  resetEventFilters,
  totalCapacity,
  totalRegistered,
  totalRevenue
} = inject('adminContext')
</script>
