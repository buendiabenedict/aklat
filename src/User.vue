<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40">
    
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-white rounded-lg flex items-center justify-center text-black font-black text-lg shadow-[0_0_15px_rgba(255,255,255,0.3)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h1 class="text-lg font-bold tracking-tighter italic uppercase">Aklat</h1>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900 px-3 py-1.5 rounded-full border border-white/5">
        <div class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
        <span class="text-[9px] font-bold uppercase tracking-widest text-zinc-400">System Ready</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'home'" key="home" class="space-y-6 py-4">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Index</p>
            <h2 class="text-4xl font-bold tracking-tighter uppercase italic">Terminal</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Archive</p>
              <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl" @click="activeTab = 'notifications'">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Activity</p>
              <p class="text-3xl font-bold tracking-tighter text-blue-500">{{ combinedHistory.length }}</p>
            </div>
          </div>

          <section @click="activeTab = 'loans'" class="bg-zinc-900 border border-white/10 p-8 rounded-[2rem] cursor-pointer hover:bg-zinc-800 transition-colors relative overflow-hidden group">
             <div class="relative z-10">
               <h3 class="text-2xl font-black tracking-tighter mb-1 italic uppercase">Active Loans</h3>
               <p class="text-zinc-500 text-xs mb-4">Tracking {{ approvedLoans.length }} confirmed assets.</p>
               <div class="w-10 h-10 bg-white text-black rounded-full flex items-center justify-center font-black text-sm">{{ approvedLoans.length }}</div>
             </div>
             <div class="absolute right-[-20px] bottom-[-20px] opacity-10 group-hover:opacity-20 transition-opacity">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-40 h-40" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253" /></svg>
             </div>
          </section>
        </div>

        <div v-else-if="activeTab === 'explore'" key="explore" class="py-4">
          <div class="mb-4 sticky top-4 z-40">
            <div class="bg-zinc-900/95 backdrop-blur-xl border border-white/10 p-1 rounded-xl flex items-center">
              <input v-model="searchQuery" type="text" placeholder="Filter collection..." class="bg-transparent border-none w-full py-3 px-4 text-sm outline-none font-bold placeholder:text-zinc-700" />
            </div>
          </div>
          
          <div class="space-y-2">
            <div v-for="book in filteredBooks" :key="book.id" class="bg-zinc-950 border border-white/5 p-4 rounded-xl flex items-center justify-between hover:border-white/20 transition-all">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-zinc-900 rounded-lg flex items-center justify-center text-zinc-600">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                </div>
                <div>
                  <h3 class="text-sm font-bold tracking-tight uppercase italic leading-none">{{ book.title }}</h3>
                  <p class="text-[8px] text-zinc-600 uppercase mt-1 tracking-widest font-black">Authorized Record</p>
                </div>
              </div>
              <button @click="openBorrowModal(book)" class="px-5 py-2.5 bg-zinc-900 text-[9px] text-white hover:bg-white hover:text-black rounded-lg font-black uppercase tracking-widest transition-all">Request</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'loans'" key="loans" class="py-10 space-y-4">
          <h2 class="text-3xl font-bold tracking-tighter mb-6 italic uppercase">Borrowed Assets</h2>
          <div v-if="approvedLoans.length === 0" class="p-16 border border-dashed border-white/10 rounded-[2rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">No Confirmed Loans</p>
          </div>
          <div v-for="loan in approvedLoans" :key="loan.id" class="bg-white text-black p-6 rounded-2xl mb-3 flex justify-between items-center shadow-2xl transition-all border-l-[6px] border-blue-500">
            <div class="max-w-[60%]">
              <p class="text-[8px] font-black uppercase tracking-widest mb-1 opacity-50">Active Possession</p>
              <h3 class="text-lg font-bold tracking-tighter uppercase leading-none">{{ loan.bookTitle }}</h3>
              <p class="text-[9px] font-bold text-zinc-400 mt-2 uppercase tracking-tighter">Verified by Admin</p>
            </div>
            <div class="text-right">
              <p class="text-[8px] font-black uppercase tracking-widest mb-1 opacity-50">Time Remaining</p>
              <p class="text-lg font-mono font-bold text-blue-600 tabular-nums">{{ calculateCountdown(loan.returnSchedule) }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'notifications'" key="notifications" class="py-10 space-y-3">
          <h2 class="text-3xl font-bold tracking-tighter mb-6 italic uppercase text-center">System Logs</h2>
          <div v-for="req in combinedHistory" :key="req.id" class="p-4 bg-zinc-950 border border-white/5 rounded-xl flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div :class="getStatusIconClass(req.status)" class="w-10 h-10 rounded-lg flex items-center justify-center">
                <svg v-if="isStatus(req.status, 'approved')" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                <svg v-else-if="isStatus(req.status, 'declined')" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="3" d="M6 18L18 6M6 6l12 12" /></svg>
                <svg v-else class="w-5 h-5 animate-pulse text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
              <div>
                <h4 class="font-bold tracking-tight text-xs uppercase">{{ req.bookTitle }}</h4>
                <p class="text-[8px] uppercase font-black tracking-widest mt-0.5" :class="getTextStatusColor(req.status)">{{ req.status || 'Processing' }}</p>
              </div>
            </div>
            <span class="text-[8px] font-mono text-zinc-800 font-bold uppercase">{{ formatTimestamp(req.createdAt) }}</span>
          </div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 space-y-10">
          <div class="text-center">
            <div class="w-20 h-20 bg-zinc-900 border border-white/10 mx-auto rounded-3xl flex items-center justify-center text-2xl font-black mb-4 shadow-2xl">{{ auth.currentUser?.email?.[0].toUpperCase() }}</div>
            <h2 class="text-2xl font-bold tracking-tighter uppercase italic">{{ auth.currentUser?.email }}</h2>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mt-2 italic">Standard Access</p>
          </div>
          <div class="max-w-xs mx-auto space-y-3">
            <button @click="showLogoutModal = true" class="w-full py-4 bg-zinc-900 text-red-500 rounded-2xl font-black uppercase text-[10px] tracking-widest border border-red-500/10 active:bg-red-600 active:text-white transition-all">Sign Out Session</button>
          </div>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 w-full max-w-[300px] px-4">
      <nav class="bg-zinc-900/90 backdrop-blur-2xl border border-white/10 rounded-full p-1.5 flex items-center justify-around shadow-2xl">
        <button @click="activeTab = 'home'" :class="activeTab === 'home' ? 'bg-white text-black' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
        </button>
        <button @click="activeTab = 'explore'" :class="activeTab === 'explore' ? 'bg-white text-black' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        </button>
        <button @click="activeTab = 'loans'" :class="activeTab === 'loans' ? 'bg-white text-black' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
          <div v-if="approvedLoans.length > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center text-[8px] font-black text-white border-2 border-black">{{ approvedLoans.length }}</div>
        </button>
        <button @click="activeTab = 'notifications'" :class="activeTab === 'notifications' ? 'bg-white text-black' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
        </button>
        <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'bg-white text-black' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-md px-6">
        <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2rem] max-w-sm w-full text-center">
          <h2 class="text-xl font-bold tracking-tighter mb-6 uppercase italic">Return Schedule</h2>
          <input type="date" v-model="returnDate" :min="minDate" @change="validateDate" class="w-full bg-zinc-900 border border-white/5 rounded-xl py-4 px-4 text-white outline-none font-bold text-center mb-2" />
          <p v-if="dateError" class="text-red-600 text-[8px] mb-4 font-black uppercase tracking-widest">{{ dateError }}</p>
          <button @click="submitRequest" :disabled="!returnDate || dateError !== ''" :class="(!returnDate || dateError !== '') ? 'bg-zinc-800 text-zinc-500' : 'bg-white text-black'" class="w-full py-4 rounded-xl font-black uppercase text-[10px] tracking-widest transition-all">Submit Asset Request</button>
          <button @click="closeModal" class="w-full py-4 text-zinc-600 font-bold uppercase text-[9px] mt-1">Cancel</button>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-md px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-6 uppercase tracking-tighter italic leading-none">Terminate Session?</h3>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="executeLogout" class="flex-1 py-4 rounded-xl bg-red-600 text-white font-black text-[10px] uppercase">Sign Out</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="slide-up">
      <div v-if="showToast" class="fixed top-8 left-1/2 -translate-x-1/2 bg-white text-black px-8 py-3 rounded-full font-black text-[9px] uppercase z-[150] shadow-2xl tracking-tighter">Request Logged</div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, defineEmits } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, query, addDoc, serverTimestamp, where } from "firebase/firestore";
import { signOut, onAuthStateChanged } from "firebase/auth";

const emit = defineEmits(['logout']);

const books = ref([]);
const notifications = ref([]);
const borrowers = ref([]); // NEW: Para sa confirmed borrowers collection
const activeTab = ref('home');
const searchQuery = ref('');
const showModal = ref(false);
const showLogoutModal = ref(false);
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

onMounted(() => {
  // 1. Listen for all books
  onSnapshot(collection(db, "books"), (s) => {
    books.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });

  // 2. Dual-Listener for Requests and Confirmed Loans
  onAuthStateChanged(auth, (user) => {
    if (user) {
      // Listen to 'notifications' (Pending and recently approved)
      onSnapshot(query(collection(db, "notifications"), where("userId", "==", user.uid)), (s) => {
        notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      });

      // Listen to 'borrowers' (Kung dito nililipat ni admin yung data pag-approve)
      onSnapshot(query(collection(db, "borrowers"), where("userId", "==", user.uid)), (s) => {
        borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      });
    }
  });

  timerInterval = setInterval(() => { currentTime.value = new Date(); }, 1000);
});

onUnmounted(() => clearInterval(timerInterval));

// UPDATED FILTER: Check both collections for approved status
const approvedLoans = computed(() => {
  // Combine all items from both collections that are marked as approved
  const fromNotif = notifications.value.filter(req => (req.status || '').toLowerCase().includes('approve'));
  const fromBorrowers = borrowers.value.filter(req => (req.status || '').toLowerCase().includes('approve') || !req.status); // Some systems move to borrowers and remove 'status' field because it's implicit
  
  // Merge and remove duplicates by ID
  const all = [...fromNotif, ...fromBorrowers];
  return Array.from(new Map(all.map(item => [item.id, item])).values());
});

const combinedHistory = computed(() => {
  return [...notifications.value, ...borrowers.value].sort((a, b) => (b.createdAt?.seconds || 0) - (a.createdAt?.seconds || 0));
});

const unreadCount = computed(() => notifications.value.filter(r => r.status?.toLowerCase().trim() !== 'pending').length);
const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));

const isStatus = (current, target) => (current || '').toString().toLowerCase().trim().includes(target.toLowerCase());
const getStatusIconClass = (status) => isStatus(status, 'approve') ? 'bg-green-500/10 text-green-500' : isStatus(status, 'decline') ? 'bg-red-500/10 text-red-500' : 'bg-zinc-800 text-zinc-500';
const getTextStatusColor = (status) => isStatus(status, 'approve') ? 'text-green-500' : isStatus(status, 'decline') ? 'text-red-500' : 'text-zinc-600';

const calculateCountdown = (dateStr) => {
  if (!dateStr) return "PENDING";
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

const formatTimestamp = (ts) => ts ? new Date(ts.seconds * 1000).toLocaleDateString() : 'SYNC';

const openBorrowModal = (book) => {
  selectedBook.value = book;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedBook.value = null;
};

const validateDate = () => {
  if (!returnDate.value) return;
  const day = new Date(returnDate.value).getDay();
  dateError.value = (day === 0 || day === 6) ? "Weekends not available" : "";
};

const submitRequest = async () => {
  if (!auth.currentUser || !returnDate.value || dateError.value !== "") return;
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
    closeModal();
    showToast.value = true;
    setTimeout(() => showToast.value = false, 2000);
  } catch (e) { console.error(e); }
};

const executeLogout = async () => {
  try { await signOut(auth); emit('logout'); } catch (e) { emit('logout'); }
};
</script>

<style scoped>
.page-enter-active, .page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.4s ease; }
.slide-up-enter-from { opacity: 0; transform: translate(-50%, -10px); }
::-webkit-scrollbar { display: none; }
</style>