
<template>
  <div class="min-h-screen bg-zinc-950 text-white font-ios selection:bg-white/20 overflow-x-hidden text-left relative">
    
    <!-- AMBIENT BACKGROUND: FLOATING BLINKING CIRCLES -->
    <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <div v-for="i in 20" :key="i" 
           class="ambient-circle" 
           :style="getCircleStyle(i)">
      </div>
    </div>

    <!-- WELCOME SEQUENCE -->
    <transition name="welcome-fade" @after-leave="onWelcomeFinished">
      <div v-if="showWelcome" class="fixed inset-0 z-[300] bg-zinc-950 flex flex-col items-center justify-center p-6">
        <div class="text-center">
          <p class="text-[10px] font-black text-white uppercase tracking-[0.5em] mb-4 animate-pulse opacity-50">System Initialized</p>
          <h1 class="text-4xl md:text-6xl font-bold tracking-tighter uppercase apple-gradient mb-2">Access Granted</h1>
          <h2 class="text-2xl md:text-4xl font-black tracking-tighter uppercase opacity-20">Member Session</h2>
        </div>
      </div>
    </transition>

    <!-- NAVIGATION BAR -->
    <div v-if="contentVisible" class="fixed bottom-8 left-0 right-0 z-[200] flex justify-center px-6 pointer-events-none">
      <nav class="bg-zinc-900/80 backdrop-blur-2xl border border-white/10 rounded-full p-2 flex items-center justify-between shadow-[0_25px_50px_-12px_rgba(0,0,0,0.8)] w-full max-w-sm pointer-events-auto animate-nav-in">
        <button v-for="tab in ['home', 'loans', 'notifications']" 
                :key="tab" @click="activeTab = tab" 
                :class="activeTab === tab ? 'bg-white text-black scale-95 shadow-lg' : 'text-zinc-500 hover:text-zinc-300'" 
                class="w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 relative group">
          
          <svg v-if="tab === 'home'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          <svg v-if="tab === 'loans'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
          <svg v-if="tab === 'notifications'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          
          <div v-if="tab === 'notifications' && unreadCount > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-blue-500 text-white rounded-full flex items-center justify-center text-[10px] font-black border-2 border-zinc-900">
            {{ unreadCount }}
          </div>
        </button>
      </nav>
    </div>

    <!-- UI LAYER -->
    <div v-if="contentVisible" class="animate-content-in relative min-h-screen z-10">
      
      <header class="p-6 flex justify-between items-center relative z-20">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-zinc-900 border border-white/10 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-bold tracking-tighter uppercase leading-none italic">Library Access</h1>
            <p class="text-[10px] font-black text-white mt-1 uppercase tracking-widest opacity-40 italic">Member Portal</p>
          </div>
        </div>
        
        <div class="flex items-center gap-4">
          <button @click="$emit('logout')" class="px-3 py-2 bg-red-600/10 text-red-500 rounded-lg font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all border border-red-500/20">Sign Out</button>
        </div>
      </header>

      <main class="max-w-5xl mx-auto px-6 relative z-10 h-[calc(100vh-140px)]">
        <div class="h-full overflow-y-auto custom-scrollbar pb-16">
          <transition name="page" mode="out-in">
            
            <!-- HOME / EXPLORE -->
            <div v-if="activeTab === 'home'" key="home" class="space-y-6 pt-4">
              <section>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1 italic">Digital Archive</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none italic">Explore</h2>
              </section>

              <div class="grid grid-cols-2 gap-3">
                <div class="bg-zinc-900/50 backdrop-blur-sm border border-white/5 p-6 rounded-[2rem]">
                  <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 italic">Total Collection</p>
                  <p class="text-4xl font-bold tracking-tighter">{{ books.length }}</p>
                </div>
                <div @click="activeTab = 'loans'" class="bg-zinc-900/50 backdrop-blur-sm border border-white/5 p-6 rounded-[2rem] cursor-pointer active:scale-95 transition-all">
                  <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 italic">Secured</p>
                  <p class="text-4xl font-bold tracking-tighter text-blue-500">{{ approvedLoans.length }}</p>
                </div>
              </div>

              <div class="space-y-3">
                <p class="text-zinc-700 text-[9px] font-black uppercase tracking-[0.3em] mb-4">Available Assets</p>
                <div v-for="book in books" :key="book.id" 
                     class="p-6 bg-zinc-900/50 backdrop-blur-sm border border-white/5 rounded-[2rem] flex justify-between items-center transition-all group">
                  <div>
                    <h3 class="text-lg font-bold tracking-tighter uppercase italic">{{ book.title }}</h3>
                    <p class="text-[8px] text-zinc-600 font-bold uppercase tracking-widest mt-1.5 flex items-center gap-1">
                      <span class="w-1 h-1 bg-green-500 rounded-full"></span>
                      Available for checkout
                    </p>
                  </div>
                  <button @click="openRequestModal(book)" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-2xl active:scale-90 transition-all">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- LOANS -->
            <div v-else-if="activeTab === 'loans'" key="loans" class="pt-4 space-y-6">
              <section>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1 italic">Active Sessions</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient leading-none">Borrowed</h2>
              </section>

              <div v-if="approvedLoans.length === 0" class="py-20 text-center text-zinc-800 text-[10px] font-black uppercase tracking-[0.5em]">Inventory Empty</div>

              <div v-for="loan in approvedLoans" :key="loan.id" 
                   :class="isOverdue(loan.returnSchedule) ? 'overdue-card' : 'standard-card'"
                   class="p-8 rounded-[2.5rem] mb-4 border shadow-2xl relative overflow-hidden transition-all group active:scale-[0.98]">
                
                <div class="relative z-10">
                  <div class="flex items-center justify-between mb-8">
                    <div class="flex items-center gap-2">
                      <div class="w-2 h-2 rounded-full" :class="isOverdue(loan.returnSchedule) ? 'bg-red-500 animate-pulse shadow-[0_0_10px_rgba(239,68,68,0.5)]' : 'bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]'"></div>
                      <p class="text-[9px] font-black uppercase tracking-widest opacity-40 italic">Secured Possession</p>
                    </div>
                    <div class="text-[9px] font-black font-mono px-3 py-1 bg-white/5 rounded-full border border-white/5">REF: {{ loan.id?.slice(-6).toUpperCase() }}</div>
                  </div>
                  
                  <h3 class="text-3xl font-bold tracking-tighter uppercase italic leading-tight mb-8">{{ loan.bookTitle }}</h3>
                  
                  <div class="flex flex-col gap-2">
                    <p class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest italic">Deadline Protocol</p>
                    <div class="flex items-center gap-3">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="text-2xl font-black font-mono tracking-tighter uppercase text-white">
                        {{ loan.returnSchedule }} <span class="text-blue-500">— 07:30 AM</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- NOTIFICATIONS -->
            <div v-else-if="activeTab === 'notifications'" key="notifications" class="pt-4 space-y-6">
              <section>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1 italic">Status Logs</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase italic apple-gradient">Requests</h2>
              </section>

              <div v-if="notifications.length === 0" class="py-20 text-center text-zinc-800 text-[10px] font-black uppercase tracking-[0.5em]">No History</div>

              <div class="space-y-3">
                <div v-for="notif in notifications" :key="notif.id" 
                     class="p-6 bg-zinc-900/50 backdrop-blur-sm border border-white/5 rounded-[1.5rem] flex justify-between items-center transition-all">
                  <div>
                    <h4 class="text-base font-bold uppercase italic tracking-tighter">{{ notif.bookTitle }}</h4>
                    <p class="text-[9px] text-zinc-600 uppercase tracking-widest mt-1.5 font-bold italic">Schedule: {{ notif.returnSchedule }}</p>
                  </div>
                  <div class="flex flex-col items-end gap-2">
                    <span class="text-[8px] px-3 py-1 rounded-full font-black uppercase tracking-[0.2em] border italic"
                          :class="getStatusClass(notif.status)">
                      {{ notif.status }}
                    </span>
                    <p class="text-[7px] text-zinc-700 font-mono">{{ formatTimestamp(notif.createdAt) }}</p>
                  </div>
                </div>
              </div>
            </div>

          </transition>
        </div>
      </main>
    </div>

    <!-- REQUEST MODAL -->
    <transition name="fade">
      <div v-if="showRequestModal" class="fixed inset-0 z-[250] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl">
          <div class="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mb-6 border border-white/5">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-white/40" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
          </div>
          <h2 class="text-3xl font-bold tracking-tighter mb-1 uppercase italic apple-gradient">Request</h2>
          <p class="text-zinc-500 text-[10px] font-black uppercase tracking-widest mb-10 italic">{{ selectedBook?.title }}</p>
          
          <div class="space-y-6 mb-12">
            <div class="flex flex-col gap-2.5">
              <label class="text-[9px] font-black uppercase tracking-[0.4em] text-zinc-600 ml-1 italic">Return Date</label>
              <input v-model="requestDate" type="date" class="w-full bg-zinc-950 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold focus:border-white transition-all uppercase appearance-none" />
            </div>
            <p class="text-zinc-700 text-[8px] font-bold uppercase tracking-widest text-center">* Default return time is 07:30 AM on the selected date.</p>
          </div>
          
          <div class="flex gap-3">
            <button @click="submitRequest" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all shadow-xl">Apply</button>
            <button @click="showRequestModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineEmits, onUnmounted } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, addDoc, query, where, serverTimestamp, orderBy } from "firebase/firestore";
import { onAuthStateChanged } from "firebase/auth";

const emit = defineEmits(['logout']);

const showWelcome = ref(true);
const contentVisible = ref(false);
const activeTab = ref('home');
const books = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const currentUser = ref(null);
const showRequestModal = ref(false);
const selectedBook = ref(null);
const requestDate = ref('');

// Logic for Welcome transition
const onWelcomeFinished = () => { 
  contentVisible.value = true; 
};

// Generate unique styles for ambient circles (Matches admin.vue)
const getCircleStyle = (index) => {
  const size = Math.random() * 200 + 100;
  const left = Math.random() * 100;
  const top = Math.random() * 100;
  const delay = Math.random() * 5;
  const duration = 10 + Math.random() * 20;
  const moveX = (Math.random() - 0.5) * 100;
  const moveY = (Math.random() - 0.5) * 100;

  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    top: `${top}%`,
    '--move-x': `${moveX}px`,
    '--move-y': `${moveY}px`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  };
};

onMounted(() => {
  setTimeout(() => { showWelcome.value = false; }, 1500);

  // Sync Books
  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  
  // Auth state listener
  onAuthStateChanged(auth, (user) => {
    if (user) {
      currentUser.value = user;
      // Sync personal notifications
      onSnapshot(query(collection(db, "notifications"), where("userId", "==", user.uid), orderBy("createdAt", "desc")), (s) => {
        notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      });
      // Sync personal active loans
      onSnapshot(query(collection(db, "borrowers"), where("userId", "==", user.uid)), (s) => {
        borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
      });
    }
  });
});

// Computed
const approvedLoans = computed(() => {
  const approvedNotifs = notifications.value.filter(n => n.status === 'approved');
  const all = [...approvedNotifs, ...borrowers.value];
  return Array.from(new Map(all.map(item => [item.bookTitle, item])).values());
});

const unreadCount = computed(() => notifications.value.filter(n => n.status !== 'pending' && n.status !== 'returned').length);

// Logic
const isOverdue = (schedule) => {
  if (!schedule) return false;
  const now = new Date();
  const target = new Date(schedule.replace(/-/g, '/'));
  target.setHours(7, 30, 0, 0); 
  return now.getTime() > target.getTime();
};

const getStatusClass = (status) => {
  const s = status?.toLowerCase();
  if (s === 'approved') return 'border-emerald-500/30 text-emerald-500 bg-emerald-500/5';
  if (s === 'pending') return 'border-blue-500/30 text-blue-500 bg-blue-500/5';
  if (s === 'declined') return 'border-red-500/30 text-red-500 bg-red-500/5';
  return 'border-zinc-800 text-zinc-600';
};

const formatTimestamp = (ts) => {
  if (!ts) return 'just now';
  return new Date(ts.seconds * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const openRequestModal = (book) => {
  selectedBook.value = book;
  showRequestModal.value = true;
};

const submitRequest = async () => {
  if (!requestDate.value || !currentUser.value) return;
  
  await addDoc(collection(db, "notifications"), {
    bookTitle: selectedBook.value.title,
    userId: currentUser.value.uid,
    userEmail: currentUser.value.email,
    returnSchedule: requestDate.value, 
    status: 'pending',
    createdAt: serverTimestamp()
  });

  showRequestModal.value = false;
  activeTab.value = 'notifications';
};
</script>

<style scoped>
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.standard-card { background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%); border-color: rgba(255,255,255,0.05); }
.overdue-card { background: linear-gradient(145deg, rgba(220,38,38,0.1) 0%, rgba(220,38,38,0.03) 100%); border-color: rgba(220,38,38,0.3); }

/* AMBIENT BACKGROUND ANIMATIONS (Matches admin.vue) */
.ambient-circle {
  position: absolute;
  border-radius: 9999px;
  background: white;
  filter: blur(80px);
  opacity: 0;
  animation: float-blink infinite ease-in-out;
}

@keyframes float-blink {
  0%, 100% {
    transform: translate(0, 0);
    opacity: 0.02;
  }
  25% {
    opacity: 0.08;
  }
  50% {
    transform: translate(var(--move-x), var(--move-y));
    opacity: 0.03;
  }
  75% {
    opacity: 0.06;
  }
}

@keyframes navIn { from { opacity: 0; transform: translateY(20px) scale(0.9); } to { opacity: 1; transform: translateY(0) scale(1); } }
.animate-nav-in { animation: navIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; animation-delay: 0.5s; }
@keyframes contentIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-content-in { animation: contentIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards; }
.welcome-fade-leave-active { transition: all 0.8s cubic-bezier(0.65, 0, 0.35, 1); }
.welcome-fade-leave-to { opacity: 0; transform: scale(1.1); filter: blur(20px); }

.page-enter-active, .page-leave-active { transition: all 0.3s ease; }
.page-enter-from { opacity: 0; transform: translateY(5px); }
.page-leave-to { opacity: 0; transform: translateY(-5px); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.custom-scrollbar::-webkit-scrollbar { width: 8px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #555; }
</style>
