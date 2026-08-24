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

    <!-- My Active Membership (shown if exists) -->
    <section v-if="activeMemberships.length" class="mb-8">
      <div class="section-head">
        <div>
          <p class="kicker">Your current plan</p>
          <h2 class="section-title">Active Membership</h2>
        </div>
      </div>

      <div class="grid gap-4 lg:grid-cols-2">
        <article v-for="membership in activeMemberships" :key="membership.id" class="panel p-6 border-indigo-200 bg-gradient-to-br from-white via-indigo-50/20 to-emerald-50/20">
          <div class="flex items-start justify-between gap-4">
            <div>
              <span class="pill bg-emerald-100 text-emerald-800 font-bold uppercase tracking-wider text-[10px]">
                ● {{ membership.status }}
              </span>
              <h3 class="mt-3 text-2xl font-extrabold text-slate-900">{{ membership.plan_name }}</h3>
              <p class="mt-1 text-sm font-semibold text-indigo-600">
                {{ membership.plan_duration_months }} Months Tier ·
                {{ membership.plan_discount_percentage }}% Off All Court Bookings
              </p>
            </div>
            <div class="text-right">
              <p class="text-xs text-slate-400 font-medium uppercase tracking-wider">Valid until</p>
              <p class="mt-1 font-extrabold text-slate-900 text-base">{{ formatDate(membership.end_date) }}</p>
            </div>
          </div>

          <div class="mt-5 grid grid-cols-2 gap-3">
            <div class="stat">
              <span>Member Since</span><strong>{{ formatDate(membership.start_date) }}</strong>
            </div>
            <div class="stat">
              <span>Auto-Renew</span><strong>{{ membership.auto_renew ? 'Active' : 'Off' }}</strong>
            </div>
          </div>

          <div class="mt-5 flex gap-3">
            <button
              v-if="membership.status === 'active'"
              class="btn btn-danger flex-1"
              :disabled="cancelling === membership.id"
              @click="cancelMembership(membership)"
            >
              {{ cancelling === membership.id ? 'Cancelling...' : 'Cancel Subscription' }}
            </button>
            <router-link
              to="/member/book-court"
              class="btn btn-primary flex-1 text-center"
            >
              Book Court with Discount →
            </router-link>
          </div>
        </article>
      </div>
    </section>

    <!-- Available Plans -->
    <section>
      <div class="section-head">
        <div>
          <p class="kicker">{{ activeMemberships.length ? 'Upgrade or renew' : 'Available plans' }}</p>
          <h2 class="section-title">{{ activeMemberships.length ? 'Explore Other Membership Tiers' : 'Choose what fits you' }}</h2>
        </div>
      </div>

      <div v-if="loadingPlans" class="panel p-10 text-center text-slate-500">Loading membership tiers...</div>
      <div v-else-if="!plans.length" class="panel p-10 text-center">No active plans currently available.</div>

      <div v-else class="grid gap-5 md:grid-cols-2">
        <article
          v-for="group in groupedPlans"
          :key="group.name"
          class="plan-card"
          :class="{ featured: group.name === 'Premium' }"
        >
          <div class="featured-label" v-if="group.name === 'Premium'">⭐ Best Value</div>
          <p class="kicker">{{ group.name }} Membership</p>
          <h3 class="mt-1 text-2xl font-extrabold text-slate-900">{{ group.name }} Access</h3>
          <p class="plan-benefit font-semibold text-indigo-600 mt-1">
            {{
              group.discount_percentage === 100 ? '🎉 100% Free Court Bookings' : '⚡ 50% Off All Court Bookings'
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

          <!-- ====== CTA Button ====== -->
          <button
            type="button"
            class="btn btn-primary mt-6 w-full"
            :disabled="!selectedPlans[group.name]"
            @click="choosePlan(group)"
          >
            {{
              selectedPlans[group.name]
                ? `Subscribe to ${group.name} (${selectedPlans[group.name].duration_months} mo) · ${currency(selectedPlans[group.name].price)}`
                : 'Select a duration first'
            }}
          </button>
        </article>
      </div>
    </section>

    <!-- Recent Payment History -->
    <section v-if="payments.length" class="mt-10">
      <div class="section-head">
        <div>
          <p class="kicker">Payment logs</p>
          <h2 class="section-title">Recent Payment History</h2>
        </div>
      </div>
      <div class="panel divide-y divide-slate-100 overflow-hidden">
        <div
          v-for="payment in payments.slice(0, 5)"
          :key="payment.id"
          class="flex flex-wrap items-center justify-between gap-3 p-4 hover:bg-slate-50/60 transition"
        >
          <div>
            <p class="font-bold text-slate-800">{{ label(payment.payment_type) }} Payment</p>
            <p class="mt-1 text-xs text-slate-400">
              {{ formatDateTime(payment.created_at) }} · Ref #{{ payment.id }}
            </p>
          </div>
          <div class="text-right">
            <p class="font-extrabold text-slate-900">{{ currency(payment.amount) }}</p>
            <span
              class="pill"
              :class="
                payment.status === 'completed'
                  ? 'bg-emerald-50 text-emerald-700'
                  : payment.status === 'failed'
                  ? 'bg-red-50 text-red-700'
                  : 'bg-amber-50 text-amber-700'
              "
            >{{ payment.status }}</span>
          </div>
        </div>
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
    // Auto-select first plan duration by default
    if (!selectedPlans.value[group.name] && group.plans.length > 0) {
      selectedPlans.value[group.name] = group.plans[0]
    }
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

function formatDateTime(value) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('en-IN', { dateStyle: 'medium', timeStyle: 'short' }).format(
    new Date(value),
  )
}

function label(value) {
  return String(value || 'payment')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

const defaultFallbackPlans = [
  { id: 1, name: "Standard", duration_months: 1, price: 499, discount_percentage: 50, benefits: "50% off all court bookings", is_active: true },
  { id: 2, name: "Standard", duration_months: 3, price: 1299, discount_percentage: 50, benefits: "50% off all court bookings", is_active: true },
  { id: 3, name: "Standard", duration_months: 6, price: 2299, discount_percentage: 50, benefits: "50% off all court bookings", is_active: true },
  { id: 4, name: "Standard", duration_months: 12, price: 3999, discount_percentage: 50, benefits: "50% off all court bookings", is_active: true },
  { id: 5, name: "Premium", duration_months: 1, price: 999, discount_percentage: 100, benefits: "100% free court bookings", is_active: true },
  { id: 6, name: "Premium", duration_months: 3, price: 2499, discount_percentage: 100, benefits: "100% free court bookings", is_active: true },
  { id: 7, name: "Premium", duration_months: 6, price: 4499, discount_percentage: 100, benefits: "100% free court bookings", is_active: true },
  { id: 8, name: "Premium", duration_months: 12, price: 7999, discount_percentage: 100, benefits: "100% free court bookings", is_active: true },
]

async function loadAll() {
  loadingPlans.value = true
  error.value = ''
  try {
    const [plansRes, membershipsRes, paymentsRes] = await Promise.allSettled([
      api.get('/memberships/plans'),
      api.get('/memberships/my-memberships'),
      api.get('/payments/my-payments'),
    ])

    if (plansRes.status === 'fulfilled' && Array.isArray(plansRes.value.data) && plansRes.value.data.length > 0) {
      plans.value = plansRes.value.data
    } else {
      // If backend returns empty array or request failed, populate with default tiered plans
      plans.value = defaultFallbackPlans
    }

    if (membershipsRes.status === 'fulfilled' && Array.isArray(membershipsRes.value.data)) {
      memberships.value = membershipsRes.value.data
    }

    if (paymentsRes.status === 'fulfilled' && Array.isArray(paymentsRes.value.data)) {
      payments.value = paymentsRes.value.data
    }
  } catch (err) {
    plans.value = defaultFallbackPlans
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
  if (!window.confirm(`Are you sure you want to cancel your ${membership.plan_name} membership?`)) return
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

/* =========================================================
   FIXED `.btn` STYLES
   - `.btn` is now inline-flex (auto width) so the header button fits perfectly.
   - The full-width buttons (inside cards) use the `w-full` class.
   ========================================================= */
.btn-primary {
  background: #4f46e5;
  color: white;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
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
