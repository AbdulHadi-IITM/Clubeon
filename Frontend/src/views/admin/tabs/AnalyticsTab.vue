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

            <!-- Dynamic KPI Cards for Analytics (in Indian Rupees ₹) -->
            <section class="kpi-grid">
              <div class="kpi-card">
                <span class="kpi-title">Total Revenue</span>
                <h3 class="kpi-value">{{ analyticsKpis.revenue }}</h3>
                <span class="trend-badge neutral">{{ analyticsKpis.window }}</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Peak Booking Hour</span>
                <h3 class="kpi-value">{{ analyticsKpis.peakHour }}</h3>
                <span class="trend-badge neutral">{{ analyticsKpis.peakBookings }}</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Active Members</span>
                <h3 class="kpi-value">{{ analyticsKpis.activeMembers }}</h3>
                <span class="trend-badge neutral">{{ analyticsKpis.totalMembers }} total</span>
              </div>
              <div class="kpi-card">
                <span class="kpi-title">Court Utilisation</span>
                <h3 class="kpi-value">{{ analyticsKpis.utilisation }}</h3>
                <span class="trend-badge neutral">{{ analyticsKpis.bookingsInWindow }} bookings</span>
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

                    <!-- Y-Axis Labels, scaled to the series actually plotted -->
                    <text x="35" y="34" text-anchor="end" font-size="10" fill="#94a3b8">
                      {{ growthChart.axis[0] }}
                    </text>
                    <text x="35" y="84" text-anchor="end" font-size="10" fill="#94a3b8">
                      {{ growthChart.axis[1] }}
                    </text>
                    <text x="35" y="134" text-anchor="end" font-size="10" fill="#94a3b8">
                      {{ growthChart.axis[2] }}
                    </text>
                    <text x="35" y="189" text-anchor="end" font-size="10" fill="#94a3b8">0</text>

                    <text
                      v-if="!growthChart.bars.length"
                      x="355" y="112" text-anchor="middle" font-size="12" fill="#94a3b8"
                    >
                      No data for this period yet.
                    </text>

                    <!-- Column Bars & Labels -->
                    <g v-for="(b, i) in growthChart.bars" :key="b.month">
                      <rect :x="b.x" y="30" :width="b.w" height="155" rx="6" ry="6" fill="#f8fafc" />
                      <rect
                        :x="b.x"
                        :y="b.y"
                        :width="b.w"
                        :height="b.h"
                        rx="6"
                        ry="6"
                        :fill="i % 2 === 0 ? 'url(#barBlueGrad)' : 'url(#barIndigoGrad)'"
                        class="graph-point"
                      />
                      <text :x="b.x + 19" :y="b.y - 6" text-anchor="middle" font-size="10" font-weight="700" fill="#1e293b">
                        {{ b.label }}
                      </text>
                      <text :x="b.x + 19" y="208" text-anchor="middle" font-size="11" font-weight="600" fill="#64748b">
                        {{ b.month }}
                      </text>
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
                        <circle
                          v-if="!donutSegments.length"
                          cx="50" cy="50" r="38" fill="none"
                          stroke="#e2e8f0" stroke-width="14"
                        />
                        <circle
                          v-for="seg in donutSegments"
                          :key="seg.sport"
                          cx="50" cy="50" r="38" fill="none"
                          :stroke="seg.color"
                          stroke-width="14"
                          :stroke-dasharray="seg.dashArray"
                          :stroke-dashoffset="seg.dashOffset"
                        />
                      </svg>
                      <div class="donut-inner-text">
                        <span class="donut-total-title">Total</span>
                        <span class="donut-total-num">{{ revenueTotalLabel }}</span>
                      </div>
                    </div>

                    <!-- Legend & Distribution Breakdown -->
                    <div class="donut-legend-list">
                      <p v-if="!sportRevenueBreakdown.length" class="legend-empty">
                        No completed payments in this period.
                      </p>
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
                          <td>
                            <span
                              class="status-badge-chip"
                              :class="{
                                'status-active': fac.status === 'Active',
                                'status-completed': fac.status === 'Inactive'
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
                      <span class="fin-label">Payments Settled</span>
                      <span class="fin-val blue">{{ financialSummary.completedPayments }}</span>
                      <span class="fin-sub">{{ financialSummary.pendingPayments }} pending</span>
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
</template>

<script setup>
import { inject } from 'vue'

const {
  activeChartMetric,
  activeMembers,
  analyticsError,
  analyticsKpis,
  analyticsLoading,
  analyticsTimeframe,
  donutSegments,
  exportAnalyticsCSV,
  financialSummary,
  growthChart,
  hourlyOccupancyData,
  paymentMethodBreakdown,
  reloadAdminData,
  revenueTotalLabel,
  sportRevenueBreakdown,
  topPerformingFacilities,
  totalMembers
} = inject('adminContext')
</script>
