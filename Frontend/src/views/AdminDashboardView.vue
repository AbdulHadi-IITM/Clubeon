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

      <!-- Sidebar Footer / Admin Profile with Discord-style Popover -->
      <div class="sidebar-footer">
        <!-- Discord-Style Floating Profile Popover Card -->
        <transition name="popover-fade">
          <div v-if="showProfilePopover" class="discord-profile-card" @click.stop>
            <!-- Header Banner -->
            <div class="discord-banner">
              <button class="close-popover-btn" @click.stop="showProfilePopover = false">✕</button>
            </div>

            <!-- Avatar with Image Upload Overlay -->
            <div class="discord-avatar-wrapper">
              <div class="discord-avatar">
                <img v-if="adminProfile.avatarUrl" :src="adminProfile.avatarUrl" alt="Admin Avatar" class="discord-avatar-img" />
                <span v-else>{{ adminProfile.initials }}</span>
                <!-- Image Upload Button overlay -->
                <label class="avatar-upload-overlay" title="Upload new profile picture">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px; color: #ffffff;"><path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  <input type="file" accept="image/*" @change="handleAvatarUpload" style="display: none;" />
                </label>
              </div>
            </div>

            <!-- Profile Info Body -->
            <div class="discord-profile-body">
              <div class="profile-title-block">
                <h4 class="discord-name">{{ adminProfile.name }}</h4>
                <span class="discord-role-badge">{{ adminProfile.role }}</span>
              </div>

              <div class="discord-divider"></div>

              <!-- Admin Profile Details -->
              <div class="discord-details-list">
                <div class="detail-row">
                  <span class="detail-label">Email</span>
                  <span class="detail-val">{{ adminProfile.email || 'Not provided' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Phone</span>
                  <span class="detail-val" :style="{ color: adminProfile.phone ? '#f1f5f9' : '#94a3b8' }">
                    {{ adminProfile.phone || 'Not provided' }}
                  </span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Club Facility</span>
                  <span class="detail-val" style="color: #60a5fa; font-weight: 700;">ClubDash</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Member Since</span>
                  <span class="detail-val">{{ adminProfile.memberSince || 'Recent' }}</span>
                </div>
              </div>

              <!-- Action Footer -->
              <div class="discord-actions-footer">
                <button type="button" class="edit-profile-btn-pill" @click="openEditProfileModal">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="15" height="15">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  <span>Edit Profile</span>
                </button>
              </div>
            </div>
          </div>
        </transition>

        <!-- Clickable Sidebar Profile Card -->
        <div
          class="sidebar-admin-profile clickable-profile"
          @click.stop="toggleProfilePopover"
          title="Click to view Discord-style Admin Profile"
        >
          <div class="user-avatar">
            <img v-if="adminProfile.avatarUrl" :src="adminProfile.avatarUrl" alt="Admin Avatar" class="user-avatar-img" />
            <span v-else>{{ adminProfile.initials }}</span>
          </div>
          <div class="user-meta">
            <span class="user-name">{{ adminProfile.name }}</span>
            <span class="user-role">{{ adminProfile.role }}</span>
          </div>
        </div>
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

          <!-- Top Header Logout Button -->
          <button class="top-header-logout-btn" @click="handleLogout" title="Logout of Admin Panel">
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
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
            <span>Logout</span>
          </button>
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

          <!-- TAB 2: MEMBERS DIRECTORY -->
          <div v-else-if="activeNav === 'Members'" class="tab-pane">
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

          <!-- TAB 4: BOOKINGS MANAGEMENT -->
          <div v-else-if="activeNav === 'Bookings'" class="tab-pane">
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
                <div v-if="filteredBookings.length === 0" class="no-bookings-empty">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="width: 48px; height: 48px; color: #94a3b8; margin-bottom: 1rem;"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                  <p class="empty-title">No bookings match your filter</p>
                  <p class="empty-sub">Try adjusting your search query or dropdown filters.</p>
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

          <!-- TAB 5: EVENTS MANAGEMENT -->
          <div v-else-if="activeNav === 'Events'" class="tab-pane">
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

          <!-- TAB 6: ANNOUNCEMENTS PREVIEW -->
          <div v-else-if="activeNav === 'Announcements'" class="tab-pane">
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

          <!-- TAB 7: ANALYTICS PREVIEW -->
          <!-- TAB 7: PERFORMANCE & ANALYTICS -->
          <div v-else-if="activeNav === 'Analytics'" class="tab-pane">
            <!-- Dynamic KPI Cards for Analytics (in Indian Rupees ₹) -->
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Revenue</span>
                <h3 class="kpi-value">₹4,82,500</h3>
                <span class="trend-badge positive">↑ +14.2% YoY</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Peak Booking Hour</span>
                <h3 class="kpi-value">06 - 08 PM</h3>
                <span class="trend-badge positive">↑ 96% Peak Occupancy</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Membership Growth</span>
                <h3 class="kpi-value">+64 Members</h3>
                <span class="trend-badge positive">↑ This Month</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Retention Rate</span>
                <h3 class="kpi-value">94.8%</h3>
                <span class="trend-badge positive">↑ Member Satisfaction</span>
              </div>
            </section>

            <!-- Main Analytics Section with Graphs -->
            <section class="section-block">
              <!-- Toolbar with Filters -->
              <div class="block-header bookings-toolbar-header">
                <div>
                  <h3>Revenue & Performance Analytics</h3>
                  <span class="subtext">Interactive visual trends, revenue distribution, and court occupancy heatmaps</span>
                </div>
                <div class="header-action-buttons">
                  <div class="view-toggle-group">
                    <button
                      v-for="tf in ['7 Days', '30 Days', '12 Months', 'This Year']"
                      :key="tf"
                      class="view-toggle-btn"
                      :class="{ active: analyticsTimeframe === tf }"
                      @click="analyticsTimeframe = tf"
                    >
                      {{ tf }}
                    </button>
                  </div>
                  <button class="export-csv-btn" @click="exportAnalyticsCSV">
                    📥 Download Report
                  </button>
                </div>
              </div>

              <!-- Main Revenue Trend Line Graph Card -->
              <div class="card-box chart-graph-card" style="margin-top: 1rem; padding: 1.5rem;">
                <div class="chart-header-row">
                  <div>
                    <h4 class="chart-card-title">Revenue & Booking Growth Trajectory</h4>
                    <p class="chart-card-sub">Monthly trend overview in Indian Rupees (₹)</p>
                  </div>
                  <div class="metric-switch-pills">
                    <button
                      class="metric-pill-btn"
                      :class="{ active: activeChartMetric === 'revenue' }"
                      @click="activeChartMetric = 'revenue'"
                    >
                      Revenue (₹)
                    </button>
                    <button
                      class="metric-pill-btn"
                      :class="{ active: activeChartMetric === 'bookings' }"
                      @click="activeChartMetric = 'bookings'"
                    >
                      Bookings Volume
                    </button>
                  </div>
                </div>

                <!-- Interactive SVG Vertical Column/Bar Chart -->
                <div class="svg-chart-container">
                  <svg viewBox="0 0 700 230" class="svg-graph">
                    <defs>
                      <linearGradient id="barBlueGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#3b82f6"/>
                        <stop offset="100%" stop-color="#1d4ed8"/>
                      </linearGradient>
                      <linearGradient id="barIndigoGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="#6366f1"/>
                        <stop offset="100%" stop-color="#4338ca"/>
                      </linearGradient>
                    </defs>

                    <!-- Horizontal Grid Lines -->
                    <line x1="40" y1="30" x2="670" y2="30" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4"/>
                    <line x1="40" y1="80" x2="670" y2="80" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4"/>
                    <line x1="40" y1="130" x2="670" y2="130" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="4"/>
                    <line x1="40" y1="185" x2="670" y2="185" stroke="#cbd5e1" stroke-width="1.5"/>

                    <!-- Y-Axis Labels -->
                    <text x="35" y="34" text-anchor="end" font-size="10" fill="#94a3b8">₹5L</text>
                    <text x="35" y="84" text-anchor="end" font-size="10" fill="#94a3b8">₹3.5L</text>
                    <text x="35" y="134" text-anchor="end" font-size="10" fill="#94a3b8">₹2L</text>
                    <text x="35" y="189" text-anchor="end" font-size="10" fill="#94a3b8">₹0</text>

                    <!-- Column Bars & Labels -->
                    <g v-for="(b, i) in [
                      { x: 55, w: 38, h: 88, y: 97, month: 'Jan', rev: '₹2.45L', vol: 320 },
                      { x: 135, w: 38, h: 101, y: 84, month: 'Feb', rev: '₹2.80L', vol: 380 },
                      { x: 215, w: 38, h: 112, y: 73, month: 'Mar', rev: '₹3.10L', vol: 420 },
                      { x: 295, w: 38, h: 105, y: 80, month: 'Apr', rev: '₹2.90L', vol: 390 },
                      { x: 375, w: 38, h: 130, y: 55, month: 'May', rev: '₹3.60L', vol: 490 },
                      { x: 455, w: 38, h: 151, y: 34, month: 'Jun', rev: '₹4.20L', vol: 560 },
                      { x: 535, w: 38, h: 162, y: 23, month: 'Jul', rev: '₹4.50L', vol: 610 },
                      { x: 615, w: 38, h: 174, y: 11, month: 'Aug', rev: '₹4.82L', vol: 648 }
                    ]" :key="i">
                      <!-- Bar Background Track -->
                      <rect :x="b.x" y="30" :width="b.w" height="155" rx="6" ry="6" fill="#f8fafc" />
                      <!-- Gradient Vertical Bar -->
                      <rect
                        :x="b.x"
                        :y="activeChartMetric === 'revenue' ? b.y : (185 - (b.vol / 700 * 155))"
                        :width="b.w"
                        :height="activeChartMetric === 'revenue' ? b.h : (b.vol / 700 * 155)"
                        rx="6"
                        ry="6"
                        :fill="i % 2 === 0 ? 'url(#barBlueGrad)' : 'url(#barIndigoGrad)'"
                        class="graph-point"
                      />
                      <!-- Top Value Label -->
                      <text :x="b.x + 19" :y="(activeChartMetric === 'revenue' ? b.y : (185 - (b.vol / 700 * 155))) - 6" text-anchor="middle" font-size="10" font-weight="700" fill="#1e293b">
                        {{ activeChartMetric === 'revenue' ? b.rev : b.vol }}
                      </text>
                      <!-- Bottom Month Label -->
                      <text :x="b.x + 19" y="208" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b">{{ b.month }}</text>
                    </g>
                  </svg>
                </div>
              </div>

              <!-- Two Column Charts Layout: Donut & Bar Charts -->
              <div class="analytics-grid" style="margin-top: 1.25rem;">
                <!-- Sport Revenue Distribution Chart -->
                <div class="widget-card chart-widget-box">
                  <div class="widget-header">
                    <h4>Sport Revenue Breakdown</h4>
                    <span class="widget-badge">Percentage Share</span>
                  </div>

                  <div class="donut-chart-flex-wrapper">
                    <!-- SVG Donut Chart -->
                    <div class="donut-svg-holder">
                      <svg viewBox="0 0 100 100" class="donut-svg">
                        <!-- Tennis 45% (0 - 162 deg) -->
                        <circle cx="50" cy="50" r="38" fill="none" stroke="#2563eb" stroke-width="14" stroke-dasharray="107 132" stroke-dashoffset="0" />
                        <!-- Badminton 30% (162 - 270 deg) -->
                        <circle cx="50" cy="50" r="38" fill="none" stroke="#059669" stroke-width="14" stroke-dasharray="71 168" stroke-dashoffset="-107" />
                        <!-- Squash 15% (270 - 324 deg) -->
                        <circle cx="50" cy="50" r="38" fill="none" stroke="#ea580c" stroke-width="14" stroke-dasharray="35 204" stroke-dashoffset="-178" />
                        <!-- Swimming 10% (324 - 360 deg) -->
                        <circle cx="50" cy="50" r="38" fill="none" stroke="#0284c7" stroke-width="14" stroke-dasharray="24 215" stroke-dashoffset="-213" />
                      </svg>
                      <div class="donut-inner-text">
                        <span class="donut-total-title">Total</span>
                        <span class="donut-total-num">₹4.82L</span>
                      </div>
                    </div>

                    <!-- Legend & Distribution Breakdown -->
                    <div class="donut-legend-list">
                      <div v-for="item in sportRevenueBreakdown" :key="item.sport" class="legend-item-row">
                        <div class="legend-color-dot" :style="{ background: item.color }"></div>
                        <div class="legend-info">
                          <span class="legend-sport-name">{{ item.sport }}</span>
                          <span class="legend-percentage">{{ item.percentage }}% (₹{{ item.revenue.toLocaleString() }})</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Hourly Peak Occupancy Bar Chart -->
                <div class="widget-card chart-widget-box">
                  <div class="widget-header">
                    <h4>24-Hour Peak Occupancy Heatmap</h4>
                    <span class="widget-badge live">Live Peak</span>
                  </div>

                  <div class="hourly-bars-chart" style="display: flex; flex-direction: row; align-items: flex-end; justify-content: space-between; gap: 0.4rem; height: 190px; padding-top: 1.25rem; padding-bottom: 0.5rem; width: 100%;">
                    <div v-for="h in hourlyOccupancyData" :key="h.hour" class="bar-col-item" style="display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 0.35rem; flex: 1; height: 100%;">
                      <span class="bar-rate-txt" style="font-size: 0.72rem; font-weight: 700; color: #1e293b;">{{ h.rate }}%</span>
                      <div class="bar-track-vertical" style="height: 120px; width: 14px; border-radius: 999px; background: #f1f5f9; display: flex; align-items: flex-end; overflow: hidden;">
                        <div
                          class="bar-fill-vertical"
                          :style="{
                            height: h.rate + '%',
                            width: '100%',
                            borderRadius: '999px',
                            background: h.rate >= 90 ? 'linear-gradient(to top, #2563eb, #4f46e5)' : (h.rate >= 70 ? 'linear-gradient(to top, #059669, #10b981)' : 'linear-gradient(to top, #8b5cf6, #a855f7)'),
                            transition: 'height 0.4s ease'
                          }"
                        ></div>
                      </div>
                      <span class="bar-hour-label" style="font-size: 0.68rem; color: #64748b; font-weight: 600; white-space: nowrap; margin-top: 0.2rem;">{{ h.hour.split(' ')[0] }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Section 3: Facility Performance Table & Payment/Financial Summary Row -->
              <div class="analytics-grid" style="margin-top: 1.25rem;">
                <!-- Top Performing Facilities Table Card -->
                <div class="widget-card chart-widget-box" style="flex: 2;">
                  <div class="widget-header">
                    <div>
                      <h4>Top Performing Facilities</h4>
                      <p class="widget-subtitle">Court hours booked, revenue generated, and occupancy rates</p>
                    </div>
                    <span class="widget-badge">This Month</span>
                  </div>

                  <div class="facilities-table-wrapper" style="overflow-x: auto; margin-top: 1rem;">
                    <table class="analytics-table">
                      <thead>
                        <tr>
                          <th>Facility Name</th>
                          <th>Sport</th>
                          <th>Hours Booked</th>
                          <th>Occupancy</th>
                          <th>Revenue (₹)</th>
                          <th>Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="fac in topPerformingFacilities" :key="fac.id">
                          <td>
                            <strong style="color: #0f172a; font-size: 0.88rem;">{{ fac.name }}</strong>
                          </td>
                          <td>
                            <span class="type-chip default">{{ fac.sport }}</span>
                          </td>
                          <td style="font-weight: 600; color: #334155;">{{ fac.hoursBooked }} hrs</td>
                          <td>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                              <div class="table-progress-bar">
                                <div class="table-progress-fill" :style="{ width: fac.occupancy }"></div>
                              </div>
                              <span style="font-size: 0.8rem; font-weight: 700; color: #0f172a;">{{ fac.occupancy }}</span>
                            </div>
                          </td>
                          <td style="font-weight: 700; color: #059669;">₹{{ fac.revenue.toLocaleString() }}</td>
                          <td>
                            <span
                              class="status-badge-chip"
                              :class="{
                                'status-active': fac.status === 'High Demand',
                                'status-completed': fac.status === 'Optimal',
                                'status-upcoming': fac.status === 'Moderate'
                              }"
                            >
                              {{ fac.status }}
                            </span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                <!-- Financial Breakdown & Payment Methods Card -->
                <div class="widget-card chart-widget-box" style="flex: 1;">
                  <div class="widget-header">
                    <h4>Financial Overview & Payments</h4>
                    <span class="widget-badge">Net Summary</span>
                  </div>

                  <!-- Financial Highlights Cards -->
                  <div class="financial-summary-grid" style="margin-top: 1rem;">
                    <div class="fin-stat-card">
                      <span class="fin-label">Gross Revenue</span>
                      <span class="fin-val positive">{{ financialSummary.grossRevenue }}</span>
                    </div>
                    <div class="fin-stat-card">
                      <span class="fin-label">Net Profit</span>
                      <span class="fin-val blue">{{ financialSummary.netProfit }}</span>
                      <span class="fin-sub">{{ financialSummary.profitMargin }} margin</span>
                    </div>
                  </div>

                  <!-- Payment Methods Stacked Bar -->
                  <div style="margin-top: 1.25rem;">
                    <h5 style="font-size: 0.84rem; font-weight: 700; color: #334155; margin-bottom: 0.5rem;">Payment Gateway Distribution</h5>
                    <div class="stacked-bar-container">
                      <div
                        v-for="pm in paymentMethodBreakdown"
                        :key="pm.method"
                        class="stacked-bar-segment"
                        :style="{ width: pm.percentage + '%', background: pm.color }"
                        :title="pm.method + ': ' + pm.percentage + '%'"
                      ></div>
                    </div>

                    <div class="payment-method-legend" style="margin-top: 0.85rem;">
                      <div v-for="pm in paymentMethodBreakdown" :key="pm.method" class="payment-legend-row">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                          <span class="legend-dot" :style="{ background: pm.color }"></span>
                          <span style="font-size: 0.82rem; color: #475569; font-weight: 600;">{{ pm.method }}</span>
                        </div>
                        <span style="font-size: 0.82rem; font-weight: 700; color: #0f172a;">{{ pm.val }} ({{ pm.percentage }}%)</span>
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
        </div>
      </main>

      <!-- ALL ADMIN POPUP MODALS -->

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

                <div class="form-row">
                  <div class="form-group">
                    <label>Sport / Court Type</label>
                    <select v-model="courtForm.sport_type" required>
                      <option v-for="sport in courtStore.sportsTypes" :key="sport.value" :value="sport.value">
                        {{ sport.icon }} {{ sport.label }}
                      </option>
                    </select>
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
                    <label>Sport / Court Type</label>
                    <select v-model="courtForm.sport_type" required>
                      <option v-for="sport in courtStore.sportsTypes" :key="sport.value" :value="sport.value">
                        {{ sport.icon }} {{ sport.label }}
                      </option>
                    </select>
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

        <!-- BOOKING DETAILS MODAL -->
        <div v-if="showBookingDetailsModal && selectedBooking" class="modal-overlay" @click.self="closeBookingDetailsModal">
          <div class="modal-card booking-detail-modal">
            <div class="modal-header">
              <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <h2 style="margin: 0;">Booking Details</h2>
                <span class="booking-ref-tag large">{{ selectedBooking.id }}</span>
                <span class="booking-status-badge" :class="'bstatus-' + selectedBooking.status.toLowerCase()">
                  {{ selectedBooking.status }}
                </span>
              </div>
              <button class="close-modal-btn" @click="closeBookingDetailsModal">✕</button>
            </div>

            <div class="modal-body booking-detail-body">
              <!-- Player Profile Section -->
              <div class="detail-section-card">
                <h4>Player Information</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Player Name</span>
                    <span class="detail-val font-bold">{{ selectedBooking.player }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Email Address</span>
                    <span class="detail-val">{{ selectedBooking.email }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Phone</span>
                    <span class="detail-val">{{ selectedBooking.phone }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">User Tier</span>
                    <span class="detail-val">{{ selectedBooking.userType }}</span>
                  </div>
                </div>
              </div>

              <!-- Reservation Details Section -->
              <div class="detail-section-card">
                <h4>Reservation & Schedule</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Facility / Court</span>
                    <span class="detail-val font-bold">{{ selectedBooking.facility }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Sport Category</span>
                    <span class="detail-val">{{ selectedBooking.sport }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Scheduled Date</span>
                    <span class="detail-val">{{ selectedBooking.dateDisplay }} ({{ selectedBooking.date }})</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Time Slot</span>
                    <span class="detail-val">{{ selectedBooking.time }} ({{ selectedBooking.duration }})</span>
                  </div>
                </div>
              </div>

              <!-- Payment & Fee Section -->
              <div class="detail-section-card">
                <h4>Payment & Billing</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Booking Fee</span>
                    <span class="detail-val font-bold" style="color: #2563eb; font-size: 1.1rem;">₹{{ selectedBooking.amount }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Payment Status</span>
                    <span class="pay-status-tag" :class="'pay-' + selectedBooking.paymentStatus.toLowerCase()">{{ selectedBooking.paymentStatus }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Payment Method</span>
                    <span class="detail-val">{{ selectedBooking.paymentMethod }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Created At</span>
                    <span class="detail-val">{{ selectedBooking.createdAt }}</span>
                  </div>
                </div>
              </div>

              <!-- Notes Section -->
              <div v-if="selectedBooking.notes" class="detail-section-card">
                <h4>Notes & Comments</h4>
                <p class="notes-text">{{ selectedBooking.notes }}</p>
              </div>
            </div>

            <div class="modal-footer">
              <div style="display: flex; gap: 0.75rem;">
                <button
                  v-if="selectedBooking.status === 'Confirmed' || selectedBooking.status === 'Pending'"
                  class="cancel-modal-btn danger-btn"
                  @click="requestCancelBooking(selectedBooking)"
                >
                  ✕ Cancel Booking
                </button>
                <button
                  v-if="selectedBooking.status === 'Confirmed'"
                  class="submit-modal-btn success-btn"
                  @click="markBookingCompleted(selectedBooking)"
                >
                  ✓ Mark Completed
                </button>
              </div>
              <button class="cancel-modal-btn" @click="closeBookingDetailsModal">Close</button>
            </div>
          </div>
        </div>

        <!-- CANCEL BOOKING CONFIRMATION MODAL -->
        <div v-if="showCancelConfirmModal && bookingToCancel" class="modal-overlay" @click.self="showCancelConfirmModal = false">
          <div class="modal-card small-confirm-modal">
            <div class="modal-header">
              <h3 style="color: #ef4444; margin: 0;">Cancel Booking</h3>
              <button class="close-modal-btn" @click="showCancelConfirmModal = false">✕</button>
            </div>
            <div class="modal-body" style="padding: 1.5rem 0;">
              <p>Are you sure you want to cancel booking <strong>{{ bookingToCancel.id }}</strong> for <strong>{{ bookingToCancel.player }}</strong>?</p>
              <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">This action will change the status to Cancelled and initiate a refund for ₹{{ bookingToCancel.amount }}.</p>
            </div>
            <div class="modal-footer">
              <button class="cancel-modal-btn" @click="showCancelConfirmModal = false">Keep Booking</button>
              <button class="submit-modal-btn danger-btn" @click="confirmCancelBooking">Confirm Cancellation</button>
            </div>
          </div>
        </div>

        <!-- CREATE NEW BOOKING MODAL -->
        <div v-if="showNewBookingModal" class="modal-overlay" @click.self="closeNewBookingModal">
          <div class="modal-card">
            <div class="modal-header">
              <h2>Add New Court Reservation</h2>
              <button class="close-modal-btn" @click="closeNewBookingModal">✕</button>
            </div>
            <form @submit.prevent="handleCreateNewBooking" class="modal-form">
              <div class="form-row">
                <div class="form-group">
                  <label>Player Name *</label>
                  <input type="text" v-model="newBookingForm.player" required placeholder="e.g. Alex Smith" />
                </div>
                <div class="form-group">
                  <label>Player Email *</label>
                  <input type="email" v-model="newBookingForm.email" required placeholder="alex@example.com" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Phone Number</label>
                  <input type="text" v-model="newBookingForm.phone" placeholder="+1 (555) 000-0000" />
                </div>
                <div class="form-group">
                  <label>User Type</label>
                  <select v-model="newBookingForm.userType">
                    <option value="Member (VIP)">Member (VIP)</option>
                    <option value="Member (Standard)">Member (Standard)</option>
                    <option value="Casual Player">Casual Player</option>
                    <option value="Guest">Guest</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Facility / Court *</label>
                  <select v-model="newBookingForm.facility" @change="newBookingForm.sport = newBookingForm.facility.includes('Tennis') ? 'Tennis' : newBookingForm.facility.includes('Badminton') ? 'Badminton' : newBookingForm.facility.includes('Squash') ? 'Squash' : 'Swimming'">
                    <option value="Tennis Court 1">Tennis Court 1</option>
                    <option value="Tennis Court 2">Tennis Court 2</option>
                    <option value="Badminton Arena A">Badminton Arena A</option>
                    <option value="Badminton Arena B">Badminton Arena B</option>
                    <option value="Squash Court 1">Squash Court 1</option>
                    <option value="Squash Court 2">Squash Court 2</option>
                    <option value="Swimming Lane 1">Swimming Lane 1</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Date *</label>
                  <input type="date" v-model="newBookingForm.date" required />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Time Slot *</label>
                  <input type="text" v-model="newBookingForm.time" required placeholder="e.g. 05:00 PM - 07:00 PM" />
                </div>
                <div class="form-group">
                  <label>Duration</label>
                  <input type="text" v-model="newBookingForm.duration" placeholder="e.g. 2.0 hrs" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Booking Fee (₹)</label>
                  <input type="number" v-model="newBookingForm.amount" min="0" step="5" />
                </div>
                <div class="form-group">
                  <label>Payment Status</label>
                  <select v-model="newBookingForm.paymentStatus">
                    <option value="Paid">Paid</option>
                    <option value="Pending">Pending</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Notes / Special Requests</label>
                <textarea v-model="newBookingForm.notes" rows="2" placeholder="Add any special instructions or equipment requests..."></textarea>
              </div>

              <div class="modal-actions">
                <button type="button" class="cancel-modal-btn" @click="closeNewBookingModal">Cancel</button>
                <button type="submit" class="submit-modal-btn">Create Reservation</button>
              </div>
            </form>
          </div>
        </div>

        <!-- CREATE EVENT MODAL -->
        <div v-if="showCreateEventModal" class="modal-overlay" @click.self="closeCreateEventModal">
          <div class="modal-card">
            <div class="modal-header">
              <h3>+ Create New Event</h3>
              <button class="close-modal-btn" @click="closeCreateEventModal">✕</button>
            </div>
            <form @submit.prevent="handleCreateEvent" class="modal-form">
              <div class="form-group">
                <label>Event Title *</label>
                <input type="text" v-model="eventForm.title" required placeholder="e.g. Apex Summer Tennis Open 2026" />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Sport Category *</label>
                  <select v-model="eventForm.sport" required>
                    <option value="Tennis">Tennis</option>
                    <option value="Badminton">Badminton</option>
                    <option value="Squash">Squash</option>
                    <option value="Swimming">Swimming</option>
                    <option value="Social">Social / General</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Event Type *</label>
                  <select v-model="eventForm.type" required>
                    <option value="Tournament">Tournament</option>
                    <option value="Coaching Clinic">Coaching Clinic</option>
                    <option value="Social League">Social League</option>
                    <option value="Exhibition">Exhibition / Match</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Event Date *</label>
                  <input type="date" v-model="eventForm.date" required />
                </div>
                <div class="form-group">
                  <label>Time Slot *</label>
                  <input type="text" v-model="eventForm.time" required placeholder="e.g. 10:00 AM - 04:00 PM" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Venue / Court Location *</label>
                  <input type="text" v-model="eventForm.venue" required placeholder="e.g. Tennis Courts 1 & 2" />
                </div>
                <div class="form-group">
                  <label>Max Player Capacity *</label>
                  <input type="number" v-model="eventForm.capacity" min="1" required />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Entry Fee (₹)</label>
                  <input type="number" v-model="eventForm.fee" min="0" step="50" placeholder="0 for Free" />
                </div>
                <div class="form-group">
                  <label>Event Status</label>
                  <select v-model="eventForm.status">
                    <option value="Upcoming">Upcoming</option>
                    <option value="Ongoing">Ongoing</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Organizer Name</label>
                <input type="text" v-model="eventForm.organizer" placeholder="e.g. Head Coach David" />
              </div>

              <div class="form-group">
                <label>Description & Rules</label>
                <textarea v-model="eventForm.description" rows="3" placeholder="Describe event details, prizes, eligibility, or equipment guidelines..."></textarea>
              </div>

              <div class="modal-actions">
                <button type="button" class="cancel-modal-btn" @click="closeCreateEventModal">Cancel</button>
                <button type="submit" class="submit-modal-btn">Publish Event</button>
              </div>
            </form>
          </div>
        </div>

        <!-- EDIT EVENT MODAL -->
        <div v-if="showEditEventModal && editingEvent" class="modal-overlay" @click.self="closeEditEventModal">
          <div class="modal-card">
            <div class="modal-header">
              <h3>✎ Edit Event: {{ editingEvent.title }}</h3>
              <button class="close-modal-btn" @click="closeEditEventModal">✕</button>
            </div>
            <form @submit.prevent="handleUpdateEvent" class="modal-form">
              <div class="form-group">
                <label>Event Title *</label>
                <input type="text" v-model="editEventForm.title" required />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Sport Category</label>
                  <select v-model="editEventForm.sport">
                    <option value="Tennis">Tennis</option>
                    <option value="Badminton">Badminton</option>
                    <option value="Squash">Squash</option>
                    <option value="Swimming">Swimming</option>
                    <option value="Social">Social</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Event Type</label>
                  <select v-model="editEventForm.type">
                    <option value="Tournament">Tournament</option>
                    <option value="Coaching Clinic">Coaching Clinic</option>
                    <option value="Social League">Social League</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Event Date</label>
                  <input type="date" v-model="editEventForm.date" />
                </div>
                <div class="form-group">
                  <label>Time Slot</label>
                  <input type="text" v-model="editEventForm.time" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Venue / Location</label>
                  <input type="text" v-model="editEventForm.venue" />
                </div>
                <div class="form-group">
                  <label>Capacity</label>
                  <input type="number" v-model="editEventForm.capacity" min="1" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Entry Fee (₹)</label>
                  <input type="number" v-model="editEventForm.fee" min="0" />
                </div>
                <div class="form-group">
                  <label>Event Status</label>
                  <select v-model="editEventForm.status">
                    <option value="Upcoming">Upcoming</option>
                    <option value="Ongoing">Ongoing</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Description</label>
                <textarea v-model="editEventForm.description" rows="3"></textarea>
              </div>

              <div class="modal-actions">
                <button type="button" class="cancel-modal-btn" @click="closeEditEventModal">Cancel</button>
                <button type="submit" class="submit-modal-btn">Save Changes</button>
              </div>
            </form>
          </div>
        </div>

        <!-- VIEW EVENT DETAILS & PARTICIPANTS MODAL -->
        <div v-if="showEventDetailsModal && selectedEvent" class="modal-overlay" @click.self="closeEventDetailsModal">
          <div class="modal-card booking-detail-modal">
            <div class="modal-header">
              <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <h2 style="margin: 0;">{{ selectedEvent.title }}</h2>
                <span class="sport-badge-pill" :class="'sport-' + selectedEvent.sport.toLowerCase()">{{ selectedEvent.sport }}</span>
                <span class="booking-status-badge" :class="'estatus-' + selectedEvent.status.toLowerCase()">{{ selectedEvent.status }}</span>
              </div>
              <button class="close-modal-btn" @click="closeEventDetailsModal">✕</button>
            </div>

            <div class="modal-body booking-detail-body">
              <div class="detail-section-card">
                <h4>Event Overview</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Event Category</span>
                    <span class="detail-val font-semibold">{{ selectedEvent.type }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Scheduled Date</span>
                    <span class="detail-val font-semibold">{{ selectedEvent.dateDisplay }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Time & Slot</span>
                    <span class="detail-val">{{ selectedEvent.time }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Venue Location</span>
                    <span class="detail-val">{{ selectedEvent.venue }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Organizer / Host</span>
                    <span class="detail-val">{{ selectedEvent.organizer }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Entry Fee</span>
                    <span class="detail-val font-bold" style="color: #2563eb;">{{ selectedEvent.fee > 0 ? '₹' + selectedEvent.fee : 'Free Entry' }}</span>
                  </div>
                </div>
              </div>

              <div class="detail-section-card">
                <h4>Event Description</h4>
                <p class="notes-text">{{ selectedEvent.description }}</p>
              </div>

              <div class="detail-section-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                  <h4 style="margin: 0; border: none; padding: 0;">Registered Participants ({{ selectedEvent.registered }} / {{ selectedEvent.capacity }})</h4>
                  <button class="export-csv-btn" style="padding: 0.35rem 0.75rem; font-size: 0.78rem;" @click="addSampleParticipant(selectedEvent)">+ Register Player</button>
                </div>

                <div v-if="!selectedEvent.participants || selectedEvent.participants.length === 0" style="color: #64748b; font-size: 0.85rem; font-style: italic;">
                  No players registered yet.
                </div>
                <div v-else class="participants-tags-list">
                  <div v-for="(p, idx) in selectedEvent.participants" :key="idx" class="participant-pill-item">
                    <span>👤 {{ p }}</span>
                    <button class="remove-participant-btn" @click="removeParticipant(selectedEvent, idx)" title="Remove">×</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <div style="display: flex; gap: 0.75rem;">
                <button class="action-icon-btn complete-btn" @click="openEditEventModal(selectedEvent)">✎ Edit Event</button>
                <button class="action-icon-btn cancel-btn" @click="requestDeleteEvent(selectedEvent)" style="display: inline-flex; align-items: center; gap: 0.4rem;">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  <span>Delete Event</span>
                </button>
              </div>
              <button class="cancel-modal-btn" @click="closeEventDetailsModal">Close</button>
            </div>
          </div>
        </div>

        <!-- DELETE EVENT CONFIRMATION MODAL -->
        <div v-if="showDeleteEventModal && eventToDelete" class="modal-overlay" @click.self="showDeleteEventModal = false">
          <div class="modal-card small-confirm-modal" style="max-width: 460px; width: 92vw; padding: 1.5rem; border-radius: 1.25rem; box-shadow: 0 20px 45px rgba(15, 23, 42, 0.22); overflow: hidden;">
            <div class="modal-header" style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.85rem;">
              <div style="display: flex; align-items: center; gap: 0.55rem;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: #fee2e2; color: #ef4444; display: grid; place-items: center; font-size: 1rem;">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </div>
                <h3 style="color: #0f172a; margin: 0; font-size: 1.1rem; font-weight: 800;">Cancel & Delete Event</h3>
              </div>
              <button class="close-modal-btn" @click="showDeleteEventModal = false">✕</button>
            </div>
            <div class="modal-body" style="padding: 1.25rem 0; overflow-wrap: break-word; word-break: break-word; white-space: normal;">
              <p style="font-size: 0.95rem; color: #334155; line-height: 1.5; margin: 0;">
                Are you sure you want to delete event <strong style="color: #0f172a;">"{{ eventToDelete.title }}"</strong>?
              </p>
              <div style="margin-top: 0.85rem; padding: 0.75rem 0.95rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: 0.75rem; color: #b91c1c; font-size: 0.82rem; line-height: 1.5; overflow-wrap: break-word; word-break: break-word;">
                📢 This action will cancel the event and automatically broadcast an announcement notice to all {{ eventToDelete.registered || 0 }} registered attendees.
              </div>
            </div>
            <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 0.75rem; border-top: 1px solid #f1f5f9; padding-top: 0.85rem; margin-top: 0.25rem;">
              <button class="cancel-modal-btn" @click="showDeleteEventModal = false">Keep Event</button>
              <button class="submit-modal-btn danger-btn" @click="confirmDeleteEvent" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: #ffffff; padding: 0.55rem 1.2rem; border-radius: 0.6rem; font-weight: 700; border: none; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);">Confirm Delete</button>
            </div>
          </div>
        </div>

        <!-- MEMBER DETAILS MODAL -->
        <div v-if="showMemberModal && selectedMemberForModal" class="modal-overlay" @click.self="showMemberModal = false">
          <div class="modal-card">
            <div class="modal-header">
              <h3>Member Profile Details</h3>
              <button class="close-modal-btn" @click="showMemberModal = false">✕</button>
            </div>
            <div class="modal-body" style="padding: 1.25rem 0;">
              <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem; background: #f8fafc; padding: 1rem; border-radius: 0.75rem; border: 1px solid #e2e8f0;">
                <div class="user-avatar-sm" style="width: 48px; height: 48px; font-size: 1.1rem; background: linear-gradient(135deg, #2563eb, #4f46e5); color: #fff; font-weight: 700; display: grid; place-items: center; border-radius: 999px;">
                  {{ selectedMemberForModal.initials }}
                </div>
                <div>
                  <h4 style="font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0;">{{ selectedMemberForModal.name }}</h4>
                  <span style="font-size: 0.85rem; color: #64748b;">{{ selectedMemberForModal.email }}</span>
                </div>
              </div>

              <div class="setting-row">
                <span class="setting-label">Membership Plan</span>
                <span style="font-weight: 700; color: #2563eb;">{{ selectedMemberForModal.plan }}</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Date Joined</span>
                <span class="setting-val">{{ selectedMemberForModal.dateJoined }}</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Total Facility Bookings</span>
                <span class="setting-val">{{ selectedMemberForModal.totalBookings }} bookings</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Contact Phone</span>
                <span class="setting-val">{{ selectedMemberForModal.phone }}</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Account Status</span>
                <span class="status-badge-chip status-active">Active & Verified</span>
              </div>
            </div>
            <div class="modal-footer">
              <button class="cancel-modal-btn" @click="showMemberModal = false">Close</button>
            </div>
          </div>
        </div>

        <!-- CREATE ANNOUNCEMENT MODAL -->
        <div v-if="showCreateAnnouncementModal" class="modal-overlay" @click.self="closeCreateAnnouncementModal">
          <div class="modal-card" style="max-width: 640px; width: 95vw; max-height: 90vh; overflow-y: auto;">
            <!-- Modern Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; border-radius: 1rem 1rem 0 0; padding: 1.25rem 1.5rem;">
              <div style="display: flex; align-items: center; gap: 0.85rem;">
                <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #3b82f6, #6366f1); display: grid; place-items: center; font-size: 1.35rem; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);">
                  📢
                </div>
                <div>
                  <h3 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Broadcast New Announcement</h3>
                  <span style="font-size: 0.82rem; color: #94a3b8;">Publish facility updates, tournament alerts, and court maintenance notices</span>
                </div>
              </div>
              <button class="close-modal-btn" @click="closeCreateAnnouncementModal" style="color: #94a3b8; background: rgba(255,255,255,0.08); border-radius: 999px; width: 32px; height: 32px; display: grid; place-items: center; border: none; font-size: 1rem;">✕</button>
            </div>

            <!-- Quick Template Bar -->
            <div style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; padding: 0.75rem 1.5rem; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Quick Starters:</span>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('maintenance')">
                🛠️ Maintenance
              </button>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('tournament')">
                🏆 Tournament
              </button>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('policy')">
                📜 Policy
              </button>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('broadcast')">
                📣 Hours Flash
              </button>
            </div>

            <div class="modal-body" style="padding: 1.5rem;">
              <!-- Title Input -->
              <div class="form-group" style="margin-bottom: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <label class="form-label font-bold" style="font-size: 0.85rem; color: #1e293b; margin: 0;">
                    Announcement Title / Headline <span style="color: #ef4444;">*</span>
                  </label>
                  <span style="font-size: 0.75rem; color: #94a3b8;">{{ announcementForm.title.length }}/100</span>
                </div>
                <input
                  v-model="announcementForm.title"
                  type="text"
                  maxlength="100"
                  class="form-control broadcast-input"
                  placeholder="e.g., Scheduled Synthetic Court Resurfacing & Lighting Upgrade"
                  required
                />
              </div>

              <!-- Category Selector Cards -->
              <div class="form-group" style="margin-bottom: 1.25rem;">
                <label class="form-label font-bold" style="display: block; font-size: 0.85rem; color: #1e293b; margin-bottom: 0.5rem;">
                  Category
                </label>
                <div class="category-selector-grid">
                  <button
                    v-for="cat in [
                      { name: 'General', icon: '📢', color: 'blue' },
                      { name: 'Broadcast', icon: '📣', color: 'purple' },
                      { name: 'Tournament', icon: '🏆', color: 'emerald' },
                      { name: 'Policy', icon: '📜', color: 'orange' },
                      { name: 'Maintenance', icon: '🛠️', color: 'rose' }
                    ]"
                    :key="cat.name"
                    type="button"
                    class="category-card-btn"
                    :class="[{ active: announcementForm.category === cat.name }, 'cat-' + cat.color]"
                    @click="announcementForm.category = cat.name"
                    style="justify-content: center; padding: 0.65rem 0.5rem;"
                  >
                    <span class="cat-icon">{{ cat.icon }}</span>
                    <span class="cat-name">{{ cat.name }}</span>
                  </button>
                </div>
              </div>

              <!-- Message / Body Textarea -->
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <label class="form-label font-bold" style="font-size: 0.85rem; color: #1e293b; margin: 0;">
                    Announcement Message Content <span style="color: #ef4444;">*</span>
                  </label>
                  <span style="font-size: 0.75rem; color: #94a3b8;">{{ announcementForm.body.length }}/500</span>
                </div>
                <textarea
                  v-model="announcementForm.body"
                  rows="5"
                  maxlength="500"
                  class="form-control broadcast-textarea"
                  placeholder="Provide comprehensive details, operational timings, affected courts, or rules..."
                  required
                ></textarea>
              </div>
            </div>

            <!-- Modal Footer -->
            <div class="modal-footer" style="display: flex; justify-content: flex-end; align-items: center; gap: 0.85rem; padding: 1.25rem 1.5rem; background: #f8fafc; border-top: 1px solid #e2e8f0; border-radius: 0 0 1rem 1rem;">
              <button type="button" class="cancel-modal-btn" @click="closeCreateAnnouncementModal">Cancel</button>
              <button
                type="button"
                class="submit-modal-btn broadcast-submit-btn"
                :disabled="isSubmittingAnnouncement"
                @click="submitCreateAnnouncement"
              >
                <span v-if="isSubmittingAnnouncement" class="spinner-xs"></span>
                <span v-else style="font-size: 1rem;">🚀</span>
                <span>{{ isSubmittingAnnouncement ? 'Publishing...' : 'Publish Announcement' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- ANNOUNCEMENT DETAILS MODAL -->
        <div v-if="showAnnouncementDetailsModal && selectedAnnouncement" class="modal-overlay" @click.self="closeAnnouncementDetails">
          <div class="modal-card modal-card-details" style="max-width: 580px; width: 95vw;">
            <div class="modal-header" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; border-radius: 1rem 1rem 0 0; padding: 1.25rem 1.5rem;">
              <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span class="announcement-badge" :class="selectedAnnouncement.categoryClass" style="font-size: 0.82rem; padding: 0.35rem 0.75rem;">
                  {{ selectedAnnouncement.icon || '📢' }} {{ selectedAnnouncement.category }}
                </span>
                <span style="font-size: 0.82rem; color: #94a3b8;">
                  {{ selectedAnnouncement.date }}
                </span>
              </div>
              <button class="close-modal-btn" @click="closeAnnouncementDetails" style="color: #94a3b8; background: rgba(255,255,255,0.08); border-radius: 999px; width: 32px; height: 32px; display: grid; place-items: center; border: none; font-size: 1rem;">✕</button>
            </div>

            <div class="modal-body" style="padding: 1.5rem;">
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0 0 1rem; line-height: 1.35; letter-spacing: -0.01em;">
                {{ selectedAnnouncement.title }}
              </h3>

              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; margin-bottom: 1.25rem;">
                <h5 style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin: 0 0 0.5rem; font-weight: 700;">Announcement Details</h5>
                <p style="font-size: 0.95rem; color: #334155; line-height: 1.65; white-space: pre-wrap; margin: 0;">
                  {{ selectedAnnouncement.body || 'No detailed message description provided.' }}
                </p>
              </div>

              <div class="announcement-meta-grid" style="grid-template-columns: 1fr 1fr;">
                <div class="meta-card">
                  <span class="meta-label">Category</span>
                  <span class="meta-val font-bold">{{ selectedAnnouncement.category }}</span>
                </div>
                <div class="meta-card">
                  <span class="meta-label">Date Published</span>
                  <span class="meta-val">{{ selectedAnnouncement.date }}</span>
                </div>
              </div>
            </div>

            <div class="modal-footer" style="display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; padding: 1.25rem 1.5rem; background: #f8fafc; border-top: 1px solid #e2e8f0; border-radius: 0 0 1rem 1rem;">
              <button
                type="button"
                class="cancel-modal-btn danger-btn"
                style="background: #fef2f2; color: #ef4444; border: 1px solid #fecaca; display: inline-flex; align-items: center; gap: 0.35rem;"
                @click="handleDeleteAnnouncement(selectedAnnouncement)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="15" height="15">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Delete Announcement</span>
              </button>
              <button type="button" class="cancel-modal-btn" @click="closeAnnouncementDetails">Close</button>
            </div>
          </div>
        </div>

        <!-- Edit Admin Profile Modal -->
        <div v-if="showEditProfileModal" class="modal-overlay" @click.self="closeEditProfileModal">
          <div class="modal-card" style="max-width: 520px; width: 95vw; max-height: 90vh; overflow-y: auto;">
            <!-- Modal Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; border-radius: 1rem 1rem 0 0; padding: 1.25rem 1.5rem; display: flex; justify-content: space-between; align-items: center;">
              <div style="display: flex; align-items: center; gap: 0.85rem;">
                <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #3b82f6, #6366f1); display: grid; place-items: center; font-size: 1.35rem; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);">
                  👤
                </div>
                <div>
                  <h3 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Edit Admin Profile</h3>
                  <span style="font-size: 0.82rem; color: #94a3b8;">Update your administrative contact details and credentials</span>
                </div>
              </div>
              <button type="button" class="close-modal-btn" @click="closeEditProfileModal" style="color: #94a3b8; background: rgba(255,255,255,0.08); border-radius: 999px; width: 32px; height: 32px; display: grid; place-items: center; border: none; font-size: 1rem; cursor: pointer;">✕</button>
            </div>

            <!-- Modal Body Form -->
            <form @submit.prevent="saveAdminProfile" class="modal-body" style="padding: 1.5rem;">
              <!-- Avatar Preview & Change -->
              <div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 0.85rem; border: 1px solid #e2e8f0;">
                <div style="position: relative; width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; display: grid; place-items: center; font-size: 1.3rem; font-weight: 800; overflow: hidden; flex-shrink: 0; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">
                  <img v-if="editProfileForm.avatarUrl" :src="editProfileForm.avatarUrl" alt="Avatar preview" style="width: 100%; height: 100%; object-fit: cover;" />
                  <span v-else>{{ getInitials(editProfileForm.name || adminProfile.name) }}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.4rem; flex: 1;">
                  <span style="font-size: 0.85rem; font-weight: 700; color: #1e293b;">Profile Avatar</span>
                  <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                    <label class="modal-upload-btn" style="background: #2563eb; color: #ffffff; font-size: 0.78rem; font-weight: 600; padding: 0.4rem 0.85rem; border-radius: 0.5rem; cursor: pointer; display: inline-flex; align-items: center; gap: 0.35rem; transition: background 0.2s ease;">
                      📷 Choose Photo
                      <input type="file" accept="image/*" @change="handleEditAvatarUpload" style="display: none;" />
                    </label>
                    <button v-if="editProfileForm.avatarUrl" type="button" @click="removeEditAvatar" style="background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; font-size: 0.78rem; font-weight: 600; padding: 0.4rem 0.85rem; border-radius: 0.5rem; cursor: pointer;">
                      Remove
                    </button>
                  </div>
                </div>
              </div>

              <!-- Full Name Field -->
              <div class="form-group" style="margin-bottom: 1.15rem;">
                <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                  Full Name <span style="color: #ef4444;">*</span>
                </label>
                <input
                  v-model="editProfileForm.name"
                  type="text"
                  required
                  placeholder="e.g. Alex Morgan"
                  class="form-control"
                  style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                />
              </div>

              <!-- Email Field -->
              <div class="form-group" style="margin-bottom: 1.15rem;">
                <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                  Email Address <span style="color: #ef4444;">*</span>
                </label>
                <input
                  v-model="editProfileForm.email"
                  type="email"
                  required
                  placeholder="e.g. alex.morgan@clubdash.com"
                  class="form-control"
                  style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                />
              </div>

              <!-- Phone Field -->
              <div class="form-group" style="margin-bottom: 1.15rem;">
                <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                  Phone Number
                </label>
                <input
                  v-model="editProfileForm.phone"
                  type="text"
                  placeholder="e.g. +91 98765 43210"
                  class="form-control"
                  style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                />
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.15rem;">
                <!-- Role / Title -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                    Role Title
                  </label>
                  <input
                    v-model="editProfileForm.role"
                    type="text"
                    placeholder="e.g. Super Admin"
                    class="form-control"
                    style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                  />
                </div>

                <!-- Club Facility -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                    Club Facility <span style="font-size: 0.72rem; color: #64748b; font-weight: 500;">(Permanent)</span>
                  </label>
                  <input
                    type="text"
                    value="ClubDash"
                    disabled
                    class="form-control"
                    style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #e2e8f0; background: #f8fafc; color: #64748b; font-weight: 600; border-radius: 0.6rem; font-size: 0.9rem; cursor: not-allowed;"
                  />
                </div>
              </div>

              <!-- Modal Footer -->
              <div class="modal-footer" style="display: flex; justify-content: flex-end; align-items: center; gap: 0.75rem; padding-top: 1.25rem; border-top: 1px solid #e2e8f0; margin-top: 1.5rem;">
                <button type="button" class="cancel-modal-btn" @click="closeEditProfileModal" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 600; padding: 0.65rem 1.25rem; border-radius: 0.6rem; cursor: pointer;">
                  Cancel
                </button>
                <button type="submit" class="submit-modal-btn" style="background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; font-weight: 700; padding: 0.65rem 1.4rem; border-radius: 0.6rem; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35); display: inline-flex; align-items: center; gap: 0.4rem;">
                  <span>Save Changes</span>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- First-Time Admin Phone Setup Modal -->
        <div v-if="showFirstTimePhoneModal" class="modal-overlay" style="z-index: 500;">
          <div class="modal-card" style="max-width: 440px; width: 95vw; border-radius: 1.25rem; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
            <!-- Modal Header -->
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; padding: 1.5rem; text-align: center; position: relative;">
              <div style="width: 52px; height: 52px; border-radius: 16px; background: linear-gradient(135deg, #2563eb, #4f46e5); display: grid; place-items: center; font-size: 1.6rem; margin: 0 auto 0.75rem; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);">
                📱
              </div>
              <h3 style="margin: 0 0 0.35rem; font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Welcome to ClubDash</h3>
              <p style="margin: 0; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                Please provide your contact phone number to complete your administrator setup.
              </p>
            </div>

            <!-- Modal Body Form -->
            <form @submit.prevent="submitFirstTimePhone" style="padding: 1.5rem; background: #ffffff;">
              <div class="form-group" style="margin-bottom: 1.25rem;">
                <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 700; color: #1e293b; margin-bottom: 0.45rem;">
                  Admin Phone Number <span style="color: #ef4444;">*</span>
                </label>
                <input
                  v-model="firstTimePhoneInput"
                  type="tel"
                  required
                  placeholder="e.g. +91 98765 43210"
                  class="form-control"
                  style="width: 100%; padding: 0.75rem 0.95rem; border: 1.5px solid #cbd5e1; border-radius: 0.65rem; font-size: 0.95rem;"
                  autofocus
                />
                <span style="display: block; font-size: 0.75rem; color: #64748b; margin-top: 0.4rem;">
                  🔒 You will only be asked for this once upon your first login.
                </span>
              </div>

              <div style="display: flex; gap: 0.75rem; justify-content: flex-end; align-items: center; margin-top: 1.5rem;">
                <button
                  type="button"
                  @click="skipFirstTimePhone"
                  style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 600; padding: 0.65rem 1.15rem; border-radius: 0.6rem; cursor: pointer; font-size: 0.85rem;"
                >
                  Skip for Now
                </button>
                <button
                  type="submit"
                  style="background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; font-weight: 700; padding: 0.65rem 1.4rem; border-radius: 0.6rem; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35); font-size: 0.85rem;"
                >
                  Save & Continue
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, inject, watch, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCourtStore } from '@/stores/courts'
import { useNotificationStore } from '@/stores/notifications'
import api from '@/api/axios'
import { getSportImage } from '@/utils/sportImages'

const toast = inject('toast')
const courtStore = useCourtStore()
const notificationStore = useNotificationStore()
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

// =========================================================
// COURTS STATE
// =========================================================
const totalCourts = computed(() => courtStore.courts.length)
const activeCourtsCount = computed(() => courtStore.courts.filter((c) => c.is_active).length)
const inactiveCourtsCount = computed(() => courtStore.courts.filter((c) => !c.is_active).length)

const clubForm = ref({
  name: '',
  address: '',
  open_time: '',
  close_time: '',
  slot_duration_minutes: 60,
})

const courtForm = ref({
  court_name: '',
  sport_type: 'tennis',
  is_active: true,
  use_defaults: true,
  open_time_override: '',
  close_time_override: '',
  slot_duration_override: '',
})

// =========================================================
// MEMBERS STATE (REAL DATA)
// =========================================================
const memberSearchQuery = ref('')
const selectedMemberPlanFilter = ref('All')
const selectedMemberForModal = ref(null)
const showMemberModal = ref(false)
const members = ref([])

// Fetch members from backend
async function fetchMembers() {
  try {
    const res = await api.get('/admin/members')
    members.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.error('Failed to fetch members:', err)
    if (toast) toast.error('Unable to load members')
  }
}

// Watch activeNav to fetch when Members tab is opened
watch(activeNav, (newTab) => {
  if (newTab === 'Members') fetchMembers()
})

// Map real backend data to display fields
const filteredMembersList = computed(() => {
  let list = members.value.map(m => ({
    id: m.id,
    name: m.name,
    email: m.email,
    initials: (m.name || 'M').charAt(0).toUpperCase(),
    plan: m.membership_plan || 'No Plan',
    dateJoined: m.created_at
      ? new Date(m.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
      : '—',
    totalBookings: m.booking_count || 0,
    phone: m.phone || '—',
    membership_status: m.membership_status || 'none'
  }))

  const q = memberSearchQuery.value.toLowerCase().trim()
  if (q) {
    list = list.filter(m =>
      (m.name && m.name.toLowerCase().includes(q)) ||
      (m.email && m.email.toLowerCase().includes(q)) ||
      (m.plan && m.plan.toLowerCase().includes(q))
    )
  }

  if (selectedMemberPlanFilter.value !== 'All') {
    list = list.filter(m => m.plan === selectedMemberPlanFilter.value)
  }
  return list
})

// KPI real values
const totalMembers = computed(() => members.value.length)
const activeMembers = computed(() => members.value.filter(m => m.membership_status === 'active').length)
const totalBookingsAll = computed(() => members.value.reduce((sum, m) => sum + (m.booking_count || 0), 0))

// =========================================================
// COURTS & CLUB ACTIONS
// =========================================================
// Fetch data on mount
// ---------------------------------------------------------------
// Live backend data (replaces the placeholder figures below)
// ---------------------------------------------------------------
const analyticsLoading = ref(false)
const analyticsError = ref('')
const adminAnalytics = ref(null)

const inr = (n) => `₹${Number(n || 0).toLocaleString('en-IN')}`

/** Pull real KPIs from /analytics/admin and map them onto the dashboard. */
async function loadAdminAnalytics() {
  analyticsLoading.value = true
  analyticsError.value = ''
  try {
    const days = parseInt(analyticsTimeframe.value, 10) || 30
    const { data } = await api.get('/analytics/admin', { params: { days } })
    adminAnalytics.value = data

    kpiCards.value = [
      {
        title: 'Total Members', value: String(data.members.total),
        icon: 'members', colorClass: 'blue',
        trend: `${data.members.active} active`, trendType: 'neutral',
      },
      {
        title: 'Active Courts',
        value: `${data.courts.active} / ${data.courts.total}`,
        icon: 'courts', colorClass: 'emerald',
        trend: `${data.courts.utilisation_percent}% utilisation`, trendType: 'neutral',
      },
      {
        title: 'Upcoming Bookings', value: String(data.bookings.upcoming),
        icon: 'bookings', colorClass: 'purple',
        trend: `${data.bookings.total} all-time`, trendType: 'neutral',
      },
      {
        title: 'Revenue', value: inr(data.revenue.total),
        icon: 'events', colorClass: 'orange',
        trend: `${data.revenue.pending_payments} pending`, trendType: 'neutral',
      },
    ]

    // Real per-court booking distribution
    const palette = ['bar-blue', 'bar-emerald', 'bar-orange', 'bar-purple']
    bookingTrends.value = data.courts.breakdown.map((c, i) => ({
      sport: c.court_name,
      count: c.bookings,
      percentage: c.percentage,
      colorClass: palette[i % palette.length],
    }))

    courtUtilization.value = [{
      period: `Overall (last ${data.window_days} days)`,
      rate: data.courts.utilisation_percent,
      colorClass: 'bar-blue',
    }]
  } catch (err) {
    analyticsError.value =
      err?.response?.data?.message || 'Could not load analytics.'
  } finally {
    analyticsLoading.value = false
  }
}

/** Real bookings for this club (owners previously could not see any). */
async function loadClubBookings() {
  try {
    const { data } = await api.get('/bookings/club')
    const statusMap = { active: 'Confirmed', released: 'Cancelled', overridden: 'Cancelled' }
    bookingsList.value = data.bookings.map((b) => {
      const initials = (b.member_name || '?')
        .split(' ').map((w) => w[0]).slice(0, 2).join('').toUpperCase()
      return {
        id: `BK-${b.id}`,
        player: b.member_name || 'Unknown',
        email: b.member_email || '',
        phone: '',
        facility: b.court_name,
        sport: b.court_name,
        date: b.date,
        dateDisplay: b.date,
        time: `${String(b.start_time).slice(0, 5)} - ${String(b.end_time).slice(0, 5)}`,
        duration: '',
        amount: 0,
        paymentStatus: '',
        paymentMethod: '',
        status: statusMap[b.status] || b.status,
        initials,
        userType: 'Member',
        createdAt: b.created_at || '',
        notes: '',
      }
    })
  } catch (err) {
    analyticsError.value =
      err?.response?.data?.message || 'Could not load bookings.'
  }
}

onMounted(async () => {
  if (!auth.initialized || !auth.user) {
    try {
      await auth.restoreUser()
    } catch (e) { /* empty */ }
  }
  syncProfileWithAuthUser(auth.user)
  checkFirstTimePhoneSetup(auth.user)
  courtStore.fetchCourts()
  notificationStore.fetchNotifications()
  loadAdminAnalytics()
  loadClubBookings()
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

const openAddCourtModal = () => {
  showEditCourtModal.value = false
  currentEditCourt.value = null
  courtForm.value = {
    court_name: '',
    sport_type: 'tennis',
    is_active: true,
    use_defaults: true,
    open_time_override: '',
    close_time_override: '',
    slot_duration_override: '',
  }
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
    sport_type: courtForm.value.sport_type,
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
    } else {
      toast.error(result.error || 'Failed to create club')
    }
  }
}

const openEditCourtModal = (court) => {
  showAddCourtModal.value = false
  currentEditCourt.value = court
  const hasOverrides =
    court.open_time_override || court.close_time_override || court.slot_duration_override
  courtForm.value = {
    court_name: court.name,
    sport_type: court.sport_type || 'multi-purpose',
    is_active: court.is_active,
    use_defaults: !hasOverrides,
    open_time_override: court.open_time_override || '',
    close_time_override: court.close_time_override || '',
    slot_duration_override: court.slot_duration_override || '',
  }
  showEditCourtModal.value = true
}

const sportLabel = (value) => {
  const sport = courtStore.sportsTypes.find((item) => item.value === value)
  return sport ? `${sport.icon} ${sport.label}` : '🏟️ Multi-purpose'
}

// =========================================================
// HEADER & NAVIGATION
// =========================================================
const headerTitle = computed(() => {
  switch (activeNav.value) {
    case 'Members': return 'Members Management'
    case 'Courts': return 'Facility & Courts'
    case 'Bookings': return 'Bookings & Reservations'
    case 'Events': return 'Events & Tournaments'
    case 'Announcements': return 'Announcements & Broadcasts'
    case 'Analytics': return 'Performance & Analytics'
    case 'Settings': return 'System Settings'
    default: return 'Admin Dashboard'
  }
})

const headerSubtitle = computed(() => {
  switch (activeNav.value) {
    case 'Members': return 'Overview of registered club members, pending requests, and player accounts.'
    case 'Courts': return 'Monitor court availability, status, and maintenance schedules.'
    case 'Bookings': return 'Track active reservations, upcoming court slots, and cancellations.'
    case 'Events': return 'Organize tournaments, coaching sessions, and social club activities.'
    case 'Announcements': return 'Broadcast facility notices, schedule updates, and tournament alerts.'
    case 'Analytics': return 'Detailed statistics on booking trends, peak hours, and membership growth.'
    case 'Settings': return 'Configure club information, operating hours, and notification preferences.'
    default: return 'Welcome back, Administrator • Monitor club operations and analytics.'
  }
})

const primaryNavItems = ref([
  { name: 'Dashboard', icon: 'dashboard' },
  { name: 'Members', icon: 'members' },
  { name: 'Courts', icon: 'courts' },
  { name: 'Bookings', icon: 'bookings' },
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

// =========================================================
// DASHBOARD MOCK DATA (keep as is if needed, but can be dynamic)
// =========================================================
const kpiCards = ref([
  { title: 'Total Members', value: '1,248', icon: 'members', colorClass: 'blue', trend: '+12.4% this month', trendType: 'positive' },
  { title: 'Active Courts', value: '14 / 16', icon: 'courts', colorClass: 'emerald', trend: '87.5% operational', trendType: 'neutral' },
  { title: "Today's Bookings", value: '42', icon: 'bookings', colorClass: 'purple', trend: '+8 vs yesterday', trendType: 'positive' },
  { title: 'Active Events', value: '6', icon: 'events', colorClass: 'orange', trend: '2 starting today', trendType: 'neutral' },
])

// =========================================================
// BOOKINGS STATE
// =========================================================
const bookingsList = ref([
  { id: 'BK-101', player: 'John Doe', email: 'john.doe@example.com', phone: '+1 (555) 234-5678', facility: 'Tennis Court 2', sport: 'Tennis', date: '2026-08-09', dateDisplay: 'Today', time: '5:00 PM - 7:00 PM', duration: '2.0 hrs', amount: 50, paymentStatus: 'Paid', paymentMethod: 'Credit Card (Stripe)', status: 'Confirmed', initials: 'JD', userType: 'Member (VIP)', createdAt: '2026-08-09 10:15 AM', notes: 'Player requested hard court surface preference.' },
  { id: 'BK-102', player: 'Jane Smith', email: 'jane.smith@example.com', phone: '+1 (555) 345-6789', facility: 'Badminton Arena A', sport: 'Badminton', date: '2026-08-09', dateDisplay: 'Today', time: '6:00 PM - 7:30 PM', duration: '1.5 hrs', amount: 35, paymentStatus: 'Paid', paymentMethod: 'UPI / Digital Wallet', status: 'Confirmed', initials: 'JS', userType: 'Member (Standard)', createdAt: '2026-08-09 11:30 AM', notes: 'Double badminton session.' },
  { id: 'BK-103', player: 'Robert Paul', email: 'robert.paul@example.com', phone: '+1 (555) 456-7890', facility: 'Squash Court 2', sport: 'Squash', date: '2026-08-09', dateDisplay: 'Today', time: '7:00 PM - 8:00 PM', duration: '1.0 hr', amount: 25, paymentStatus: 'Refunded', paymentMethod: 'Credit Card', status: 'Cancelled', initials: 'RP', userType: 'Casual Player', createdAt: '2026-08-08 09:45 AM', notes: 'Cancelled by user due to personal conflict.' },
  { id: 'BK-104', player: 'Alice Johnson', email: 'alice.johnson@example.com', phone: '+1 (555) 567-8901', facility: 'Tennis Court 1', sport: 'Tennis', date: '2026-08-10', dateDisplay: 'Tomorrow', time: '09:00 AM - 11:00 AM', duration: '2.0 hrs', amount: 60, paymentStatus: 'Paid', paymentMethod: 'Credit Card', status: 'Confirmed', initials: 'AJ', userType: 'Member (VIP)', createdAt: '2026-08-08 14:20 PM', notes: 'Coaching session booking.' },
  { id: 'BK-105', player: 'Michael Brown', email: 'michael.b@example.com', phone: '+1 (555) 678-9012', facility: 'Swimming Lane 1', sport: 'Swimming', date: '2026-08-10', dateDisplay: 'Tomorrow', time: '07:00 AM - 08:00 AM', duration: '1.0 hr', amount: 20, paymentStatus: 'Paid', paymentMethod: 'Debit Card', status: 'Completed', initials: 'MB', userType: 'Casual Player', createdAt: '2026-08-07 16:10 PM', notes: 'Morning swim session.' },
  { id: 'BK-106', player: 'Sophia Martinez', email: 'sophia.m@example.com', phone: '+1 (555) 789-0123', facility: 'Badminton Arena B', sport: 'Badminton', date: '2026-08-11', dateDisplay: 'Aug 11', time: '04:00 PM - 05:30 PM', duration: '1.5 hrs', amount: 35, paymentStatus: 'Pending', paymentMethod: 'Pay at Desk', status: 'Pending', initials: 'SM', userType: 'Guest', createdAt: '2026-08-09 15:00 PM', notes: 'Pending walk-in payment at desk.' },
  { id: 'BK-107', player: 'David Lee', email: 'david.lee@example.com', phone: '+1 (555) 890-1234', facility: 'Squash Court 1', sport: 'Squash', date: '2026-08-12', dateDisplay: 'Aug 12', time: '06:00 PM - 07:00 PM', duration: '1.0 hr', amount: 30, paymentStatus: 'Paid', paymentMethod: 'Credit Card', status: 'Confirmed', initials: 'DL', userType: 'Member (Standard)', createdAt: '2026-08-09 16:30 PM', notes: 'Regular member slot.' }
])

const bookingSearchQuery = ref('')
const bookingStatusFilter = ref('All')
const bookingFacilityFilter = ref('All')
const bookingDateFilter = ref('All')
const bookingSortBy = ref('newest')

const showBookingDetailsModal = ref(false)
const selectedBooking = ref(null)
const showNewBookingModal = ref(false)
const showCancelConfirmModal = ref(false)
const bookingToCancel = ref(null)

const newBookingForm = reactive({
  player: '',
  email: '',
  phone: '',
  facility: 'Tennis Court 1',
  sport: 'Tennis',
  date: new Date().toISOString().split('T')[0],
  time: '10:00 AM - 11:00 AM',
  duration: '1.0 hr',
  amount: 40,
  paymentStatus: 'Paid',
  status: 'Confirmed',
  userType: 'Casual Player',
  notes: ''
})

function isTimeCompleted(booking) {
  if (!booking || booking.status === 'Cancelled' || booking.status === 'Completed') return false
  const today = new Date().toISOString().split('T')[0]
  if (booking.date < today) return true
  return false
}

function getEffectiveStatus(booking) {
  if (!booking) return 'Confirmed'
  if (booking.status === 'Cancelled') return 'Cancelled'
  if (booking.status === 'Completed') return 'Completed'
  if (isTimeCompleted(booking)) return 'Completed'
  return booking.status
}

function resetBookingFilters() {
  bookingSearchQuery.value = ''
  bookingStatusFilter.value = 'All'
  bookingFacilityFilter.value = 'All'
  bookingDateFilter.value = 'All'
  bookingSortBy.value = 'newest'
}

const filteredBookings = computed(() => {
  return bookingsList.value.filter(b => {
    const q = bookingSearchQuery.value.trim().toLowerCase()
    const matchesSearch = !q ||
      b.id.toLowerCase().includes(q) ||
      b.player.toLowerCase().includes(q) ||
      b.email.toLowerCase().includes(q) ||
      b.facility.toLowerCase().includes(q)

    const effStatus = getEffectiveStatus(b)
    const matchesStatus = bookingStatusFilter.value === 'All' || effStatus.toLowerCase() === bookingStatusFilter.value.toLowerCase()
    const matchesFacility = bookingFacilityFilter.value === 'All' ||
      b.sport.toLowerCase() === bookingFacilityFilter.value.toLowerCase() ||
      b.facility.toLowerCase().includes(bookingFacilityFilter.value.toLowerCase())

    let matchesDate = true
    if (bookingDateFilter.value === 'Today') {
      matchesDate = b.dateDisplay === 'Today' || b.date === new Date().toISOString().split('T')[0]
    } else if (bookingDateFilter.value === 'Upcoming') {
      matchesDate = effStatus === 'Confirmed' || effStatus === 'Pending'
    } else if (bookingDateFilter.value === 'Past') {
      matchesDate = effStatus === 'Completed' || effStatus === 'Cancelled'
    }

    return matchesSearch && matchesStatus && matchesFacility && matchesDate
  }).sort((a, b) => {
    if (bookingSortBy.value === 'newest') return b.id.localeCompare(a.id)
    if (bookingSortBy.value === 'oldest') return a.id.localeCompare(b.id)
    if (bookingSortBy.value === 'name') return a.player.localeCompare(b.player)
    if (bookingSortBy.value === 'amount') return b.amount - a.amount
    return 0
  })
})

const bookingKpis = computed(() => {
  const total = bookingsList.value.length
  const confirmed = bookingsList.value.filter(b => getEffectiveStatus(b) === 'Confirmed').length
  const completed = bookingsList.value.filter(b => getEffectiveStatus(b) === 'Completed').length
  const autoCompleted = bookingsList.value.filter(b => isTimeCompleted(b)).length
  const cancelled = bookingsList.value.filter(b => b.status === 'Cancelled').length
  return { total, confirmed, completed, autoCompleted, cancelled }
})

function openBookingDetails(booking) {
  selectedBooking.value = booking
  showBookingDetailsModal.value = true
}

function closeBookingDetailsModal() {
  showBookingDetailsModal.value = false
  selectedBooking.value = null
}

function requestCancelBooking(booking) {
  showBookingDetailsModal.value = false
  selectedBooking.value = null
  bookingToCancel.value = booking
  showCancelConfirmModal.value = true
}

function confirmCancelBooking() {
  if (!bookingToCancel.value) return
  const target = bookingsList.value.find(b => b.id === bookingToCancel.value.id)
  if (target) {
    target.status = 'Cancelled'
    target.paymentStatus = 'Refunded'
  }
  if (selectedBooking.value && selectedBooking.value.id === bookingToCancel.value.id) {
    selectedBooking.value.status = 'Cancelled'
    selectedBooking.value.paymentStatus = 'Refunded'
  }
  showCancelConfirmModal.value = false
  bookingToCancel.value = null
  if (toast) toast.success('Booking cancelled successfully!')
}

function markBookingCompleted(booking) {
  const target = bookingsList.value.find(b => b.id === booking.id)
  if (target) target.status = 'Completed'
  if (selectedBooking.value && selectedBooking.value.id === booking.id) selectedBooking.value.status = 'Completed'
  if (toast) toast.success(`Booking ${booking.id} marked as Completed!`)
}

function openNewBookingModal() {
  newBookingForm.player = ''
  newBookingForm.email = ''
  newBookingForm.phone = ''
  newBookingForm.notes = ''
  showNewBookingModal.value = true
}

function closeNewBookingModal() {
  showNewBookingModal.value = false
}

function handleCreateNewBooking() {
  if (!newBookingForm.player || !newBookingForm.email) {
    if (toast) toast.error('Please enter player name and email.')
    return
  }
  const newId = `BK-${100 + bookingsList.value.length + 1}`
  const initials = newBookingForm.player.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2) || 'BK'

  const createdBooking = {
    id: newId,
    player: newBookingForm.player,
    email: newBookingForm.email,
    phone: newBookingForm.phone || '+1 (555) 000-0000',
    facility: newBookingForm.facility,
    sport: newBookingForm.sport,
    date: newBookingForm.date,
    dateDisplay: newBookingForm.date,
    time: newBookingForm.time,
    duration: newBookingForm.duration || '1.0 hr',
    amount: Number(newBookingForm.amount) || 0,
    paymentStatus: newBookingForm.paymentStatus,
    paymentMethod: 'Admin Manual Entry',
    status: newBookingForm.status,
    initials: initials,
    userType: newBookingForm.userType,
    createdAt: new Date().toLocaleString(),
    notes: newBookingForm.notes || 'Created manually by Admin'
  }

  bookingsList.value.unshift(createdBooking)
  showNewBookingModal.value = false
  if (toast) toast.success(`New booking ${newId} created successfully!`)
}

async function loadAdminBookings() {
  try {
    const res = await api.get('/bookings')
    if (Array.isArray(res.data) && res.data.length > 0) {
      const realBookings = res.data.map(b => {
        const courtName = b.court?.name || 'Main Court'
        const sport = b.court?.sport_type || (courtName.toLowerCase().includes('badminton') ? 'Badminton' : courtName.toLowerCase().includes('squash') ? 'Squash' : 'Tennis')
        const playerName = b.user?.name || (b.user_id ? `Member #${b.user_id}` : 'Club Member')
        const initials = playerName.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2) || 'MB'
        return {
          id: `BK-${b.id}`,
          player: playerName,
          email: b.user?.email || 'member@clubdash.com',
          phone: b.user?.phone || '+91 98765 43210',
          facility: courtName,
          sport: sport.charAt(0).toUpperCase() + sport.slice(1),
          date: b.booking_date,
          dateDisplay: b.booking_date,
          time: `${(b.start_time || '09:00').substring(0, 5)} - ${(b.end_time || '10:00').substring(0, 5)}`,
          duration: '1.0 hr',
          amount: b.court?.price_per_hour || 500,
          paymentStatus: 'Paid',
          paymentMethod: 'Online Payment',
          status: b.status ? (b.status.charAt(0).toUpperCase() + b.status.slice(1)) : 'Confirmed',
          initials,
          userType: 'Active Member',
          createdAt: b.created_at || b.booking_date,
          notes: ''
        }
      })
      bookingsList.value = realBookings
    }
  } catch (err) {
    console.warn('Could not fetch real bookings for admin:', err)
  }
}

function exportBookingsCSV() {
  const headers = ['Booking ID', 'Player', 'Email', 'Facility', 'Sport', 'Date', 'Time', 'Amount', 'Payment Status', 'Booking Status']
  const rows = filteredBookings.value.map(b => [
    b.id,
    `"${b.player}"`,
    `"${b.email}"`,
    `"${b.facility}"`,
    b.sport,
    b.date,
    `"${b.time}"`,
    b.amount,
    b.paymentStatus,
    b.status
  ])

  const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `clubdash_bookings_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  if (toast) toast.success('Bookings exported to CSV!')
}

// =========================================================
// ANALYTICS DATA (MOCK)
// =========================================================
const bookingTrends = ref([
  { sport: 'Tennis Courts', count: 189, percentage: 45, colorClass: 'bar-blue' },
  { sport: 'Badminton Arenas', count: 126, percentage: 30, colorClass: 'bar-emerald' },
  { sport: 'Squash Courts', count: 63, percentage: 15, colorClass: 'bar-orange' },
  { sport: 'Swimming Lanes', count: 42, percentage: 10, colorClass: 'bar-purple' },
])

const courtUtilization = ref([
  { period: 'Prime Hours (5 PM - 10 PM)', rate: 92, colorClass: 'bar-blue' },
  { period: 'Afternoon (12 PM - 5 PM)', rate: 68, colorClass: 'bar-indigo' },
  { period: 'Morning (6 AM - 12 PM)', rate: 54, colorClass: 'bar-purple' },
])

// =========================================================
// ANNOUNCEMENTS STATE
// =========================================================
const announcementsSearchQuery = ref('')
const announcementsCategoryFilter = ref('All')
const showCreateAnnouncementModal = ref(false)
const showAnnouncementDetailsModal = ref(false)
const selectedAnnouncement = ref(null)
const isSubmittingAnnouncement = ref(false)

const announcementForm = ref({
  title: '',
  category: 'General',
  body: '',
})

const announcements = computed(() => notificationStore.announcements)

const filteredAnnouncements = computed(() => {
  let list = announcements.value
  if (announcementsCategoryFilter.value !== 'All') {
    list = list.filter(item => item.category.toLowerCase() === announcementsCategoryFilter.value.toLowerCase())
  }
  if (announcementsSearchQuery.value.trim()) {
    const q = announcementsSearchQuery.value.toLowerCase()
    list = list.filter(item =>
      (item.title && item.title.toLowerCase().includes(q)) ||
      (item.body && item.body.toLowerCase().includes(q))
    )
  }
  return list
})

const openCreateAnnouncementModal = () => {
  showAnnouncementDetailsModal.value = false
  selectedAnnouncement.value = null
  announcementForm.value = {
    title: '',
    category: 'General',
    body: '',
  }
  showCreateAnnouncementModal.value = true
}

const applyAnnouncementTemplate = (templateType) => {
  if (templateType === 'maintenance') {
    announcementForm.value = {
      title: 'Scheduled Court Maintenance & Surface Care',
      category: 'Maintenance',
      body: 'Courts 1 and 2 will be temporarily unavailable on Thursday from 08:00 AM to 02:00 PM for deep surface cleaning and line recoating. Regular reservations resume at 02:30 PM.',
    }
  } else if (templateType === 'tournament') {
    announcementForm.value = {
      title: 'Registrations Open: Club Summer Grand Slam 2026',
      category: 'Tournament',
      body: 'Sign-ups are officially live for our annual summer championship! Singles and doubles brackets available with trophies, medal awards, and ₹50,000 cash prize pool.',
    }
  } else if (templateType === 'policy') {
    announcementForm.value = {
      title: 'Updated Court Booking Rules & Footwear Guidelines',
      category: 'Policy',
      body: 'All players are kindly reminded to check in with front desk reception prior to slot start time. Strict non-marking sports shoes are required on all indoor synthetic courts.',
    }
  } else if (templateType === 'broadcast') {
    announcementForm.value = {
      title: 'Flash Alert: Evening Facility Hours Extended',
      category: 'Broadcast',
      body: 'Due to overwhelming demand, court floodlight operating hours are extended until 11:00 PM throughout this weekend. Slots are now open on the booking calendar.',
    }
  }
  toast ? toast.success('Template loaded!') : null
}

const handleCreateAnnouncement = () => {
  openCreateAnnouncementModal()
}

const closeCreateAnnouncementModal = () => {
  showCreateAnnouncementModal.value = false
}

const submitCreateAnnouncement = async () => {
  if (!announcementForm.value.title.trim()) {
    toast ? toast.error('Please enter an announcement title') : alert('Please enter an announcement title')
    return
  }
  if (!announcementForm.value.body.trim()) {
    toast ? toast.error('Please enter announcement message content') : alert('Please enter announcement message content')
    return
  }
  isSubmittingAnnouncement.value = true
  const result = await notificationStore.createAnnouncement({
    title: announcementForm.value.title.trim(),
    body: announcementForm.value.body.trim(),
    category: announcementForm.value.category,
  })
  isSubmittingAnnouncement.value = false

  if (result.success) {
    closeCreateAnnouncementModal()
    toast ? toast.success('Announcement broadcasted successfully! 📢') : alert('Announcement broadcasted!')
  } else {
    toast ? toast.error(result.error || 'Failed to broadcast announcement') : alert(result.error || 'Failed to broadcast')
  }
}

const openAnnouncementDetails = (item) => {
  showCreateAnnouncementModal.value = false
  selectedAnnouncement.value = item
  showAnnouncementDetailsModal.value = true
  if (!item.is_read) notificationStore.markAsRead(item.id)
}

const closeAnnouncementDetails = () => {
  showAnnouncementDetailsModal.value = false
  selectedAnnouncement.value = null
}

const refreshAnnouncements = async () => {
  await notificationStore.fetchNotifications()
  toast ? toast.success('Announcements refreshed') : null
}

const handleDeleteAnnouncement = (item) => {
  if (!item) return
  if (confirm(`Are you sure you want to delete "${item.title}"?`)) {
    notificationStore.deleteAnnouncement(item.id)
    if (selectedAnnouncement.value && selectedAnnouncement.value.id === item.id) closeAnnouncementDetails()
    toast ? toast.success('Announcement removed') : null
  }
}

// =========================================================
// EVENTS STATE
// =========================================================
const eventViewMode = ref('grid')
const eventSearchQuery = ref('')
const eventStatusFilter = ref('All')
const eventSportFilter = ref('All')
const eventTypeFilter = ref('All')
const eventSortBy = ref('date')

const showCreateEventModal = ref(false)
const showEditEventModal = ref(false)
const showEventDetailsModal = ref(false)
const showDeleteEventModal = ref(false)

const selectedEvent = ref(null)
const editingEvent = ref(null)
const eventToDelete = ref(null)

const eventsList = ref([])

async function loadEvents() {
  try {
    const clubId = courtStore.club?.id || (courtStore.courts && courtStore.courts[0]?.club_id) || ''
    const url = clubId ? `/events?club_id=${clubId}&status=all` : '/events?status=all'
    const res = await api.get(url)
    eventsList.value = (res.data || []).map(e => ({
      id: e.id,
      title: e.title,
      type: e.type || 'Tournament',
      sport: e.sport || 'Sports',
      date: e.date,
      dateDisplay: new Date(e.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      time: `${(e.start_time || '09:00').substring(0, 5)} - ${(e.end_time || '18:00').substring(0, 5)}`,
      start_time: (e.start_time || '09:00').substring(0, 5),
      end_time: (e.end_time || '18:00').substring(0, 5),
      venue: e.venue || (courtStore.club?.name || 'Main Arena'),
      capacity: e.max_attendees || 30,
      registered: e.registered_count || 0,
      fee: e.registration_fee || 0,
      status: e.status ? (e.status.charAt(0).toUpperCase() + e.status.slice(1)) : 'Upcoming',
      organizer: 'Club Owner',
      description: e.description || '',
      participants: []
    }))
  } catch (error) {
    console.error('Failed to load events:', error)
  }
}

onMounted(() => {
  loadEvents()
  loadAdminBookings()
})

watch(() => courtStore.club, () => {
  loadEvents()
  loadAdminBookings()
})

const upcomingEvents = computed(() => {
  return eventsList.value.map(e => ({
    id: e.id,
    title: e.title,
    type: e.type,
    date: e.dateDisplay,
    info: `${e.registered} / ${e.capacity} Registered Players`,
    status: e.status,
    chipClass: e.sport === 'Tennis' ? 'chip-blue' : e.sport === 'Badminton' ? 'chip-emerald' : 'chip-orange',
    statusClass: e.status === 'Upcoming' ? 'status-open' : 'status-confirmed'
  }))
})

const eventForm = reactive({
  title: '', sport: 'Tennis', type: 'Tournament',
  date: new Date().toISOString().split('T')[0],
  time: '10:00 - 16:00',
  venue: 'Tennis Court 1',
  capacity: 16,
  fee: 0,
  status: 'Upcoming',
  organizer: 'Club Staff',
  description: ''
})

const editEventForm = reactive({
  id: '', title: '', sport: 'Tennis', type: 'Tournament', date: '',
  time: '', venue: '', capacity: 16, fee: 0, status: 'Upcoming', description: ''
})

const filteredEvents = computed(() => {
  return eventsList.value.filter(e => {
    const q = eventSearchQuery.value.trim().toLowerCase()
    const matchesSearch = !q ||
      e.title.toLowerCase().includes(q) ||
      e.venue.toLowerCase().includes(q) ||
      e.organizer.toLowerCase().includes(q)
    const matchesStatus = eventStatusFilter.value === 'All' || e.status.toLowerCase() === eventStatusFilter.value.toLowerCase()
    const matchesSport = eventSportFilter.value === 'All' || e.sport.toLowerCase() === eventSportFilter.value.toLowerCase()
    const matchesType = eventTypeFilter.value === 'All' || e.type.toLowerCase() === eventTypeFilter.value.toLowerCase()
    return matchesSearch && matchesStatus && matchesSport && matchesType
  }).sort((a, b) => {
    if (eventSortBy.value === 'date') return a.date.localeCompare(b.date)
    if (eventSortBy.value === 'title') return a.title.localeCompare(b.title)
    if (eventSortBy.value === 'registered') return b.registered - a.registered
    if (eventSortBy.value === 'fee') return b.fee - a.fee
    return 0
  })
})

const eventsKpis = computed(() => {
  const total = eventsList.value.length
  const upcoming = eventsList.value.filter(e => e.status === 'Upcoming' || e.status === 'Ongoing').length
  const totalRegistered = eventsList.value.reduce((sum, e) => sum + e.registered, 0)
  const totalCapacity = eventsList.value.reduce((sum, e) => sum + e.capacity, 0)
  const totalRevenue = eventsList.value.reduce((sum, e) => sum + (e.registered * e.fee), 0)
  return { total, upcoming, totalRegistered, totalCapacity, totalRevenue }
})

function resetEventFilters() {
  eventSearchQuery.value = ''
  eventStatusFilter.value = 'All'
  eventSportFilter.value = 'All'
  eventTypeFilter.value = 'All'
  eventSortBy.value = 'date'
}

function openCreateEventModal() {
  eventForm.title = ''
  eventForm.description = ''
  showCreateEventModal.value = true
}

function closeCreateEventModal() {
  showCreateEventModal.value = false
}

function _parseTimeString(t, defaultTime = '10:00') {
  if (!t) return defaultTime
  const raw = t.trim()
  if (raw.includes(':')) {
    const parts = raw.replace(/(am|pm)/i, '').trim().split(':')
    let h = parseInt(parts[0])
    if (/pm/i.test(raw) && h < 12) h += 12
    return `${h.toString().padStart(2, '0')}:${(parts[1] || '00').padStart(2, '0')}`
  }
  return defaultTime
}

async function handleCreateEvent() {
  if (!eventForm.title) {
    if (toast) toast.error('Please fill in event title.')
    return
  }
  const clubId = courtStore.club?.id || (courtStore.courts && courtStore.courts[0]?.club_id) || undefined
  let [startTimeStr, endTimeStr] = ['10:00', '16:00']
  if (eventForm.time && eventForm.time.includes('-')) {
    const parts = eventForm.time.split('-')
    startTimeStr = parts[0].trim()
    endTimeStr = parts[1].trim()
  }

  const payload = {
    club_id: clubId,
    title: eventForm.title,
    description: eventForm.description || '',
    event_date: eventForm.date || new Date().toISOString().split('T')[0],
    start_time: _parseTimeString(startTimeStr, '10:00'),
    end_time: _parseTimeString(endTimeStr, '16:00'),
    max_attendees: Number(eventForm.capacity) || 20,
    registration_fee: Number(eventForm.fee) || 0
  }

  try {
    await api.post('/events', payload)
    showCreateEventModal.value = false
    await loadEvents()
    if (toast) toast.success(`Event "${payload.title}" created successfully!`)
  } catch (err) {
    if (toast) toast.error(err.response?.data?.message || 'Failed to create event.')
  }
}

function openEventDetails(event) {
  selectedEvent.value = event
  showEventDetailsModal.value = true
}

function closeEventDetailsModal() {
  showEventDetailsModal.value = false
  selectedEvent.value = null
}

function openEditEventModal(event) {
  showEventDetailsModal.value = false
  selectedEvent.value = null
  editingEvent.value = event
  editEventForm.id = event.id
  editEventForm.title = event.title
  editEventForm.sport = event.sport
  editEventForm.type = event.type
  editEventForm.date = event.date
  editEventForm.time = event.time
  editEventForm.venue = event.venue
  editEventForm.capacity = event.capacity
  editEventForm.fee = event.fee
  editEventForm.status = event.status
  editEventForm.description = event.description
  showEditEventModal.value = true
}

function closeEditEventModal() {
  showEditEventModal.value = false
  editingEvent.value = null
}

async function handleUpdateEvent() {
  if (!editingEvent.value) return
  let [startTimeStr, endTimeStr] = [editingEvent.value.start_time || '10:00', editingEvent.value.end_time || '16:00']
  if (editEventForm.time && editEventForm.time.includes('-')) {
    const parts = editEventForm.time.split('-')
    startTimeStr = parts[0].trim()
    endTimeStr = parts[1].trim()
  }

  const payload = {
    title: editEventForm.title,
    description: editEventForm.description,
    event_date: editEventForm.date,
    start_time: _parseTimeString(startTimeStr, '10:00'),
    end_time: _parseTimeString(endTimeStr, '16:00'),
    max_attendees: Number(editEventForm.capacity) || 20,
    registration_fee: Number(editEventForm.fee) || 0,
    status: (editEventForm.status || 'upcoming').toLowerCase()
  }

  try {
    await api.put(`/events/${editingEvent.value.id}`, payload)
    showEditEventModal.value = false
    editingEvent.value = null
    await loadEvents()
    if (toast) toast.success('Event details updated successfully!')
  } catch (err) {
    if (toast) toast.error(err.response?.data?.message || 'Failed to update event.')
  }
}

function requestDeleteEvent(event) {
  showEventDetailsModal.value = false
  selectedEvent.value = null
  eventToDelete.value = event
  showDeleteEventModal.value = true
}

async function confirmDeleteEvent() {
  if (!eventToDelete.value) return
  try {
    await api.delete(`/events/${eventToDelete.value.id}`)
    showDeleteEventModal.value = false
    if (showEventDetailsModal.value) showEventDetailsModal.value = false
    if (toast) toast.success(`Event "${eventToDelete.value.title}" cancelled.`)
    eventToDelete.value = null
    await loadEvents()
  } catch (err) {
    if (toast) toast.error(err.response?.data?.message || 'Failed to cancel event.')
  }
}

function addSampleParticipant(event) {
  const sampleNames = ['Alex Morgan', 'Carlos Alcaraz', 'Coco Gauff', 'Novak D.', 'Iga Swiatek', 'Jannik Sinner']
  const randomName = sampleNames[Math.floor(Math.random() * sampleNames.length)]
  if (event.registered < event.capacity) {
    event.participants = event.participants || []
    event.participants.push(randomName)
    event.registered += 1
    if (toast) toast.success(`Registered ${randomName} to event!`)
  } else {
    if (toast) toast.error('Event is already at full capacity!')
  }
}

function removeParticipant(event, index) {
  if (event.participants && event.participants[index]) {
    const removedName = event.participants[index]
    event.participants.splice(index, 1)
    event.registered = Math.max(0, event.registered - 1)
    if (toast) toast.success(`Removed ${removedName} from event.`)
  }
}

// =========================================================
// ANALYTICS TAB REACTIVE STATE & EXPORT
// =========================================================
const analyticsTimeframe = ref('30 Days')
// Re-fetch real analytics when the timeframe selector changes
watch(analyticsTimeframe, () => loadAdminAnalytics())
const activeChartMetric = ref('revenue')

const sportRevenueBreakdown = ref([
  { sport: 'Tennis Courts', revenue: 217125, percentage: 45, color: '#2563eb' },
  { sport: 'Badminton Arenas', revenue: 144750, percentage: 30, color: '#059669' },
  { sport: 'Squash Courts', revenue: 72375, percentage: 15, color: '#ea580c' },
  { sport: 'Swimming Lanes', revenue: 48250, percentage: 10, color: '#0284c7' }
])

const hourlyOccupancyData = ref([
  { hour: '06:00 AM', rate: 42 }, { hour: '08:00 AM', rate: 68 }, { hour: '10:00 AM', rate: 54 },
  { hour: '12:00 PM', rate: 60 }, { hour: '02:00 PM', rate: 72 }, { hour: '04:00 PM', rate: 85 },
  { hour: '06:00 PM', rate: 96 }, { hour: '08:00 PM', rate: 92 }, { hour: '10:00 PM', rate: 38 }
])

const topPerformingFacilities = ref([
  { id: 1, name: 'Tennis Court 1 (Clay)', sport: 'Tennis', hoursBooked: 248, revenue: 186000, occupancy: '92%', status: 'High Demand' },
  { id: 2, name: 'Badminton Arena A', sport: 'Badminton', hoursBooked: 310, revenue: 124000, occupancy: '88%', status: 'Optimal' },
  { id: 3, name: 'Squash Court 2', sport: 'Squash', hoursBooked: 185, revenue: 92500, occupancy: '76%', status: 'Moderate' },
  { id: 4, name: 'Olympic Swimming Lane 1', sport: 'Swimming', hoursBooked: 160, revenue: 80000, occupancy: '81%', status: 'Optimal' }
])

const paymentMethodBreakdown = ref([
  { method: 'UPI / NetBanking', percentage: 65, color: '#2563eb', val: '₹3,13,625' },
  { method: 'Credit / Debit Cards', percentage: 22, color: '#059669', val: '₹1,06,150' },
  { method: 'Counter Cash / POS', percentage: 13, color: '#ea580c', val: '₹62,725' }
])

const financialSummary = ref({
  grossRevenue: '₹4,82,500', operationalCosts: '₹1,12,000',
  maintenanceTaxes: '₹38,500', netProfit: '₹3,32,000', profitMargin: '+68.8%'
})

function exportAnalyticsCSV() {
  const headers = ['Report Metric / Category', 'Value / Details', 'Timeframe / Period']
  const rows = [
    ['Report Title', 'Apex Club Revenue & Performance Analytics Report', `Generated: ${new Date().toLocaleDateString()}`],
    ['Selected Timeframe', analyticsTimeframe.value, ''],
    ['Total Revenue', 'INR 4,82,500', '+14.2% YoY'],
    ['Peak Booking Hour', '06:00 PM - 08:00 PM', '96% Peak Occupancy'],
    ['Membership Growth', '+64 Members', 'This Month'],
    ['Retention Rate', '94.8%', 'Member Satisfaction'],
    ['---', '---', '---'],
    ['Monthly Revenue Trend', 'Revenue (INR)', 'Booking Volume'],
    ['Jan', '2,45,000', '320'], ['Feb', '2,80,000', '380'], ['Mar', '3,10,000', '420'],
    ['Apr', '2,90,000', '390'], ['May', '3,60,000', '490'], ['Jun', '4,20,000', '560'],
    ['Jul', '4,50,000', '610'], ['Aug', '4,82,000', '648'],
    ['---', '---', '---'],
    ['Sport Revenue Breakdown', 'Percentage', 'Revenue (INR)'],
    ['Tennis Courts', '45%', '2,17,125'], ['Badminton Arenas', '30%', '1,44,750'],
    ['Squash Courts', '15%', '72,375'], ['Swimming Lanes', '10%', '48,250'],
    ['---', '---', '---'],
    ['Court Utilization', 'Occupancy Rate', 'Period'],
    ['Prime Hours (5 PM - 10 PM)', '92%', 'Evening'], ['Afternoon (12 PM - 5 PM)', '68%', 'Afternoon'], ['Morning (6 AM - 12 PM)', '54%', 'Morning'],
  ]
  const csvContent = [headers.join(','), ...rows.map(e => e.map(cell => `"${cell}"`).join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `clubdash_analytics_report_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  if (toast) toast.success('Analytics report downloaded successfully! 📊')
}

// =========================================================
// MEMBER DETAILS & EXPORT (UPDATED)
// =========================================================
function viewMemberDetails(member) {
  selectedMemberForModal.value = member
  showMemberModal.value = true
}

function exportMembersCSV() {
  const headers = ['Name', 'Email', 'Membership Plan', 'Booking Count', 'Status']
  const rows = filteredMembersList.value.map(m => [
    m.name,
    m.email,
    m.plan,
    m.totalBookings,
    m.membership_status
  ])
  const csv = [headers, ...rows].map(r => r.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'club_members.csv'
  link.click()
}

// --- REAL-TIME ADMIN PROFILE STATE ---
const showProfilePopover = ref(false)
const showEditProfileModal = ref(false)
const showFirstTimePhoneModal = ref(false)
const firstTimePhoneInput = ref('')

const adminProfile = reactive({
  name: '',
  role: 'Super Admin',
  email: '',
  phone: '',
  facility: 'ClubDash',
  memberSince: '',
  initials: 'AD',
  avatarUrl: null
})

const editProfileForm = reactive({
  name: '',
  email: '',
  phone: '',
  role: '',
  facility: 'ClubDash',
  avatarUrl: null
})

function formatRole(role) {
  if (!role) return 'Super Admin'
  if (role.toLowerCase() === 'owner') return 'Super Admin'
  if (role.toLowerCase() === 'front-desk') return 'Front Desk'
  return role.charAt(0).toUpperCase() + role.slice(1)
}

function formatMemberSince(createdAt) {
  if (!createdAt) return 'Recent'
  try {
    const d = new Date(createdAt)
    if (isNaN(d.getTime())) return 'Recent'
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
  } catch {
    return 'Recent'
  }
}

function getInitials(name) {
  if (!name) return 'AD'
  const parts = name.trim().split(' ').filter(Boolean)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  } else if (parts.length === 1 && parts[0].length > 0) {
    return parts[0].slice(0, 2).toUpperCase()
  }
  return 'AD'
}

function checkFirstTimePhoneSetup(u) {
  if (!u) return
  const userKey = `phone_prompt_done_${u.id || u.email}`
  const alreadyPrompted = localStorage.getItem(userKey)
  // If user has no phone in db and has not completed initial prompt
  if (!u.phone && !alreadyPrompted) {
    firstTimePhoneInput.value = ''
    showFirstTimePhoneModal.value = true
  }
}

async function submitFirstTimePhone() {
  const phoneVal = firstTimePhoneInput.value.trim()
  if (!phoneVal) {
    if (toast) toast.error('Please enter a valid phone number.')
    return
  }

  try {
    if (auth.isAuthenticated()) {
      await auth.updateProfile({ phone: phoneVal })
    } else if (auth.user) {
      auth.user.phone = phoneVal
    }
  } catch (err) {
    console.warn('Error saving initial phone:', err)
  }

  adminProfile.phone = phoneVal
  const userKey = `phone_prompt_done_${auth.user?.id || auth.user?.email || 'default'}`
  localStorage.setItem(userKey, 'true')

  showFirstTimePhoneModal.value = false
  if (toast) toast.success('Phone number saved successfully! 📱')
}

function skipFirstTimePhone() {
  const userKey = `phone_prompt_done_${auth.user?.id || auth.user?.email || 'default'}`
  localStorage.setItem(userKey, 'true')
  showFirstTimePhoneModal.value = false
}

function syncProfileWithAuthUser(u) {
  if (!u) {
    adminProfile.name = 'Admin User'
    adminProfile.email = 'admin@clubdash.com'
    adminProfile.role = 'Super Admin'
    adminProfile.phone = ''
    adminProfile.facility = 'ClubDash'
    adminProfile.memberSince = 'Recent'
    adminProfile.initials = 'AD'
    return
  }

  adminProfile.name = u.name || 'Admin User'
  adminProfile.email = u.email || 'admin@clubdash.com'
  adminProfile.role = formatRole(u.role)
  adminProfile.initials = getInitials(adminProfile.name)
  adminProfile.phone = (u.phone && u.phone !== '+91 98765 43210') ? u.phone : ''
  adminProfile.facility = 'ClubDash'
  adminProfile.memberSince = formatMemberSince(u.created_at)

  // Load user-specific avatar or valid custom phone
  try {
    const userKey = `admin_profile_${u.id || u.email}`
    const saved = localStorage.getItem(userKey)
    if (saved) {
      const parsed = JSON.parse(saved)
      if (parsed.phone && parsed.phone !== '+91 98765 43210' && !adminProfile.phone) {
        adminProfile.phone = parsed.phone
      }
      if (parsed.avatarUrl) adminProfile.avatarUrl = parsed.avatarUrl
    }
  } catch (err) {
    console.warn('Error reading stored profile extra:', err)
  }
}

// Reactively watch for auth.user changes
watch(
  () => auth.user,
  (newUser) => {
    syncProfileWithAuthUser(newUser)
    if (newUser) {
      checkFirstTimePhoneSetup(newUser)
    }
  },
  { immediate: true, deep: true }
)

function toggleProfilePopover() {
  showProfilePopover.value = !showProfilePopover.value
}

function openEditProfileModal() {
  editProfileForm.name = adminProfile.name
  editProfileForm.email = adminProfile.email
  editProfileForm.phone = adminProfile.phone
  editProfileForm.role = adminProfile.role
  editProfileForm.facility = 'ClubDash'
  editProfileForm.avatarUrl = adminProfile.avatarUrl
  showEditProfileModal.value = true
}

function closeEditProfileModal() {
  showEditProfileModal.value = false
}

function handleEditAvatarUpload(event) {
  const file = event.target.files && event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      editProfileForm.avatarUrl = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

function removeEditAvatar() {
  editProfileForm.avatarUrl = null
}

async function saveAdminProfile() {
  if (!editProfileForm.name || !editProfileForm.name.trim()) {
    if (toast) toast.error('Please enter a valid full name.')
    return
  }
  if (!editProfileForm.email || !editProfileForm.email.trim()) {
    if (toast) toast.error('Please enter a valid email address.')
    return
  }

  const newName = editProfileForm.name.trim()
  const newEmail = editProfileForm.email.trim()
  const newPhone = editProfileForm.phone.trim()

  try {
    // Update on the backend
    if (auth.isAuthenticated()) {
      await auth.updateProfile({
        name: newName,
        email: newEmail,
        phone: newPhone,
        facility: 'ClubDash'
      })
    } else if (auth.user) {
      auth.user.name = newName
      auth.user.email = newEmail
      auth.user.phone = newPhone
    }
  } catch (err) {
    console.warn('Backend profile update note:', err)
    if (toast && err?.response?.data?.message) {
      toast.error(err.response.data.message)
      return
    }
  }

  adminProfile.name = newName
  adminProfile.email = newEmail
  adminProfile.phone = newPhone
  adminProfile.role = editProfileForm.role.trim() || adminProfile.role
  adminProfile.facility = 'ClubDash'
  adminProfile.avatarUrl = editProfileForm.avatarUrl
  adminProfile.initials = getInitials(adminProfile.name)

  // Save user-specific preferences to localStorage
  try {
    const userKey = `admin_profile_${auth.user?.id || auth.user?.email || 'default'}`
    localStorage.setItem(userKey, JSON.stringify({
      phone: adminProfile.phone,
      facility: 'ClubDash',
      avatarUrl: adminProfile.avatarUrl
    }))
  } catch (err) {
    console.warn('Failed to save profile preferences to localStorage:', err)
  }

  showEditProfileModal.value = false
  if (toast) toast.success('Profile details saved successfully! ✨')
}

function handleAvatarUpload(event) {
  const file = event.target.files && event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      adminProfile.avatarUrl = e.target.result
      try {
        const userKey = `admin_profile_${auth.user?.id || auth.user?.email || 'default'}`
        const existing = JSON.parse(localStorage.getItem(userKey) || '{}')
        existing.avatarUrl = adminProfile.avatarUrl
        localStorage.setItem(userKey, JSON.stringify(existing))
      } catch (err) {}
      if (toast) toast.success('Profile picture updated successfully! 📸')
    }
    reader.readAsDataURL(file)
  }
}
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
  max-width: 42rem;
  max-height: calc(100dvh - 3rem);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: scaleUp 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.75rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  background: #ffffff;
  flex: 0 0 auto;
  position: sticky;
  top: 0;
  z-index: 2;
}

.modal-header h2,
.modal-header h3 {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
}

.close-btn,
.close-modal-btn {
  background: #f1f5f9;
  border: none;
  border-radius: 0.5rem;
  width: 32px;
  height: 32px;
  font-size: 1rem;
  color: #64748b;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
  line-height: 1;
}

.close-btn:hover,
.close-modal-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.modal-form {
  padding: 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  scrollbar-gutter: stable;
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  border: 1px solid #cbd5e1;
  font-family: inherit;
  font-size: 0.92rem;
  color: #0f172a;
  background: #ffffff;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 1rem 1.75rem;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  margin: 0.5rem -1.75rem -1.5rem;
  padding: 1rem 1.75rem;
  position: sticky;
  bottom: -1.5rem;
  z-index: 2;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.cancel-modal-btn {
  padding: 0.65rem 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #475569;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-modal-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.submit-modal-btn {
  padding: 0.65rem 1.5rem;
  border-radius: 0.75rem;
  border: none;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.submit-modal-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #4338ca);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
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

.court-sport-type {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  margin: .35rem 0 .15rem;
  padding: .28rem .55rem;
  border: 1px solid #dfe6f0;
  border-radius: 999px;
  background: #f6f8fc;
  color: #526078;
  font-size: .72rem;
  font-weight: 700;
}

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
    max-height: calc(100dvh - 1rem);
    margin: 0;
    border-radius: 1.25rem;
  }
  .modal-overlay {
    padding: 0.5rem;
  }
  .modal-header {
    padding: 1rem 1.25rem;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
  .modal-form {
    padding: 1.25rem;
    gap: 1rem;
  }
  .modal-actions {
    margin: 0.25rem -1.25rem -1.25rem;
    padding: 0.9rem 1.25rem;
    bottom: -1.25rem;
  }
}

/* --- BOOKINGS TAB CUSTOM STYLES --- */
.bookings-toolbar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-action-buttons {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.export-csv-btn {
  display: inline-flex;
  align-items: center;
  padding: 0.65rem 1.1rem;
  border-radius: 0.75rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.export-csv-btn:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
  color: #0f172a;
}

.add-booking-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.65rem 1.25rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
  transition: all 0.2s ease;
}

.add-booking-btn:hover {
  background: linear-gradient(135deg, #1d4ed8, #4338ca);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

.bookings-filter-box {
  padding: 1rem 1.25rem;
}

.filter-controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-input-wrapper {
  position: relative;
  flex: 1 1 260px;
  max-width: 380px;
}

.search-icon {
  position: absolute;
  left: 0.85rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.1rem;
  height: 1.1rem;
  color: #94a3b8;
  pointer-events: none;
}

.booking-search-input {
  width: 100%;
  padding: 0.6rem 2.2rem 0.6rem 2.5rem;
  border-radius: 0.65rem;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  font-size: 0.86rem;
  color: #0f172a;
  outline: none;
  transition: all 0.2s ease;
}

.booking-search-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.clear-search-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.1rem;
  color: #94a3b8;
  cursor: pointer;
}

.filter-dropdowns-group {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-wrap: wrap;
}

.filter-select-group {
  display: flex;
  flex-direction: column;
}

.filter-select {
  padding: 0.6rem 2rem 0.6rem 0.8rem;
  border-radius: 0.65rem;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  font-size: 0.84rem;
  font-weight: 500;
  color: #334155;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-select:focus {
  border-color: #2563eb;
}

.reset-filters-btn {
  padding: 0.6rem 0.9rem;
  border-radius: 0.65rem;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-filters-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

/* Bookings Table */
.admin-bookings-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.88rem;
}

.admin-bookings-table th {
  padding: 0.9rem 1.25rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.booking-table-row {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.15s ease;
}

.booking-table-row:hover {
  background: #f8fafc;
}

.booking-table-row td {
  padding: 1.15rem 1.25rem;
  vertical-align: middle;
}

.player-info-meta {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.player-name-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.booking-ref-tag {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 0.375rem;
  background: #eff6ff;
  color: #2563eb;
  font-family: monospace;
  font-size: 0.76rem;
  font-weight: 700;
  border: 1px solid #dbeafe;
}

.booking-ref-tag.large {
  font-size: 0.9rem;
  padding: 0.25rem 0.65rem;
}

.usertype-tag {
  color: #64748b;
  font-weight: 500;
}

.facility-head-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.2rem;
}

.court-info-cell {
  display: flex;
  flex-direction: column;
}

.court-name-txt {
  font-weight: 600;
  color: #0f172a;
}

.sport-badge-pill {
  display: inline-block;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
}

.sport-tennis { background: #eff6ff; color: #2563eb; }
.sport-badminton { background: #ecfdf5; color: #059669; }
.sport-squash { background: #fff7ed; color: #ea580c; }
.sport-swimming { background: #f0f9ff; color: #0284c7; }

.time-subtxt {
  font-size: 0.8rem;
  color: #64748b;
}

.auto-completed.bar-hour-label {
  font-size: 0.7rem;
  color: #64748b;
  font-weight: 600;
}

/* Analytics Table & Financial Styles */
.facilities-table-wrapper {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  overflow: hidden;
}

.analytics-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.84rem;
}

.analytics-table th {
  background: #f8fafc;
  color: #475569;
  font-weight: 700;
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.analytics-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.analytics-table tr:last-child td {
  border-bottom: none;
}

.table-progress-bar {
  flex: 1;
  height: 7px;
  background: #e2e8f0;
  border-radius: 999px;
  overflow: hidden;
  min-width: 60px;
}

.table-progress-fill {
  height: 100%;
  background: linear-gradient(to right, #2563eb, #3b82f6);
  border-radius: 999px;
}

.financial-summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.fin-stat-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.65rem;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
}

.fin-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.fin-val {
  font-size: 1.1rem;
  font-weight: 800;
  margin-top: 0.2rem;
}

.fin-val.positive { color: #059669; }
.fin-val.blue { color: #2563eb; }

.fin-sub {
  font-size: 0.72rem;
  color: #10b981;
  font-weight: 600;
  margin-top: 0.15rem;
}

.stacked-bar-container {
  display: flex;
  height: 10px;
  border-radius: 999px;
  overflow: hidden;
  background: #f1f5f9;
}

.stacked-bar-segment {
  height: 100%;
  transition: width 0.3s ease;
}

.payment-legend-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.35rem 0;
  border-bottom: 1px solid #f8fafc;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
}

.payment-cell {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.amount-txt {
  font-weight: 700;
  color: #0f172a;
}

.pay-status-tag {
  font-size: 0.72rem;
  font-weight: 600;
  width: fit-content;
}

.pay-paid { color: #16a34a; }
.pay-pending { color: #d97706; }
.pay-refunded { color: #dc2626; }

.booking-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

.bstatus-confirmed { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; }
.bstatus-completed { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.bstatus-pending { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.bstatus-cancelled { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }

.table-actions-group {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.4rem;
}

.action-icon-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.15s ease;
}

.action-icon-btn svg {
  width: 14px;
  height: 14px;
}

.view-btn {
  background: #f1f5f9;
  color: #334155;
  border-color: #e2e8f0;
}

.view-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.complete-btn {
  background: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}

.complete-btn:hover {
  background: #dbeafe;
}

.cancel-btn {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.cancel-btn:hover {
  background: #fee2e2;
}

.no-bookings-empty {
  text-align: center;
  padding: 3rem 1.5rem;
}

.empty-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #334155;
  margin-bottom: 0.35rem;
}

.empty-sub {
  font-size: 0.85rem;
  color: #64748b;
}

/* Modals for Booking Details & Confirm */
.booking-detail-modal {
  max-width: 620px;
  width: 90%;
}

.booking-detail-body {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  max-height: 70vh;
  overflow-y: auto;
  padding: 1.5rem;
}

.detail-section-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem;
}

.detail-section-card h4 {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #64748b;
  margin-bottom: 0.75rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #e2e8f0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.85rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #64748b;
}

.detail-val {
  font-size: 0.88rem;
  color: #0f172a;
}

.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }

.notes-text {
  font-size: 0.88rem;
  color: #334155;
  line-height: 1.5;
  margin: 0;
}

.danger-btn {
  background: #dc2626 !important;
  color: #ffffff !important;
  border-color: #dc2626 !important;
}

.danger-btn:hover {
  background: #b91c1c !important;
}

.success-btn {
  background: #059669 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
}

.success-btn:hover {
  background: #047857 !important;
}

.small-confirm-modal {
  max-width: 440px;
}

/* --- EVENTS TAB STYLES --- */
.view-toggle-group {
  display: flex;
  background: #f1f5f9;
  padding: 0.2rem;
  border-radius: 0.65rem;
  border: 1px solid #cbd5e1;
}

.view-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.45rem 0.65rem;
  border-radius: 0.5rem;
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.view-toggle-btn:hover {
  color: #0f172a;
}

.view-toggle-btn.active {
  background: #ffffff;
  color: #2563eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.admin-events-grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}

.event-card-rich {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.event-card-rich:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
  transform: translateY(-2px);
}

.event-card-rich-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.25rem 0.5rem;
}

.event-card-rich-body {
  padding: 0.5rem 1.25rem 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.event-rich-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.2rem;
  line-height: 1.35;
}

.event-type-subtag {
  font-size: 0.76rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 0.75rem;
  display: inline-block;
}

.event-rich-desc {
  font-size: 0.84rem;
  color: #475569;
  line-height: 1.45;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.event-meta-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  font-size: 0.82rem;
  color: #334155;
  margin-bottom: 1rem;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-icn {
  width: 15px;
  height: 15px;
  color: #64748b;
  flex-shrink: 0;
}

.capacity-progress-wrapper {
  margin-top: auto;
  padding-top: 0.5rem;
}

.capacity-progress-bar {
  height: 6px;
  border-radius: 999px;
  background: #e2e8f0;
  overflow: hidden;
}

.capacity-progress-fill {
  height: 100%;
  border-radius: 999px;
  background: #2563eb;
  transition: width 0.3s ease;
}

.capacity-progress-fill.full {
  background: #ef4444;
}

.event-card-rich-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1.25rem;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
}

.estatus-upcoming { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.estatus-ongoing { background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; }
.estatus-completed { background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; }
.estatus-cancelled { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }

.participants-tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.participant-pill-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  font-size: 0.8rem;
  font-weight: 500;
  color: #1e293b;
}

.remove-participant-btn {
  background: none;
  border: none;
  font-size: 1rem;
  line-height: 1;
  color: #94a3b8;
  cursor: pointer;
  padding: 0 0.15rem;
}

.remove-participant-btn:hover {
  color: #ef4444;
}

/* Hourly Bars Chart Layout */
.hourly-bars-chart {
  display: flex !important;
  flex-direction: row !important;
  align-items: flex-end !important;
  justify-content: space-between !important;
  gap: 0.4rem !important;
  height: 190px !important;
}

.bar-col-item {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: flex-end !important;
  flex: 1 !important;
}

.bar-track-vertical {
  height: 120px !important;
  width: 14px !important;
  border-radius: 999px !important;
  background: #f1f5f9 !important;
  display: flex !important;
  align-items: flex-end !important;
  overflow: hidden !important;
}

.bar-fill-vertical {
  width: 100% !important;
  border-radius: 999px !important;
}

/* --- SIDEBAR ADMIN PROFILE STYLES --- */
.sidebar-footer {
  padding: 1rem !important;
  border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
  margin-top: auto !important;
  background: #0f172a !important;
}

.sidebar-admin-profile {
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  gap: 0.75rem !important;
  padding: 0.75rem 0.85rem !important;
  border-radius: 0.75rem !important;
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.sidebar-admin-profile .user-avatar {
  width: 38px !important;
  height: 38px !important;
  border-radius: 999px !important;
  background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 0.88rem !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
}

.sidebar-admin-profile .user-meta {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  overflow: hidden !important;
}

.sidebar-admin-profile .user-name {
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  line-height: 1.25 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.sidebar-admin-profile .user-role {
  font-size: 0.75rem !important;
  color: #94a3b8 !important;
  font-weight: 500 !important;
  white-space: nowrap !important;
}

/* --- TOP HEADER LOGOUT BUTTON STYLES --- */
.top-header-logout-btn {
  display: inline-flex !important;
  flex-direction: row !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.45rem !important;
  padding: 0.55rem 1.1rem !important;
  border-radius: 0.65rem !important;
  background: #fef2f2 !important;
  border: 1px solid #fecaca !important;
  color: #dc2626 !important;
  font-size: 0.85rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.1) !important;
  white-space: nowrap !important;
  flex-shrink: 0 !important;
}

.top-header-logout-btn:hover {
  background: #fee2e2 !important;
  border-color: #fca5a5 !important;
  color: #b91c1c !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.18) !important;
}

.top-header-logout-btn:active {
  transform: translateY(0) !important;
}

.top-header-logout-btn svg {
  width: 16px !important;
  height: 16px !important;
  flex-shrink: 0 !important;
}

/* --- DISCORD STYLE PROFILE POPOVER CARD STYLES --- */
.clickable-profile {
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}

.clickable-profile:hover {
  background: rgba(255, 255, 255, 0.14) !important;
  border-color: #3b82f6 !important;
  box-shadow: 0 0 12px rgba(59, 130, 246, 0.3) !important;
}

.user-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 999px;
  object-fit: cover;
}

.sidebar-footer {
  position: relative !important;
}

.discord-profile-card {
  position: absolute;
  bottom: 80px;
  left: 10px;
  width: 270px;
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 1rem;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.08);
  z-index: 350;
  overflow: hidden;
  color: #ffffff;
}

.discord-banner {
  height: 65px;
  background: linear-gradient(135deg, #2563eb, #4f46e5, #7c3aed);
  position: relative;
}

.close-popover-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.35);
  border: none;
  color: #ffffff;
  width: 22px;
  height: 22px;
  border-radius: 999px;
  font-size: 0.75rem;
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: background 0.2s ease;
}

.close-popover-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

.discord-avatar-wrapper {
  padding: 0 0.85rem;
  margin-top: -30px;
  margin-bottom: 0.4rem;
}

.discord-avatar {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 999px;
  background: linear-gradient(135deg, #3b82f6, #6366f1);
  border: 3.5px solid #1e293b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 800;
  color: #ffffff;
  overflow: hidden;
}

.discord-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-upload-overlay {
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.discord-avatar:hover .avatar-upload-overlay {
  opacity: 1;
}

.discord-profile-body {
  padding: 0 0.85rem 0.85rem 0.85rem;
}

.profile-title-block {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.discord-name {
  font-size: 1.05rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
  line-height: 1.25;
}

.discord-role-badge {
  display: inline-block;
  align-self: flex-start;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  background: rgba(37, 99, 235, 0.3);
  color: #60a5fa;
  border: 1px solid rgba(96, 165, 250, 0.3);
  padding: 0.12rem 0.5rem;
  border-radius: 999px;
  letter-spacing: 0.04em;
}

.discord-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0.65rem 0;
}

.discord-details-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.78rem;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 0.12rem;
}

.detail-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

.detail-val {
  color: #f1f5f9;
  font-weight: 600;
  word-break: break-all;
}

.discord-actions-footer {
  display: flex;
  align-items: center;
  margin-top: 0.85rem;
}

.edit-profile-btn-pill {
  width: 100%;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  color: #ffffff;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 0.55rem 0.85rem;
  border-radius: 0.6rem;
  text-align: center;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
  transition: all 0.2s ease;
}

.edit-profile-btn-pill:hover {
  background: linear-gradient(135deg, #1d4ed8, #4338ca);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.45);
}

.modal-upload-btn:hover {
  background: #1d4ed8;
}

.popover-fade-enter-active,
.popover-fade-leave-active {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.popover-fade-enter-from,
.popover-fade-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.95);
}

/* Announcements & Broadcasts Component Styles */
.filter-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #475569;
  font-size: 0.82rem;
  font-weight: 600;
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-pill-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.filter-pill-btn.active {
  background: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.pill-count {
  font-size: 0.75rem;
  opacity: 0.85;
}

.quick-template-btn {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-size: 0.76rem;
  font-weight: 600;
  padding: 0.3rem 0.65rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.quick-template-btn:hover {
  background: #eff6ff;
  border-color: #3b82f6;
  color: #2563eb;
  transform: translateY(-1px);
}

.broadcast-modal-grid {
  display: grid;
  grid-template-columns: 1.25fr 0.95fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 768px) {
  .broadcast-modal-grid {
    grid-template-columns: 1fr;
  }
}

.broadcast-input,
.broadcast-textarea {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.broadcast-input:focus,
.broadcast-textarea:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

/* Category Selector Cards */
.category-selector-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.5rem;
}

.category-card-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.65rem;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
}

.category-card-btn:hover {
  border-color: #94a3b8;
  background: #f8fafc;
}

.category-card-btn .cat-icon {
  font-size: 1.2rem;
}

.category-card-btn .cat-name {
  display: block;
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
}

.category-card-btn .cat-desc {
  display: block;
  font-size: 0.68rem;
  color: #64748b;
}

.category-card-btn.active.cat-blue {
  border-color: #2563eb;
  background: #eff6ff;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
}

.category-card-btn.active.cat-purple {
  border-color: #8b5cf6;
  background: #f5f3ff;
  box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.15);
}

.category-card-btn.active.cat-emerald {
  border-color: #10b981;
  background: #ecfdf5;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.15);
}

.category-card-btn.active.cat-orange {
  border-color: #f59e0b;
  background: #fffbeb;
  box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.15);
}

.category-card-btn.active.cat-rose {
  border-color: #ef4444;
  background: #fef2f2;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.15);
}

/* Audience and Priority Stacks */
.audience-selector-stack,
.priority-selector-stack {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.audience-radio-card,
.priority-radio-card {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.5rem 0.75rem;
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  color: #334155;
  transition: all 0.15s ease;
}

.audience-radio-card:hover,
.priority-radio-card:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.audience-radio-card.active {
  border-color: #2563eb;
  background: #eff6ff;
  color: #1d4ed8;
}

.priority-radio-card .prio-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  line-height: 1.2;
}

.priority-radio-card .prio-desc {
  display: block;
  font-size: 0.68rem;
  color: #64748b;
}

.priority-radio-card.active.prio-normal {
  border-color: #10b981;
  background: #ecfdf5;
}

.priority-radio-card.active.prio-high {
  border-color: #f59e0b;
  background: #fffbeb;
}

.priority-radio-card.active.prio-urgent {
  border-color: #ef4444;
  background: #fef2f2;
}

/* Priority & Audience Pills */
.priority-pill {
  font-size: 0.7rem;
  font-weight: 800;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.priority-pill.urgent {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fca5a5;
  animation: pulse-glow 2s infinite;
}

.priority-pill.high {
  background: #fef3c7;
  color: #d97706;
  border: 1px solid #fde68a;
}

.audience-pill {
  font-size: 0.72rem;
  font-weight: 600;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  padding: 0.15rem 0.55rem;
  border-radius: 999px;
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15);
  }
}

/* Live Preview Mockup */
.broadcast-preview-col {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  padding: 1.25rem;
}

.preview-header-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.85rem;
}

.live-pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
  animation: spin 3s linear infinite;
}

.preview-phone-mockup {
  background: #0f172a;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.18);
}

.preview-notification-card {
  background: #ffffff;
  border-radius: 0.75rem;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.preview-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.preview-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
}

.preview-badge.cat-general { background: #dbeafe; color: #1d4ed8; }
.preview-badge.cat-broadcast { background: #ede9fe; color: #6d28d9; }
.preview-badge.cat-tournament { background: #d1fae5; color: #047857; }
.preview-badge.cat-policy { background: #fef3c7; color: #b45309; }
.preview-badge.cat-maintenance { background: #fee2e2; color: #b91c1c; }

.preview-time {
  font-size: 0.7rem;
  color: #94a3b8;
}

.preview-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 0.35rem;
  line-height: 1.35;
}

.preview-body {
  font-size: 0.8rem;
  color: #475569;
  line-height: 1.5;
  margin: 0 0 0.75rem;
}

.preview-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 0.5rem;
  border-top: 1px solid #f1f5f9;
  font-size: 0.72rem;
  color: #64748b;
  font-weight: 600;
}

.broadcast-submit-btn {
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  color: #ffffff;
  font-weight: 700;
  padding: 0.65rem 1.35rem;
  border-radius: 0.6rem;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  transition: all 0.2s ease;
}

.broadcast-submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45);
}

.broadcast-submit-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
}

.btn-icon-trash {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #ef4444;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-icon-trash:hover {
  background: #fee2e2;
  border-color: #ef4444;
  transform: scale(1.05);
}

.announcement-meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-top: 1rem;
}

.meta-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.6rem;
  padding: 0.75rem;
}

.meta-label {
  display: block;
  font-size: 0.68rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}

.meta-val {
  font-size: 0.88rem;
  color: #0f172a;
  font-weight: 600;
}

.announcements-list-rich {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.announcement-item-rich {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  padding: 1.25rem 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  background: #ffffff;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.02);
}

.announcement-item-rich:hover {
  border-color: #93c5fd;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
}

.announcement-item-rich.unread {
  background: #f8faff;
}

.announcement-item-main {
  flex: 1;
  min-width: 0;
}

.announcement-body-preview {
  font-size: 0.88rem;
  color: #475569;
  margin: 0.35rem 0 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.unread-indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #2563eb;
  display: inline-block;
  box-shadow: 0 0 0 3px #dbeafe;
}

.btn-view-announcement {
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  color: #1e293b;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 0.45rem 0.95rem;
  border-radius: 0.5rem;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.btn-view-announcement:hover {
  background: #eff6ff;
  border-color: #2563eb;
  color: #2563eb;
}

.spin-animate {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>

