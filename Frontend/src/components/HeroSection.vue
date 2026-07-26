<template>
	<section class="hero">
		<video
			ref="videoRef"
			class="hero-video"
			autoplay
			muted
			loop
			playsinline
			aria-hidden="true"
		>
			<source :src="landingVideo" type="video/mp4" />
		</video>

		<div class="hero-overlay" aria-hidden="true"></div>

		<div class="hero-shell">
			<div class="hero-copy">
				<p class="badge">Sports Facility Booking Platform</p>

				<h1 class="hero-heading">
					<span>One Platform.</span>
					<span>Every Sport.</span>
					<span>Every Booking.</span>
				</h1>

				<p class="lede">
					ClubDash simplifies facility bookings, memberships, tournaments and club operations through one modern platform.
				</p>

				<div class="hero-actions">
					<router-link :to="primaryRoute" class="primary-action">{{ primaryActionLabel }}</router-link>
					<a class="secondary-action" href="#features">Watch Demo</a>
				</div>

				<dl class="stats" aria-label="Platform statistics">
					<div>
						<dt>20K+</dt>
						<dd>Bookings</dd>
					</div>
					<div>
						<dt>100+</dt>
						<dd>Sports Clubs</dd>
					</div>
					<div>
						<dt>50K+</dt>
						<dd>Users</dd>
					</div>
				</dl>
			</div>
		</div>
	</section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import landingVideo from '@/assets/LandingVideo.mp4'

const videoRef = ref(null)
const auth = useAuthStore()

const primaryRoute = computed(() => {
  if (!auth.isAuthenticated()) return { name: 'register' }
  return { name: auth.user?.role === 'owner' ? 'admin' : 'profile' }
})

const primaryActionLabel = computed(() => (auth.isAuthenticated() ? 'Go to Dashboard' : 'Get Started'))
</script>

<style scoped>
.hero {
	position: relative;
	height: 100vh;
	min-height: 100vh;
	overflow: hidden;
	display: flex;
	align-items: center;
	background: #0f172a;
}

.hero-video {
	position: absolute;
	inset: 0;
	width: 100%;
	height: 100%;
	object-fit: cover;
	z-index: 0;
}

.hero-overlay {
	position: absolute;
	inset: 0;
	background: rgba(0, 0, 0, 0.65);
	z-index: 1;
}

.hero-shell {
	position: relative;
	z-index: 2;
	width: min(1200px, calc(100% - 2rem));
	margin: 0 auto;
	padding: 9rem 0 5rem 4.5rem;
}

.hero-copy {
	max-width: 36rem;
}

.badge {
	display: inline-flex;
	align-items: center;
	margin: 0 0 2rem;
	padding: 0.5rem 1.1rem;
	border-radius: 999px;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.16);
	color: rgba(255, 255, 255, 0.9);
	font-family: 'Inter', sans-serif;
	font-size: 0.7rem;
	font-weight: 700;
	letter-spacing: 0.16em;
	text-transform: uppercase;
	animation: fadeIn 0.8s ease both;
}

.hero-heading {
	margin: 0;
	color: #ffffff;
	font-family: 'Inter', sans-serif;
	font-size: clamp(2.75rem, 5.8vw, 4.75rem);
	font-weight: 800;
	line-height: 1.08;
	letter-spacing: -0.04em;
	animation: fadeIn 1s ease 0.15s both;
}

.hero-heading span {
	display: block;
}

.hero-heading span + span {
	margin-top: 0.08em;
}

.lede {
	max-width: 32rem;
	margin: 2rem 0 0;
	color: rgba(255, 255, 255, 0.72);
	font-family: 'Inter', sans-serif;
	font-size: clamp(1rem, 1.35vw, 1.125rem);
	font-weight: 400;
	line-height: 1.8;
	animation: fadeIn 1s ease 0.3s both;
}

.hero-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 1.125rem;
	margin-top: 2.75rem;
	animation: fadeIn 1s ease 0.45s both;
}

.primary-action,
.secondary-action {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-height: 3.35rem;
	padding: 0.9rem 1.75rem;
	border-radius: 999px;
	font-family: 'Inter', sans-serif;
	font-size: 0.95rem;
	font-weight: 600;
	text-decoration: none;
	transition:
		transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
		box-shadow 0.25s ease,
		border-color 0.25s ease,
		background-color 0.25s ease;
}

.primary-action {
	color: #ffffff;
	background: #f97316;
	box-shadow: 0 12px 28px rgba(249, 115, 22, 0.38);
}

.secondary-action {
	color: #ffffff;
	background: rgba(255, 255, 255, 0.08);
	border: 1px solid rgba(255, 255, 255, 0.35);
	backdrop-filter: blur(16px);
	-webkit-backdrop-filter: blur(16px);
}

.primary-action:hover,
.secondary-action:hover,
.primary-action:focus-visible,
.secondary-action:focus-visible {
	transform: translateY(-3px);
}

.primary-action:hover,
.primary-action:focus-visible {
	background: #fb923c;
	box-shadow: 0 18px 36px rgba(249, 115, 22, 0.48);
}

.secondary-action:hover,
.secondary-action:focus-visible {
	background: rgba(255, 255, 255, 0.14);
	border-color: rgba(255, 255, 255, 0.55);
	box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}

.stats {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 1.125rem;
	margin: 4rem 0 0;
	padding: 0;
	animation: fadeUp 0.9s ease 0.65s both;
}

.stats div {
	padding: 1.35rem 1.4rem;
	border-radius: 1.25rem;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	backdrop-filter: blur(20px);
	-webkit-backdrop-filter: blur(20px);
	box-shadow:
		0 8px 32px rgba(0, 0, 0, 0.2),
		inset 0 1px 0 rgba(255, 255, 255, 0.12);
	transition:
		transform 0.3s cubic-bezier(0.22, 1, 0.36, 1),
		box-shadow 0.3s ease,
		border-color 0.3s ease;
}

.stats div:hover {
	transform: translateY(-4px);
	border-color: rgba(255, 255, 255, 0.32);
	box-shadow:
		0 16px 40px rgba(0, 0, 0, 0.28),
		0 0 24px rgba(255, 255, 255, 0.06),
		inset 0 1px 0 rgba(255, 255, 255, 0.18);
}

.stats dt {
	color: #ffffff;
	font-family: 'Inter', sans-serif;
	font-size: clamp(1.5rem, 2.4vw, 2rem);
	font-weight: 700;
	letter-spacing: -0.03em;
	line-height: 1.1;
}

.stats dd {
	margin: 0.45rem 0 0;
	color: rgba(255, 255, 255, 0.68);
	font-family: 'Inter', sans-serif;
	font-size: 0.875rem;
	font-weight: 500;
}

@keyframes fadeIn {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

@keyframes fadeUp {
	from {
		opacity: 0;
		transform: translateY(24px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

@media (max-width: 960px) {
	.hero-shell {
		padding: 8rem 0 4rem 2rem;
	}
}

@media (max-width: 720px) {
	.hero-shell {
		width: min(100% - 1.25rem, 1200px);
		padding: 7rem 0 3rem 0;
	}

	.hero-heading {
		font-size: clamp(2.25rem, 10vw, 3.25rem);
	}

	.stats {
		grid-template-columns: 1fr;
		margin-top: 3rem;
	}

	.hero-actions {
		flex-direction: column;
	}

	.primary-action,
	.secondary-action {
		width: 100%;
	}
}
</style>
