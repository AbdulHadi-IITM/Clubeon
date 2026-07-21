<template>
	<section class="reviews-section" id="contact">
		<div class="section-shell">
			<div class="section-heading">
				<p class="eyebrow">Customer reviews</p>
				<h2>Loved by active clubs and members</h2>
				<p>
					See how facility managers and sports coordinators use ClubDash to simplify scheduling, optimize utilization, and deliver a modern member experience.
				</p>
			</div>

			<div class="reviews-slider">
				<div class="reviews-track">
					<div
						v-for="(review, index) in reviews"
						:key="review.name"
						class="review-card"
						:class="getCardClass(index)"
						@click="setIndex(index)"
					>
						<div class="review-stars">
							<span v-for="star in review.rating" :key="star" class="star">★</span>
						</div>
						<p class="review-text">"{{ review.text }}"</p>
						<div class="review-author">
							<div class="author-avatar">{{ review.avatar }}</div>
							<div class="author-info">
								<span class="author-name">{{ review.name }}</span>
								<span class="author-role">{{ review.role }}</span>
							</div>
						</div>
					</div>
				</div>

				<div class="slider-dots">
					<span
						v-for="(review, index) in reviews"
						:key="'dot-' + index"
						class="slider-dot"
						:class="{ active: currentIndex === index }"
						@click="setIndex(index)"
					></span>
				</div>
			</div>
		</div>
	</section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const reviews = [
	{
		name: 'Sarah Jenkins',
		role: 'Director, Apex Tennis Arena',
		text: 'ClubDash transformed our court operations. Bookings increased by 40% and members love the mobile experience.',
		rating: 5,
		avatar: '👩‍💼',
	},
	{
		name: 'Marcus Chen',
		role: 'Owner, Elite Badminton Club',
		text: 'The tournament bracket system saved us dozens of hours. The real-time booking updates are flawless.',
		rating: 5,
		avatar: '👨‍💼',
	},
	{
		name: 'Elena Rostova',
		role: 'Manager, Wave Aquatics',
		text: 'Highly recommend! Membership tracking and auto-renewals solved our late payment issues completely.',
		rating: 5,
		avatar: '👩‍🔬',
	},
	{
		name: 'David Miller',
		role: 'President, Unity Soccer League',
		text: 'Our league scheduling went from a spreadsheet nightmare to a smooth 5-minute automated setup.',
		rating: 5,
		avatar: '👨‍💻',
	},
]

const currentIndex = ref(0)

const getCardClass = (index) => {
	const diff = (index - currentIndex.value + reviews.length) % reviews.length
	if (diff === 0) return 'card-active'
	if (diff === 1) return 'card-next'
	if (diff === reviews.length - 1) return 'card-prev'
	return 'card-hidden'
}

const setIndex = (index) => {
	currentIndex.value = index
	resetTimer()
}

let timer = null
const startTimer = () => {
	timer = setInterval(() => {
		currentIndex.value = (currentIndex.value + 1) % reviews.length
	}, 5000)
}
const resetTimer = () => {
	if (timer) clearInterval(timer)
	startTimer()
}

onMounted(() => {
	startTimer()
})

onBeforeUnmount(() => {
	if (timer) clearInterval(timer)
})
</script>

<style scoped>
.reviews-section {
	padding: 6rem 0;
	background: #f8fafc;
}

.section-shell {
	width: min(1200px, calc(100% - 2rem));
	margin: 0 auto;
}

.section-heading {
	max-width: 44rem;
	margin-bottom: 3.5rem;
	text-align: center;
	margin-left: auto;
	margin-right: auto;
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

.reviews-slider {
	position: relative;
	width: 100%;
	height: 380px;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	perspective: 1200px;
	overflow: visible;
}

.reviews-track {
	position: relative;
	width: 100%;
	height: 300px;
	overflow: visible;
}

.review-card {
	position: absolute;
	top: 50%;
	left: 50%;
	width: 320px;
	padding: 2rem;
	border-radius: 1.65rem;
	background: #ffffff;
	border: 1px solid rgba(226, 232, 240, 0.8);
	color: #0f172a;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
	cursor: pointer;
	user-select: none;
	transition:
		transform 0.65s cubic-bezier(0.25, 1, 0.5, 1),
		opacity 0.65s cubic-bezier(0.25, 1, 0.5, 1),
		box-shadow 0.65s ease,
		border-color 0.65s ease;
}

.review-stars {
	display: flex;
	gap: 0.25rem;
	margin-bottom: 0.85rem;
	color: #f59e0b;
	font-size: 1rem;
}

.review-text {
	font-size: 0.95rem;
	line-height: 1.65;
	color: #334155;
	margin: 0 0 1.25rem;
	font-style: italic;
	display: -webkit-box;
	-webkit-line-clamp: 4;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.review-author {
	display: flex;
	align-items: center;
	gap: 0.75rem;
	border-top: 1px solid rgba(226, 232, 240, 0.8);
	padding-top: 0.85rem;
}

.author-avatar {
	width: 2.5rem;
	height: 2.5rem;
	border-radius: 50%;
	background: #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 1.35rem;
}

.author-info {
	display: flex;
	flex-direction: column;
}

.author-name {
	font-weight: 700;
	font-size: 0.92rem;
	color: #0f172a;
}

.author-role {
	font-size: 0.75rem;
	color: #64748b;
	font-weight: 500;
}

.card-active {
	transform: translate(-50%, -50%) scale(1.06);
	opacity: 1;
	z-index: 3;
	box-shadow: 0 25px 50px rgba(15, 23, 42, 0.12);
	border-color: rgba(37, 99, 235, 0.15);
}

.card-prev {
	transform: translate(-120%, -50%) scale(0.85) rotateY(18deg);
	opacity: 0.55;
	z-index: 1;
}

.card-next {
	transform: translate(20%, -50%) scale(0.85) rotateY(-18deg);
	opacity: 0.55;
	z-index: 2;
}

.card-hidden {
	transform: translate(-50%, -50%) scale(0.6);
	opacity: 0;
	z-index: 0;
	pointer-events: none;
}

.card-prev:hover,
.card-next:hover {
	opacity: 0.85;
}

.slider-dots {
	display: flex;
	gap: 0.5rem;
	margin-top: 1rem;
	z-index: 5;
}

.slider-dot {
	width: 0.5rem;
	height: 0.5rem;
	border-radius: 50%;
	background: #cbd5e1;
	cursor: pointer;
	transition:
		background-color 0.3s ease,
		transform 0.3s ease;
}

.slider-dot.active {
	background: #2563eb;
	transform: scale(1.25);
}

@media (max-width: 640px) {
	.reviews-section {
		padding: 4rem 0;
	}

	.reviews-slider {
		height: 340px;
	}

	.reviews-track {
		height: 260px;
	}

	.review-card {
		width: 250px;
		padding: 1.25rem;
	}

	.card-prev {
		transform: translate(-115%, -50%) scale(0.8);
	}

	.card-next {
		transform: translate(15%, -50%) scale(0.8);
	}
}
</style>
