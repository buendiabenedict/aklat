<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40">
    
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-lg shadow-[0_0_20px_rgba(37,99,235,0.4)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.744c0 5.548 4.075 10.14 9 10.856 4.925-.716 9-5.308 9-10.856 0-1.31-.21-2.57-.598-3.744A11.959 11.959 0 0112 2.714z" />
          </svg>
        </div>
        <h1 class="text-lg font-bold tracking-tighter uppercase">Admin Central</h1>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900 px-3 py-1.5 rounded-full border border-white/5">
        <div class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
        <span class="text-[9px] font-bold uppercase tracking-widest text-zinc-400">Root Access</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 py-4 text-left">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Overview</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Dashboard</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Total Assets</p>
              <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Loans</p>
              <p class="text-3xl font-bold tracking-tighter text-blue-500">{{ borrowers.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl col-span-2">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Total History Logs</p>
              <p class="text-3xl font-bold tracking-tighter text-zinc-300">{{ historyLogs.length }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'inventory'" key="inventory" class="py-4 text-left">
          <section class="mb-6 flex justify-between items-end">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Repository</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Inventory</h2>
            </div>
            <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4.5v15m7.5-7.5h-15" /></svg>
            </button>
          </section>
          
          <div class="space-y-2">
            <div v-for="book in books" :key="book.id" class="bg-zinc-950 border border-white/5 p-4 rounded-xl flex items-center justify-between hover:border-white/10 transition-all">
              <div>
                <h3 class="text-sm font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
                <p class="text-[8px] text-zinc-600 uppercase mt-1 tracking-widest">ID: {{ book.id.slice(0,8) }}</p>
              </div>
              <button @click="deleteBook(book.id)" class="p-2 text-zinc-800 hover:text-red-500 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'requests'" key="requests" class="py-10 text-left">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Queue</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Requests</h2>
          </section>

          <div v-if="pendingRequests.length === 0" class="p-16 border border-dashed border-white/10 rounded-[2rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">Clear Queue</p>
          </div>

          <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-950 border border-white/10 p-6 rounded-3xl mb-4">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-lg font-bold tracking-tighter uppercase leading-none">{{ req.bookTitle }}</h3>
                <p class="text-[9px] text-blue-500 font-bold uppercase tracking-widest mt-1">{{ req.userEmail }}</p>
              </div>
              <span class="text-[8px] font-mono text-zinc-700">{{ formatTimestamp(req.createdAt) }}</span>
            </div>
            <div class="flex gap-2">
              <button @click="approveRequest(req)" class="flex-1 py-3 bg-white text-black rounded-xl font-black text-[9px] uppercase tracking-widest">Approve</button>
              <button @click="declineRequest(req.id)" class="flex-1 py-3 bg-zinc-900 text-red-500 rounded-xl font-black text-[9px] uppercase tracking-widest border border-red-500/10">Decline</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="py-10 text-left">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Live Assets</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Borrowers</h2>
          </section>

          <div v-if="borrowers.length === 0" class="p-16 border border-dashed border-white/10 rounded-[2rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">No Active Borrowers</p>
          </div>

          <div v-for="person in borrowers" :key="person.id" class="bg-white text-black p-5 rounded-2xl mb-3 flex justify-between items-center shadow-xl border-l-[6px] border-blue-600">
            <div>
              <h3 class="text-sm font-black uppercase tracking-tighter leading-none">{{ person.bookTitle }}</h3>
              <p class="text-[9px] font-bold text-zinc-400 uppercase mt-1">{{ person.userEmail }}</p>
            </div>
            <button @click="markAsReturned(person)" class="px-4 py-2 bg-black text-white rounded-lg text-[8px] font-black uppercase tracking-widest">Returned</button>
          </div>
        </div>

        <div v-else-if="activeTab === 'logs'" key="logs" class="py-10 text-left">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Historical Archive</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">System Logs</h2>
          </section>
          
          <div v-if="historyLogs.length === 0" class="p-16 border border-dashed border-white/10 rounded-[2rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">No Records in History</p>
          </div>

          <div class="space-y-2">
            <div v-for="log in historyLogs" :key="log.id" class="p-4 bg-zinc-950 border border-white/5 rounded-xl flex justify-between items-center hover:bg-zinc-900 transition-colors">
              <div class="max-w-[70%]">
                <p class="text-[10px] font-bold uppercase tracking-tight truncate">{{ log.bookTitle || 'Archived Entry' }}</p>
                <div class="flex items-center gap-2 mt-0.5">
                  <span class="text-[7px] font-black tracking-widest uppercase px-1.5 py-0.5 rounded" :class="getLogBadgeClass(log.status)">
                    {{ log.status || 'Archived' }}
                  </span>
                  <p class="text-[8px] font-bold text-zinc-500 truncate">{{ log.userEmail }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-[8px] font-mono text-zinc-700 uppercase">{{ formatTimestamp(log.createdAt) }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 text-center">
          <section class="text-left mb-10">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Identity</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Admin Profile</h2>
          </section>

          <div class="w-24 h-24 bg-blue-600 border border-blue-400 mx-auto rounded-[2.5rem] flex items-center justify-center text-3xl font-black mb-4 shadow-2xl">A</div>
          <h2 class="text-2xl font-bold tracking-tighter uppercase">{{ auth.currentUser?.email }}</h2>
          <p class="text-blue-500 text-[9px] font-bold uppercase tracking-[0.4em] mt-2">System Administrator</p>
          
          <div class="max-w-xs mx-auto pt-20">
            <button @click="showLogoutModal = true" class="w-full py-4 bg-zinc-900 text-red-500 rounded-2xl font-black uppercase text-[10px] tracking-widest border border-red-500/10 active:bg-red-600 active:text-white transition-all">Sign Out Admin Session</button>
          </div>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-[340px] px-2">
      <nav class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-full p-1.5 flex items-center justify-between shadow-2xl">
        <button @click="activeTab = 'dashboard'" :class="activeTab === 'dashboard' ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25h-2.25a2.25 2.25 0 01-2.25-2.25v-2.25z" /></svg>
        </button>
        <button @click="activeTab = 'inventory'" :class="activeTab === 'inventory' ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" /></svg>
        </button>
        <button @click="activeTab = 'requests'" :class="activeTab === 'requests' ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all relative">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>
          <div v-if="pendingRequests.length > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-amber-500 rounded-full flex items-center justify-center text-[8px] font-black text-black border-2 border-black">{{ pendingRequests.length }}</div>
        </button>
        <button @click="activeTab = 'borrowers'" :class="activeTab === 'borrowers' ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
        </button>
        <button @click="activeTab = 'logs'" :class="activeTab === 'logs' ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </button>
        <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 rounded-full flex items-center justify-center transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-xl font-bold tracking-tighter mb-6 uppercase apple-gradient text-center">New Asset</h2>
          <input v-model="newBookTitle" type="text" placeholder="Entry Title" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-4 px-6 text-white outline-none font-bold mb-4" />
          <button @click="addBook" :disabled="!newBookTitle" class="w-full py-4 bg-white text-black rounded-2xl font-black uppercase text-[10px] tracking-widest active:scale-95 transition-all">Initialize Entry</button>
          <button @click="showAddModal = false" class="w-full py-4 text-zinc-600 font-bold uppercase text-[9px] mt-1">Cancel</button>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-6 uppercase tracking-tighter leading-none">Terminate?</h3>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="executeLogout" class="flex-1 py-4 rounded-2xl bg-red-600 text-white font-black text-[10px] uppercase">Yes</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineEmits } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, addDoc, deleteDoc, doc, updateDoc, serverTimestamp, query, orderBy } from "firebase/firestore";
import { signOut } from "firebase/auth";

const emit = defineEmits(['logout']);

const activeTab = ref('dashboard');
const books = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]); // Dedicated ref for the history collection
const showAddModal = ref(false);
const showLogoutModal = ref(false);
const newBookTitle = ref('');

onMounted(() => {
  // 1. Fetch Books
  onSnapshot(collection(db, "books"), (s) => {
    books.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });

  // 2. Fetch Notifications (Pending Requests)
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => {
    notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });

  // 3. Fetch History (System Logs)
  // FIX: Explicitly fetching from the 'history' collection as confirmed
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => {
    historyLogs.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
    console.log("History records found:", historyLogs.value.length);
  });

  // 4. Fetch Active Borrowers
  onSnapshot(collection(db, "borrowers"), (s) => {
    borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });
});

const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

const getLogBadgeClass = (status) => {
  if (!status) return 'bg-zinc-900 text-zinc-500';
  const s = status.toLowerCase();
  if (s.includes('approve') || s.includes('returned')) return 'bg-green-500/10 text-green-500';
  if (s.includes('decline')) return 'bg-red-500/10 text-red-500';
  return 'bg-zinc-900 text-zinc-400';
};

const formatTimestamp = (ts) => {
  if (!ts) return 'Archived';
  const date = new Date(ts.seconds * 1000);
  return date.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ' ' + 
         date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const addBook = async () => {
  if (!newBookTitle.value) return;
  await addDoc(collection(db, "books"), { title: newBookTitle.value, createdAt: serverTimestamp() });
  newBookTitle.value = '';
  showAddModal.value = false;
};

const deleteBook = async (id) => {
  if (confirm('Delete asset permanently?')) await deleteDoc(doc(db, "books", id));
};

const approveRequest = async (req) => {
  // Update Notification
  await updateDoc(doc(db, "notifications", req.id), { status: 'approved' });
  
  // Add to Borrowers
  await addDoc(collection(db, "borrowers"), {
    ...req,
    status: 'approved',
    approvedAt: serverTimestamp()
  });

  // Log to History
  await addDoc(collection(db, "history"), {
    bookTitle: req.bookTitle,
    userEmail: req.userEmail,
    status: 'approved',
    createdAt: serverTimestamp()
  });
};

const declineRequest = async (id) => {
  const req = notifications.value.find(n => n.id === id);
  await updateDoc(doc(db, "notifications", id), { status: 'declined' });
  
  // Log to History
  await addDoc(collection(db, "history"), {
    bookTitle: req?.bookTitle || 'Unknown',
    userEmail: req?.userEmail || 'Unknown',
    status: 'declined',
    createdAt: serverTimestamp()
  });
};

const markAsReturned = async (person) => {
  await deleteDoc(doc(db, "borrowers", person.id));
  
  // Log Return to History
  await addDoc(collection(db, "history"), {
    bookTitle: person.bookTitle,
    userEmail: person.userEmail,
    status: 'returned',
    createdAt: serverTimestamp()
  });
};

const executeLogout = async () => {
  await signOut(auth);
  emit('logout');
};
</script>

<style scoped>
/* HEADERS NO LONGER ITALIC */
.apple-gradient {
  background: linear-gradient(180deg, #ffffff 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.page-enter-active, .page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
::-webkit-scrollbar { display: none; }
</style>