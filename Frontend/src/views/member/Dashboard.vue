<template>
<div class="space-y-6">
  <div><p class="kicker">Member workspace</p><h1 class="title mt-1">Welcome back, {{ firstName }}</h1><p class="muted mt-2 text-sm">Your next reservation, activity and club events in one place.</p></div>
  <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
  <section class="panel overflow-hidden">
    <div class="p-6 md:p-7 bg-gradient-to-r from-indigo-50 to-emerald-50">
      <p class="kicker">Next booking</p>
      <div v-if="nextBooking" class="mt-3 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div><h2 class="text-xl font-extrabold text-slate-900">{{ nextBooking.court_name }}</h2><p class="mt-1 text-sm text-slate-600">{{ nextBooking.club_name }}</p><p class="mt-3 text-sm font-semibold text-slate-700">{{ formatDate(nextBooking.date) }} · {{ formatTime(nextBooking.start_time) }} – {{ formatTime(nextBooking.end_time) }}</p></div>
        <router-link to="/member/my-bookings" class="btn btn-primary2 text-center">View booking</router-link>
      </div>
      <div v-else class="mt-3 flex flex-col gap-3 md:flex-row md:items-center md:justify-between"><p class="text-sm text-slate-600">You have no upcoming court reservation.</p><router-link to="/member/book-court" class="btn btn-primary2 text-center">Book a court</router-link></div>
    </div>
  </section>
  <div class="grid gap-4 sm:grid-cols-3"><div class="stat"><p class="kicker">Upcoming</p><p class="mt-2 text-3xl font-extrabold text-slate-900">{{ upcoming.length }}</p><p class="muted mt-1 text-xs">court bookings</p></div><div class="stat"><p class="kicker">Total bookings</p><p class="mt-2 text-3xl font-extrabold text-slate-900">{{ bookings.length }}</p><p class="muted mt-1 text-xs">all reservations</p></div><div class="stat"><p class="kicker">Upcoming events</p><p class="mt-2 text-3xl font-extrabold text-slate-900">{{ events.length }}</p><p class="muted mt-1 text-xs">club activities</p></div></div>
  <div class="grid gap-5 lg:grid-cols-[1.35fr_.65fr]">
    <section class="panel p-5"><div class="flex items-center justify-between"><div><h2 class="font-bold text-slate-900">Upcoming bookings</h2><p class="muted mt-1 text-xs">Your nearest reservations</p></div><router-link to="/member/my-bookings" class="text-xs font-bold text-indigo-600">View all</router-link></div><div class="mt-4 space-y-3"><div v-for="b in upcoming.slice(0,4)" :key="b.id" class="rounded-xl border border-slate-200 bg-slate-50/70 p-4 flex items-center justify-between gap-4"><div><p class="text-sm font-bold text-slate-900">{{ b.court_name }}</p><p class="mt-1 text-xs text-slate-500">{{ formatDate(b.date) }} · {{ formatTime(b.start_time) }}</p></div><span class="pill bg-emerald-50 text-emerald-700">Confirmed</span></div><p v-if="!upcoming.length" class="py-8 text-center text-sm text-slate-500">No upcoming bookings.</p></div></section>
    <section class="panel p-5"><div class="flex items-center justify-between"><h2 class="font-bold text-slate-900">Quick actions</h2></div><div class="mt-4 grid gap-2"><router-link to="/member/book-court" class="btn btn-primary2 text-center">Book a Court</router-link><router-link to="/member/my-bookings" class="btn btn-soft text-center">My Bookings</router-link><router-link to="/member/events" class="btn btn-soft text-center">Explore Events</router-link></div><div class="mt-6 border-t border-slate-100 pt-5"><h3 class="text-sm font-bold text-slate-900">Next club event</h3><div v-if="events[0]" class="mt-3"><p class="text-sm font-semibold text-slate-800">{{ events[0].title }}</p><p class="mt-1 text-xs text-slate-500">{{ formatDate(events[0].date) }} · {{ formatTime(events[0].start_time) }}</p></div><p v-else class="mt-3 text-xs text-slate-500">No upcoming events.</p></div></section>
  </div>
</div>
</template>
<script setup>
import {computed,onMounted,ref} from 'vue';import api from '@/api/axios';import {useAuthStore} from '@/stores/auth';
const auth=useAuthStore(),bookings=ref([]),events=ref([]),error=ref('');const firstName=computed(()=>String(auth.user?.name||auth.user?.username||'Member').split(' ')[0]);
function dt(b){return new Date(`${b.date}T${String(b.start_time||'00:00').slice(0,8)}`)}const upcoming=computed(()=>bookings.value.filter(b=>b.status==='active'&&dt(b)>=new Date()).sort((a,b)=>dt(a)-dt(b)));const nextBooking=computed(()=>upcoming.value[0]||null);
function formatDate(v){if(!v)return'—';return new Intl.DateTimeFormat('en-IN',{day:'numeric',month:'short',year:'numeric'}).format(new Date(`${v}T00:00:00`))}function formatTime(v){if(!v)return'—';const[h,m]=String(v).split(':');const d=new Date();d.setHours(+h,+m||0);return new Intl.DateTimeFormat('en-IN',{hour:'numeric',minute:'2-digit'}).format(d)}
async function load(){error.value='';try{const [b,e]=await Promise.all([api.get('/bookings'),api.get('/events')]);bookings.value=Array.isArray(b.data)?b.data:[];events.value=Array.isArray(e.data)?e.data:[]}catch(err){error.value=err?.response?.data?.message||'Unable to load dashboard.'}}onMounted(async()=>{if(!auth.user)await auth.restoreUser();await load()})
</script>
<style scoped>
.panel{background:rgba(255,255,255,.92);border:1px solid #dfe7f1;border-radius:18px;box-shadow:0 12px 35px rgba(51,65,85,.06)}
.kicker{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#64748b}.title{font-size:28px;line-height:1.15;font-weight:800;letter-spacing:-.035em;color:#172033}.muted{color:#64748b}.stat{background:rgba(255,255,255,.9);border:1px solid #e2e8f0;border-radius:16px;padding:18px}.pill{display:inline-flex;align-items:center;border-radius:999px;padding:6px 10px;font-size:11px;font-weight:700}.btn{border-radius:11px;padding:10px 14px;font-size:12px;font-weight:700;transition:.2s}.btn-primary2{background:#4f46e5;color:white;box-shadow:0 8px 18px rgba(79,70,229,.18)}.btn-soft{background:#f8fafc;color:#475569;border:1px solid #dfe7f1}.field2{width:100%;border:1px solid #dbe4ef;border-radius:11px;background:#f8fafc;padding:10px 12px;color:#172033;outline:none}.field2:focus{border-color:#818cf8;box-shadow:0 0 0 3px rgba(99,102,241,.1)}
</style>