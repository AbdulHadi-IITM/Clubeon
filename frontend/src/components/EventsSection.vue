<template>
	<section class="features" id="features">
		<div class="section-shell">
			<div class="section-heading">
				<p class="eyebrow">Platform capabilities</p>
				<h2>Everything Your Club Needs</h2>
				<p>
					ClubDash unifies bookings, memberships, tournaments and alerts into one modern software workspace for clubs
					that want clarity and control.
				</p>
			</div>

			<div class="feature-grid">
				<article v-for="item in features" :key="item.title" class="feature-card">
					<div class="icon-wrap" aria-hidden="true">
						<svg v-if="item.icon === 'booking'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
							<rect x="3" y="4" width="18" height="18" rx="2" />
							<path d="M16 2v4M8 2v4M3 10h18" />
							<path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01" />
						</svg>
						<svg v-else-if="item.icon === 'membership'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
							<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
							<circle cx="9" cy="7" r="4" />
							<path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
						</svg>
						<svg v-else-if="item.icon === 'tournament'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
							<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
							<path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
							<path d="M4 22h16" />
							<path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22" />
							<path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22" />
							<path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" />
						</svg>
						<svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
							<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
							<path d="M13.73 21a2 2 0 0 1-3.46 0" />
						</svg>
					</div>
					<h3>{{ item.title }}</h3>
					<p>{{ item.description }}</p>
				</article>
			</div>
		</div>
	</section>
</template>

<script setup>
const features = [
	{
		icon: 'booking',
		title: 'Court Booking',
		description: 'Offer real-time availability, frictionless reservations and clear booking workflows for every court.',
	},
	{
		icon: 'membership',
		title: 'Membership Management',
		description: 'Manage plans, renewals and member records from one elegant admin interface.',
	},
	{
		icon: 'tournament',
		title: 'Tournament Management',
		description: 'Coordinate brackets, schedules and event logistics without spreadsheet chaos.',
	},
	{
		icon: 'notifications',
		title: 'Notifications',
		description: 'Keep members informed with smart alerts for bookings, renewals and club updates.',
	},
]
</script>

<style scoped>
.features {
	padding: 6rem 0;
	background: #ffffff;
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
	background: rgba(37, 99, 235, 0.1);
	color: #1d4ed8;
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
	font-size: 1.03rem;
	line-height: 1.8;
}

.feature-grid {
	display: grid;
	grid-template-columns: repeat(4, minmax(0, 1fr));
	gap: 1.125rem;
}

.feature-card {
	position: relative;
	overflow: hidden;
	padding: 1.5rem;
	border-radius: 1.5rem;
	background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), #f8fafc);
	border: 1px solid rgba(226, 232, 240, 0.96);
	box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
	transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s ease, border-color 0.3s ease;
}

.feature-card::before {
	content: '';
	position: absolute;
	inset: 0;
	background: linear-gradient(135deg, rgba(37, 99, 235, 0.04), rgba(249, 115, 22, 0.04));
	opacity: 0;
	transition: opacity 0.3s ease;
}

.feature-card:hover {
	transform: translateY(-6px);
	border-color: rgba(37, 99, 235, 0.2);
	box-shadow: 0 24px 52px rgba(15, 23, 42, 0.1);
}

.feature-card:hover::before {
	opacity: 1;
}

.icon-wrap {
	position: relative;
	width: 3.1rem;
	height: 3.1rem;
	display: grid;
	place-items: center;
	border-radius: 1rem;
	background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(249, 115, 22, 0.08));
	color: #2563eb;
}

.icon-wrap svg {
	width: 1.45rem;
	height: 1.45rem;
}

h3 {
	position: relative;
	margin: 1.15rem 0 0.6rem;
	color: #0f172a;
	font-size: 1.08rem;
}

.feature-card p {
	position: relative;
	margin: 0;
	color: #64748b;
	line-height: 1.75;
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
	.feature-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 640px) {
	.features {
		padding: 4.5rem 0;
	}

	.section-shell {
		width: min(100% - 1rem, 1200px);
	}

	.feature-grid {
		grid-template-columns: 1fr;
	}
}
</style>
