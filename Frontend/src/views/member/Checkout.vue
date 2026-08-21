<template>
  <div class="member-page">
    <div class="page-head">
      <div>
        <p class="kicker">Secure checkout</p>
        <h1 class="title">Complete Payment</h1>
        <p class="muted">Your payment is processed securely by Stripe.</p>
      </div>
      <button class="btn btn-soft" type="button" @click="router.back()">Back</button>
    </div>

    <div v-if="loading" class="panel p-10 text-center text-slate-500">
      Preparing secure checkout...
    </div>

    <div v-else-if="success" class="panel success-panel p-8 text-center sm:p-12">
      <div class="success-icon">✓</div>
      <p class="kicker mt-5">Payment successful</p>
      <h2 class="mt-2 text-3xl font-extrabold tracking-tight text-slate-900">You're all set</h2>
      <p class="mx-auto mt-3 max-w-lg text-sm leading-6 text-slate-500">{{ successMessage }}</p>
      <div class="mt-7 flex flex-col justify-center gap-3 sm:flex-row">
        <router-link
          v-if="paymentType === 'membership'"
          to="/member/membership"
          class="btn btn-primary"
          >View Membership</router-link
        >
        <router-link v-else-if="paymentType === 'event'" to="/member/events" class="btn btn-primary"
          >View Events</router-link
        >
        <router-link v-else to="/member/my-bookings" class="btn btn-primary"
          >View My Bookings</router-link
        >
      </div>
    </div>

    <div v-else-if="error" class="panel p-6">
      <div class="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
        {{ error }}
      </div>
      <button class="btn btn-soft mt-4" @click="prepare">Try again</button>
    </div>

    <div v-else class="grid gap-5 lg:grid-cols-[.8fr_1.2fr]">
      <aside class="panel p-6 sm:p-7">
        <p class="kicker">Order summary</p>
        <h2 class="mt-2 text-xl font-extrabold text-slate-900">{{ summary.title }}</h2>
        <p class="mt-2 text-sm leading-6 text-slate-500">{{ summary.description }}</p>

        <div class="mt-7 space-y-3 border-t border-slate-100 pt-5">
          <div class="flex justify-between gap-4 text-sm">
            <span class="text-slate-500">Amount</span>
            <strong class="text-slate-900">{{ currency(amount) }}</strong>
          </div>
          <div class="flex justify-between gap-4 text-sm">
            <span class="text-slate-500">Currency</span>
            <strong class="uppercase text-slate-900">{{ currencyCode }}</strong>
          </div>
          <div class="flex justify-between gap-4 border-t border-slate-100 pt-4">
            <span class="font-bold text-slate-700">Total</span>
            <strong class="text-xl text-slate-900">{{ currency(amount) }}</strong>
          </div>
        </div>

        <div
          v-if="paymentType === 'membership'"
          class="mt-6 rounded-2xl border border-indigo-100 bg-indigo-50/60 p-4"
        >
          <label class="flex cursor-pointer items-start gap-3">
            <input v-model="autoRenew" type="checkbox" class="mt-1 h-4 w-4 accent-indigo-600" />
            <span>
              <span class="block text-sm font-bold text-indigo-950">Enable auto-renewal</span>
              <span class="mt-1 block text-xs leading-5 text-indigo-700"
                >Your preference will be saved with the membership.</span
              >
            </span>
          </label>
        </div>
      </aside>

      <section class="panel p-6 sm:p-7">
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="kicker">Payment method</p>
            <h2 class="mt-2 text-xl font-extrabold text-slate-900">Card & supported methods</h2>
          </div>
          <div class="stripe-badge">stripe</div>
        </div>

        <div
          v-if="stripeError"
          class="mt-5 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
        >
          {{ stripeError }}
        </div>

        <div class="mt-6 rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
          <div id="payment-element"></div>
        </div>

        <button
          class="btn btn-primary mt-5 w-full"
          :disabled="processing || !paymentElementReady"
          @click="pay"
        >
          {{ processing ? 'Processing payment...' : `Pay ${currency(amount)}` }}
        </button>

        <p class="mt-4 text-center text-xs leading-5 text-slate-400">
          Your card details are collected by Stripe and are never sent to ClubDash.
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const stripeError = ref('')
const processing = ref(false)
const paymentElementReady = ref(false)
const success = ref(false)
const successMessage = ref('')
const amount = ref(0)
const currencyCode = ref('inr')
const autoRenew = ref(false)
const summary = ref({ title: 'Payment', description: 'Secure payment for your ClubDash service.' })

let stripe = null
let elements = null
let paymentElement = null
let paymentId = null

const paymentType = computed(() => String(route.query.payment_type || '').toLowerCase())
const referenceId = computed(() => String(route.query.reference_id || ''))

function currency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: currencyCode.value.toUpperCase(),
    maximumFractionDigits: 2,
  }).format(Number(value || 0))
}

function loadStripeJs() {
  if (window.Stripe) return Promise.resolve(window.Stripe)
  return new Promise((resolve, reject) => {
    const existing = document.querySelector('script[data-clubdash-stripe]')
    if (existing) {
      existing.addEventListener('load', () => resolve(window.Stripe))
      existing.addEventListener('error', reject)
      return
    }
    const script = document.createElement('script')
    script.src = 'https://js.stripe.com/v3/'
    script.async = true
    script.dataset.clubdashStripe = 'true'
    script.onload = () => resolve(window.Stripe)
    script.onerror = () => reject(new Error('Unable to load Stripe.js.'))
    document.head.appendChild(script)
  })
}

async function loadReference() {
  if (!referenceId.value || !['membership', 'event', 'booking'].includes(paymentType.value)) {
    throw new Error('Invalid checkout request.')
  }

  if (paymentType.value === 'membership') {
    const { data } = await api.get('/memberships/plans')
    const plan = (Array.isArray(data) ? data : []).find(
      (item) => String(item.id) === referenceId.value,
    )
    if (!plan) throw new Error('Membership plan not found.')
    amount.value = Number(plan.price_monthly || 0)
    summary.value = {
      title: plan.name,
      description: parseBenefits(plan.benefits).join(' · ') || 'Monthly ClubDash membership',
    }
    return
  }

  if (paymentType.value === 'event') {
    const { data } = await api.get('/events')
    const event = (Array.isArray(data) ? data : []).find(
      (item) => String(item.id) === referenceId.value,
    )
    if (!event) throw new Error('Event not found.')
    amount.value = Number(event.registration_fee || 0)
    summary.value = {
      title: event.title,
      description: event.description || 'Event registration',
    }
    if (amount.value <= 0) throw new Error('This event does not require payment.')
    return
  }

  const { data } = await api.get('/bookings')
  const booking = (Array.isArray(data) ? data : []).find(
    (item) => String(item.id) === referenceId.value,
  )
  if (!booking) throw new Error('Booking not found.')
  amount.value = Number(booking.amount ?? booking.price ?? booking.total_amount ?? 0)
  summary.value = {
    title: booking.courtName || booking.court_name || `Booking #${booking.id}`,
    description: 'Court booking payment',
  }
}

function parseBenefits(value) {
  if (!value) return []
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

async function prepare() {
  loading.value = true
  error.value = ''
  stripeError.value = ''
  paymentElementReady.value = false
  try {
    await loadReference()

    const { data } = await api.post('/payments/stripe/create-payment-intent', {
      payment_type: paymentType.value,
      reference_id: Number(referenceId.value),
      currency: 'inr',
    })

    paymentId = data.payment_id
    amount.value = Number(data.amount)
    currencyCode.value = String(data.currency || 'inr').toLowerCase()

    const Stripe = await loadStripeJs()
    if (!data.publishable_key)
      throw new Error('Stripe publishable key was not returned by the backend.')

    stripe = Stripe(data.publishable_key)
    elements = stripe.elements({
      clientSecret: data.client_secret,
      appearance: {
        theme: 'stripe',
        variables: {
          colorPrimary: '#4f46e5',
          colorText: '#172033',
          borderRadius: '12px',
          fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
        },
      },
    })

    await nextTick()
    const mountPoint = document.getElementById('payment-element')
    if (!mountPoint) throw new Error('Payment form could not be mounted.')
    paymentElement?.destroy()
    paymentElement = elements.create('payment', { layout: 'tabs' })
    paymentElement.mount(mountPoint)
    paymentElement.on('ready', () => {
      paymentElementReady.value = true
    })
  } catch (err) {
    error.value = err?.response?.data?.message || err?.message || 'Unable to prepare payment.'
  } finally {
    loading.value = false
  }
}

async function pay() {
  if (!stripe || !elements || !paymentElement) return
  processing.value = true
  stripeError.value = ''
  try {
    const result = await stripe.confirmPayment({
      elements,
      redirect: 'if_required',
    })

    if (result.error) {
      stripeError.value = result.error.message || 'Payment could not be completed.'
      return
    }

    // The existing backend exposes subscription/event registration separately.
    // Complete those domain actions only after Stripe confirms the payment.
    if (paymentType.value === 'membership') {
      await api.post('/memberships/subscribe', {
        plan_id: Number(referenceId.value),
        auto_renew: autoRenew.value,
      })
      successMessage.value =
        'Your payment was confirmed and your membership subscription has been created.'
    } else if (paymentType.value === 'event') {
      await api.post(`/events/${referenceId.value}/register`)
      successMessage.value =
        'Your payment was confirmed and your event registration has been created.'
    } else {
      successMessage.value =
        'Your payment was confirmed successfully. The payment record will be updated by the Stripe webhook.'
    }

    success.value = true
  } catch (err) {
    stripeError.value =
      err?.response?.data?.message ||
      'Payment was successful, but the follow-up action could not be completed. Please check your account before retrying.'
  } finally {
    processing.value = false
  }
}

onMounted(prepare)

onBeforeUnmount(() => {
  paymentElement?.destroy()
  paymentElement = null
})
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
  margin-bottom: 24px;
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
.panel {
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #dfe7f1;
  border-radius: 20px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.06);
}
.stripe-badge {
  border-radius: 999px;
  background: #635bff;
  color: #fff;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.03em;
}
.success-panel {
  min-height: 430px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.success-icon {
  display: grid;
  height: 72px;
  width: 72px;
  place-items: center;
  border-radius: 50%;
  background: #ecfdf5;
  color: #059669;
  font-size: 34px;
  font-weight: 900;
  box-shadow: 0 0 0 10px #f0fdf4;
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
  color: #fff;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
</style>
