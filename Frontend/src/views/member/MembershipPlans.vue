<template>
  <div class="member-page">
    <div class="page-head">
      <div>
        <p class="kicker">Membership</p>
        <h1 class="title">Plans & Membership</h1>
        <p class="muted">Choose a plan and duration, unlock court discounts.</p>
      </div>
      <button class="btn btn-soft" @click="loadAll">Refresh</button>
    </div>

    <div v-if="error" class="panel mb-5 border-red-200 bg-red-50 p-4 text-sm text-red-700">
      {{ error }}
    </div>

    <!-- My Active Membership (shown only if exists) -->
    <section v-if="activeMemberships.length" class="mb-7">
      <div class="section-head">
        <div>
          <p class="kicker">Your membership</p>
          <h2 class="section-title">Active & recent memberships</h2>
        </div>
      </div>

      <div class="grid gap-4 lg:grid-cols-2">
        <article v-for="membership in activeMemberships" :key="membership.id" class="panel p-6">
          <div class="flex items-start justify-between gap-4">
            <div>
              <span class="pill bg-emerald-50 text-emerald-700">{{ membership.status }}</span>
              <h3 class="mt-3 text-xl font-extrabold text-slate-900">{{ membership.plan_name }}</h3>
              <p class="mt-1 text-sm text-slate-500">
                {{ membership.plan_duration_months }} months ·
                {{ membership.plan_discount_percentage }}% off
              </p>
            </div>
            <div class="text-right">
              <p class="text-xs text-slate-400">Valid until</p>
              <p class="mt-1 font-bold text-slate-800">{{ formatDate(membership.end_date) }}</p>
            </div>
          </div>

          <div class="mt-5 grid grid-cols-2 gap-3">
            <div class="stat">
              <span>Started</span><strong>{{ formatDate(membership.start_date) }}</strong>
            </div>
            <div class="stat">
              <span>Auto-renew</span><strong>{{ membership.auto_renew ? 'On' : 'Off' }}</strong>
            </div>
          </div>

          <button
            v-if="membership.status === 'active'"
            class="btn btn-danger mt-5 w-full"
            :disabled="cancelling === membership.id"
            @click="cancelMembership(membership)"
          >
            {{ cancelling === membership.id ? 'Cancelling...' : 'Cancel Membership' }}
          </button>
        </article>
      </div>
    </section>

    <!-- Available Plans (shown only if no active membership) -->
    <section v-else>
      <div class="section-head">
        <div>
          <p class="kicker">Available plans</p>
          <h2 class="section-title">Choose what fits you</h2>
        </div>
      </div>

      <div v-if="loadingPlans" class="panel p-10 text-center text-slate-500">Loading plans...</div>
      <div v-else-if="!plans.length" class="panel p-10 text-center">No active plans.</div>

      <div v-else class="grid gap-5 md:grid-cols-2">
        <article
          v-for="group in groupedPlans"
          :key="group.name"
          class="plan-card"
          :class="{ featured: group.name === 'Premium' }"
        >
          <div class="featured-label" v-if="group.name === 'Premium'">Best Value</div>
          <p class="kicker">{{ group.name }} Membership</p>
          <p class="plan-benefit">
            {{
              group.discount_percentage === 100 ? 'Free court bookings' : '50% off court bookings'
            }}
          </p>

          <!-- ====== Duration Selector ====== -->
          <div class="duration-grid mt-6">
            <button
              v-for="plan in group.plans"
              :key="plan.id"
              type="button"
              class="duration-btn"
              :class="{ 'duration-active': selectedPlans[group.name]?.id === plan.id }"
              @click="selectedPlans[group.name] = plan"
            >
              <span class="duration-months">{{ plan.duration_months }} mo</span>
              <span class="duration-price">{{ currency(plan.price) }}</span>
            </button>
          </div>

          <!-- ====== CTA Button (always a button, no layout shift) ====== -->
          <button
            type="button"
            class="btn btn-primary mt-6 w-full"
            :disabled="!selectedPlans[group.name]"
            @click="choosePlan(group)"
          >
            {{
              selectedPlans[group.name]
                ? `Choose ${group.name} · ${currency(selectedPlans[group.name].price)}`
                : 'Select a duration first'
            }}
          </button>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()
const plans = ref([])
const memberships = ref([])
const payments = ref([])
const loadingPlans = ref(true)
const error = ref('')
const cancelling = ref(null)

// Keyed by group name (e.g., "Standard", "Premium")
const selectedPlans = ref({})

const groupedPlans = computed(() => {
  const groups = {}
  for (const plan of plans.value) {
    if (!groups[plan.name]) {
      groups[plan.name] = {
        name: plan.name,
        discount_percentage: plan.discount_percentage,
        plans: [],
      }
    }
    groups[plan.name].plans.push(plan)
  }
  for (const group of Object.values(groups)) {
    group.plans.sort((a, b) => a.duration_months - b.duration_months)
  }
  return Object.values(groups)
})

const activeMemberships = computed(() => memberships.value.filter((m) => m.status === 'active'))

function currency(value) {
  return `₹\u00A0${Number(value).toLocaleString('en-IN')}`
}

function formatDate(value) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${value}T00:00:00`))
}

async function loadAll() {
  loadingPlans.value = true
  error.value = ''
  try {
    const [plansRes, membershipsRes, paymentsRes] = await Promise.all([
      api.get('/memberships/plans'),
      api.get('/memberships/my-memberships'),
      api.get('/payments/my-payments'),
    ])
    plans.value = Array.isArray(plansRes.data) ? plansRes.data : []
    memberships.value = Array.isArray(membershipsRes.data) ? membershipsRes.data : []
    payments.value = Array.isArray(paymentsRes.data) ? paymentsRes.data : []
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to load plans.'
  } finally {
    loadingPlans.value = false
  }
}

function choosePlan(group) {
  const plan = selectedPlans.value[group.name]
  if (!plan) return
  router.push({
    name: 'member-checkout',
    query: {
      payment_type: 'membership',
      reference_id: String(plan.id),
    },
  })
}

async function cancelMembership(membership) {
  if (!window.confirm(`Cancel ${membership.plan_name}?`)) return
  cancelling.value = membership.id
  error.value = ''
  try {
    await api.post(`/memberships/${membership.id}/cancel`)
    await loadAll()
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to cancel membership.'
  } finally {
    cancelling.value = null
  }
}

onMounted(loadAll)
</script>

<style scoped>
.member-page {
  max-width: 1180px;
  margin: 0 auto;
}
.page-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 28px;
}
.kicker {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #64748b;
}
.title {
  font-size: 30px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: #172033;
  margin-top: 4px;
}
.muted {
  color: #64748b;
  margin-top: 8px;
  font-size: 14px;
}
.section-head {
  margin-bottom: 15px;
}
.section-title {
  margin-top: 4px;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #172033;
}
.panel {
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #dfe7f1;
  border-radius: 20px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.06);
}
.plan-card {
  position: relative;
  background: #fff;
  border: 1px solid #dfe7f1;
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.06);
  transition: 0.2s;
}
.plan-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 42px rgba(51, 65, 85, 0.1);
}
.plan-card.featured {
  border-color: #818cf8;
  box-shadow: 0 18px 45px rgba(79, 70, 229, 0.13);
}
.featured-label {
  position: absolute;
  right: 18px;
  top: 18px;
  border-radius: 999px;
  background: #eef2ff;
  color: #4f46e5;
  padding: 6px 9px;
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.stat {
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 14px;
  padding: 12px;
}
.stat span {
  display: block;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
}
.stat strong {
  display: block;
  margin-top: 5px;
  font-size: 13px;
  color: #334155;
}
.pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 9px;
  font-size: 10px;
  font-weight: 800;
  text-transform: capitalize;
}

/* =========================================================
   FIXED `.btn` STYLES
   - `.btn` is now inline-flex (auto width) so the header button fits perfectly.
   - The full-width buttons (inside cards) use the `w-full` class.
   ========================================================= */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 11px;
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 800;
  transition: 0.2s;
}
.btn-primary {
  background: #4f46e5;
  color: white;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.btn-danger {
  background: #dc2626;
  color: #fff;
}
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

/* ====== Duration Grid: Flex row ====== */
.duration-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.duration-btn {
  flex: 1 1 auto;
  min-width: 70px;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #f8fafc;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.2rem;
  transition: all 0.15s ease;
}

.duration-btn:hover {
  border-color: #a5b4fc;
  background: #eef2ff;
}

.duration-active {
  border-color: #4f46e5 !important;
  background: #e0e7ff !important;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.15);
}

.duration-months {
  font-size: 0.85rem;
  font-weight: 700;
  color: #1e293b;
}

.duration-price {
  font-size: 0.8rem;
  color: #64748b;
}
</style>
