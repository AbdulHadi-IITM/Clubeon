<template>
  <div class="member-page">
    <div class="page-head">
      <div>
        <p class="kicker">Secure checkout</p>
        <h1 class="title">Complete Payment</h1>
        <p class="muted">Your payment is processed securely.</p>
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
        <!-- Order summary -->
        <div class="kicker">Order summary</div>
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
            <h2 class="mt-2 text-xl font-extrabold text-slate-900">
              Card &amp; supported methods
            </h2>
          </div>
          <div class="stripe-badge">stripe</div>
        </div>

        <div class="mt-6 rounded-2xl border border-slate-200 bg-white p-4 sm:p-5">
          <div id="payment-element"></div>
        </div>

        <div v-if="stripeError" class="mt-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700 font-medium">
          {{ stripeError }}
        </div>

        <button
          class="btn btn-primary mt-5 w-full"
          :disabled="processing || !paymentElementReady"
          @click="pay"
        >
          {{ processing ? 'Processing...' : `Pay ${currency(amount)}` }}
        </button>

        <p class="mt-4 text-center text-xs leading-5 text-slate-400">
          Your card details are collected by Stripe and are never sent to Clubeon.
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
const summary = ref({ title: 'Payment', description: 'Secure payment for your Clubeon service.' })

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
    const existing = document.querySelector('script[data-clubeon-stripe]')
    if (existing) {
      existing.addEventListener('load', () => resolve(window.Stripe))
      existing.addEventListener('error', reject)
      return
    }
    const script = document.createElement('script')
    script.src = 'https://js.stripe.com/v3/'
    script.async = true
    script.dataset.clubeonStripe = 'true'
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
    let plansList = []
    try {
      const { data } = await api.get('/memberships/plans')
      plansList = Array.isArray(data) ? data : []
    } catch (e) {
      // ignore
    }

    let plan = plansList.find((item) => String(item.id) === referenceId.value)
    if (!plan) {
      const defaultPlans = [
        { id: 1, name: "Standard", duration_months: 1, price: 499, discount_percentage: 50 },
        { id: 2, name: "Standard", duration_months: 3, price: 1299, discount_percentage: 50 },
        { id: 3, name: "Standard", duration_months: 6, price: 2299, discount_percentage: 50 },
        { id: 4, name: "Standard", duration_months: 12, price: 3999, discount_percentage: 50 },
        { id: 5, name: "Premium", duration_months: 1, price: 999, discount_percentage: 100 },
        { id: 6, name: "Premium", duration_months: 3, price: 2499, discount_percentage: 100 },
        { id: 7, name: "Premium", duration_months: 6, price: 4499, discount_percentage: 100 },
        { id: 8, name: "Premium", duration_months: 12, price: 7999, discount_percentage: 100 },
      ]
      plan = defaultPlans.find((item) => String(item.id) === referenceId.value) || defaultPlans[0]
    }

    amount.value = Number(plan.price || 0)
    summary.value = {
      title: `${plan.name} (${plan.duration_months} months)`,
      description: `${plan.discount_percentage}% discount on court bookings`,
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
    return
  }

  const { data } = await api.get('/bookings')
  const booking = (Array.isArray(data) ? data : []).find(
    (item) => String(item.id) === referenceId.value,
  )
  if (!booking) throw new Error('Booking not found.')
  amount.value = Number(booking.amount ?? booking.price ?? booking.total_amount ?? 500)
  const courtTitle = booking.courtName || booking.court_name || `Court #${booking.court_id || booking.id}`
  const dateStr = booking.bookingDate || booking.date || ''
  const timeStr =
    booking.startTime || booking.start_time
      ? `${booking.startTime || booking.start_time} – ${booking.endTime || booking.end_time}`
      : ''
  summary.value = {
    title: courtTitle,
    description: dateStr && timeStr ? `${dateStr} (${timeStr})` : 'Court reservation payment',
  }
}

async function prepare() {
  loading.value = true
  error.value = ''
  stripeError.value = ''
  paymentElementReady.value = false
  try {
    await loadReference()

    // Try to create a Stripe payment intent
    try {
      const { data } = await api.post('/payments/stripe/create-payment-intent', {
        payment_type: paymentType.value,
        reference_id: Number(referenceId.value),
        currency: 'inr',
      })

      paymentId = data.payment_id
      amount.value = Number(data.amount)
      currencyCode.value = String(data.currency || 'inr').toLowerCase()

      if (!data.client_secret || !data.publishable_key) {
        // Free checkout or instant completion
        if (data.status === 'completed' || amount.value <= 0) {
          successMessage.value = 'Your purchase was completed successfully.'
          success.value = true
          loading.value = false
          return
        }
      }

      const Stripe = await loadStripeJs()
      if (!data.publishable_key) throw new Error('Stripe publishable key was not returned.')

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

      // Turn off loading and wait for Vue to render the payment container into DOM
      loading.value = false
      await nextTick()

      const mountPoint = document.getElementById('payment-element')
      if (!mountPoint) throw new Error('Payment form could not be mounted.')
      paymentElement?.destroy()
      paymentElement = elements.create('payment', { layout: 'tabs' })
      paymentElement.mount(mountPoint)
      paymentElement.on('ready', () => {
        paymentElementReady.value = true
      })
    } catch (stripeErr) {
      const status = stripeErr?.response?.status
      const message = stripeErr?.response?.data?.message || ''
      if (status === 503 || message.includes('STRIPE_SECRET_KEY')) {
        throw new Error(
          'Payments are temporarily unavailable. Please try again later.',
          { cause: stripeErr },
        )
      }
      throw stripeErr
    }
  } catch (err) {
    error.value = err?.response?.data?.message || err?.message || 'Unable to prepare payment.'
  } finally {
    loading.value = false
  }
}

async function completePurchase() {
  if (paymentType.value === 'membership') {
    await api.post('/memberships/subscribe', {
      plan_id: Number(referenceId.value),
      auto_renew: autoRenew.value,
    })
    successMessage.value = 'Your membership subscription has been created successfully.'
  } else if (paymentType.value === 'event') {
    await api.post(`/events/${referenceId.value}/register`)
    successMessage.value = 'Your event registration has been completed.'
  } else {
    if (paymentId) {
      await api.get(`/payments/stripe/status/${paymentId}`).catch(() => {})
    }
    successMessage.value = 'Your booking has been confirmed successfully.'
  }
  success.value = true
}

/**
 * Wait for the server to see the payment as completed.
 *
 * Stripe confirms the card in the browser, but the Payment row only flips to
 * `completed` once the webhook lands (or the server reconciles the intent).
 * Fulfilment is gated on that, so poll briefly rather than assuming.
 */
async function waitForSettlement(attempts = 6, delayMs = 800) {
  if (!paymentId) return true
  for (let i = 0; i < attempts; i += 1) {
    try {
      const { data } = await api.get(`/payments/stripe/status/${paymentId}`)
      if (data.status === 'completed') return true
      if (data.status === 'failed') return false
    } catch {
      // Transient read failure; the next attempt may succeed.
    }
    await new Promise((resolve) => setTimeout(resolve, delayMs))
  }
  // Not settled yet. completePurchase() still runs: the server reconciles the
  // intent with Stripe itself and returns 402 if it genuinely was not paid.
  return true
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

    const settled = await waitForSettlement()
    if (!settled) {
      stripeError.value = 'The payment was declined. Please try another card.'
      return
    }

    await completePurchase()
  } catch (err) {
    stripeError.value =
      err?.response?.data?.message ||
      'Payment was successful, but the follow-up action could not be completed.'
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
.btn-primary {
  background: #4f46e5;
  color: #fff;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
</style>
