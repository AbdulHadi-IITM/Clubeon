<template>
  <div class="landing-view" id="top">
    <Navbar />

    <main>
      <HeroSection />
      <EventsSection />
      <FacilitiesSection />
      <MembershipSection />
      <CallToActionSection />
      <FooterSection />
    </main>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import HeroSection from '@/components/HeroSection.vue'
import EventsSection from '@/components/EventsSection.vue'
import FacilitiesSection from '@/components/FacilitiesSection.vue'
import MembershipSection from '@/components/MembershipSection.vue'
import CallToActionSection from '@/components/CallToActionSection.vue'
import FooterSection from '@/components/FooterSection.vue'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');

:global(*) {
  box-sizing: border-box;
}

:global(html) {
  scroll-behavior: smooth;
}

:global(body) {
  margin: 0;
  background: #f8fafc;
  color: #0f172a;
  font-family: 'Inter', sans-serif;
  overflow-x: clip;
}

:global(a) {
  color: inherit;
}

.landing-view {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 30%),
    radial-gradient(circle at right 18rem, rgba(249, 115, 22, 0.08), transparent 26%),
    #f8fafc;
  color: #0f172a;
  overflow-x: clip;
}

main {
  padding-top: 0;
}
</style>