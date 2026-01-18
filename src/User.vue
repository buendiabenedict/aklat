<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40">
    
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-white rounded-lg flex items-center justify-center text-black font-black text-lg shadow-[0_0_20px_rgba(255,255,255,0.2)]">
          <span class="text-[10px] tracking-tighter">AK</span>
        </div>
        <h1 class="text-lg font-bold tracking-tighter italic uppercase">Aklat</h1>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900 px-3 py-1.5 rounded-full border border-white/5">
        <div class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
        <span class="text-[9px] font-bold uppercase tracking-widest text-zinc-400">System Ready</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'home'" key="home" class="space-y-6 py-4 text-left">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Index</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient">Home</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Archive</p>
              <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl" @click="activeTab = 'notifications'">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Logs</p>
              <p class="text-3xl font-bold tracking-tighter text-blue-500">{{ combinedHistory.length }}</p>
            </div>
          </div>

          <section @click="activeTab = 'loans'" class="bg-zinc-900 border border-white/10 p-8 rounded-[2rem] cursor-pointer hover:bg-zinc-800 transition-colors relative overflow-hidden group">
             <div class="relative z-10">
               <h3 class="text-2xl font-black tracking-tighter mb-1 italic uppercase">Active Loans</h3>
               <p class="text-zinc-500 text-xs mb-4 tracking-tight">Managing {{ approvedLoans.length }} secured assets.</p>
               <div class="w-10 h-10 bg-white text-black rounded-full flex items-center justify-center font-black text-sm">{{ approvedLoans.length }}</div>
             </div>
          </section>
        </div>

        <div v-else-if="activeTab === 'explore'" key="explore" class="py-4 text-left">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Discovery</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient">Books</h2>
          </section>

          <div class="mb-6 sticky top-4 z-40">
            <div class="bg-zinc-900/95 backdrop-blur-xl border border-white/10 p-1 rounded-2xl flex items-center">
              <input v-model="searchQuery" type="text" placeholder="Filter archive..." class="bg-transparent border-none w-full py-3 px-4 text-sm outline-none font-bold placeholder:text-zinc-700" />
            </div>
          </div>
          
          <div class="space-y-2">
            <div v-for="book in filteredBooks" :key="book.id" class="bg-zinc-950 border border-white/5 p-4 rounded-xl flex items-center justify-between hover:border-white/20 transition-all">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-zinc-900 rounded-lg flex items-center justify-center text-zinc-600">
                  <span class="text-[8px] font-black uppercase">BOOK</span>
                </div>
                <div>
                  <h3 class="text-sm font-bold tracking-tight uppercase italic leading-none">{{ book.title }}</h3>
                  <p class="text-[8px] text-zinc-600 uppercase mt-1 tracking-widest font-black">Archive ID: {{ book.id.slice(0,5) }}</p>
                </div>
              </div>
              <button @click="openBorrowModal(book)" class="px-5 py-2.5 bg-zinc-900 text-[9px] text-white hover:bg-white hover:text-black rounded-lg font-black uppercase tracking-widest transition-all">Request</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'loans'" key="loans" class="py-10 space-y-4 text-left">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Status</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient leading-tight">Borrowed</h2>
          </section>

          <div v-if="approvedLoans.length === 0" class="p-16 border border-dashed border-white/10 rounded-[2rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">No Active Possession</p>
          </div>

          <div v-for="loan in approvedLoans" :key="loan.id" 
               :class="isOverdue(loan.returnSchedule) ? 'overdue-card' : 'standard-card'"
               class="p-6 rounded-[2rem] mb-4 flex justify-between items-center border shadow-2xl relative overflow-hidden transition-all">
            
            <div class="relative z-10 flex-1">
              <p class="text-[8px] font-black uppercase tracking-widest mb-1 opacity-40">Verified Sync</p>
              <h3 class="text-xl font-bold tracking-tighter uppercase leading-none mb-4 italic">{{ loan.bookTitle }}</h3>
              
              <div class="flex flex-col">
                <span class="text-[8px] font-black uppercase opacity-40 tracking-widest mb-0.5">Scheduled Return</span>
                <span class="text-[14px] font-bold font-mono tracking-tighter uppercase">
                  {{ loan.returnSchedule }} — 07:30 AM
                </span>
              </div>
            </div>

            <div v-if="isOverdue(loan.returnSchedule)" class="relative z-10">
              <span class="px-3 py-1 rounded-full bg-red-600 text-white text-[8px] font-black uppercase animate-pulse">Overdue</span>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'notifications'" key="notifications" class="py-10 space-y-3 text-left">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Activity</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient">System Logs</h2>
          </section>

          <div v-for="req in combinedHistory" :key="req.id" class="p-4 bg-zinc-950 border border-white/5 rounded-2xl flex items-center justify-between">
            <div class="flex items-center gap-4">
              <div :class="getStatusIconClass(req.status)" class="w-10 h-10 rounded-xl flex items-center justify-center shadow-lg font-black text-[8px]">
                {{ req.status?.slice(0,3).toUpperCase() || '...' }}
              </div>
              <div>
                <h4 class="font-bold tracking-tight text-xs uppercase italic">{{ req.bookTitle }}</h4>
                <p class="text-[8px] uppercase font-black tracking-widest mt-0.5" :class="getTextStatusColor(req.status)">{{ req.status || 'Processing' }}</p>
              </div>
            </div>
            <span class="text-[8px] font-mono text-zinc-800 font-bold uppercase">{{ formatTimestamp(req.createdAt) }}</span>
          </div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 space-y-10 text-center">
          <section class="text-left mb-10">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">User</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient">Profile</h2>
          </section>

          <div class="w-24 h-24 bg-zinc-900 border border-white/10 mx-auto rounded-[2rem] flex items-center justify-center text-3xl font-black mb-4 shadow-[0_20px_40px_rgba(0,0,0,0.5)] border-t-white/10">{{ auth.currentUser?.email?.[0].toUpperCase() }}</div>
          <h2 class="text-2xl font-bold tracking-tighter uppercase italic">{{ auth.currentUser?.email }}</h2>
          
          <div class="max-w-xs mx-auto pt-6">
            <button @click="showLogoutModal = true" class="w-full py-4 bg-zinc-900 text-red-500 rounded-2xl font-black uppercase text-[10px] tracking-widest border border-red-500/5 active:bg-red-600 active:text-white transition-all">Terminate Session</button>
          </div>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-[300px]">
      <nav class="bg-zinc-900/60 backdrop-blur-3xl border border-white/10 rounded-full p-1.5 flex items-center justify-around shadow-2xl">
        <button v-for="tab in ['home', 'explore', 'loans', 'notifications', 'profile']" :key="tab" @click="activeTab = tab" :class="activeTab === tab ? 'bg-white text-black shadow-lg scale-110' : 'text-zinc-600 hover:text-white'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 relative">
          <div v-if="tab === 'loans' && approvedLoans.length > 0" class="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full flex items-center justify-center text-[7px] font-black text-white border border-black">{{ approvedLoans.length }}</div>
          <span class="text-[8px] font-black uppercase">{{ tab.slice(0, 3) }}</span>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem] max-w-sm w-full text-center shadow-2xl">
          <h2 class="text-xl font-bold tracking-tighter mb-6 uppercase italic apple-gradient">Schedule Return</h2>
          <input type="date" v-model="returnDate" :min="minDate" @change="validateDate" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-4 px-4 text-white outline-none font-bold text-center mb-2" />
          <p v-if="dateError" class="text-red-600 text-[8px] mb-4 font-black uppercase tracking-widest">{{ dateError }}</p>
          <button @click="submitRequest" :disabled="!returnDate || dateError !== ''" :class="(!returnDate || dateError !== '') ? 'bg-zinc-800 text-zinc-500' : 'bg-white text-black'" class="w-full py-4 rounded-2xl font-black uppercase text-[10px] tracking-widest transition-all">Confirm Access</button>
          <button @click="closeModal" class="w-full py-4 text-zinc-600 font-bold uppercase text-[9px] mt-1">Abort</button>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-6 uppercase tracking-tighter italic leading-none">Sign Out?</h3>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="executeLogout" class="flex-1 py-4 rounded-2xl bg-red-600 text-white font-black text-[10px] uppercase">Yes</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="slide-up">
      <div v-if="showToast" class="fixed top-8 left-1/2 -translate-x-1/2 bg-white text-black px-8 py-3 rounded-full font-black text-[9px] uppercase z-[150] shadow-2xl">Asset Requested</div>
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
const borrowers = ref([]);
const activeTab = ref('home');
const searchQuery = ref('');
const showModal = ref(false);
const showLogoutModal = ref(false);
const showToast = ref(false);
const selectedBook = ref(null);
const returnDate = ref('');
const dateError = ref('');

const minDate = computed(() => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split('T')[0];
});

// OVERDUE CHECKER
const isOverdue = (schedule) => {
  if (!schedule) return false;
  const now = new Date();
  const target = new Date(schedule.replace(/-/g, '/'));
  target.setHours(7, 30, 0, 0); 
  return now.getTime() > target.getTime();
};

onMounted(() => {
  onSnapshot(collection(db, "books"), (s) => {
    books.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });

  onAuthStateChanged(auth, (user) => {
    if (user) {
      onSnapshot(query(collection(db, "notifications"), where("userId", "==", user.uid)), (s) => {
        notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      });
      onSnapshot(query(collection(db, "borrowers"), where("userId", "==", user.uid)), (s) => {
        borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      });
    }
  });
});

const approvedLoans = computed(() => {
  const fromNotif = notifications.value.filter(req => (req.status || '').toLowerCase().includes('approve'));
  const fromBorrowers = borrowers.value.filter(req => (req.status || '').toLowerCase().includes('approve') || !req.status);
  const all = [...fromNotif, ...fromBorrowers];
  return Array.from(new Map(all.map(item => [item.bookTitle, item])).values());
});

const combinedHistory = computed(() => {
  return [...notifications.value, ...borrowers.value].sort((a, b) => (b.createdAt?.seconds || 0) - (a.createdAt?.seconds || 0));
});

const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));

const isStatus = (current, target) => (current || '').toString().toLowerCase().trim().includes(target.toLowerCase());
const getStatusIconClass = (status) => isStatus(status, 'approve') ? 'bg-green-500/10 text-green-500' : isStatus(status, 'decline') ? 'bg-red-500/10 text-red-500' : 'bg-zinc-800 text-zinc-500';
const getTextStatusColor = (status) => isStatus(status, 'approve') ? 'text-green-500' : isStatus(status, 'decline') ? 'text-red-500' : 'text-zinc-600';

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
  dateError.value = (day === 0 || day === 6) ? "Weekends Restricted" : "";
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
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.standard-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
  border-color: rgba(255,255,255,0.08);
}

.overdue-card {
  background: linear-gradient(145deg, rgba(220,38,38,0.1) 0%, rgba(220,38,38,0.05) 100%);
  border-color: rgba(220,38,38,0.3);
}

.page-enter-active, .page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.4s ease; }
.slide-up-enter-from { opacity: 0; transform: translate(-50%, -10px); }
::-webkit-scrollbar { display: none; }
</style>