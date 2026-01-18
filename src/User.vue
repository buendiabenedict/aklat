<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40">
    
    <header class="p-8 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-black font-black text-xl shadow-[0_0_20px_rgba(255,255,255,0.2)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h1 class="text-xl font-bold tracking-tighter italic uppercase">Aklat</h1>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900/50 px-4 py-2 rounded-full border border-white/5">
        <div class="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_8px_rgba(34,197,94,0.6)]"></div>
        <span class="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-400">System Live</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'home'" key="home" class="space-y-10 py-6">
          <section>
            <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-2">Interface Main</p>
            <h2 class="text-5xl font-bold tracking-tighter">Terminal</h2>
          </section>

          <div class="grid grid-cols-2 gap-4">
            <div class="bg-zinc-950 border border-white/5 p-8 rounded-[2.5rem]">
              <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-1">Index</p>
              <p class="text-4xl font-bold tracking-tighter text-white">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-8 rounded-[2.5rem]" @click="activeTab = 'notifications'">
              <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-1">Alerts</p>
              <p class="text-4xl font-bold tracking-tighter text-blue-500">{{ userRequests.length }}</p>
            </div>
          </div>

          <section @click="activeTab = 'loans'" class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] group cursor-pointer active:scale-95 transition-all">
             <h3 class="text-3xl font-black tracking-tighter mb-2 italic">MY LOANS</h3>
             <p class="text-zinc-500 text-sm mb-6">View your {{ approvedRequests.length }} active borrowed assets.</p>
             <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center text-black">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
             </div>
          </section>
        </div>

        <div v-else-if="activeTab === 'explore'" key="explore" class="py-6">
          <div class="mb-12 sticky top-6 z-40">
            <div class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 p-2 rounded-2xl flex items-center">
              <input v-model="searchQuery" type="text" placeholder="Search archives..." class="bg-transparent border-none w-full py-4 px-6 text-lg outline-none font-bold placeholder:text-zinc-800" />
            </div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div v-for="book in filteredBooks" :key="book.id" class="group bg-zinc-950 border border-white/5 p-10 rounded-[2.5rem] flex flex-col justify-between h-80">
              <h3 class="text-2xl font-bold tracking-tight italic">{{ book.title }}</h3>
              <button @click="openBorrowModal(book)" class="w-full py-4 bg-zinc-900 text-white hover:bg-white hover:text-black rounded-xl font-black text-[10px] uppercase tracking-widest transition-all">Request Asset</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'loans'" key="loans" class="py-10 space-y-6">
          <h2 class="text-4xl font-bold tracking-tighter mb-10 italic">ACTIVE LOANS</h2>
          <div v-if="approvedRequests.length === 0" class="p-20 border border-dashed border-white/10 rounded-[3rem] text-center text-zinc-800 font-bold uppercase tracking-widest text-xs">No active books found.</div>
          <div v-for="loan in approvedRequests" :key="loan.id" class="bg-white text-black p-8 rounded-[2.5rem] relative overflow-hidden mb-4">
            <div class="flex justify-between items-end">
              <div>
                <p class="text-[10px] font-black uppercase tracking-widest mb-1 opacity-60">Currently Holding</p>
                <h3 class="text-2xl font-bold tracking-tighter uppercase">{{ loan.bookTitle }}</h3>
              </div>
              <div class="text-right">
                <p class="text-[9px] font-black uppercase tracking-widest mb-1 opacity-60">Return Countdown</p>
                <p class="text-2xl font-mono font-bold text-blue-600">{{ calculateCountdown(loan.returnSchedule) }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'notifications'" key="notifications" class="py-10 space-y-6">
          <h2 class="text-4xl font-bold tracking-tighter mb-10 italic uppercase">Inbox</h2>
          <div v-if="userRequests.length === 0" class="p-20 border border-dashed border-white/10 rounded-[3rem] text-center text-zinc-800 font-bold uppercase tracking-widest text-xs">Nothing to show.</div>
          <div v-for="req in sortedRequests" :key="req.id" class="p-8 bg-zinc-950 border border-white/5 rounded-3xl flex items-center justify-between mb-4 hover:border-white/20 transition-all">
            <div class="flex items-center gap-6">
              <div :class="getStatusIconClass(req.status)" class="w-12 h-12 rounded-2xl flex items-center justify-center">
                <svg v-if="isStatus(req.status, 'approved')" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="2.5" d="M5 13l4 4L19 7" /></svg>
                <svg v-else-if="isStatus(req.status, 'declined')" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="2.5" d="M6 18L18 6M6 6l12 12" /></svg>
                <svg v-else class="w-6 h-6 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
              <div>
                <h4 class="font-bold tracking-tight text-lg">{{ req.bookTitle }}</h4>
                <p class="text-[10px] uppercase font-black tracking-widest mt-1" :class="getTextStatusColor(req.status)">
                  Status: {{ req.status || 'Pending' }}
                </p>
              </div>
            </div>
            <span class="text-[9px] font-mono text-zinc-700 font-bold">{{ formatTimestamp(req.createdAt) }}</span>
          </div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10">
           <div class="text-center mb-10">
              <div class="w-24 h-24 bg-zinc-900 border border-white/10 mx-auto rounded-[2.5rem] flex items-center justify-center text-3xl font-black mb-6">{{ auth.currentUser?.email?.[0].toUpperCase() }}</div>
              <h2 class="text-3xl font-bold tracking-tighter">{{ auth.currentUser?.email }}</h2>
           </div>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-[450px] px-6">
      <nav class="bg-zinc-900/90 backdrop-blur-3xl border border-white/10 rounded-full p-2.5 flex items-center justify-between shadow-2xl">
        <button @click="activeTab = 'home'" :class="activeTab === 'home' ? 'bg-white text-black' : 'text-zinc-500'" class="w-12 h-12 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
        </button>
        <button @click="activeTab = 'explore'" :class="activeTab === 'explore' ? 'bg-white text-black' : 'text-zinc-500'" class="w-12 h-12 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        </button>
        <button @click="activeTab = 'loans'" :class="activeTab === 'loans' ? 'bg-white text-black' : 'text-zinc-500'" class="w-12 h-12 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
        </button>
        <button @click="activeTab = 'notifications'" :class="activeTab === 'notifications' ? 'bg-white text-black' : 'text-zinc-500'" class="w-12 h-12 rounded-full flex items-center justify-center transition-all relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          <div v-if="unreadCount > 0" class="absolute top-2 right-2 w-2 h-2 bg-blue-500 rounded-full animate-ping"></div>
        </button>
        <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'bg-white text-black' : 'text-zinc-500'" class="w-12 h-12 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-md px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3.5rem] max-w-sm w-full text-center">
          <h2 class="text-3xl font-bold tracking-tighter mb-2 italic">BORROW ASSET</h2>
          <input type="date" v-model="returnDate" :min="minDate" @input="validateDate" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-6 px-6 text-white outline-none font-bold text-center mb-4" />
          <p v-if="dateError" class="text-red-600 text-[9px] mb-6 font-black uppercase tracking-widest">{{ dateError }}</p>
          <button @click="submitRequest" :disabled="!returnDate || dateError" class="w-full py-5 bg-white text-black rounded-2xl font-black uppercase text-[10px] tracking-widest disabled:opacity-20 transition-all">Confirm</button>
          <button @click="showModal = false" class="w-full py-4 text-zinc-600 font-bold uppercase text-[10px] mt-2">Cancel</button>
        </div>
      </div>
    </transition>

    <transition name="slide-up">
      <div v-if="showToast" class="fixed top-12 left-1/2 -translate-x-1/2 bg-white text-black px-10 py-4 rounded-full font-black text-[10px] uppercase z-[150] shadow-2xl">Entry Logged</div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, defineEmits } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, query, orderBy, addDoc, serverTimestamp, where } from "firebase/firestore";

const emit = defineEmits(['logout']);
const books = ref([]);
const userRequests = ref([]);
const activeTab = ref('home');
const searchQuery = ref('');
const showModal = ref(false);
const showToast = ref(false);
const selectedBook = ref(null);
const returnDate = ref('');
const dateError = ref('');
const currentTime = ref(new Date());

let timerInterval;

const minDate = computed(() => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split('T')[0];
});

// REAL-TIME LISTENER FOR NOTIFICATIONS
onMounted(() => {
  // Books Listener
  onSnapshot(query(collection(db, "books")), (s) => {
    books.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });

  // User Requests/Notifications Listener
  if (auth.currentUser) {
    console.log("Listening for UID:", auth.currentUser.uid);
    onSnapshot(query(collection(db, "notifications"), where("userId", "==", auth.currentUser.uid)), (s) => {
      userRequests.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      console.log("Current Data in userRequests:", userRequests.value);
    });
  }

  timerInterval = setInterval(() => { currentTime.value = new Date(); }, 1000);
});

onUnmounted(() => clearInterval(timerInterval));

// COMPUTED: APPROVED LOANS
const approvedRequests = computed(() => {
  return userRequests.value.filter(req => req.status?.toLowerCase() === 'approved');
});

const sortedRequests = computed(() => {
  return [...userRequests.value].sort((a, b) => (b.createdAt?.seconds || 0) - (a.createdAt?.seconds || 0));
});

const unreadCount = computed(() => userRequests.value.filter(r => r.status?.toLowerCase() !== 'pending').length);

const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));

// HELPERS
const isStatus = (current, target) => current?.toLowerCase() === target.toLowerCase();

const getStatusIconClass = (status) => {
  if (isStatus(status, 'approved')) return 'bg-green-500/10 text-green-500 border border-green-500/20';
  if (isStatus(status, 'declined')) return 'bg-red-500/10 text-red-500 border border-red-500/20';
  return 'bg-zinc-800 text-zinc-500';
};

const getTextStatusColor = (status) => {
  if (isStatus(status, 'approved')) return 'text-green-500';
  if (isStatus(status, 'declined')) return 'text-red-500';
  return 'text-zinc-600';
};

const calculateCountdown = (dateStr) => {
  if (!dateStr) return "00:00:00";
  const target = new Date(dateStr);
  target.setHours(23, 59, 59);
  const diff = target - currentTime.value;
  if (diff <= 0) return "DUE";
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor((diff % 86400000) / 3600000);
  const mins = Math.floor((diff % 3600000) / 60000);
  const secs = Math.floor((diff % 60000) / 1000);
  return `${days}d ${hours}h ${mins}m ${secs}s`;
};

const formatTimestamp = (ts) => ts ? new Date(ts.seconds * 1000).toLocaleDateString() : 'Now';

const openBorrowModal = (book) => {
  selectedBook.value = book;
  showModal.value = true;
  returnDate.value = '';
};

const validateDate = () => {
  if (!returnDate.value) return;
  const day = new Date(returnDate.value).getDay();
  dateError.value = (day === 0 || day === 6) ? "Weekends not allowed" : "";
};

const submitRequest = async () => {
  if (!auth.currentUser || !returnDate.value || dateError.value) return;
  try {
    await addDoc(collection(db, "notifications"), {
      bookId: selectedBook.value.id,
      bookTitle: selectedBook.value.title,
      userId: auth.currentUser.uid,
      userEmail: auth.currentUser.email,
      returnSchedule: returnDate.value,
      createdAt: serverTimestamp(),
      status: 'pending'
    });
    showModal.value = false;
    showToast.value = true;
    setTimeout(() => showToast.value = false, 3000);
  } catch (e) { console.error(e); }
};
</script>

<style scoped>
.page-enter-active, .page-leave-active { transition: all 0.3s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.4s ease; }
.slide-up-enter-from { opacity: 0; transform: translate(-50%, -20px); }
</style>