<template>
      <div class="tab-pane">
        <!-- Shared data-state banner: keeps the admin tabs consistent with
             the member/staff screens, which already surface load errors. -->
            <div v-if="analyticsLoading" class="data-state data-state--loading">
              Loading live data…
            </div>
            <div v-else-if="analyticsError" class="data-state data-state--error" role="alert">
              {{ analyticsError }}
              <button class="data-state__retry" @click="reloadAdminData">Retry</button>
            </div>

            <!-- KPI Cards (4 cards) -->
            <section class="kpi-grid" aria-label="Key Performance Indicators">
              <div class="kpi-card" v-for="kpi in kpiCards" :key="kpi.title">
                <div class="kpi-header">
                  <div class="kpi-icon-box" :class="kpi.colorClass">
                    <svg
                      v-if="kpi.icon === 'members'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                    <svg
                      v-else-if="kpi.icon === 'courts'"
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
                    <svg
                      v-else-if="kpi.icon === 'bookings'"
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
                    <svg
                      v-else-if="kpi.icon === 'events'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M5 3v4M19 3v4M3 11h18M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                      />
                    </svg>
                  </div>
                  <span class="trend-badge" :class="kpi.trendType">
                    <span v-if="kpi.trendType === 'positive'">↑</span>
                    <span v-else-if="kpi.trendType === 'neutral'">•</span>
                    {{ kpi.trend }}
                  </span>
                </div>
                <div class="kpi-body">
                  <span class="kpi-title">{{ kpi.title }}</span>
                  <h3 class="kpi-value">{{ kpi.value }}</h3>
                </div>
              </div>
            </section>

            <!-- Upcoming Events Section (Moved to top below 4 KPI boxes) -->
            <section class="section-block">
              <div class="block-header">
                <h3>Upcoming Events</h3>
                <span class="subtext"
                  >Scheduled tournaments, coaching clinics, and facility maintenance</span
                >
              </div>

              <div class="events-grid">
                <div v-for="event in upcomingEvents" :key="event.id" class="admin-event-card">
                  <div class="event-card-top">
                    <span class="event-type-chip" :class="event.chipClass">{{ event.type }}</span>
                    <span class="event-status-pill" :class="event.statusClass">{{
                      event.status
                    }}</span>
                  </div>
                  <h4 class="event-card-title">{{ event.title }}</h4>
                  <div class="event-details">
                    <div class="detail-item">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                        width="16"
                        height="16"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                      </svg>
                      <span>{{ event.date }}</span>
                    </div>
                    <div class="detail-item">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                        width="16"
                        height="16"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                      <span>{{ event.info }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- Analytics Section (2 Dashboard Widgets) -->
            <section class="section-block">
              <div class="block-header">
                <h3>Analytics Overview</h3>
                <span class="subtext">Real-time facility utilization and booking statistics</span>
              </div>

              <div class="analytics-grid">
                <!-- Widget 1: Booking Trends -->
                <div class="widget-card">
                  <div class="widget-header">
                    <div>
                      <h4>Booking Trends</h4>
                      <p class="widget-subtitle">Weekly distribution by sport facility</p>
                    </div>
                    <span class="widget-badge">This Week</span>
                  </div>

                  <div class="chart-placeholder">
                    <div v-for="item in bookingTrends" :key="item.sport" class="chart-row">
                      <div class="row-info">
                        <span class="sport-name">{{ item.sport }}</span>
                        <span class="sport-count"
                          >{{ item.count }} bookings ({{ item.percentage }}%)</span
                        >
                      </div>
                      <div class="progress-track">
                        <div
                          class="progress-fill"
                          :style="{ width: item.percentage + '%' }"
                          :class="item.colorClass"
                        ></div>
                      </div>
                    </div>
                  </div>

                  <div class="widget-footer">
                    <div
                      v-for="item in bookingTrends"
                      :key="item.sport"
                      class="legend-item"
                    >
                      <span class="dot" :class="item.colorClass.replace('bar-', '')"></span>
                      {{ item.sport }}
                    </div>
                  </div>
                </div>

                <!-- Widget 2: Court Utilization -->
                <div class="widget-card">
                  <div class="widget-header">
                    <div>
                      <h4>Court Utilization</h4>
                      <p class="widget-subtitle">Peak occupancy breakdown by time slot</p>
                    </div>
                    <span class="widget-badge live">Live Peak</span>
                  </div>

                  <div class="chart-placeholder">
                    <div v-for="slot in courtUtilization" :key="slot.period" class="chart-row">
                      <div class="row-info">
                        <span class="sport-name">{{ slot.period }}</span>
                        <span class="sport-count">{{ slot.rate }}% Occupied</span>
                      </div>
                      <div class="progress-track">
                        <div
                          class="progress-fill"
                          :style="{ width: slot.rate + '%' }"
                          :class="slot.colorClass"
                        ></div>
                      </div>
                    </div>
                  </div>

                  <div class="utilization-summary">
                    <div class="summary-box">
                      <span class="summary-num">{{ analyticsKpis.utilisation }}</span>
                      <span class="summary-lbl">Avg. Occupancy</span>
                    </div>
                    <div class="summary-box">
                      <span class="summary-num">{{ analyticsKpis.peakHour }}</span>
                      <span class="summary-lbl">Peak Hours</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- Membership Overview & Recent Announcements -->
            <div class="dashboard-dual-grid">
              <!-- Membership Overview -->
              <div class="dual-column">
                <div class="card-box">
                  <div class="box-header">
                    <div class="header-title">
                      <div class="icon-bubble blue">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          stroke-width="2"
                          width="20"
                          height="20"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                          />
                        </svg>
                      </div>
                      <h3>Membership Overview</h3>
                    </div>
                    <span class="total-tag">{{ membershipOverview.total }} Total</span>
                  </div>

                  <div class="membership-list">
                    <div class="member-type-row">
                      <div class="member-type-info">
                        <span class="type-name">Permanent Members</span>
                        <span class="type-desc">Full club access & priority court booking</span>
                      </div>
                      <div class="member-type-stat">
                        <span class="type-value">{{ membershipOverview.permanent }}</span>
                        <span class="type-pct">{{ membershipOverview.permanentPct }}%</span>
                      </div>
                    </div>

                    <div class="member-type-row">
                      <div class="member-type-info">
                        <span class="type-name">Public Players</span>
                        <span class="type-desc">Pay-per-play & guest pass holders</span>
                      </div>
                      <div class="member-type-stat">
                        <span class="type-value">{{ membershipOverview.publicPlayers }}</span>
                        <span class="type-pct">{{ membershipOverview.publicPct }}%</span>
                      </div>
                    </div>

                    <div class="member-type-row highlighted">
                      <div class="member-type-info">
                        <span class="type-name">New Registrations</span>
                        <span class="type-desc">Signed up in the last 7 days</span>
                      </div>
                      <div class="member-type-stat">
                        <span class="type-value text-emerald">+64</span>
                        <span class="new-pill">This Week</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Recent Announcements -->
              <div class="dual-column">
                <div class="card-box">
                  <div class="box-header flex-between">
                    <div class="header-title">
                      <div class="icon-bubble orange">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          stroke-width="2"
                          width="20"
                          height="20"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"
                          />
                        </svg>
                      </div>
                      <h3>Recent Announcements</h3>
                    </div>
                    <button
                      class="view-all-link-btn"
                      @click="activeNav = 'Announcements'"
                      style="background: none; border: none; font-size: 0.82rem; font-weight: 600; color: #2563eb; cursor: pointer; padding: 0.25rem 0.5rem;"
                    >
                      View All →
                    </button>
                  </div>

                  <div v-if="announcements.length === 0" style="padding: 1.5rem 1rem; text-align: center; color: #94a3b8; font-size: 0.88rem;">
                    No announcements published yet.
                  </div>
                  <div v-else class="announcements-list">
                    <div
                      v-for="item in announcements.slice(0, 3)"
                      :key="item.id"
                      class="announcement-item"
                      style="cursor: pointer;"
                      @click="openAnnouncementDetails(item)"
                    >
                      <div class="announcement-top">
                        <div style="display: flex; align-items: center; gap: 0.4rem;">
                          <span class="announcement-badge" :class="item.categoryClass">{{
                            item.category
                          }}</span>
                          <span v-if="!item.is_read" class="unread-indicator-dot" title="Unread"></span>
                        </div>
                        <span class="announcement-date">{{ item.date }}</span>
                      </div>
                      <h4 class="announcement-title">{{ item.title }}</h4>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
</template>

<script setup>
import { inject } from 'vue'

const {
  activeNav,
  analyticsError,
  analyticsKpis,
  analyticsLoading,
  announcements,
  bookingTrends,
  courtUtilization,
  kpiCards,
  membershipOverview,
  openAnnouncementDetails,
  reloadAdminData,
  upcomingEvents
} = inject('adminContext')
</script>
