<template>
	<section class="membership" id="membership">
		<div class="section-shell">
			<div class="section-heading">
				<p class="eyebrow">Membership plans</p>
				<h2>Flexible pricing for clubs at every stage</h2>
				<p>
					Pick a plan that matches your club's scale today and move up without disrupting your workflows or member
					experience.
				</p>
			</div>

			<div class="pricing-grid">
				<article v-for="plan in plans" :key="plan.name" class="pricing-card">
					<span v-if="plan.featured" class="badge">Most Popular</span>
					<h3>{{ plan.name }}</h3>
					<p class="price">{{ plan.price }}<span>/mo</span></p>
					<p class="summary">{{ plan.summary }}</p>

					<ul>
						<li v-for="benefit in plan.benefits" :key="benefit">{{ benefit }}</li>
					</ul>

					<router-link :to="planRoute" class="plan-link">
						{{ plan.cta }}
					</router-link>
				</article>
			</div>
		</div>
	</section>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const planRoute = computed(() => {
  if (!auth.isAuthenticated()) return { name: 'register' }
  return { name: auth.user?.role === 'owner' ? 'admin' : 'profile' }
})

const plans = [
	{
		name: 'Basic',
		price: '₹1,499',
		summary: 'A lightweight plan for boutique clubs and smaller facilities that need modern booking tools.',
		benefits: ['Facility booking', 'Member directory', 'Email reminders'],
		cta: 'Start Basic',
		featured: false,
	},
	{
		name: 'Premium',
		price: '₹3,999',
		summary: 'The best balance for growing sports clubs that need stronger coordination and analytics.',
		benefits: ['Everything in Basic', 'Event scheduling', 'Advanced notifications'],
		cta: 'Choose Premium',
		featured: true,
	},
	{
		name: 'Elite',
		price: '₹7,999',
		summary: 'For multi-facility clubs that want elevated support, visibility and operational control.',
		benefits: ['Everything in Premium', 'Priority onboarding', 'Dedicated support'],
		cta: 'Go Elite',
		featured: false,
	},
]
</script>

<style scoped>
.membership {
	padding: 6rem 0;
	background: #f8fafc;
}

.section-shell {
	width: min(1200px, calc(100% - 2rem));
	margin: 0 auto;
}

.section-heading {
	max-width: 44rem;
	margin-bottom: 2.5rem;
	animation: fadeUp 0.7s ease both;
}

.eyebrow {
	display: inline-flex;
	margin: 0 0 0.85rem;
	padding: 0.5rem 0.88rem;
	border-radius: 999px;
	background: rgba(249, 115, 22, 0.1);
	color: #c2410c;
	font-size: 0.78rem;
	font-weight: 800;
	letter-spacing: 0.12em;
	text-transform: uppercase;
}

h2 {
	margin: 0;
	color: #0f172a;
	font-family: 'Poppins', sans-serif;
	font-size: clamp(2rem, 4vw, 3.2rem);
	line-height: 1.05;
	letter-spacing: -0.04em;
}

.section-heading p:last-child {
	margin: 1rem 0 0;
	color: #64748b;
	font-size: 1.02rem;
	line-height: 1.8;
}

.pricing-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 1.125rem;
}

.pricing-card {
	position: relative;
	padding: 2.25rem 1.75rem 1.75rem;
	border-radius: 1.65rem;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), #ffffff);
	border: 1px solid rgba(226, 232, 240, 0.96);
	box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
	transition:
		transform 0.35s cubic-bezier(0.22, 1, 0.36, 1),
		box-shadow 0.35s ease,
		border-color 0.35s ease;
	display: flex;
	flex-direction: column;
}

.pricing-card:hover {
	transform: translateY(-10px) scale(1.05);
	border-color: rgba(37, 99, 235, 0.18);
	box-shadow: 0 28px 56px rgba(15, 23, 42, 0.12);
}

.pricing-card > * {
	position: relative;
	z-index: 1;
}

.badge {
	position: absolute;
	top: -14px;
	left: 50%;
	transform: translateX(-50%);
	display: inline-flex;
	padding: 0.45rem 0.78rem;
	border-radius: 999px;
	background: rgba(249, 115, 22, 0.12);
	color: #c2410c;
	font-size: 0.78rem;
	font-weight: 800;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	box-shadow: 0 4px 12px rgba(249, 115, 22, 0.1);
}

h3 {
	margin: 0;
	color: #0f172a;
	font-size: 1.12rem;
}

.price {
	margin: 0.85rem 0 0;
	color: #0f172a;
	font-family: 'Poppins', sans-serif;
	font-size: 2.7rem;
	font-weight: 700;
	letter-spacing: -0.04em;
}

.price span {
	color: #64748b;
	font-family: 'Inter', sans-serif;
	font-size: 1rem;
	font-weight: 600;
}

.summary {
	margin: 0.85rem 0 1.25rem;
	color: #64748b;
	line-height: 1.75;
}

ul {
	display: grid;
	gap: 0.7rem;
	margin: 0 0 1.5rem;
	padding: 0;
	list-style: none;
}

li {
	position: relative;
	padding-left: 1.3rem;
	color: #334155;
	line-height: 1.6;
}

li::before {
	content: '';
	position: absolute;
	top: 0.54rem;
	left: 0;
	width: 0.46rem;
	height: 0.46rem;
	border-radius: 50%;
	background: linear-gradient(135deg, #2563eb, #f97316);
}

.plan-link {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 100%;
	min-height: 3.05rem;
	margin-top: auto;
	padding: 0.8rem 1rem;
	border-radius: 999px;
	border: 1px solid rgba(37, 99, 235, 0.16);
	color: #1d4ed8;
	text-decoration: none;
	font-weight: 700;
	transition: transform 0.25s ease, background-color 0.25s ease, box-shadow 0.25s ease;
}

.plan-link:hover,
.plan-link:focus-visible {
	transform: translateY(-2px);
}

@keyframes fadeUp {
	from {
		opacity: 0;
		transform: translateY(14px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

@media (max-width: 1100px) {
	.pricing-grid {
		grid-template-columns: 1fr;
		gap: 2rem;
	}
}

@media (max-width: 640px) {
	.membership {
		padding: 4.5rem 0;
	}

	.section-shell {
		width: min(100% - 1rem, 1200px);
	}

	.pricing-card {
		padding: 2rem 1.35rem 1.35rem;
	}
}
</style>
