<template>
  <div class="space-y-6" :class="{ 'nearby-fullscreen-active': isFullscreen }">
    <!-- =====================================================
         PAGE HEADER & QUICK ACTIONS
    ====================================================== -->
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <div
          class="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-indigo-500"
        >
          <span>ClubDash</span>
          <span class="text-slate-300">/</span>
          <span class="text-slate-400">Bengaluru Sports Network</span>
        </div>
        <h1 class="mt-2 text-3xl font-extrabold tracking-tight text-slate-900">
          Nearby Courts & Sports Clubs
        </h1>
        <p class="mt-1 max-w-2xl text-sm text-slate-500">
          Discover sports venues across Bengaluru, preview real turn-by-turn road routes, and
          reserve your court in seconds.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-2.5">
        <!-- Re-center Bengaluru -->
        <button
          type="button"
          class="btn-secondary inline-flex items-center justify-center gap-2 text-xs font-bold px-3.5 py-2.5 rounded-xl"
          title="Center map on Bengaluru"
          @click="centerOnBangalore"
        >
          <svg
            class="h-4 w-4 text-indigo-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          Bengaluru Center
        </button>

        <!-- Fit all clubs -->
        <button
          type="button"
          class="btn-secondary inline-flex items-center justify-center gap-2 text-xs font-bold px-3.5 py-2.5 rounded-xl"
          title="Fit all clubs in view"
          @click="fitMap"
        >
          <svg class="h-4 w-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
            />
          </svg>
          Fit All
        </button>

        <!-- Use my location -->
        <button
          type="button"
          class="btn-primary inline-flex items-center justify-center gap-2 text-xs font-bold px-4 py-2.5 rounded-xl"
          :disabled="locating"
          @click="locateMember"
        >
          <span
            v-if="locating"
            class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white"
          />
          <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 21a9 9 0 100-18 9 9 0 000 18zm0-12v6m-3-3h6"
            />
          </svg>
          {{ locating ? 'Locating GPS…' : userLocation ? 'Update Location' : 'Use My Location' }}
        </button>
      </div>
    </div>

    <!-- =====================================================
         ERROR / INFO BANNER
    ====================================================== -->
    <div
      v-if="error"
      class="glass flex items-start gap-3 border border-amber-200 bg-amber-50/80 p-4 text-sm text-amber-900 rounded-2xl"
    >
      <div class="mt-0.5 font-bold text-amber-600">ⓘ</div>
      <div class="flex-1">
        <p class="font-semibold text-amber-950">{{ error }}</p>
        <p class="mt-0.5 text-xs text-amber-800">
          Showing real sports clubs across Bengaluru. You can filter by locality, sport, or search
          above.
        </p>
      </div>
      <button
        type="button"
        class="text-xs font-bold text-amber-900 underline hover:text-amber-700"
        @click="error = ''"
      >
        Dismiss
      </button>
    </div>

    <!-- =====================================================
         LOCATION PERMISSION BANNER (WHEN GPS NOT YET DETECTED)
    ====================================================== -->
    <div
      v-if="!userLocation && !loading"
      class="glass flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border border-indigo-200/80 bg-gradient-to-r from-indigo-50/90 to-blue-50/80 p-4 rounded-2xl shadow-xs"
    >
      <div class="flex items-center gap-3">
        <span class="text-xl">📍</span>
        <div>
          <p class="text-xs font-extrabold text-indigo-950">Location Permission Active</p>
          <p class="text-xs text-indigo-700/90">
            Allow location access in your browser to sort courts by proximity and calculate exact
            driving times.
          </p>
        </div>
      </div>
      <button
        type="button"
        class="btn-primary shrink-0 px-4 py-2 rounded-xl text-xs font-bold shadow-xs"
        :disabled="locating"
        @click="locateMember(false)"
      >
        {{ locating ? 'Detecting GPS…' : 'Allow / Detect Location' }}
      </button>
    </div>

    <!-- =====================================================
         SEARCH & FILTER CONTROL BAR
    ====================================================== -->
    <div
      class="glass p-4 sm:p-5 rounded-2xl space-y-4 shadow-sm border border-slate-200/80 bg-white"
    >
      <!-- Row 1: Search Input & Distance Radius Dropdown -->
      <div class="grid gap-3 md:grid-cols-[1fr_200px]">
        <!-- Search Input -->
        <div class="relative">
          <div
            class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-400"
          >
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search clubs, localities (Koramangala, Indiranagar, Ashok Nagar, Yelahanka)..."
            class="filter-search-input pl-10 pr-9 w-full"
            @input="onSearchChange"
          />
          <button
            v-if="searchQuery"
            type="button"
            class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600"
            title="Clear search"
            @click="clearSearch"
          >
            ✕
          </button>
        </div>

        <!-- Distance Radius Dropdown -->
        <div class="relative">
          <select
            v-model="selectedDistanceRadius"
            class="filter-select-input w-full"
            :disabled="!userLocation"
            @change="applyFilters"
          >
            <option value="all">
              {{ userLocation ? 'Any Distance' : 'Distance (Enable GPS)' }}
            </option>
            <option value="5">Within 5 km</option>
            <option value="10">Within 10 km</option>
            <option value="15">Within 15 km</option>
            <option value="25">Within 25 km</option>
            <option value="50">Within 50 km</option>
          </select>
        </div>
      </div>

      <!-- Row 2: Sport Category Pills -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1.5 scrollbar-thin">
        <button
          v-for="sport in sportOptions"
          :key="sport.value"
          type="button"
          class="sport-pill"
          :class="{ 'sport-pill-active': selectedSport === sport.value }"
          @click="selectSport(sport.value)"
        >
          <span class="sport-pill-emoji">{{ sport.emoji }}</span>
          <span class="sport-pill-label">{{ sport.label }}</span>
          <span
            v-if="sportCounts[sport.value]"
            class="sport-pill-count"
            :class="{ 'sport-pill-count-active': selectedSport === sport.value }"
          >
            {{ sportCounts[sport.value] }}
          </span>
        </button>
      </div>

      <!-- Filter Stats and Clear Link -->
      <div
        class="flex flex-wrap items-center justify-between gap-2 border-t border-slate-100 pt-3 text-xs text-slate-500"
      >
        <div>
          Showing <span class="font-bold text-slate-800">{{ filteredClubs.length }}</span> club{{
            filteredClubs.length === 1 ? '' : 's'
          }}
          with <span class="font-bold text-indigo-600">{{ totalFilteredCourts }}</span> court{{
            totalFilteredCourts === 1 ? '' : 's'
          }}
          <span v-if="selectedSport !== 'all'">
            in
            <span class="font-bold text-slate-800 capitalize">{{
              displaySport(selectedSport)
            }}</span></span
          >
        </div>

        <button
          v-if="isFiltered"
          type="button"
          class="font-semibold text-indigo-600 hover:text-indigo-800"
          @click="resetFilters"
        >
          Reset all filters
        </button>
      </div>
    </div>

    <!-- =====================================================
         MAP & SIDEBAR MAIN GRID
    ====================================================== -->
    <div
      ref="mapContainerRef"
      class="grid gap-5 xl:grid-cols-[minmax(0,1fr)_420px]"
      :class="{ 'fullscreen-map-wrapper': isFullscreen }"
    >
      <!-- MAP SECTION -->
      <section
        class="glass overflow-hidden rounded-2xl flex flex-col relative border border-slate-200/80 shadow-sm bg-white"
      >
        <!-- Floating Map Controls -->
        <div class="absolute top-4 right-4 z-[400] flex flex-col gap-2">
          <!-- Fullscreen Button -->
          <button
            type="button"
            class="map-control-btn"
            :title="isFullscreen ? 'Exit Fullscreen' : 'Fullscreen Map'"
            @click="toggleFullscreen"
          >
            <svg
              v-if="!isFullscreen"
              class="h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
              />
            </svg>
            <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <!-- Re-center on user or Bangalore -->
          <button type="button" class="map-control-btn" title="Recenter Map" @click="fitMap">
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 21a9 9 0 100-18 9 9 0 000 18zm0-12v6m-3-3h6"
              />
            </svg>
          </button>
        </div>

        <!-- Leaflet Map Mount Point -->
        <div
          ref="mapElement"
          class="nearby-map flex-1"
          :class="{ 'nearby-map-fullscreen': isFullscreen }"
          aria-label="Interactive map showing Bengaluru sports clubs and courts"
        />

        <!-- Map Footer Legend & Context -->
        <div class="border-t border-slate-200 bg-slate-50/80 px-4 py-3">
          <div
            class="flex flex-wrap items-center justify-between gap-x-5 gap-y-2 text-xs text-slate-600"
          >
            <div class="flex flex-wrap items-center gap-x-4 gap-y-2">
              <span class="flex items-center gap-1.5">
                <span class="legend-dot bg-indigo-600" />
                <span>Club Venue</span>
              </span>
              <span v-if="userLocation" class="flex items-center gap-1.5">
                <span class="legend-dot bg-sky-500 ring-2 ring-sky-200" />
                <span>Your Location</span>
              </span>
              <span v-if="activeRoute" class="flex items-center gap-1.5">
                <span class="legend-dot bg-indigo-500 ring-2 ring-indigo-300" />
                <span>Road Navigation ({{ activeRoute.durationMin }} mins)</span>
              </span>
              <span v-else-if="selectedCourt" class="flex items-center gap-1.5">
                <span class="legend-dot bg-emerald-600" />
                <span>Selected Court Preview</span>
              </span>
            </div>

            <span class="text-[11px] text-slate-400">
              Click any club to book or calculate road route
            </span>
          </div>
        </div>
      </section>

      <!-- SIDEBAR CONTROLS & CLUB / COURT DETAILS -->
      <aside class="space-y-4">
        <!-- =====================================================
             ACTIVE IN-APP ROAD NAVIGATION CARD
        ====================================================== -->
        <div
          v-if="activeRoute"
          class="glass p-5 rounded-2xl border-2 border-indigo-500 bg-gradient-to-br from-indigo-50/60 to-white shadow-md space-y-3.5 transition"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2">
                <span
                  class="px-2 py-0.5 rounded-md bg-indigo-600 text-[10px] font-extrabold uppercase tracking-wider text-white shadow-xs"
                >
                  🛣️ In-App Road Route
                </span>
                <span class="text-[11px] text-slate-500 font-medium truncate">
                  {{ activeRoute.summary }}
                </span>
              </div>
              <h3 class="mt-1 text-lg font-extrabold text-slate-900 truncate">
                To {{ activeRoute.destinationClub.name }}
              </h3>
            </div>

            <button
              type="button"
              class="text-xs font-bold text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100"
              title="Clear Route"
              @click="clearRoute"
            >
              ✕
            </button>
          </div>

          <!-- Travel Time & Distance Badges -->
          <div class="grid grid-cols-2 gap-2.5">
            <div class="rounded-xl border border-indigo-100 bg-white p-2.5 text-center shadow-xs">
              <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Est. Travel Time
              </p>
              <p class="mt-0.5 text-xl font-black text-indigo-600">
                {{ activeRoute.durationMin }} mins
              </p>
            </div>
            <div class="rounded-xl border border-indigo-100 bg-white p-2.5 text-center shadow-xs">
              <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Road Distance
              </p>
              <p class="mt-0.5 text-xl font-black text-slate-800">
                {{ activeRoute.distanceKm }} km
              </p>
            </div>
          </div>

          <!-- Mode Switcher (Driving vs Walking) -->
          <div class="flex items-center gap-2 bg-slate-100/80 p-1 rounded-xl">
            <button
              type="button"
              class="flex-1 py-1.5 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5"
              :class="
                routeMode === 'driving'
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              "
              @click="changeRouteMode('driving')"
            >
              🚗 Driving (Car/Bike)
            </button>
            <button
              type="button"
              class="flex-1 py-1.5 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5"
              :class="
                routeMode === 'walking'
                  ? 'bg-indigo-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              "
              @click="changeRouteMode('walking')"
            >
              🚶 Walking
            </button>
          </div>

          <!-- Turn-by-Turn Collapsible Steps -->
          <div class="border-t border-indigo-100 pt-3">
            <button
              type="button"
              class="w-full flex items-center justify-between py-1 text-xs font-bold text-slate-700 hover:text-indigo-600 transition"
              @click="showTurnByTurn = !showTurnByTurn"
            >
              <span>Turn-by-Turn Directions ({{ activeRoute.steps?.length || 0 }} steps)</span>
              <span class="text-indigo-600">{{
                showTurnByTurn ? '▲ Hide Steps' : '▼ Show Steps'
              }}</span>
            </button>

            <div
              v-if="showTurnByTurn"
              class="mt-2.5 space-y-1.5 max-h-[220px] overflow-y-auto pr-1 scrollbar-thin"
            >
              <div
                v-for="(step, idx) in activeRoute.steps"
                :key="step.id"
                class="flex items-start gap-2.5 rounded-lg border border-slate-100 bg-white p-2.5 text-xs shadow-xs"
              >
                <span
                  class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-indigo-50 text-[10px] font-black text-indigo-600"
                >
                  {{ idx + 1 }}
                </span>
                <div class="min-w-0 flex-1">
                  <p class="font-semibold text-slate-800 leading-snug">{{ step.instruction }}</p>
                </div>
                <span class="shrink-0 text-[11px] font-bold text-slate-400">{{
                  step.distanceText
                }}</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center justify-between pt-1">
            <button
              type="button"
              class="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
              @click="openDirections(activeRoute.destinationClub)"
            >
              <span>Live Voice GPS (Google Maps)</span>
              <span>↗</span>
            </button>
            <button
              type="button"
              class="text-xs font-semibold text-slate-500 hover:text-slate-700"
              @click="clearRoute"
            >
              Clear Route
            </button>
          </div>
        </div>

        <!-- SELECTED CLUB DETAILS CARD -->
        <div
          v-if="selectedClub"
          class="glass p-5 rounded-2xl border border-indigo-100 bg-white shadow-sm transition"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2">
                <span
                  class="px-2 py-0.5 rounded-md bg-indigo-50 text-[10px] font-extrabold uppercase tracking-wider text-indigo-600"
                >
                  Selected Venue
                </span>
                <span
                  v-if="selectedClub.open_time"
                  class="text-[11px] font-semibold text-slate-400"
                >
                  🕒 {{ selectedClub.open_time }} – {{ selectedClub.close_time || '22:00' }}
                </span>
              </div>
              <h2 class="mt-1 text-xl font-extrabold text-slate-900 truncate">
                {{ selectedClub.name }}
              </h2>
            </div>

            <span
              v-if="selectedClub.distanceKm != null"
              class="shrink-0 rounded-full bg-emerald-50 px-3 py-1 text-xs font-extrabold text-emerald-700 border border-emerald-200/50"
            >
              {{ formatDistance(selectedClub.distanceKm) }}
            </span>
          </div>

          <p class="mt-2 text-xs text-slate-500 leading-relaxed">
            {{ selectedClub.address || 'Address in Bengaluru' }}
          </p>

          <!-- Routing & Directions Actions -->
          <div class="mt-3.5 flex flex-wrap items-center gap-2">
            <button
              type="button"
              class="btn-primary inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-xl shadow-sm"
              :disabled="routingLoading"
              @click="calculateRoute(selectedClub)"
            >
              <span
                v-if="routingLoading"
                class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/40 border-t-white"
              />
              <svg v-else class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 20l-5-2V6l5 2m0 12l6-2m-6 2V8m6 10l5 2V6l-5-2m0 12V4"
                />
              </svg>
              {{ routingLoading ? 'Calculating…' : 'In-App Road Route' }}
            </button>

            <button
              type="button"
              class="btn-secondary inline-flex items-center gap-1.5 text-xs font-bold px-3 py-1.5 rounded-xl"
              @click="openDirections(selectedClub)"
            >
              <svg
                class="h-3.5 w-3.5 text-slate-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
              Google Maps
            </button>

            <button
              type="button"
              class="text-xs font-semibold text-slate-400 hover:text-slate-600 ml-auto"
              @click="clearSelection"
            >
              Deselect
            </button>
          </div>

          <!-- Courts at this club -->
          <div class="mt-5 border-t border-slate-100 pt-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-extrabold text-slate-900">Available Courts</h3>
              <span
                class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600"
              >
                {{ getFilteredClubCourts(selectedClub).length }} court{{
                  getFilteredClubCourts(selectedClub).length === 1 ? '' : 's'
                }}
              </span>
            </div>

            <div class="mt-3 space-y-2 max-h-[290px] overflow-y-auto pr-1 scrollbar-thin">
              <div
                v-for="court in getFilteredClubCourts(selectedClub)"
                :key="court.id"
                class="court-card-item"
                :class="{ 'court-card-selected': selectedCourt?.id === court.id }"
              >
                <div
                  class="flex items-center gap-3 min-w-0 flex-1 cursor-pointer"
                  @click="selectCourt(selectedClub, court)"
                >
                  <span class="court-sport-icon" :class="sportClass(court.sport_type)">
                    {{ sportEmoji(court.sport_type) }}
                  </span>

                  <div class="min-w-0 flex-1 text-left">
                    <div class="flex items-center gap-2">
                      <span class="block truncate text-sm font-bold text-slate-800">
                        {{ court.name }}
                      </span>
                      <span
                        v-if="selectedCourt?.id === court.id"
                        class="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded"
                      >
                        Mapped
                      </span>
                    </div>
                    <span class="block text-xs capitalize text-slate-400">
                      {{ displaySport(court.sport_type) }}
                    </span>
                  </div>
                </div>

                <!-- Direct Book Button -->
                <button
                  type="button"
                  class="btn-primary text-xs font-bold px-3 py-1.5 rounded-xl shrink-0"
                  @click="navigateToBook(selectedClub, court)"
                >
                  Book Slot →
                </button>
              </div>

              <div
                v-if="!getFilteredClubCourts(selectedClub).length"
                class="py-6 text-center text-xs text-slate-400"
              >
                No courts match the "{{ displaySport(selectedSport) }}" filter at this club.
              </div>
            </div>
          </div>
        </div>

        <!-- EXPLORE / LIST OF CLUBS -->
        <div class="glass p-5 rounded-2xl border border-slate-200/80 bg-white shadow-sm">
          <div class="flex items-center justify-between">
            <h2 class="font-extrabold text-slate-900 text-sm">
              {{ userLocation ? 'Nearby Sports Venues' : 'Bengaluru Sports Venues' }}
            </h2>
            <span class="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">
              {{ filteredClubs.length }} Found
            </span>
          </div>

          <!-- Loading state -->
          <div v-if="loading" class="mt-4 space-y-2">
            <div v-for="item in 3" :key="item" class="h-20 animate-pulse rounded-xl bg-slate-100" />
          </div>

          <!-- List of filtered clubs -->
          <div
            v-else-if="filteredClubs.length"
            class="mt-3 space-y-2.5 max-h-[440px] overflow-y-auto pr-1 scrollbar-thin"
          >
            <div
              v-for="club in filteredClubs"
              :key="club.id"
              class="club-list-card"
              :class="{ 'club-list-card-active': selectedClub?.id === club.id }"
              @click="focusClub(club)"
            >
              <div class="flex items-start justify-between gap-3">
                <div class="min-w-0 flex-1">
                  <div class="flex items-center gap-1.5">
                    <span class="truncate text-sm font-bold text-slate-900">
                      {{ club.name }}
                    </span>
                  </div>
                  <p class="mt-0.5 truncate text-xs text-slate-500">
                    {{ club.address }}
                  </p>
                </div>

                <span
                  v-if="club.distanceKm != null"
                  class="shrink-0 text-xs font-extrabold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-md"
                >
                  {{ formatDistance(club.distanceKm) }}
                </span>
              </div>

              <!-- Sport badges on club card -->
              <div class="mt-2.5 flex flex-wrap items-center gap-1.5">
                <span v-for="sport in getClubSports(club)" :key="sport" class="club-sport-tag">
                  {{ sportEmoji(sport) }} {{ displaySport(sport) }}
                </span>
                <span class="text-[11px] text-slate-400 ml-auto font-medium">
                  {{ club.courts?.length || 0 }} courts
                </span>
              </div>
            </div>
          </div>

          <!-- Empty search state -->
          <div v-else-if="!loading" class="py-8 text-center space-y-3">
            <div
              class="w-12 h-12 mx-auto rounded-full bg-slate-100 flex items-center justify-center text-slate-400"
            >
              🔍
            </div>
            <p class="text-sm font-bold text-slate-700">No clubs match your criteria</p>
            <p class="text-xs text-slate-400 max-w-xs mx-auto">
              Try adjusting your search query, selecting "All Sports", or expanding your distance
              radius.
            </p>
            <button
              type="button"
              class="btn-secondary text-xs font-bold px-3 py-1.5 rounded-lg"
              @click="resetFilters"
            >
              Reset Filters
            </button>
          </div>
        </div>
      </aside>
    </div>

    <!-- Footnote -->
    <p class="text-xs text-slate-400 text-center sm:text-left">
      Location access stays entirely within your browser. All Bengaluru venues support live court
      discovery, sport filtering, in-app road routing, and instant booking deep-linking.
    </p>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import {
  distanceInKm,
  fetchRoute,
  geocodeClubAddress,
  getCurrentPosition,
  loadLeaflet,
} from '@/services/leaflet'

const router = useRouter()

// =========================================================
// REAL BENGALURU SPORTS VENUES (PRACTICAL & COMPLETE)
// =========================================================
const REAL_BANGALORE_CLUBS = [
  {
    id: 101,
    name: 'Bangalore Club',
    address:
      '10, Field Marshal Cariappa Rd, Shanthala Nagar, Ashok Nagar, Bengaluru, Karnataka 560025',
    lat: 12.9698,
    lng: 77.5986,
    open_time: '06:00',
    close_time: '23:00',
    courts: [
      { id: 1001, name: 'Centre Clay Tennis Court', sport_type: 'tennis', is_active: true },
      {
        id: 1002,
        name: 'Wooden Badminton Hall - Court 1',
        sport_type: 'badminton',
        is_active: true,
      },
      {
        id: 1003,
        name: 'Wooden Badminton Hall - Court 2',
        sport_type: 'badminton',
        is_active: true,
      },
      { id: 1004, name: 'Glass Back Squash Court', sport_type: 'squash', is_active: true },
      { id: 1005, name: 'Main Cricket Nets & Pitch', sport_type: 'multi-purpose', is_active: true },
    ],
  },
  {
    id: 102,
    name: 'Padukone - Dravid Centre for Sports Excellence (CSE)',
    address:
      'Survey No 336, Bettahalasuru Jala Hobli, Yelahanka Taluk, Bengaluru, Karnataka 562157',
    lat: 13.1783,
    lng: 77.6358,
    open_time: '05:30',
    close_time: '22:30',
    courts: [
      { id: 1006, name: 'Olympic Badminton Arena 1', sport_type: 'badminton', is_active: true },
      { id: 1007, name: 'Olympic Badminton Arena 2', sport_type: 'badminton', is_active: true },
      {
        id: 1008,
        name: 'Grand Slam Synthetic Tennis Court',
        sport_type: 'tennis',
        is_active: true,
      },
      { id: 1009, name: 'FIFA Pro Football Turf', sport_type: 'football', is_active: true },
      { id: 1010, name: 'FIBA Basketball Court', sport_type: 'basketball', is_active: true },
      { id: 1011, name: 'Padel Arena Bengaluru', sport_type: 'padel', is_active: true },
      { id: 1012, name: 'Pro Pickleball Court', sport_type: 'pickleball', is_active: true },
    ],
  },
  {
    id: 103,
    name: 'The Koramangala Club',
    address: '6th Cross, 6th Block, Koramangala, Bengaluru, Karnataka 560095',
    lat: 12.9345,
    lng: 77.62,
    open_time: '06:00',
    close_time: '22:00',
    courts: [
      { id: 1013, name: 'Floodlit Tennis Court 1', sport_type: 'tennis', is_active: true },
      { id: 1014, name: 'Floodlit Tennis Court 2', sport_type: 'tennis', is_active: true },
      { id: 1015, name: 'Indoor Badminton Court A', sport_type: 'badminton', is_active: true },
      { id: 1016, name: 'Air-Conditioned Squash Court', sport_type: 'squash', is_active: true },
    ],
  },
  {
    id: 104,
    name: 'Indiranagar Club',
    address: '9th Main Road, 4th Cross, HAL 2nd Stage, Indiranagar, Bengaluru, Karnataka 560008',
    lat: 12.9676,
    lng: 77.6432,
    open_time: '06:00',
    close_time: '22:30',
    courts: [
      { id: 1017, name: 'Synthetic Tennis Court 1', sport_type: 'tennis', is_active: true },
      { id: 1018, name: 'Indoor Badminton Arena', sport_type: 'badminton', is_active: true },
      { id: 1019, name: 'Squash Court 1', sport_type: 'squash', is_active: true },
      {
        id: 1020,
        name: 'Outdoor Basketball Half-Court',
        sport_type: 'basketball',
        is_active: true,
      },
    ],
  },
  {
    id: 105,
    name: 'Play Arena Sports Complex',
    address: 'Sarjapur Main Road, Central Jail Road, Kasavanahalli, Bengaluru, Karnataka 560035',
    lat: 12.8988,
    lng: 77.6744,
    open_time: '06:00',
    close_time: '23:00',
    courts: [
      { id: 1021, name: '5v5 AstroTurf Football Pitch', sport_type: 'football', is_active: true },
      { id: 1022, name: 'Outdoor Hardcourt Basketball', sport_type: 'basketball', is_active: true },
      { id: 1023, name: 'Pro Padel Court 1', sport_type: 'padel', is_active: true },
      { id: 1024, name: 'Sand Volleyball Court', sport_type: 'volleyball', is_active: true },
      { id: 1025, name: 'Pickleball Zone A', sport_type: 'pickleball', is_active: true },
    ],
  },
  {
    id: 106,
    name: 'KSCA Chinnaswamy Stadium Complex',
    address: 'Cubbon Road, Shivaji Nagar, Bengaluru, Karnataka 560001',
    lat: 12.9788,
    lng: 77.5996,
    open_time: '06:00',
    close_time: '22:00',
    courts: [
      {
        id: 1026,
        name: 'Chinnaswamy Cricket Nets & Arena',
        sport_type: 'multi-purpose',
        is_active: true,
      },
      { id: 1027, name: 'Club House Badminton Court', sport_type: 'badminton', is_active: true },
      { id: 1028, name: 'Members Lawn Tennis', sport_type: 'tennis', is_active: true },
    ],
  },
  {
    id: 107,
    name: 'Bowring Institute',
    address: "St Mark's Rd, Shantala Nagar, Ashok Nagar, Bengaluru, Karnataka 560001",
    lat: 12.9734,
    lng: 77.6041,
    open_time: '06:00',
    close_time: '23:00',
    courts: [
      { id: 1029, name: 'Heritage Clay Tennis Court 1', sport_type: 'tennis', is_active: true },
      { id: 1030, name: 'Heritage Clay Tennis Court 2', sport_type: 'tennis', is_active: true },
      { id: 1031, name: 'Indoor Badminton Hall', sport_type: 'badminton', is_active: true },
      { id: 1032, name: 'Squash Pavilion', sport_type: 'squash', is_active: true },
    ],
  },
]

// =========================================================
// REACTIVE STATE
// =========================================================
const mapElement = ref(null)
const mapContainerRef = ref(null)
const clubs = ref([])
const loading = ref(true)
const locating = ref(false)
const routingLoading = ref(false)
const error = ref('')
const userLocation = ref(null)
const selectedClub = ref(null)
const selectedCourt = ref(null)
const isFullscreen = ref(false)

// Routing state
const activeRoute = ref(null)
const routeMode = ref('driving')
const showTurnByTurn = ref(false)

// Filters
const searchQuery = ref('')
const selectedSport = ref('all')
const selectedDistanceRadius = ref('all')

let map = null
let markerLayer = null
let courtLayer = null
let routeLayer = null
let userMarker = null
let userAccuracyCircle = null

// Sport Options definition
const sportOptions = [
  { value: 'all', label: 'All Sports', emoji: '🏟️' },
  { value: 'tennis', label: 'Tennis', emoji: '🎾' },
  { value: 'badminton', label: 'Badminton', emoji: '🏸' },
  { value: 'football', label: 'Football', emoji: '⚽' },
  { value: 'basketball', label: 'Basketball', emoji: '🏀' },
  { value: 'squash', label: 'Squash', emoji: '🎾' },
  { value: 'padel', label: 'Padel', emoji: '🎾' },
  { value: 'pickleball', label: 'Pickleball', emoji: '🥒' },
  { value: 'volleyball', label: 'Volleyball', emoji: '🏐' },
  { value: 'golf', label: 'Golf', emoji: '⛳' },
  { value: 'multi-purpose', label: 'Multi-Purpose', emoji: '🏟️' },
]

// =========================================================
// COMPUTED FILTERED CLUBS & STATS
// =========================================================
const locatedClubs = computed(() => {
  return clubs.value
    .filter((club) => Number.isFinite(club.lat) && Number.isFinite(club.lng))
    .sort(
      (a, b) =>
        (a.distanceKm ?? Number.POSITIVE_INFINITY) - (b.distanceKm ?? Number.POSITIVE_INFINITY),
    )
})

const isFiltered = computed(() => {
  return (
    Boolean(searchQuery.value.trim()) ||
    selectedSport.value !== 'all' ||
    selectedDistanceRadius.value !== 'all'
  )
})

const filteredClubs = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  const sport = selectedSport.value.toLowerCase()
  const maxDist =
    selectedDistanceRadius.value === 'all'
      ? Number.POSITIVE_INFINITY
      : Number(selectedDistanceRadius.value)

  return locatedClubs.value.filter((club) => {
    // 1. Search Query Filter (name, address, sport)
    if (query) {
      const matchName = String(club.name || '')
        .toLowerCase()
        .includes(query)
      const matchAddress = String(club.address || '')
        .toLowerCase()
        .includes(query)
      const matchCourts = (club.courts || []).some(
        (c) =>
          String(c.name || '')
            .toLowerCase()
            .includes(query) ||
          String(c.sport_type || '')
            .toLowerCase()
            .includes(query),
      )
      if (!matchName && !matchAddress && !matchCourts) return false
    }

    // 2. Sport Type Filter
    if (sport !== 'all') {
      const hasSport = (club.courts || []).some((c) => {
        const cSport = String(c.sport_type || '')
          .toLowerCase()
          .replace(/_/g, '-')
        return cSport === sport || (sport === 'football' && cSport === 'soccer')
      })
      if (!hasSport) return false
    }

    // 3. Distance Radius Filter
    if (Number.isFinite(maxDist) && maxDist > 0) {
      if (club.distanceKm == null || club.distanceKm > maxDist) return false
    }

    return true
  })
})

const totalFilteredCourts = computed(() => {
  return filteredClubs.value.reduce((total, club) => {
    return total + getFilteredClubCourts(club).length
  }, 0)
})

const sportCounts = computed(() => {
  const counts = { all: 0 }
  sportOptions.forEach((s) => {
    if (s.value !== 'all') counts[s.value] = 0
  })

  locatedClubs.value.forEach((club) => {
    ;(club.courts || []).forEach((c) => {
      counts.all += 1
      const normalized = String(c.sport_type || 'multi-purpose')
        .toLowerCase()
        .replace(/_/g, '-')
      if (counts[normalized] !== undefined) {
        counts[normalized] += 1
      }
    })
  })

  return counts
})

// =========================================================
// HELPER FUNCTIONS
// =========================================================
function formatDistance(value) {
  if (!Number.isFinite(value)) return '—'
  if (value < 1) return `${Math.round(value * 1000)} m`
  return `${value.toFixed(1)} km`
}

function displaySport(value) {
  const sport = String(value || 'multi-purpose').replaceAll('-', ' ')
  return sport.replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function sportEmoji(value) {
  const sport = String(value || 'multi-purpose')
    .toLowerCase()
    .replace(/_/g, '-')

  const icons = {
    tennis: '🎾',
    badminton: '🏸',
    basketball: '🏀',
    football: '⚽',
    soccer: '⚽',
    golf: '⛳',
    volleyball: '🏐',
    pickleball: '🥒',
    padel: '🎾',
    squash: '🎾',
    'multi-purpose': '🏟️',
  }

  return icons[sport] || '🏟️'
}

function sportClass(value) {
  const sport = String(value || 'multi-purpose')
    .toLowerCase()
    .replace(/_/g, '-')
  return `sport-${sport.replaceAll(' ', '-')}`
}

function getClubSports(club) {
  const sports = new Set()
  ;(club.courts || []).forEach((c) => {
    if (c.sport_type) sports.add(c.sport_type)
  })
  return Array.from(sports).slice(0, 4)
}

function getFilteredClubCourts(club) {
  if (!club || !Array.isArray(club.courts)) return []
  if (selectedSport.value === 'all') return club.courts

  return club.courts.filter((c) => {
    const s = String(c.sport_type || '')
      .toLowerCase()
      .replace(/_/g, '-')
    return s === selectedSport.value
  })
}

function getDirectionsUrl(club) {
  if (!club?.lat || !club?.lng) return '#'

  const destination = `${club.lat},${club.lng}`
  const origin = userLocation.value ? `${userLocation.value.lat},${userLocation.value.lng}` : ''

  const params = new URLSearchParams({
    api: '1',
    destination,
  })

  if (origin) params.set('origin', origin)

  return `https://www.google.com/maps/dir/?${params.toString()}`
}

function openDirections(club) {
  const url = getDirectionsUrl(club)
  if (url !== '#') window.open(url, '_blank', 'noopener,noreferrer')
}

function navigateToBook(club, court) {
  if (!club) return
  router.push({
    name: 'member-book-court',
    query: {
      club_id: club.id,
      court_id: court?.id || undefined,
    },
  })
}

function clearSelection() {
  selectedClub.value = null
  selectedCourt.value = null
  clearCourtSelection()
  refreshMarkerHighlight()
}

async function refreshMarkerHighlight() {
  if (!map) return
  const L = await loadLeaflet()
  filteredClubs.value.forEach((c) => {
    if (c._marker) {
      const isSelected = selectedClub.value?.id === c.id
      c._marker.setIcon(clubIcon(L, isSelected))
      if (isSelected) {
        c._marker.setZIndexOffset(1000)
      } else {
        c._marker.setZIndexOffset(0)
      }
    }
  })
}

// =========================================================
// IN-APP ROAD ROUTING ENGINE
// =========================================================
async function calculateRoute(club, mode = routeMode.value) {
  if (!club || !Number.isFinite(club.lat) || !Number.isFinite(club.lng)) return

  routingLoading.value = true
  selectedClub.value = club

  // Start point: user GPS coordinates if enabled, otherwise central Bengaluru
  const startLat = userLocation.value ? userLocation.value.lat : 12.9716
  const startLng = userLocation.value ? userLocation.value.lng : 77.5946
  const startName = userLocation.value ? 'Your Location' : 'Bengaluru City Center'

  try {
    const routeResult = await fetchRoute(startLat, startLng, club.lat, club.lng, mode)

    activeRoute.value = {
      ...routeResult,
      startName,
      destinationClub: club,
      mode,
    }

    const L = await loadLeaflet()
    drawRoadRoute(L, routeResult.coordinates)
  } catch (err) {
    error.value = 'Could not calculate road route. Please check your internet connection.'
    console.error('Road routing error:', err)
  } finally {
    routingLoading.value = false
  }
}

async function changeRouteMode(mode) {
  routeMode.value = mode
  if (activeRoute.value?.destinationClub) {
    await calculateRoute(activeRoute.value.destinationClub, mode)
  }
}

function clearRoute() {
  activeRoute.value = null
  showTurnByTurn.value = false
  if (routeLayer) routeLayer.clearLayers()
  if (map) fitMap()
}

function drawRoadRoute(L, coordinates) {
  if (!map || !routeLayer || !coordinates || !coordinates.length) return

  routeLayer.clearLayers()
  if (courtLayer) courtLayer.clearLayers()

  // 1. Background glow / casing polyline
  L.polyline(coordinates, {
    color: '#1e1b4b',
    weight: 8,
    opacity: 0.35,
    lineCap: 'round',
    lineJoin: 'round',
  }).addTo(routeLayer)

  // 2. Main sharp road route polyline
  const mainLine = L.polyline(coordinates, {
    color: '#4f46e5',
    weight: 5,
    opacity: 0.95,
    lineCap: 'round',
    lineJoin: 'round',
  }).addTo(routeLayer)

  mainLine.bindTooltip(
    `Road Route: ${activeRoute.value?.durationMin || 0} mins (${activeRoute.value?.distanceKm || 0} km)`,
    { sticky: true, direction: 'center' },
  )

  map.fitBounds(coordinates, {
    padding: [60, 60],
    animate: true,
  })
}

// =========================================================
// FILTERS HANDLERS
// =========================================================
function selectSport(sport) {
  selectedSport.value = sport
  applyFilters()
}

function onSearchChange() {
  applyFilters()
}

function clearSearch() {
  searchQuery.value = ''
  applyFilters()
}

function resetFilters() {
  searchQuery.value = ''
  selectedSport.value = 'all'
  selectedDistanceRadius.value = 'all'
  applyFilters()
}

async function applyFilters() {
  if (!map) return
  const L = await loadLeaflet()
  drawClubs(L)
}

// =========================================================
// LEAFLET MAP INITIALIZATION & RENDERING
// =========================================================
function createMap(L) {
  if (map || !mapElement.value) return

  // Default centered in Bengaluru, Karnataka (12.9716, 77.5946)
  map = L.map(mapElement.value, {
    zoomControl: true,
    attributionControl: true,
  }).setView([12.9716, 77.5946], 12)

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map)

  markerLayer = L.layerGroup().addTo(map)
  courtLayer = L.layerGroup().addTo(map)
  routeLayer = L.layerGroup().addTo(map)
}

function clubIcon(L, isSelected = false) {
  return L.divIcon({
    className: 'club-map-icon-wrapper',
    html: `
      <div class="club-map-icon ${isSelected ? 'club-map-icon-active' : ''}">
        🏟️
        ${isSelected ? '<span class="pulse-ring"></span>' : ''}
      </div>
    `,
    iconSize: [44, 44],
    iconAnchor: [22, 40],
    popupAnchor: [0, -36],
  })
}

function courtIcon(L, sportType) {
  const emoji = escapeHtml(sportEmoji(sportType))

  return L.divIcon({
    className: 'court-map-icon-wrapper',
    html: `<div class="court-map-icon">${emoji}</div>`,
    iconSize: [42, 42],
    iconAnchor: [21, 38],
    popupAnchor: [0, -34],
  })
}

function drawUserLocation(L) {
  if (!map || !userLocation.value) return

  const { lat, lng, accuracy } = userLocation.value

  if (userMarker) userMarker.remove()
  if (userAccuracyCircle) userAccuracyCircle.remove()

  userMarker = L.circleMarker([lat, lng], {
    radius: 10,
    color: '#ffffff',
    weight: 3,
    fillColor: '#3b82f6',
    fillOpacity: 1,
  })
    .bindPopup('<strong>📍 Your Current Location</strong>')
    .addTo(map)

  userAccuracyCircle = L.circle([lat, lng], {
    radius: accuracy || 100,
    color: '#3b82f6',
    weight: 1,
    fillColor: '#3b82f6',
    fillOpacity: 0.1,
  }).addTo(map)
}

function createClubPopup(club) {
  const courts = getFilteredClubCourts(club)

  const courtRows = courts.length
    ? courts
        .slice(0, 4)
        .map(
          (court) => `
            <div class="map-court-row-wrapper">
              <button
                type="button"
                class="map-court-row"
                data-court-id="${escapeHtml(court.id)}"
                data-club-id="${escapeHtml(club.id)}"
              >
                <span class="map-court-icon">${escapeHtml(sportEmoji(court.sport_type))}</span>
                <span class="map-court-copy">
                  <strong>${escapeHtml(court.name)}</strong>
                  <small>${escapeHtml(displaySport(court.sport_type))}</small>
                </span>
              </button>
              <button
                type="button"
                class="map-court-book-btn"
                data-book-court-id="${escapeHtml(court.id)}"
                data-book-club-id="${escapeHtml(club.id)}"
                title="Book this court now"
              >
                Book
              </button>
            </div>
          `,
        )
        .join('')
    : '<p class="map-empty">No matching courts found.</p>'

  const distanceHtml =
    club.distanceKm != null
      ? `<span class="map-popup-badge">${formatDistance(club.distanceKm)} away</span>`
      : ''

  return `
    <div class="map-club-popup">
      <div class="flex items-center justify-between">
        <div class="map-popup-kicker">Bengaluru Sports Venue</div>
        ${distanceHtml}
      </div>
      <strong class="map-popup-title">${escapeHtml(club.name)}</strong>
      <div class="map-popup-address">${escapeHtml(club.address || 'Address in Bengaluru')}</div>

      <div class="map-popup-section-title">
        Available Courts
        <span>${courts.length}</span>
      </div>

      <div class="map-court-list">${courtRows}</div>

      <div class="map-popup-actions">
        <button
          type="button"
          class="map-popup-btn-route"
          data-route-club-id="${escapeHtml(club.id)}"
        >
          🧭 Road Route
        </button>
        <button
          type="button"
          class="map-popup-btn-full"
          data-explore-club-id="${escapeHtml(club.id)}"
        >
          Details →
        </button>
      </div>
    </div>
  `
}

function attachPopupCourtHandlers(L, club, marker) {
  marker.on('popupopen', (event) => {
    const popupElement = event.popup.getElement()
    if (!popupElement) return

    // Click on court row -> preview court on map
    popupElement.querySelectorAll('[data-court-id]').forEach((button) => {
      button.addEventListener('click', (e) => {
        e.stopPropagation()
        const courtId = Number(button.dataset.courtId)
        const court = club.courts?.find((item) => Number(item.id) === courtId)
        if (court) {
          selectCourt(club, court)
        }
      })
    })

    // Click on Book button -> navigate to BookCourt.vue directly
    popupElement.querySelectorAll('[data-book-court-id]').forEach((button) => {
      button.addEventListener('click', (e) => {
        e.stopPropagation()
        const courtId = Number(button.dataset.bookCourtId)
        const court = club.courts?.find((item) => Number(item.id) === courtId)
        navigateToBook(club, court)
      })
    })

    // Click on Road Route button -> calculate and draw in-app road route
    popupElement.querySelectorAll('[data-route-club-id]').forEach((button) => {
      button.addEventListener('click', (e) => {
        e.stopPropagation()
        calculateRoute(club)
        event.popup.remove()
      })
    })

    // Click on Explore Club -> select club in sidebar
    popupElement.querySelectorAll('[data-explore-club-id]').forEach((button) => {
      button.addEventListener('click', (e) => {
        e.stopPropagation()
        selectedClub.value = club
        selectedCourt.value = null
        clearCourtSelection()
        refreshMarkerHighlight()
        event.popup.remove()
      })
    })
  })
}

function drawClubs(L) {
  if (!map || !markerLayer) return

  markerLayer.clearLayers()

  filteredClubs.value.forEach((club) => {
    const isSelected = selectedClub.value?.id === club.id
    const marker = L.marker([club.lat, club.lng], {
      icon: clubIcon(L, isSelected),
      title: club.name,
    })
      .bindPopup(createClubPopup(club), {
        maxWidth: 320,
        minWidth: 270,
        closeButton: true,
      })
      .addTo(markerLayer)

    marker.on('click', () => {
      selectedClub.value = club
      selectedCourt.value = null
      clearCourtSelection()
      refreshMarkerHighlight()
    })

    attachPopupCourtHandlers(L, club, marker)
    club._marker = marker
  })
}

function escapeHtml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function centerOnBangalore() {
  if (!map) return
  map.setView([12.9716, 77.5946], 12, { animate: true })
}

function fitMap() {
  if (!map) return

  if (activeRoute.value?.coordinates?.length) {
    map.fitBounds(activeRoute.value.coordinates, { padding: [60, 60], animate: true })
    return
  }

  const points = []

  if (userLocation.value) {
    points.push([userLocation.value.lat, userLocation.value.lng])
  }

  filteredClubs.value.forEach((club) => {
    if (Number.isFinite(club.lat) && Number.isFinite(club.lng)) {
      points.push([club.lat, club.lng])
    }
  })

  if (points.length === 1) {
    map.setView(points[0], 14, { animate: true })
  } else if (points.length > 1) {
    map.fitBounds(points, {
      padding: [45, 45],
      maxZoom: 15,
      animate: true,
    })
  } else {
    centerOnBangalore()
  }
}

function focusClub(club) {
  if (!map || !club) return

  selectedClub.value = club
  selectedCourt.value = null
  clearCourtSelection()
  refreshMarkerHighlight()

  map.setView([club.lat, club.lng], 16, { animate: true })
  club._marker?.openPopup()
}

function clearCourtSelection() {
  if (courtLayer) courtLayer.clearLayers()
  if (routeLayer && !activeRoute.value) routeLayer.clearLayers()
}

function courtDisplayPoint(club, court, index) {
  if (Number.isFinite(Number(court.latitude)) && Number.isFinite(Number(court.longitude))) {
    return {
      lat: Number(court.latitude),
      lng: Number(court.longitude),
      approximate: false,
    }
  }

  const positions = [
    [0.00035, 0],
    [0, 0.00042],
    [-0.00035, 0],
    [0, -0.00042],
    [0.00025, 0.00032],
    [-0.00025, -0.00032],
    [0.00025, -0.00032],
    [-0.00025, 0.00032],
  ]

  const [latOffset, lngOffset] = positions[index % positions.length]

  return {
    lat: club.lat + latOffset,
    lng: club.lng + lngOffset,
    approximate: true,
  }
}

async function selectCourt(club, court) {
  if (!map || !club || !court) return

  selectedClub.value = club
  selectedCourt.value = court

  const index = club.courts?.findIndex((item) => Number(item.id) === Number(court.id)) ?? 0
  const point = courtDisplayPoint(club, court, Math.max(index, 0))

  const L = await loadLeaflet()
  drawSelectedCourt(L, point, club, court)

  map.setView([point.lat, point.lng], 17, { animate: true })
}

function drawSelectedCourt(L, point, club, court) {
  if (!map || !courtLayer || !routeLayer) return

  courtLayer.clearLayers()
  if (!activeRoute.value) {
    routeLayer.clearLayers()

    const line = L.polyline(
      [
        [club.lat, club.lng],
        [point.lat, point.lng],
      ],
      {
        color: '#4f46e5',
        weight: 4,
        opacity: 0.9,
        dashArray: '7 7',
        lineCap: 'round',
      },
    ).addTo(routeLayer)

    line.bindTooltip(point.approximate ? 'Court location inside club premises' : 'Route to court', {
      sticky: true,
      direction: 'center',
    })
  }

  const marker = L.marker([point.lat, point.lng], {
    icon: courtIcon(L, court.sport_type),
    title: court.name,
    zIndexOffset: 1000,
  })
    .bindPopup(
      `
      <div style="min-width:200px">
        <div style="font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:#4f46e5">
          ${escapeHtml(displaySport(court.sport_type))}
        </div>
        <strong style="display:block;margin-top:3px;font-size:14px;color:#0f172a">
          ${escapeHtml(court.name)}
        </strong>
        <div style="margin-top:4px;font-size:11px;color:#64748b">
          ${escapeHtml(club.name)}
        </div>
      </div>
    `,
    )
    .addTo(courtLayer)

  marker.openPopup()
}

// =========================================================
// FULLSCREEN TOGGLE
// =========================================================
function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
  nextTick(() => {
    if (map) {
      map.invalidateSize()
      setTimeout(() => map.invalidateSize(), 300)
    }
  })
}

// =========================================================
// DATA LOADING (BACKEND API + REAL BENGALURU VENUES)
// =========================================================
async function loadClubData() {
  let backendClubs = []

  try {
    const response = await api.get('/clubs')
    const rawClubs = Array.isArray(response.data) ? response.data : []

    for (const club of rawClubs) {
      let courts = []
      try {
        const courtResponse = await api.get(`/clubs/${club.id}/courts`)
        courts = Array.isArray(courtResponse.data)
          ? courtResponse.data.filter((c) => c.is_active !== false)
          : []
      } catch {
        courts = []
      }

      let point = null
      if (Number.isFinite(Number(club.latitude)) && Number.isFinite(Number(club.longitude))) {
        point = { lat: Number(club.latitude), lng: Number(club.longitude) }
      } else {
        try {
          point = await geocodeClubAddress(club.address || club.name)
        } catch {
          point = null
        }
      }

      backendClubs.push({
        ...club,
        courts,
        lat: point?.lat,
        lng: point?.lng,
      })
    }
  } catch (err) {
    console.warn('Backend /clubs not reachable, using Bengaluru venues network:', err)
  }

  // Merge real Bengaluru venues with any backend clubs (preventing duplicates)
  const combined = [...backendClubs]
  for (const bVenue of REAL_BANGALORE_CLUBS) {
    if (!combined.some((c) => c.name?.toLowerCase() === bVenue.name.toLowerCase())) {
      combined.push(bVenue)
    }
  }

  clubs.value = combined
}

async function locateMember(showErrorOnDeny = true) {
  locating.value = true
  if (showErrorOnDeny) error.value = ''

  try {
    const position = await getCurrentPosition({ timeout: 12000 })

    userLocation.value = {
      lat: position.coords.latitude,
      lng: position.coords.longitude,
      accuracy: position.coords.accuracy,
    }

    clubs.value = clubs.value.map((club) => ({
      ...club,
      distanceKm:
        Number.isFinite(club.lat) && Number.isFinite(club.lng)
          ? distanceInKm(userLocation.value.lat, userLocation.value.lng, club.lat, club.lng)
          : null,
    }))

    const L = await loadLeaflet()
    drawUserLocation(L)
    drawClubs(L)
    fitMap()
  } catch (locationError) {
    const code = locationError?.code
    if (code === 1) {
      if (showErrorOnDeny) {
        error.value =
          'Location permission was denied. You can still search and filter all Bengaluru clubs manually or grant permission in your browser address bar.'
      }
    } else if (code === 3) {
      if (showErrorOnDeny) {
        error.value = 'Location lookup timed out. Defaulting to Bengaluru center.'
      }
    } else if (showErrorOnDeny) {
      error.value = locationError?.message || 'Unable to detect current GPS location.'
    }
  } finally {
    locating.value = false
  }
}

async function initialize() {
  loading.value = true
  error.value = ''

  try {
    const L = await loadLeaflet()
    await nextTick()
    createMap(L)
    await loadClubData()
    drawClubs(L)
    fitMap()
  } catch (loadError) {
    error.value = loadError?.message || 'Unable to initialize Bengaluru map.'
  } finally {
    loading.value = false
  }

  // Actively ask for browser location permission on load
  await locateMember(false)
}

onMounted(initialize)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
.nearby-map {
  height: min(65vh, 640px);
  min-height: 460px;
  width: 100%;
  background: #e2e8f0;
}

.nearby-map-fullscreen {
  height: calc(100vh - 120px) !important;
  min-height: 500px;
}

.fullscreen-map-wrapper {
  position: fixed;
  inset: 12px;
  z-index: 9999;
  background: #ffffff;
  border-radius: 20px;
  padding: 12px;
  box-shadow: 0 25px 60px rgba(15, 23, 42, 0.35);
}

.map-control-btn {
  display: flex;
  width: 36px;
  height: 36px;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: #ffffff;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
  transition: all 160ms ease;
  cursor: pointer;
}

.map-control-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.legend-dot {
  display: inline-block;
  width: 9px;
  height: 9px;
  border-radius: 999px;
}

/* Filter controls */
.filter-search-input {
  height: 42px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  font-size: 13px;
  color: #1e293b;
  outline: none;
  transition: all 160ms ease;
}

.filter-search-input:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

.filter-select-input {
  height: 42px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: #f8fafc;
  padding: 0 12px;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  outline: none;
  transition: all 160ms ease;
}

.filter-select-input:focus {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

/* Sport pills */
.sport-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #475569;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  transition: all 150ms ease;
  cursor: pointer;
}

.sport-pill:hover {
  border-color: #c7d2fe;
  background: #eef2ff;
  color: #4338ca;
}

.sport-pill-active {
  border-color: #4f46e5;
  background: #4f46e5;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

.sport-pill-count {
  padding: 1px 6px;
  border-radius: 999px;
  background: #e2e8f0;
  color: #475569;
  font-size: 10px;
  font-weight: 700;
}

.sport-pill-count-active {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

/* Club list cards in sidebar */
.club-list-card {
  padding: 12px;
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  cursor: pointer;
  transition: all 160ms ease;
}

.club-list-card:hover {
  border-color: #a5b4fc;
  background: #f8faff;
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}

.club-list-card-active {
  border-color: #6366f1 !important;
  background: #eef2ff !important;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}

.club-sport-tag {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 2px 7px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
  font-size: 10px;
  font-weight: 600;
}

/* Court items inside selected club card */
.court-card-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
  background: #f8fafc;
  transition: all 150ms ease;
}

.court-card-item:hover {
  border-color: #c7d2fe;
  background: #eef2ff;
}

.court-card-selected {
  border-color: #818cf8;
  background: #e0e7ff;
}

.court-sport-icon {
  display: flex;
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: #e2e8f0;
  font-size: 17px;
}

/* Leaflet DivIcons */
:deep(.club-map-icon-wrapper),
:deep(.court-map-icon-wrapper) {
  background: transparent;
  border: 0;
}

:deep(.club-map-icon) {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border: 3px solid #ffffff;
  border-radius: 999px;
  background: linear-gradient(135deg, #4f46e5, #4338ca);
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
  font-size: 22px;
  color: #ffffff;
  transition: transform 150ms ease;
}

:deep(.club-map-icon:hover) {
  transform: scale(1.08);
}

:deep(.club-map-icon-active) {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  box-shadow:
    0 0 0 4px rgba(59, 130, 246, 0.3),
    0 8px 25px rgba(29, 78, 216, 0.5);
}

:deep(.court-map-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 3px solid #ffffff;
  border-radius: 999px;
  background: linear-gradient(135deg, #059669, #047857);
  box-shadow: 0 7px 18px rgba(5, 150, 105, 0.35);
  font-size: 20px;
}

:deep(.pulse-ring) {
  position: absolute;
  inset: -6px;
  border-radius: 999px;
  border: 2px solid #6366f1;
  animation: mapPulse 2s cubic-bezier(0.24, 0, 0.38, 1) infinite;
}

@keyframes mapPulse {
  0% {
    transform: scale(0.9);
    opacity: 0.9;
  }
  70% {
    transform: scale(1.5);
    opacity: 0;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

/* Map Popups */
:deep(.map-club-popup) {
  min-width: 250px;
  padding: 4px 2px;
}

:deep(.map-popup-kicker) {
  color: #4f46e5;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

:deep(.map-popup-badge) {
  font-size: 10px;
  font-weight: 700;
  color: #059669;
  background: #ecfdf5;
  padding: 1px 6px;
  border-radius: 6px;
}

:deep(.map-popup-title) {
  display: block;
  margin-top: 2px;
  color: #0f172a;
  font-size: 15px;
  font-weight: 800;
}

:deep(.map-popup-address) {
  margin-top: 3px;
  color: #64748b;
  font-size: 11px;
  line-height: 1.4;
}

:deep(.map-popup-section-title) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  margin-bottom: 5px;
  color: #0f172a;
  font-size: 11px;
  font-weight: 800;
}

:deep(.map-popup-section-title span) {
  color: #4f46e5;
  background: #eef2ff;
  padding: 1px 5px;
  border-radius: 4px;
}

:deep(.map-court-list) {
  display: grid;
  gap: 4px;
}

:deep(.map-court-row-wrapper) {
  display: flex;
  align-items: center;
  gap: 4px;
}

:deep(.map-court-row) {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 7px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
  padding: 5px 7px;
  text-align: left;
  cursor: pointer;
  transition: all 140ms ease;
}

:deep(.map-court-row:hover) {
  border-color: #a5b4fc;
  background: #eef2ff;
}

:deep(.map-court-icon) {
  display: flex;
  width: 24px;
  height: 24px;
  flex: 0 0 24px;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #ffffff;
  font-size: 13px;
}

:deep(.map-court-copy) {
  min-width: 0;
  flex: 1;
}

:deep(.map-court-copy strong) {
  display: block;
  overflow: hidden;
  color: #1e293b;
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.map-court-copy small) {
  display: block;
  color: #94a3b8;
  font-size: 9px;
}

:deep(.map-court-book-btn) {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 9px;
  border-radius: 8px;
  background: #4f46e5;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: background 140ms ease;
}

:deep(.map-court-book-btn:hover) {
  background: #4338ca;
}

:deep(.map-popup-actions) {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
}

:deep(.map-popup-btn-route) {
  flex: 1;
  padding: 6px 10px;
  border-radius: 8px;
  background: #4f46e5;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  text-align: center;
  border: none;
  cursor: pointer;
  transition: all 140ms ease;
}

:deep(.map-popup-btn-route:hover) {
  background: #4338ca;
}

:deep(.map-popup-btn-full) {
  flex: 1;
  padding: 6px 10px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #4338ca;
  font-size: 10px;
  font-weight: 700;
  text-align: center;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 140ms ease;
}

:deep(.map-popup-btn-full:hover) {
  background: #eef2ff;
  border-color: #c7d2fe;
}

:deep(.map-empty) {
  margin: 0;
  color: #94a3b8;
  font-size: 11px;
}

/* Base custom classes */
.btn-primary {
  background: linear-gradient(135deg, #4f46e5, #4338ca);
  color: #ffffff;
  border: 1px solid #4338ca;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
  transition: all 160ms ease;
  cursor: pointer;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #4338ca, #3730a3);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #ffffff;
  color: #334155;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
  transition: all 160ms ease;
  cursor: pointer;
}

.btn-secondary:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #0f172a;
}

/* Glass panel */
.glass {
  background: #ffffff;
  border: 1px solid #e2e8f0;
}

@media (max-width: 1023px) {
  .nearby-map {
    height: 52vh;
    min-height: 380px;
  }
}
</style>
