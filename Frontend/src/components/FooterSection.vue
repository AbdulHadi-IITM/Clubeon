<template>
	<footer class="footer">
		<div class="section-shell">
			<div class="footer-top">
				<a href="#top" class="logo" aria-label="ClubDash home">
					<span class="mark">C</span>
					<span>ClubDash</span>
				</a>

				<div class="footer-columns">
					<section>
						<h3>Quick Links</h3>
						<nav aria-label="Footer quick links">
							<a href="#features">Features</a>
							<a href="#facilities">Facilities</a>
							<a href="#membership">Membership</a>
							<a href="#contact">Contact</a>
						</nav>
					</section>

					<section>
						<h3>Company</h3>
						<nav aria-label="Footer company links">
							<a href="#top">About</a>
							<a href="#top">Privacy Policy</a>
							<a href="#top">Terms</a>
						</nav>
					</section>

					<section>
						<h3>Contact</h3>
						<ul>
							<li>hello@clubdash.com</li>
							<li>Mon - Fri, 9:00 AM - 6:00 PM</li>
						</ul>
					</section>
				</div>
			</div>

			<div class="footer-bottom">
				<p>&copy; 2026 ClubDash. All rights reserved.</p>
			</div>
		</div>
	</footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
	padding: 0 0 2rem;
	background: #0f172a;
	color: #e2e8f0;
}

.section-shell {
	width: min(1200px, calc(100% - 2rem));
	margin: 0 auto;
}

.footer-top {
	display: grid;
	grid-template-columns: auto 1fr;
	gap: 2rem;
	align-items: start;
	padding: 3rem 0 1.8rem;
	border-bottom: 1px solid rgba(148, 163, 184, 0.18);
}

.logo {
	display: inline-flex;
	align-items: center;
	gap: 0.72rem;
	color: #ffffff;
	text-decoration: none;
	font-family: 'Poppins', sans-serif;
	font-size: 1.1rem;
	font-weight: 700;
	letter-spacing: -0.02em;
}

.mark {
	width: 2.4rem;
	height: 2.4rem;
	display: grid;
	place-items: center;
	border-radius: 0.95rem;
	background: linear-gradient(135deg, #2563eb, #f97316);
	box-shadow: 0 14px 28px rgba(37, 99, 235, 0.2);
}

.footer-columns {
	display: grid;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	gap: 2rem;
}

h3 {
	margin: 0 0 1rem;
	color: #ffffff;
	font-size: 1rem;
}

nav {
	display: grid;
	gap: 0.8rem;
}

nav a {
	width: fit-content;
	color: #cbd5e1;
	text-decoration: none;
	transition: color 0.2s ease, transform 0.2s ease;
}

nav a:hover,
nav a:focus-visible {
	color: #ffffff;
	transform: translateX(2px);
}

ul {
	display: grid;
	gap: 0.75rem;
	margin: 0;
	padding: 0;
	list-style: none;
	color: #cbd5e1;
}

.footer-bottom {
	padding-top: 1.2rem;
}

.footer-bottom p {
	margin: 0;
	color: #94a3b8;
	font-size: 0.92rem;
}

@media (max-width: 720px) {
	.footer-top {
		grid-template-columns: 1fr;
		gap: 1.5rem;
	}

	.footer-columns {
		grid-template-columns: 1fr;
	}
}

@media (max-width: 640px) {
	.footer {
		padding-bottom: 1.5rem;
	}

	.section-shell {
		width: min(100% - 1rem, 1200px);
	}
}
</style>
