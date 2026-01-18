<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40 text-left">
    
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-lg shadow-[0_0_20px_rgba(37,99,235,0.4)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
          </svg>
        </div>
        <div>
          <h1 class="text-sm font-bold tracking-tighter uppercase leading-none">Admin Central</h1>
          <p class="text-[10px] font-black text-blue-500 mt-1 uppercase tracking-widest">{{ currentTimeDisplay }}</p>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <button @click="$emit('logout')" class="text-zinc-500 hover:text-red-500 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 py-4">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Metrics</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Overview</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem]">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Inventory</p>
              <p class="text-4xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem]">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Loans</p>
              <p class="text-4xl font-bold tracking-tighter text-amber-500">{{ borrowers.length }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'inventory'" key="inventory" class="py-4">
          <section class="mb-8 flex justify-between items-end">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Asset Management</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Inventory</h2>
            </div>
            <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
            </button>
          </section>
          
          <div class="space-y-2">
            <div v-for="book in books" :key="book.id" class="p-6 bg-zinc-950 border border-white/5 rounded-[1.5rem] flex items-center justify-between">
              <h3 class="text-base font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
              <button @click="deleteBook(book.id)" class="text-zinc-800 hover:text-red-500 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'requests'" key="requests" class="py-10">
          <section class="mb-8">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Queue Management</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Approvals</h2>
          </section>

          <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-950 border border-white/5 p-8 rounded-[2.5rem] mb-6">
            <h3 class="text-2xl font-bold tracking-tighter uppercase leading-none mb-3">{{ req.bookTitle }}</h3>
            <p class="text-[10px] text-blue-500 font-bold uppercase tracking-widest mb-6">{{ req.userEmail }}</p>
            <div class="flex gap-3">
              <button @click="approveRequest(req)" class="flex-1 py-4 bg-white text-black rounded-xl font-black text-[10px] uppercase">Authorize</button>
              <button @click="declineRequest(req.id)" class="flex-1 py-4 bg-zinc-900 text-red-500 rounded-xl font-black text-[10px] uppercase">Decline</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="py-10">
          <section class="mb-8">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Live Tracking</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Borrowers</h2>
          </section>
          
          <div v-for="person in borrowers" :key="person.id" 
               class="p-8 bg-zinc-950 rounded-[2.5rem] mb-4 flex justify-between items-center border border-white/5">
            <div class="flex-1">
              <h3 class="text-lg font-black uppercase tracking-tighter mb-1">{{ person.bookTitle }}</h3>
              <p class="text-[10px] font-bold uppercase opacity-60 tracking-widest mb-4">{{ person.userEmail }}</p>
              <p class="text-[12px] font-mono text-blue-500 uppercase tracking-tighter">{{ person.returnSchedule }} — 07:30 AM</p>
            </div>
            <button @click="markAsReturned(person)" 
                    class="px-8 py-4 rounded-xl text-[10px] font-black uppercase bg-white text-black active:scale-95 transition-all">
              Return
            </button>
          </div>
        </div>

        <div v-else-if="activeTab === 'logs'" key="logs" class="py-10">
          <section class="mb-8">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Audit Record</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">History</h2>
          </section>
          <div class="space-y-3">
            <div v-for="log in historyLogs" :key="log.id" class="p-6 bg-zinc-950 border border-white/5 rounded-[1.5rem] flex justify-between items-center">
              <div>
                <p class="text-[11px] font-bold uppercase tracking-tight mb-0.5">{{ log.bookTitle }}</p>
                <p class="text-[9px] text-zinc-500 uppercase tracking-widest font-black">{{ log.userEmail }}</p>
              </div>
              <span class="text-[8px] px-3 py-1 rounded-full font-black uppercase tracking-widest border" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
            </div>
          </div>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 w-full max-w-[360px] px-6">
      <nav class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-full p-1.5 flex items-center justify-between shadow-2xl">
        <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'logs']" :key="tab" @click="activeTab = tab" 
                :class="activeTab === tab ? 'bg-white text-black' : 'text-zinc-500'" 
                class="w-11 h-11 rounded-full flex items-center justify-center transition-all duration-300 relative">
          <svg v-if="tab === 'dashboard'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          <svg v-if="tab === 'inventory'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
          <svg v-if="tab === 'requests'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          <svg v-if="tab === 'borrowers'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0" /></svg>
          <svg v-if="tab === 'logs'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute top-0 right-0 w-3.5 h-3.5 bg-blue-600 rounded-full border-2 border-black flex items-center justify-center text-[7px] font-black">{{ pendingRequests.length }}</div>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full">
          <h2 class="text-3xl font-bold tracking-tighter mb-8 uppercase apple-gradient">Add Asset</h2>
          <input v-model="newBook.title" type="text" placeholder="Entry Title" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold mb-10 uppercase" @keyup.enter="addBook" />
          <div class="flex gap-3">
            <button @click="addBook" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px]">Submit</button>
            <button @click="showAddModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px]">Abort</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { db } from './lib/firebase';
import { collection, onSnapshot, addDoc, deleteDoc, doc, updateDoc, serverTimestamp, query, orderBy } from "firebase/firestore";

const activeTab = ref('dashboard');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);
const showAddModal = ref(false);
const newBook = ref({ title: '' });
const currentTimeDisplay = ref('');

let clockInterval;
const updateClock = () => {
  const now = new Date();
  currentTimeDisplay.value = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' });
};

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  // Sync Data
  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ docId: d.id, ...d.data() })));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => historyLogs.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  
  // Dito natin kukunin ang totoong Document ID ng borrowers
  onSnapshot(collection(db, "borrowers"), (s) => {
    borrowers.value = s.docs.map(d => ({ 
      id: d.id, // Ito ang Firestore Document ID na kailangan para sa deleteDoc
      ...d.data() 
    }));
  });
});

onUnmounted(() => clearInterval(clockInterval));

const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

const addBook = async () => {
  if (!newBook.value.title.trim()) return;
  await addDoc(collection(db, "books"), { title: newBook.value.title.toUpperCase(), createdAt: serverTimestamp() });
  newBook.value.title = '';
  showAddModal.value = false;
};

const deleteBook = async (id) => {
  await deleteDoc(doc(db, "books", id));
};

const approveRequest = async (req) => {
  await updateDoc(doc(db, "notifications", req.id), { status: 'approved' });
  // Kapag inapprove, gumagawa ng bagong doc sa borrowers
  await addDoc(collection(db, "borrowers"), { 
    ...req, 
    status: 'active', 
    approvedAt: serverTimestamp() 
  });
  await addDoc(collection(db, "history"), { ...req, status: 'approved', createdAt: serverTimestamp() });
};

const declineRequest = async (id) => {
  await updateDoc(doc(db, "notifications", id), { status: 'declined' });
};

const markAsReturned = async (person) => {
  try {
    // 1. Send to history collection
    await addDoc(collection(db, "history"), {
      bookTitle: person.bookTitle,
      userEmail: person.userEmail,
      userId: person.userId,
      returnSchedule: person.returnSchedule,
      status: 'returned',
      createdAt: serverTimestamp()
    });

    // 2. Delete from borrowers collection using the Firestore Document ID
    await deleteDoc(doc(db, "borrowers", person.id));
    
    console.log("Success: Asset removed from live borrowers.");
  } catch (err) {
    console.error("Delete failed:", err);
    alert("System Error: Could not remove record.");
  }
};

const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s.includes('approved') || s.includes('returned')) return 'text-green-500 bg-green-500/10 border-green-500/20';
  if (s.includes('declined')) return 'text-red-500 bg-red-500/10 border-red-500/20';
  return 'text-zinc-500';
};
</script>

<style scoped>
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.page-enter-active, .page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
</style>