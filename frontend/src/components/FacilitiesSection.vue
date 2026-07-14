<template>
	<section class="facilities" id="facilities">
		<div class="section-shell">
			<div class="section-heading">
				<p class="eyebrow">Facility showcase</p>
				<h2>Modern facilities built for active members</h2>
				<p>
					A polished library of premium venues gives each member a quick way to find the right space and book with
					confidence.
				</p>
			</div>

			<div class="facility-grid">
				<article v-for="facility in facilities" :key="facility.title" class="facility-card">
					<div class="image-frame">
						<img :src="facility.image" :alt="facility.title" loading="lazy" />
						<div class="image-overlay" aria-hidden="true"></div>
						<h3>{{ facility.title }}</h3>
					</div>
					<div class="facility-body">
						<p>{{ facility.description }}</p>
					</div>
				</article>
			</div>
		</div>
	</section>
</template>

<script setup>
import badmintonCourtImg from '@/assets/badminton_court.png'
import tennisCourtImg from '@/assets/tennis_court.png'

const facilities = [
	{
		title: 'Badminton Court',
		description: 'Well-lit courts with seamless reservations for training, social play and club nights.',
		image: badmintonCourtImg,
	},
	{
		title: 'Tennis Court',
		description: 'Dedicated court access with polished scheduling for singles, doubles and coaching sessions.',
		image: tennisCourtImg,
	},
	{
		title: 'Basketball Court',
		description: 'High-energy spaces for practice, tournaments and community league play.',
		image: 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800&auto=format&fit=crop&q=80',
	},
]
</script>

<style scoped>
.facilities {
	padding: 6rem 0;
	background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
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

.facility-grid {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 1.125rem;
}

.facility-card {
	overflow: hidden;
	border-radius: 1.65rem;
	background: #ffffff;
	border: 1px solid rgba(226, 232, 240, 0.95);
	box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
	transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s ease, border-color 0.3s ease;
}

.facility-card:hover {
	transform: translateY(-6px);
	border-color: rgba(37, 99, 235, 0.18);
	box-shadow: 0 26px 54px rgba(15, 23, 42, 0.12);
}

.image-frame {
	position: relative;
	overflow: hidden;
	aspect-ratio: 4 / 3;
	background: #0f172a;
}

.image-overlay {
	position: absolute;
	inset: 0;
	background: linear-gradient(180deg, rgba(15, 23, 42, 0.05) 0%, rgba(15, 23, 42, 0.72) 100%);
	z-index: 1;
	transition: opacity 0.3s ease;
}

.image-frame h3 {
	position: absolute;
	left: 1.15rem;
	right: 1.15rem;
	bottom: 1.15rem;
	z-index: 2;
	margin: 0;
	color: #ffffff;
	font-family: 'Inter', sans-serif;
	font-size: 1.05rem;
	font-weight: 700;
	letter-spacing: -0.02em;
}

.image-frame img {
	width: 100%;
	height: 100%;
	object-fit: cover;
	display: block;
	transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.facility-card:hover .image-frame img {
	transform: scale(1.06);
}

.facility-body {
	padding: 1.25rem 1.3rem 1.35rem;
}

.facility-body p {
	margin: 0;
	color: #64748b;
	line-height: 1.75;
	font-size: 0.95rem;
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
	.facility-grid {
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}
}

@media (max-width: 640px) {
	.facilities {
		padding: 4.5rem 0;
	}

	.section-shell {
		width: min(100% - 1rem, 1200px);
	}

	.facility-grid {
		grid-template-columns: 1fr;
	}
}
</style>
