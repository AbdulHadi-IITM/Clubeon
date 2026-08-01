<template>
  <div class="admin-app-layout">
    <!-- Mobile Sidebar Backdrop -->
    <div
      v-if="isMobileSidebarOpen"
      class="sidebar-backdrop"
      @click="isMobileSidebarOpen = false"
    ></div>

    <!-- Fixed Left Sidebar -->
    <aside class="admin-sidebar" :class="{ 'mobile-show': isMobileSidebarOpen }">
      <!-- Sidebar Header / Logo -->
      <div class="sidebar-header">
        <router-link :to="{ name: 'landing' }" class="brand-logo" aria-label="ClubDash Home">
          <span class="logo-mark">⚡</span>
          <span class="logo-text">ClubDash</span>
        </router-link>
        <span class="admin-portal-badge">Admin</span>
      </div>

      <!-- Navigation Menu -->
      <nav class="sidebar-menu" aria-label="Admin Sidebar Navigation">
        <div class="menu-group">
          <span class="menu-label">OVERVIEW</span>
          <a
            v-for="item in primaryNavItems"
            :key="item.name"
            href="#"
            class="menu-item"
            :class="{ active: activeNav === item.name }"
            @click.prevent="setActiveNav(item.name)"
          >
            <div class="item-icon-wrapper">
              <!-- SVG Icons -->
              <svg
                v-if="item.icon === 'dashboard'"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
                />
              </svg>
              <svg
                v-else-if="item.icon === 'members'"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                />
              </svg>
              <svg
                v-else-if="item.icon === 'courts'"
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
                v-else-if="item.icon === 'bookings'"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <svg
                v-else-if="item.icon === 'events'"
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
              <svg
                v-else-if="item.icon === 'announcements'"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"
                />
              </svg>
              <svg
                v-else-if="item.icon === 'analytics'"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
              <svg
                v-else-if="item.icon === 'settings'"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            </div>
            <span class="item-name">{{ item.name }}</span>
            <span v-if="item.badge" class="item-badge">{{ item.badge }}</span>
          </a>
        </div>
      </nav>

      <!-- Sidebar Footer / Logout -->
      <div class="sidebar-footer">
        <a href="#" class="menu-item logout-link" @click.prevent="handleLogout">
          <div class="item-icon-wrapper">
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
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
          </div>
          <span class="item-name">Logout</span>
        </a>
      </div>
    </aside>

    <!-- Main Application Wrapper -->
    <div class="main-wrapper">
      <!-- Top Header -->
      <header class="admin-top-header">
        <div class="header-left">
          <button
            class="mobile-menu-btn"
            @click="isMobileSidebarOpen = !isMobileSidebarOpen"
            aria-label="Toggle Sidebar"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
              width="22"
              height="22"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div class="page-title-block">
            <h1 class="header-title">{{ headerTitle }}</h1>
            <p class="header-subtitle">{{ headerSubtitle }}</p>
          </div>
        </div>

        <div class="header-right">
          <!-- Live Date Chip -->
          <div class="header-date-chip">
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
            <span>{{ currentDate }}</span>
          </div>

          <!-- Notification Bell -->
          <button class="header-action-btn" aria-label="Notifications" @click="handleNotifications">
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
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 01-6 0v-1m6 0H9"
              />
            </svg>
            <span class="unread-dot">3</span>
          </button>

          <!-- Admin Avatar & Profile -->
          <div class="admin-user-profile">
            <div class="user-avatar">
              <span>AD</span>
            </div>
            <div class="user-meta">
              <span class="user-name">Alex Morgan</span>
              <span class="user-role">Super Admin</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Dashboard Main Scrollable Area -->
      <main class="dashboard-body">
        <div class="content-container">
          <!-- TAB 1: DASHBOARD (MAIN OVERVIEW) -->
          <div v-if="activeNav === 'Dashboard'" class="tab-pane">
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
                        d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
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

            <!-- Quick Actions Section -->
            <section class="section-block">
              <div class="block-header">
                <h3>Quick Actions</h3>
                <span class="subtext">Administrative tools and workflows</span>
              </div>

              <div class="quick-actions-grid">
                <button
                  v-for="action in quickActions"
                  :key="action.title"
                  class="action-card"
                  @click="handleQuickAction(action.title)"
                >
                  <div class="action-icon" :class="action.colorClass">
                    <svg
                      v-if="action.icon === 'users'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                      />
                    </svg>
                    <svg
                      v-else-if="action.icon === 'court'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                    <svg
                      v-else-if="action.icon === 'calendar'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    <svg
                      v-else-if="action.icon === 'megaphone'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z"
                      />
                    </svg>
                    <svg
                      v-else-if="action.icon === 'chart'"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                  </div>
                  <div class="action-info">
                    <span class="action-title">{{ action.title }}</span>
                    <span class="action-desc">{{ action.desc }}</span>
                  </div>
                  <div class="action-arrow">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                      width="16"
                      height="16"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </button>
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
                    <div class="legend-item"><span class="dot blue"></span> Tennis</div>
                    <div class="legend-item"><span class="dot emerald"></span> Badminton</div>
                    <div class="legend-item"><span class="dot orange"></span> Squash</div>
                    <div class="legend-item"><span class="dot purple"></span> Swimming</div>
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
                      <span class="summary-num">87.5%</span>
                      <span class="summary-lbl">Avg. Occupancy</span>
                    </div>
                    <div class="summary-box">
                      <span class="summary-num">5:00 - 9:00 PM</span>
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
                    <span class="total-tag">1,248 Total</span>
                  </div>

                  <div class="membership-list">
                    <div class="member-type-row">
                      <div class="member-type-info">
                        <span class="type-name">Permanent Members</span>
                        <span class="type-desc">Full club access & priority court booking</span>
                      </div>
                      <div class="member-type-stat">
                        <span class="type-value">820</span>
                        <span class="type-pct">65.7%</span>
                      </div>
                    </div>

                    <div class="member-type-row">
                      <div class="member-type-info">
                        <span class="type-name">Public Players</span>
                        <span class="type-desc">Pay-per-play & guest pass holders</span>
                      </div>
                      <div class="member-type-stat">
                        <span class="type-value">428</span>
                        <span class="type-pct">34.3%</span>
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
                  <div class="box-header">
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
                  </div>

                  <div class="announcements-list">
                    <div v-for="item in announcements" :key="item.id" class="announcement-item">
                      <div class="announcement-top">
                        <span class="announcement-badge" :class="item.categoryClass">{{
                          item.category
                        }}</span>
                        <span class="announcement-date">{{ item.date }}</span>
                      </div>
                      <h4 class="announcement-title">{{ item.title }}</h4>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Upcoming Events Section -->
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
                          d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                        />
                      </svg>
                      <span>{{ event.info }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- TAB 2: MEMBERS PREVIEW -->
          <div v-else-if="activeNav === 'Members'" class="tab-pane">
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Members</span>
                <h3 class="kpi-value">1,248</h3>
                <span class="trend-badge positive">↑ +12.4% this month</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Active Members</span>
                <h3 class="kpi-value">1,180</h3>
                <span class="trend-badge positive">↑ 94.5% Active Rate</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Pending Requests</span>
                <h3 class="kpi-value">14</h3>
                <span class="trend-badge neutral">• Action Required</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Recent Registrations</span>
                <h3 class="kpi-value">64</h3>
                <span class="trend-badge positive">↑ This Week</span>
              </div>
            </section>

            <section class="section-block">
              <div class="block-header">
                <h3>Pending Membership Requests</h3>
                <span class="subtext">Review and approve new member applications</span>
              </div>

              <div class="card-box">
                <div class="pending-list">
                  <div v-for="req in pendingRequests" :key="req.email" class="pending-row">
                    <div class="user-cell">
                      <div class="user-avatar-sm">{{ req.initials }}</div>
                      <div>
                        <span class="user-name-txt">{{ req.name }}</span>
                        <span class="user-email-txt">{{ req.email }}</span>
                      </div>
                    </div>
                    <span class="plan-badge">{{ req.plan }}</span>
                    <span class="date-txt">{{ req.date }}</span>
                    <div class="action-buttons">
                      <button class="btn-approve" @click="handleMemberAction('Approve', req.name)">
                        Approve
                      </button>
                      <button class="btn-decline" @click="handleMemberAction('Decline', req.name)">
                        Decline
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- TAB 3: COURTS PREVIEW -->
          <div v-else-if="activeNav === 'Courts'" class="tab-pane">
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
                  <h3 class="kpi-value">87.5%</h3>
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
                <div v-for="court in courtStore.courts" :key="court.id" class="admin-event-card">
                  <div class="event-card-top">
                    <span class="event-type-chip chip-blue">Court</span>
                    <span
                      class="event-status-pill"
                      :class="court.is_active ? 'status-open' : 'status-scheduled'"
                    >
                      {{ court.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <h4 class="event-card-title">{{ court.name }}</h4>

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
            </section>
          </div>

          <!-- TAB 4: BOOKINGS PREVIEW -->
          <div v-else-if="activeNav === 'Bookings'" class="tab-pane">
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Today's Bookings</span>
                <h3 class="kpi-value">42</h3>
                <span class="trend-badge positive">↑ +8 vs yesterday</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Upcoming (7 Days)</span>
                <h3 class="kpi-value">215</h3>
                <span class="trend-badge positive">↑ High Demand</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Completed Today</span>
                <h3 class="kpi-value">28</h3>
                <span class="trend-badge neutral">• On Schedule</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Cancellations</span>
                <h3 class="kpi-value">3</h3>
                <span class="trend-badge neutral">• Low Rate</span>
              </div>
            </section>

            <section class="section-block">
              <div class="block-header">
                <h3>Recent Reservations</h3>
                <span class="subtext">Real-time schedule of court bookings</span>
              </div>

              <div class="card-box">
                <div class="pending-list">
                  <div v-for="b in recentBookings" :key="b.id" class="pending-row">
                    <div class="user-cell">
                      <div class="user-avatar-sm">{{ b.initials }}</div>
                      <div>
                        <span class="user-name-txt">{{ b.player }}</span>
                        <span class="user-email-txt">{{ b.facility }}</span>
                      </div>
                    </div>
                    <span class="date-txt">{{ b.time }}</span>
                    <span class="event-status-pill" :class="b.statusClass">{{ b.status }}</span>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- TAB 5: EVENTS PREVIEW -->
          <div v-else-if="activeNav === 'Events'" class="tab-pane">
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Active Events</span>
                <h3 class="kpi-value">6</h3>
                <span class="trend-badge neutral">• Scheduled this month</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Tournament Entries</span>
                <h3 class="kpi-value">32 / 32</h3>
                <span class="trend-badge positive">↑ Fully Booked</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Upcoming Clinics</span>
                <h3 class="kpi-value">2</h3>
                <span class="trend-badge positive">↑ Coaching Sessions</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Completed Events</span>
                <h3 class="kpi-value">18</h3>
                <span class="trend-badge neutral">• This Season</span>
              </div>
            </section>

            <section class="section-block">
              <div class="block-header">
                <h3>Upcoming Tournaments & Clinics</h3>
                <span class="subtext">Manage upcoming competitive leagues and masterclasses</span>
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
                      <span>Date: {{ event.date }}</span>
                    </div>
                    <div class="detail-item">
                      <span>Attendees: {{ event.info }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- TAB 6: ANNOUNCEMENTS PREVIEW -->
          <div v-else-if="activeNav === 'Announcements'" class="tab-pane">
            <section class="section-block">
              <div class="block-header flex-between">
                <div>
                  <h3>Broadcast Announcements</h3>
                  <span class="subtext">Facility updates, policy changes, and tournament news</span>
                </div>
                <button class="btn-primary-action" @click="handleCreateAnnouncement">
                  + Create Announcement
                </button>
              </div>

              <div class="card-box">
                <div class="announcements-list">
                  <div v-for="item in announcements" :key="item.id" class="announcement-item">
                    <div class="announcement-top">
                      <span class="announcement-badge" :class="item.categoryClass">{{
                        item.category
                      }}</span>
                      <span class="announcement-date">{{ item.date }}</span>
                    </div>
                    <h4 class="announcement-title">{{ item.title }}</h4>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- TAB 7: ANALYTICS PREVIEW -->
          <div v-else-if="activeNav === 'Analytics'" class="tab-pane">
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Revenue</span>
                <h3 class="kpi-value">$48,250</h3>
                <span class="trend-badge positive">↑ +14.2% YoY</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Peak Booking Hour</span>
                <h3 class="kpi-value">6 - 8 PM</h3>
                <span class="trend-badge positive">↑ 92% Occupancy</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Membership Growth</span>
                <h3 class="kpi-value">+64</h3>
                <span class="trend-badge positive">↑ This Week</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Retention Rate</span>
                <h3 class="kpi-value">94.8%</h3>
                <span class="trend-badge positive">↑ Member Satisfaction</span>
              </div>
            </section>

            <section class="section-block">
              <div class="analytics-grid">
                <div class="widget-card">
                  <div class="widget-header">
                    <h4>Booking Trends</h4>
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
                </div>

                <div class="widget-card">
                  <div class="widget-header">
                    <h4>Peak Hours Occupancy</h4>
                    <span class="widget-badge live">Live</span>
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
                </div>
              </div>
            </section>
          </div>

          <!-- TAB 8: SETTINGS PREVIEW -->
          <div v-else-if="activeNav === 'Settings'" class="tab-pane">
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
                    <span class="setting-val">admin@clubdash.com</span>
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">Contact Phone</span>
                    <span class="setting-val">+1 (555) 234-5678</span>
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

          <!-- ADD COURT MODAL -->
          <div v-if="showAddCourtModal" class="modal-overlay" role="dialog" aria-modal="true">
            <div class="modal-card">
              <div class="modal-header">
                <h3>
                  {{
                    courtStore.courts.length === 0
                      ? 'Setup Your Club & First Court'
                      : 'Create New Court'
                  }}
                </h3>
                <button @click="closeAddCourtModal" class="close-btn">×</button>
              </div>
              <form @submit.prevent="handleCreateCourt" class="modal-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Court Name</label>
                    <input
                      type="text"
                      v-model="courtForm.court_name"
                      placeholder="e.g. Tennis Court 1"
                      required
                    />
                  </div>
                </div>

                <!-- Show Club setup fields only if this is the first court (courts array is empty) -->
                <div v-if="!courtStore.club" class="form-row">
                  <div class="form-group">
                    <label>Club Name</label>
                    <input
                      type="text"
                      v-model="courtForm.club_name"
                      placeholder="e.g. Apex Sports Arena"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label>Club Address</label>
                    <input
                      type="text"
                      v-model="courtForm.club_address"
                      placeholder="Full physical address"
                      required
                    />
                  </div>
                </div>

                <div class="modal-actions">
                  <button type="button" @click="closeAddCourtModal" class="cancel-modal-btn">
                    Cancel
                  </button>
                  <button type="submit" class="submit-modal-btn">Create Court</button>
                </div>
              </form>
            </div>
          </div>

          <!-- EDIT COURT MODAL -->
          <div v-if="showEditCourtModal" class="modal-overlay" role="dialog" aria-modal="true">
            <div class="modal-card">
              <div class="modal-header">
                <h3>Edit Court</h3>
                <button @click="closeEditCourtModal" class="close-btn">×</button>
              </div>
              <form @submit.prevent="handleUpdateCourt" class="modal-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Court Name</label>
                    <input type="text" v-model="courtForm.court_name" required />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Status</label>
                    <select v-model="courtForm.is_active">
                      <option :value="true">Active</option>
                      <option :value="false">Inactive</option>
                    </select>
                  </div>
                </div>

                <!-- Toggle: Use Defaults or Custom -->
                <div class="toggle-section">
                  <label class="toggle-label">Operating Hours & Slot Duration</label>
                  <div class="toggle-group">
                    <button
                      type="button"
                      class="toggle-btn"
                      :class="{ active: courtForm.use_defaults }"
                      @click="courtForm.use_defaults = true"
                    >
                      Use Club Defaults
                    </button>
                    <button
                      type="button"
                      class="toggle-btn"
                      :class="{ active: !courtForm.use_defaults }"
                      @click="courtForm.use_defaults = false"
                    >
                      Custom Settings
                    </button>
                  </div>
                </div>

                <!-- Override inputs – enabled only when custom is selected -->
                <div class="form-row" :class="{ 'disabled-section': courtForm.use_defaults }">
                  <div class="form-group">
                    <label>Open Time</label>
                    <input
                      type="time"
                      v-model="courtForm.open_time_override"
                      :disabled="courtForm.use_defaults"
                    />
                  </div>
                  <div class="form-group">
                    <label>Close Time</label>
                    <input
                      type="time"
                      v-model="courtForm.close_time_override"
                      :disabled="courtForm.use_defaults"
                    />
                  </div>
                </div>
                <div class="form-row" :class="{ 'disabled-section': courtForm.use_defaults }">
                  <div class="form-group">
                    <label>Slot Duration (minutes)</label>
                    <input
                      type="number"
                      v-model="courtForm.slot_duration_override"
                      :disabled="courtForm.use_defaults"
                      min="15"
                      step="15"
                      placeholder="e.g. 60"
                    />
                  </div>
                </div>

                <div class="modal-actions">
                  <button type="button" @click="closeEditCourtModal" class="cancel-modal-btn">
                    Cancel
                  </button>
                  <button type="submit" class="submit-modal-btn">Save Changes</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCourtStore } from '@/stores/courts'

const toast = inject('toast')
const courtStore = useCourtStore()
const showAddCourtModal = ref(false)
const showEditCourtModal = ref(false)
const currentEditCourt = ref(null)
const router = useRouter()
const auth = useAuthStore()
const isMobileSidebarOpen = ref(false)
const activeNav = ref('Dashboard')

const currentDate = ref(
  new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }),
)

const totalCourts = computed(() => courtStore.courts.length)
const activeCourtsCount = computed(() => courtStore.courts.filter((c) => c.is_active).length)
const inactiveCourtsCount = computed(() => courtStore.courts.filter((c) => !c.is_active).length)

// Form state for modals
const clubForm = ref({
  name: '',
  address: '',
  open_time: '',
  close_time: '',
  slot_duration_minutes: 60,
})

const courtForm = ref({
  court_name: '',
  is_active: true,
  use_defaults: true, // new
  open_time_override: '',
  close_time_override: '',
  slot_duration_override: '',
})

// Fetch data on mount
onMounted(() => {
  courtStore.fetchCourts()
})

watch(
  () => courtStore.club,
  (newClub) => {
    if (newClub) {
      clubForm.value = {
        name: newClub.name,
        address: newClub.address || '',
        open_time: newClub.open_time || '',
        close_time: newClub.close_time || '',
        slot_duration_minutes: newClub.slot_duration_minutes || 60,
      }
    } else {
      // Reset the form if no club exists
      clubForm.value = {
        name: '',
        address: '',
        open_time: '',
        close_time: '',
        slot_duration_minutes: 60,
      }
    }
  },
  { immediate: true },
)

// Modal Handlers
const openAddCourtModal = () => {
  courtForm.value = { court_name: '', club_name: '', club_address: '', is_active: true }
  showAddCourtModal.value = true
}

const closeAddCourtModal = () => {
  showAddCourtModal.value = false
}

const handleCreateCourt = async () => {
  const result = await courtStore.createCourt(courtForm.value)
  if (result.success) {
    closeAddCourtModal()
    toast.success('Court created successfully! 🎾')
  } else {
    toast.error(result.error || 'Failed to create court')
  }
}

const closeEditCourtModal = () => {
  showEditCourtModal.value = false
  currentEditCourt.value = null
}

const handleUpdateCourt = async () => {
  const payload = {
    court_name: courtForm.value.court_name,
    is_active: courtForm.value.is_active,
    open_time_override: courtForm.value.use_defaults
      ? null
      : courtForm.value.open_time_override || null,
    close_time_override: courtForm.value.use_defaults
      ? null
      : courtForm.value.close_time_override || null,
    slot_duration_override: courtForm.value.use_defaults
      ? null
      : courtForm.value.slot_duration_override
        ? Number(courtForm.value.slot_duration_override)
        : null,
  }
  const result = await courtStore.updateCourt(currentEditCourt.value.id, payload)
  if (result.success) {
    closeEditCourtModal()
    toast.success('Court updated successfully! ✨')
  } else {
    toast.error(result.error || 'Failed to update court')
  }
}

const handleDeleteCourt = async (courtId) => {
  if (confirm('Are you sure you want to delete this court?')) {
    const result = await courtStore.deleteCourt(courtId)
    if (result.success) {
      toast.success('Court deleted successfully.')
    } else {
      toast.error(result.error || 'Failed to delete court')
    }
  }
}

const saveOrCreateClub = async () => {
  if (courtStore.club) {
    // === UPDATE ===
    const result = await courtStore.updateClubSettings({
      name: clubForm.value.name,
      address: clubForm.value.address,
      open_time: clubForm.value.open_time || null,
      close_time: clubForm.value.close_time || null,
      slot_duration_minutes: clubForm.value.slot_duration_minutes || null,
    })
    if (result.success) {
      toast.success('Club settings updated successfully!')
    } else {
      toast.error(result.error || 'Failed to update club settings')
    }
  } else {
    // === CREATE ===
    if (!clubForm.value.name || !clubForm.value.address) {
      toast.error('Please provide a Club Name and Address')
      return
    }
    const result = await courtStore.createClub({
      name: clubForm.value.name,
      address: clubForm.value.address,
      open_time: clubForm.value.open_time || null,
      close_time: clubForm.value.close_time || null,
      slot_duration_minutes: clubForm.value.slot_duration_minutes || null,
    })
    if (result.success) {
      toast.success('Club created successfully! 🏛️')
      // fetchCourts() is already called inside createClub, so the UI will auto-switch to Update mode.
    } else {
      toast.error(result.error || 'Failed to create club')
    }
  }
}

const openEditCourtModal = (court) => {
  currentEditCourt.value = court
  const hasOverrides =
    court.open_time_override || court.close_time_override || court.slot_duration_override
  courtForm.value = {
    court_name: court.name,
    is_active: court.is_active,
    use_defaults: !hasOverrides,
    open_time_override: court.open_time_override || '',
    close_time_override: court.close_time_override || '',
    slot_duration_override: court.slot_duration_override || '',
  }
  showEditCourtModal.value = true
}

// Header title and subtitle reactive computation based on active sidebar tab
const headerTitle = computed(() => {
  switch (activeNav.value) {
    case 'Members':
      return 'Members Management'
    case 'Courts':
      return 'Facility & Courts'
    case 'Bookings':
      return 'Bookings & Reservations'
    case 'Events':
      return 'Events & Tournaments'
    case 'Announcements':
      return 'Announcements & Broadcasts'
    case 'Analytics':
      return 'Performance & Analytics'
    case 'Settings':
      return 'System Settings'
    default:
      return 'Admin Dashboard'
  }
})

const headerSubtitle = computed(() => {
  switch (activeNav.value) {
    case 'Members':
      return 'Overview of registered club members, pending requests, and player accounts.'
    case 'Courts':
      return 'Monitor court availability, status, and maintenance schedules.'
    case 'Bookings':
      return 'Track active reservations, upcoming court slots, and cancellations.'
    case 'Events':
      return 'Organize tournaments, coaching sessions, and social club activities.'
    case 'Announcements':
      return 'Broadcast facility notices, schedule updates, and tournament alerts.'
    case 'Analytics':
      return 'Detailed statistics on booking trends, peak hours, and membership growth.'
    case 'Settings':
      return 'Configure club information, operating hours, and notification preferences.'
    default:
      return 'Welcome back, Administrator • Monitor club operations and analytics.'
  }
})

// Primary Sidebar Navigation Items
const primaryNavItems = ref([
  { name: 'Dashboard', icon: 'dashboard' },
  { name: 'Members', icon: 'members', badge: '1,248' },
  { name: 'Courts', icon: 'courts' },
  { name: 'Bookings', icon: 'bookings', badge: '42' },
  { name: 'Events', icon: 'events' },
  { name: 'Announcements', icon: 'announcements' },
  { name: 'Analytics', icon: 'analytics' },
  { name: 'Settings', icon: 'settings' },
])

const setActiveNav = (navName) => {
  activeNav.value = navName
  isMobileSidebarOpen.value = false
}

const handleLogout = async () => {
  await auth.logout()
  router.push({ name: 'login' })
}

const handleNotifications = () => {
  alert('3 New Notifications: 1 system update, 2 event registrations')
}

const handleMemberAction = (action, name) => {
  alert(`${action} request for ${name}`)
}

const handleCreateAnnouncement = () => {
  alert('Open Create Announcement modal')
}

// KPI Cards mock data
const kpiCards = ref([
  {
    title: 'Total Members',
    value: '1,248',
    icon: 'members',
    colorClass: 'blue',
    trend: '+12.4% this month',
    trendType: 'positive',
  },
  {
    title: 'Active Courts',
    value: '14 / 16',
    icon: 'courts',
    colorClass: 'emerald',
    trend: '87.5% operational',
    trendType: 'neutral',
  },
  {
    title: "Today's Bookings",
    value: '42',
    icon: 'bookings',
    colorClass: 'purple',
    trend: '+8 vs yesterday',
    trendType: 'positive',
  },
  {
    title: 'Active Events',
    value: '6',
    icon: 'events',
    colorClass: 'orange',
    trend: '2 starting today',
    trendType: 'neutral',
  },
])

// Quick Actions mock list
const quickActions = ref([
  {
    title: 'Manage Members',
    desc: 'View & edit member profiles',
    icon: 'users',
    colorClass: 'blue',
  },
  {
    title: 'Manage Courts',
    desc: 'Update court availability',
    icon: 'court',
    colorClass: 'emerald',
  },
  {
    title: 'Manage Events',
    desc: 'Create & schedule tournaments',
    icon: 'calendar',
    colorClass: 'purple',
  },
  {
    title: 'Announcements',
    desc: 'Broadcast news & updates',
    icon: 'megaphone',
    colorClass: 'orange',
  },
  {
    title: 'View Analytics',
    desc: 'Detailed revenue & stats',
    icon: 'chart',
    colorClass: 'indigo',
  },
])

const handleQuickAction = (actionTitle) => {
  if (actionTitle === 'Manage Members') activeNav.value = 'Members'
  else if (actionTitle === 'Manage Courts') activeNav.value = 'Courts'
  else if (actionTitle === 'Manage Events') activeNav.value = 'Events'
  else if (actionTitle === 'Announcements') activeNav.value = 'Announcements'
  else if (actionTitle === 'View Analytics') activeNav.value = 'Analytics'
  else alert(`Quick Action triggered: ${actionTitle}`)
}

// Pending Requests mock data for Members tab
const pendingRequests = ref([
  {
    name: 'John Smith',
    email: 'john.smith@example.com',
    initials: 'JS',
    plan: 'Gold Member',
    date: 'Applied Jul 22',
  },
  {
    name: 'Sarah Jenkins',
    email: 'sarah.j@example.com',
    initials: 'SJ',
    plan: 'Regular Member',
    date: 'Applied Jul 21',
  },
  {
    name: 'Mike Ross',
    email: 'mike.ross@example.com',
    initials: 'MR',
    plan: 'VIP Pass',
    date: 'Applied Jul 20',
  },
])

// Recent Bookings mock data for Bookings tab
const recentBookings = ref([
  {
    id: 101,
    player: 'John Doe',
    facility: 'Tennis Court 2',
    time: 'Today, 5:00 - 7:00 PM',
    initials: 'JD',
    status: 'Confirmed',
    statusClass: 'status-confirmed',
  },
  {
    id: 102,
    player: 'Jane Smith',
    facility: 'Badminton Arena A',
    time: 'Today, 6:00 - 7:30 PM',
    initials: 'JS',
    status: 'Confirmed',
    statusClass: 'status-confirmed',
  },
  {
    id: 103,
    player: 'Robert Paul',
    facility: 'Squash Court 2',
    time: 'Today, 7:00 - 8:00 PM',
    initials: 'RP',
    status: 'Cancelled',
    statusClass: 'status-scheduled',
  },
])

// Analytics - Booking Trends mock data
const bookingTrends = ref([
  { sport: 'Tennis Courts', count: 189, percentage: 45, colorClass: 'bar-blue' },
  { sport: 'Badminton Arenas', count: 126, percentage: 30, colorClass: 'bar-emerald' },
  { sport: 'Squash Courts', count: 63, percentage: 15, colorClass: 'bar-orange' },
  { sport: 'Swimming Lanes', count: 42, percentage: 10, colorClass: 'bar-purple' },
])

// Analytics - Court Utilization mock data
const courtUtilization = ref([
  { period: 'Prime Hours (5 PM - 10 PM)', rate: 92, colorClass: 'bar-blue' },
  { period: 'Afternoon (12 PM - 5 PM)', rate: 68, colorClass: 'bar-indigo' },
  { period: 'Morning (6 AM - 12 PM)', rate: 54, colorClass: 'bar-purple' },
])

// Announcements mock data
const announcements = ref([
  {
    id: 1,
    title: 'Annual Facility Maintenance Shutdown Schedule Announced',
    date: 'July 20, 2026',
    category: 'General',
    categoryClass: 'blue',
  },
  {
    id: 2,
    title: 'Updated Peak-Hour Court Reservation Policy & Guidelines',
    date: 'July 15, 2026',
    category: 'Policy',
    categoryClass: 'orange',
  },
  {
    id: 3,
    title: 'Registration Open for Fall Junior Championship Series',
    date: 'July 10, 2026',
    category: 'Tournament',
    categoryClass: 'emerald',
  },
])

// Upcoming Events sample items
const upcomingEvents = ref([
  {
    id: 1,
    title: 'Apex Summer Tennis Open 2026',
    type: 'Tournament',
    date: 'July 28 - July 30, 2026',
    info: '32 / 32 Registered Players',
    status: 'Registration Open',
    chipClass: 'chip-blue',
    statusClass: 'status-open',
  },
  {
    id: 2,
    title: 'Masterclass Badminton Clinic',
    type: 'Coaching Session',
    date: 'August 02, 2026',
    info: '15 / 20 Spots Filled',
    status: 'Confirmed',
    chipClass: 'chip-emerald',
    statusClass: 'status-confirmed',
  },
  {
    id: 3,
    title: 'Courts 3 & 4 Lighting Upgrade',
    type: 'Maintenance Schedule',
    date: 'August 05, 2026',
    info: 'Temporary Court Closure',
    status: 'Scheduled',
    chipClass: 'chip-orange',
    statusClass: 'status-scheduled',
  },
])
</script>

<style scoped>
/* App Layout Container */
.admin-app-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family: 'Inter', sans-serif;
  color: #0f172a;
}

/* Mobile Sidebar Backdrop */
.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  z-index: 150;
}

/* Fixed Left Sidebar */
.admin-sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: 260px;
  background: #0f172a;
  color: #ffffff;
  z-index: 200;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.sidebar-header {
  height: 4.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  text-decoration: none;
  color: #ffffff;
}

.logo-mark {
  width: 2rem;
  height: 2rem;
  border-radius: 0.6rem;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  display: grid;
  place-items: center;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.logo-text {
  font-family: 'Poppins', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.admin-portal-badge {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  background: rgba(37, 99, 235, 0.25);
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.3);
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  letter-spacing: 0.05em;
}

/* Sidebar Navigation Menu */
.sidebar-menu {
  flex: 1;
  padding: 1.25rem 0.85rem;
  overflow-y: auto;
}

.menu-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.menu-label {
  font-size: 0.68rem;
  font-weight: 800;
  color: #64748b;
  letter-spacing: 0.08em;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.25rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0.85rem;
  border-radius: 0.65rem;
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.menu-item:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}

.menu-item.active {
  color: #ffffff;
  background: #2563eb;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
}

.item-icon-wrapper {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.item-icon-wrapper svg {
  width: 100%;
  height: 100%;
}

.item-name {
  flex: 1;
}

.item-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #cbd5e1;
}

.menu-item.active .item-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

/* Sidebar Footer / Logout */
.sidebar-footer {
  padding: 1rem 0.85rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.logout-link {
  color: #f87171;
}

.logout-link:hover {
  background: rgba(239, 68, 68, 0.12);
  color: #fca5a5;
}

/* Main Application Wrapper */
.main-wrapper {
  margin-left: 260px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Top Header */
.admin-top-header {
  height: 4.5rem;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 90;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: #475569;
  cursor: pointer;
  padding: 0.4rem;
  border-radius: 0.5rem;
}

.mobile-menu-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.page-title-block {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-family: 'Poppins', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.header-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.header-date-chip {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 0.4rem 0.8rem;
  border-radius: 0.65rem;
}

.header-action-btn {
  position: relative;
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 0.65rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.header-action-btn:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
}

.unread-dot {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 1.1rem;
  height: 1.1rem;
  border-radius: 50%;
  background: #ef4444;
  color: #ffffff;
  font-size: 0.65rem;
  font-weight: 700;
  display: grid;
  place-items: center;
  border: 2px solid #ffffff;
}

.admin-user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-left: 0.75rem;
  border-left: 1px solid #e2e8f0;
}

.user-avatar {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.85rem;
  display: grid;
  place-items: center;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
}

.user-role {
  font-size: 0.72rem;
  color: #64748b;
}

/* Dashboard Body Main Scroll Content */
.dashboard-body {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* KPI Cards Grid */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.kpi-icon-box {
  width: 2.6rem;
  height: 2.6rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-icon-box svg {
  width: 1.35rem;
  height: 1.35rem;
}

.kpi-icon-box.blue {
  background: #eff6ff;
  color: #2563eb;
}
.kpi-icon-box.emerald {
  background: #ecfdf5;
  color: #059669;
}
.kpi-icon-box.purple {
  background: #f3e8ff;
  color: #9333ea;
}
.kpi-icon-box.orange {
  background: #fff7ed;
  color: #ea580c;
}

.trend-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
}

.trend-badge.positive {
  background: #ecfdf5;
  color: #047857;
}
.trend-badge.neutral {
  background: #f1f5f9;
  color: #475569;
}

.kpi-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
  display: block;
  margin-bottom: 0.3rem;
}

.kpi-value {
  font-family: 'Poppins', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  line-height: 1.1;
}

/* Section Blocks */
.section-block {
  margin-bottom: 2rem;
}

.block-header {
  margin-bottom: 1.15rem;
}

.block-header.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.block-header h3 {
  font-family: 'Poppins', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.2rem;
}

.subtext {
  font-size: 0.85rem;
  color: #64748b;
}

/* Quick Actions Grid */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.15rem;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
  width: 100%;
}

.action-card:hover {
  border-color: #2563eb;
  background: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.08);
}

.action-icon {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
}

.action-icon svg {
  width: 1.25rem;
  height: 1.25rem;
}

.action-icon.blue {
  background: #eff6ff;
  color: #2563eb;
}
.action-icon.emerald {
  background: #ecfdf5;
  color: #059669;
}
.action-icon.purple {
  background: #f3e8ff;
  color: #9333ea;
}
.action-icon.orange {
  background: #fff7ed;
  color: #ea580c;
}
.action-icon.indigo {
  background: #e0e7ff;
  color: #4338ca;
}

.action-info {
  margin-bottom: 0.75rem;
}

.action-title {
  display: block;
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.15rem;
}

.action-desc {
  display: block;
  font-size: 0.76rem;
  color: #64748b;
  line-height: 1.3;
}

.action-arrow {
  margin-top: auto;
  color: #94a3b8;
  transition:
    color 0.2s ease,
    transform 0.2s ease;
}

.action-card:hover .action-arrow {
  color: #2563eb;
  transform: translateX(3px);
}

/* Analytics Widgets Grid */
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.widget-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.35rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.widget-header h4 {
  font-family: 'Poppins', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.2rem;
}

.widget-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.widget-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  background: #f1f5f9;
  color: #475569;
}

.widget-badge.live {
  background: #ecfdf5;
  color: #047857;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.chart-row {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.row-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
}

.sport-name {
  font-weight: 600;
  color: #334155;
}
.sport-count {
  font-weight: 600;
  color: #64748b;
}

.progress-track {
  width: 100%;
  height: 0.6rem;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
}

.progress-fill.bar-blue {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}
.progress-fill.bar-emerald {
  background: linear-gradient(90deg, #10b981, #059669);
}
.progress-fill.bar-orange {
  background: linear-gradient(90deg, #f97316, #ea580c);
}
.progress-fill.bar-purple {
  background: linear-gradient(90deg, #a855f7, #9333ea);
}
.progress-fill.bar-indigo {
  background: linear-gradient(90deg, #6366f1, #4f46e5);
}

.widget-footer {
  display: flex;
  gap: 1.15rem;
  padding-top: 0.85rem;
  border-top: 1px solid #f1f5f9;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.76rem;
  font-weight: 600;
  color: #64748b;
}

.dot {
  width: 0.45rem;
  height: 0.45rem;
  border-radius: 50%;
}

.dot.blue {
  background: #2563eb;
}
.dot.emerald {
  background: #059669;
}
.dot.orange {
  background: #ea580c;
}
.dot.purple {
  background: #9333ea;
}

.utilization-summary {
  display: flex;
  gap: 0.85rem;
  padding-top: 0.85rem;
  border-top: 1px solid #f1f5f9;
}

.summary-box {
  flex: 1;
  background: #f8fafc;
  border-radius: 0.65rem;
  padding: 0.65rem;
  text-align: center;
}

.summary-num {
  display: block;
  font-family: 'Poppins', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
}

.summary-lbl {
  display: block;
  font-size: 0.72rem;
  color: #64748b;
}

/* Dual Column Layout */
.dashboard-dual-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.card-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.35rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
  height: 100%;
}

.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.15rem;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.header-title h3 {
  font-family: 'Poppins', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.icon-bubble {
  width: 2.1rem;
  height: 2.1rem;
  border-radius: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-bubble.blue {
  background: #eff6ff;
  color: #2563eb;
}
.icon-bubble.orange {
  background: #fff7ed;
  color: #ea580c;
}

.total-tag {
  font-size: 0.75rem;
  font-weight: 700;
  color: #2563eb;
  background: #eff6ff;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
}

/* Membership List */
.membership-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.member-type-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.85rem;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 0.75rem;
}

.member-type-row.highlighted {
  background: #ecfdf5;
  border-color: #a7f3d0;
}

.member-type-info {
  display: flex;
  flex-direction: column;
}

.type-name {
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
}

.type-desc {
  font-size: 0.76rem;
  color: #64748b;
}

.member-type-stat {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.type-value {
  font-family: 'Poppins', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #0f172a;
}

.type-pct {
  font-size: 0.72rem;
  color: #64748b;
}

.text-emerald {
  color: #059669;
}

.new-pill {
  font-size: 0.68rem;
  font-weight: 700;
  background: #10b981;
  color: #ffffff;
  padding: 0.12rem 0.4rem;
  border-radius: 999px;
}

/* Pending Requests & Tables */
.pending-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.pending-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #ffffff;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar-sm {
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  font-weight: 700;
  font-size: 0.8rem;
  display: grid;
  place-items: center;
}

.user-name-txt {
  display: block;
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
}

.user-email-txt {
  display: block;
  font-size: 0.76rem;
  color: #64748b;
}

.plan-badge {
  font-size: 0.72rem;
  font-weight: 700;
  background: #eff6ff;
  color: #2563eb;
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
}

.date-txt {
  font-size: 0.78rem;
  color: #64748b;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-approve {
  padding: 0.35rem 0.75rem;
  border-radius: 0.5rem;
  border: none;
  background: #10b981;
  color: #ffffff;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-decline {
  padding: 0.35rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #64748b;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-approve:hover {
  background: #059669;
}
.btn-decline:hover {
  background: #f8fafc;
  color: #0f172a;
}

.btn-primary-action {
  padding: 0.5rem 1rem;
  border-radius: 0.65rem;
  border: none;
  background: #2563eb;
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
}
.btn-primary-action:hover {
  background: #1d4ed8;
}

/* Settings Rows */
.settings-card-title {
  font-family: 'Poppins', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 1rem;
}

.setting-row {
  display: flex;
  justify-content: space-between;
  padding: 0.65rem 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.85rem;
}

.setting-row:last-child {
  border-bottom: none;
}

.setting-label {
  color: #64748b;
  font-weight: 500;
}
.setting-val {
  color: #0f172a;
  font-weight: 700;
}

/* Announcements List */
.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.announcement-item {
  padding: 0.85rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #ffffff;
  transition: border-color 0.2s ease;
}

.announcement-item:hover {
  border-color: #cbd5e1;
}

.announcement-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.35rem;
}

.announcement-badge {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.12rem 0.45rem;
  border-radius: 999px;
  text-transform: uppercase;
}

.announcement-badge.blue {
  background: #eff6ff;
  color: #2563eb;
}
.announcement-badge.orange {
  background: #fff7ed;
  color: #ea580c;
}
.announcement-badge.emerald {
  background: #ecfdf5;
  color: #059669;
}

.announcement-date {
  font-size: 0.75rem;
  color: #94a3b8;
}

.announcement-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  line-height: 1.35;
}

/* Upcoming Events Grid */
.events-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.admin-event-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.admin-event-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.event-card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.event-type-chip {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.18rem 0.55rem;
  border-radius: 0.45rem;
}

.chip-blue {
  background: #eff6ff;
  color: #2563eb;
}
.chip-emerald {
  background: #ecfdf5;
  color: #059669;
}
.chip-orange {
  background: #fff7ed;
  color: #ea580c;
}

.event-status-pill {
  font-size: 0.72rem;
  font-weight: 600;
}

.status-open {
  color: #2563eb;
}
.status-confirmed {
  color: #059669;
}
.status-scheduled {
  color: #d97706;
}

.event-card-title {
  font-family: 'Poppins', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.75rem;
  line-height: 1.35;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.8rem;
  color: #64748b;
}

/* ================================================= */
/*  MODAL STYLES (Copied & Adjusted from ProfileView) */
/* ================================================= */
.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.loading-state {
  padding: 2rem;
  text-align: center;
  color: #64748b;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 300;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
  padding: 1.5rem;
  animation: fadeIn 0.3s ease;
}

.modal-card {
  background: #ffffff;
  border-radius: 1.75rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.15);
  width: 100%;
  max-width: 38rem;
  overflow: hidden;
  animation: scaleUp 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

.modal-header h3 {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.75rem;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #4f46e5;
}

.modal-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  font-family: inherit;
  font-size: 0.95rem;
  color: #0f172a;
  background: #ffffff;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-modal-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-modal-btn:hover {
  background: #f8fafc;
}

.submit-modal-btn {
  padding: 0.75rem 1.75rem;
  border-radius: 0.75rem;
  border: none;
  background: #4f46e5;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.submit-modal-btn:hover {
  background: #4338ca;
}

/* Club Banner */
.club-banner {
  margin-bottom: 2rem;
  padding: 1.5rem 2rem;
  border-radius: 1.25rem;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.05), rgba(139, 92, 246, 0.05));
  border: 1px solid rgba(37, 99, 235, 0.15);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.03);
}

.club-banner.glass-empty {
  background: #ffffff;
  border: 1px dashed #e2e8f0;
  color: #64748b;
  text-align: center;
  justify-content: center;
}

.club-banner-icon {
  font-size: 2.5rem;
}

.club-banner-info h2 {
  font-family: 'Poppins', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.25rem;
}

.club-banner-info p {
  color: #64748b;
  margin: 0 0 0.5rem;
}

.club-hours-badge {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.club-hours-badge span {
  background: rgba(226, 232, 240, 0.6);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
}

/* Settings Inputs */
.settings-input {
  width: 100%;
  padding: 0.4rem 0.6rem;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  font-family: inherit;
  font-size: 0.85rem;
  color: #0f172a;
  background: #ffffff;
  transition: border-color 0.2s ease;
}

.settings-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Ensure setting-row aligns inputs */
.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.65rem 0;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.85rem;
  gap: 1rem;
}
.setting-label {
  flex: 0 0 30%;
}
.settings-input {
  flex: 1;
}

.court-settings-badge {
  margin-bottom: 0.75rem;
}
.badge-default,
.badge-custom {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  letter-spacing: 0.02em;
}
.badge-default {
  background: rgba(100, 116, 139, 0.1);
  color: #475569;
}
.badge-custom {
  background: rgba(37, 99, 235, 0.1);
  color: #2563eb;
}

/* Toggle section */
.toggle-section {
  margin: 0.5rem 0 1rem;
  padding: 0.5rem 0;
  border-top: 1px solid rgba(226, 232, 240, 0.6);
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}
.toggle-label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.5rem;
}
.toggle-group {
  display: flex;
  gap: 0.5rem;
}
.toggle-btn {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #64748b;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.toggle-btn:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}
.toggle-btn.active {
  border-color: #2563eb;
  background: #eff6ff;
  color: #2563eb;
}

/* Disable visual style for override inputs when using defaults */
.disabled-section .form-group input,
.disabled-section .form-group select {
  opacity: 0.5;
  background: #f1f5f9;
  cursor: not-allowed;
}

/* Date Picker Wrapper */
.date-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Court Settings Badges */
.court-settings-badge {
  margin-bottom: 0.75rem;
}
.badge-default,
.badge-custom {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  letter-spacing: 0.02em;
}
.badge-default {
  background: rgba(100, 116, 139, 0.1);
  color: #475569;
}
.badge-custom {
  background: rgba(37, 99, 235, 0.1);
  color: #2563eb;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes scaleUp {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.35rem;
  padding: 0.5rem 0.85rem;
  border-radius: 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1);
  border: 1px solid transparent;
  background: transparent;
}

/* "Edit" (View) Button */
.view-btn {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  color: #475569;
}
.view-btn:hover {
  background: #f1f5f9;
  border-color: rgba(203, 213, 225, 0.9);
  color: #0f172a;
}

/* "Delete" (Cancel) Button */
.cancel-btn {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.15);
  color: #dc2626;
}
.cancel-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

/* Responsive Rules */
@media (max-width: 1024px) {
  .admin-sidebar {
    transform: translateX(-100%);
  }

  .admin-sidebar.mobile-show {
    transform: translateX(0);
  }

  .main-wrapper {
    margin-left: 0;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .quick-actions-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .analytics-grid,
  .dashboard-dual-grid {
    grid-template-columns: 1fr;
  }

  .events-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .admin-top-header {
    padding: 0 1rem;
  }

  .header-subtitle,
  .header-date-chip,
  .user-meta {
    display: none;
  }

  .dashboard-body {
    padding: 1rem;
  }

  .kpi-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .events-grid {
    grid-template-columns: 1fr;
  }

  .modal-card {
    max-width: 100%;
    margin: 0 1rem;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .modal-form {
    padding: 1.25rem;
  }
}
</style>
