<template>
  <div class="member-page">
    <div class="page-head">
      <div>
        <p class="kicker">Membership</p>
        <h1 class="title">Plans & Membership</h1>
        <p class="muted">Choose a plan, manage your active membership, and review payments.</p>
      </div>
      <button class="btn btn-soft" type="button" @click="loadAll">Refresh</button>
    </div>

    <div v-if="error" class="panel mb-5 border-red-200 bg-red-50 p-4 text-sm text-red-700">
      {{ error }}
    </div>

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

    <section>
      <div class="section-head">
        <div>
          <p class="kicker">Available plans</p>
          <h2 class="section-title">Choose what fits you</h2>
        </div>
      </div>

      <div v-if="loadingPlans" class="panel p-10 text-center text-slate-500">
        Loading membership plans...
      </div>

      <div v-else-if="!plans.length" class="panel p-10 text-center">
        <p class="font-bold text-slate-800">No active membership plans are available.</p>
        <p class="mt-2 text-sm text-slate-500">Please check again later or contact the club.</p>
      </div>

      <div v-else class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        <article
          v-for="(plan, index) in plans"
          :key="plan.id"
          class="plan-card"
          :class="{ featured: index === 1 }"
        >
          <div v-if="index === 1" class="featured-label">Popular</div>
          <p class="kicker">{{ plan.club_id ? `Club #${plan.club_id}` : 'Club membership' }}</p>
          <h3 class="mt-2 text-xl font-extrabold text-slate-900">{{ plan.name }}</h3>
          <div class="mt-5 flex items-end gap-1">
            <span class="text-3xl font-black tracking-tight text-slate-900">{{
              currency(plan.price_monthly)
            }}</span>
            <span class="pb-1 text-sm text-slate-400">/ month</span>
          </div>

          <ul class="mt-6 space-y-3">
            <li
              v-for="benefit in benefits(plan.benefits)"
              :key="benefit"
              class="flex gap-2 text-sm text-slate-600"
            >
              <span
                class="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded-full bg-emerald-50 text-emerald-600"
                >✓</span
              >
              <span>{{ benefit }}</span>
            </li>
          </ul>

          <button class="btn btn-primary mt-7 w-full" @click="choosePlan(plan)">
            Choose {{ plan.name }}
          </button>
        </article>
      </div>
    </section>

    <section v-if="payments.length" class="mt-8">
      <div class="section-head">
        <div>
          <p class="kicker">Payments</p>
          <h2 class="section-title">Recent payment history</h2>
        </div>
      </div>
      <div class="panel divide-y divide-slate-100">
        <div
          v-for="payment in payments.slice(0, 5)"
          :key="payment.id"
          class="flex flex-wrap items-center justify-between gap-3 p-4"
        >
          <div>
            <p class="font-bold text-slate-800">{{ label(payment.payment_type) }}</p>
            <p class="mt-1 text-xs text-slate-400">
              {{ formatDateTime(payment.created_at) }} · #{{ payment.id }}
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
              >{{ payment.status }}</span
            >
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

const activeMemberships = computed(() => memberships.value.filter((m) => m.status === 'active'))

function currency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(Number(value || 0))
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

function benefits(value) {
  if (!value) return ['Club membership access']
  if (Array.isArray(value)) return value
  try {
    const parsed = JSON.parse(value)
    if (Array.isArray(parsed)) return parsed
  } catch {}
  return String(value)
    .split(/\r?\n|•|,/)
    .map((x) => x.trim())
    .filter(Boolean)
}

function label(value) {
  return String(value || 'payment')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

function choosePlan(plan) {
  router.push({
    name: 'member-checkout',
    query: { payment_type: 'membership', reference_id: String(plan.id) },
  })
}

async function loadAll() {
  loadingPlans.value = true
  error.value = ''
  try {
    const [plansResponse, membershipsResponse, paymentsResponse] = await Promise.all([
      api.get('/memberships/plans'),
      api.get('/memberships/my-memberships'),
      api.get('/payments/my-payments'),
    ])
    plans.value = Array.isArray(plansResponse.data) ? plansResponse.data : []
    memberships.value = Array.isArray(membershipsResponse.data) ? membershipsResponse.data : []
    payments.value = Array.isArray(paymentsResponse.data) ? paymentsResponse.data : []
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to load membership information.'
  } finally {
    loadingPlans.value = false
  }
}

async function cancelMembership(membership) {
  if (!window.confirm(`Cancel ${membership.plan_name}?`)) return
  cancelling.value = membership.id
  error.value = ''
  try {
    await api.post(`/memberships/${membership.id}/cancel`)
    await loadAll()
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to cancel membership.'
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
.btn {
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
</style>
