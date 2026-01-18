<template>
  <div class="min-h-screen bg-black text-white font-sans selection:bg-blue-500/30 overflow-x-hidden pb-40">
    
    <!-- Header -->
    <header class="p-6 flex justify-between items-center sticky top-0 z-30 bg-black/80 backdrop-blur-md border-b border-white/5">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
          </svg>
        </div>
        <div>
          <h1 class="text-sm font-bold tracking-tighter uppercase italic">Control Panel</h1>
          <p class="text-[10px] font-black text-blue-500 uppercase tracking-widest">{{ currentTimeDisplay }}</p>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="hidden md:flex items-center gap-2 bg-zinc-900 px-4 py-2 rounded-full border border-white/5">
          <div class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-[10px] font-bold uppercase tracking-widest text-zinc-400">Database Encrypted</span>
        </div>
        <button @click="$emit('logout')" class="p-2 hover:bg-red-500/10 rounded-full transition-all group">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-zinc-500 group-hover:text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 mt-8">
      <transition name="page" mode="out-in">
        
        <!-- DASHBOARD TAB -->
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6">
          <section>
            <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-1">System Intelligence</p>
            <h2 class="text-6xl font-black tracking-tighter uppercase italic apple-gradient">Snapshot</h2>
          </section>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="stat in stats" :key="stat.label" 
                 class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem] hover:bg-zinc-900 transition-all">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-2 italic">{{ stat.label }}</p>
              <p class="text-4xl font-bold tracking-tighter" :class="stat.color">{{ stat.value }}</p>
            </div>
          </div>

          <section v-if="pendingRequests.length > 0" @click="activeTab = 'requests'" 
                   class="group bg-blue-600 p-8 rounded-[3rem] cursor-pointer hover:bg-blue-500 transition-all relative overflow-hidden active:scale-[0.98]">
             <div class="relative z-10 text-black flex justify-between items-center">
               <div>
                 <h3 class="text-3xl font-black tracking-tighter mb-1 italic uppercase">Action Required</h3>
                 <p class="text-black/60 text-[11px] tracking-widest font-bold uppercase">{{ pendingRequests.length }} requests pending approval</p>
               </div>
               <div class="w-16 h-16 bg-black text-white rounded-2xl flex items-center justify-center font-black text-2xl shadow-2xl group-hover:rotate-12 transition-transform">
                 {{ pendingRequests.length }}
               </div>
             </div>
          </section>
        </div>

        <!-- INVENTORY TAB -->
        <div v-else-if="activeTab === 'inventory'" key="inventory">
          <section class="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Asset Repository</p>
              <h2 class="text-6xl font-black tracking-tighter uppercase apple-gradient italic leading-none">Catalog</h2>
            </div>
            <div class="flex gap-3">
              <input v-model="searchQuery" type="text" placeholder="Search assets..." 
                     class="bg-zinc-900 border border-white/10 rounded-2xl px-5 text-sm focus:border-blue-500 outline-none transition-all" />
              <button v-if="selectedBooks.length > 0" @click="showDeleteModal = true" class="w-14 h-14 bg-red-600/20 text-red-500 rounded-2xl flex items-center justify-center border border-red-500/20 hover:bg-red-600 hover:text-white transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
              <button @click="showAddModal = true" class="w-14 h-14 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
              </button>
            </div>
          </section>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div v-for="book in filteredBooks" :key="book.id" @click="toggleSelectBook(book.id)" 
                 :class="selectedBooks.includes(book.id) ? 'border-blue-600 bg-blue-600/10' : 'border-white/5 bg-zinc-950'" 
                 class="p-6 rounded-[2rem] flex items-center justify-between border transition-all cursor-pointer group">
              <div class="flex items-center gap-5">
                <div class="w-6 h-6 rounded-lg border-2 border-zinc-800 flex items-center justify-center transition-colors" :class="selectedBooks.includes(book.id) ? 'bg-blue-600 border-blue-600' : ''">
                   <svg v-if="selectedBooks.includes(book.id)" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                </div>
                <div>
                  <h3 class="text-lg font-bold tracking-tight uppercase italic leading-none group-hover:text-blue-400 transition-colors">{{ book.title }}</h3>
                  <p class="text-[9px] text-zinc-600 uppercase mt-2 tracking-widest font-black">UID: {{ book.id.slice(0,12) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Add other tabs similarly... -->

      </transition>
    </main>

    <!-- NAVIGATION DOCK -->
    <div class="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-[440px] px-6">
      <nav class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-[2.5rem] p-3 flex items-center justify-between shadow-2xl">
        <button v-for="item in navItems" :key="item.tab" @click="activeTab = item.tab" 
                :class="activeTab === item.tab ? 'bg-white text-black scale-110 shadow-xl' : 'text-zinc-500 hover:text-zinc-200'" 
                class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 relative">
          <component :is="item.icon" class="w-5 h-5" />
          <div v-if="item.tab === 'requests' && pendingRequests.length > 0" 
               class="absolute -top-1 -right-1 w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center text-[10px] font-black text-white border-2 border-zinc-900 animate-pulse">
               {{ pendingRequests.length }}
          </div>
        </button>
      </nav>
    </div>

    <!-- MODALS (Using Teleport for better layering) -->
    <teleport to="body">
      <transition name="fade">
        <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 backdrop-blur-xl p-6">
          <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl">
            <h2 class="text-3xl font-black tracking-tighter mb-8 uppercase italic apple-gradient">New Asset</h2>
            <input v-model="newBook.title" type="text" placeholder="Title" 
                   class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold focus:border-blue-600 mb-8 uppercase italic" 
                   @keyup.enter="addBook" />
            <div class="flex gap-3">
              <button @click="addBook" :disabled="isLoading" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest disabled:opacity-50">
                {{ isLoading ? 'Processing...' : 'Confirm' }}
              </button>
              <button @click="showAddModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px]">Back</button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, markRaw } from 'vue';
import { db } from './lib/firebase';
import { 
  collection, onSnapshot, addDoc, deleteDoc, doc, 
  updateDoc, serverTimestamp, query, orderBy, writeBatch 
} from "firebase/firestore";

// --- State ---
const activeTab = ref('dashboard');
const isLoading = ref(false);
const searchQuery = ref('');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);
const selectedBooks = ref([]);
const showAddModal = ref(false);
const showDeleteModal = ref(false);
const newBook = ref({ title: '' });
const currentTimeDisplay = ref('');

// --- Icons (Using standard SVG components or Heroicons) ---
const DashboardIcon = markRaw({ template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>'});
// ... define other icons ...

const navItems = [
  { tab: 'dashboard', icon: DashboardIcon },
  // ... rest of items
];

// --- Computed ---
const stats = computed(() => [
  { label: 'Inventory', value: books.value.length, color: 'text-white' },
  { label: 'Users', value: users.value.length, color: 'text-blue-500' },
  { label: 'Loans', value: borrowers.value.length, color: 'text-amber-500' },
  { label: 'Alerts', value: pendingRequests.value.length, color: 'text-red-500' }
]);

const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value;
  return books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
});

// --- Methods ---
const updateClock = () => {
  currentTimeDisplay.value = new Date().toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' });
};

const addBook = async () => {
  if (!newBook.value.title.trim()) return;
  isLoading.value = true;
  try {
    await addDoc(collection(db, "books"), { 
      title: newBook.value.title.toUpperCase(), 
      createdAt: serverTimestamp(),
      status: 'available' 
    });
    newBook.value.title = '';
    showAddModal.value = false;
  } catch (e) {
    console.error("Error adding book:", e);
  } finally {
    isLoading.value = false;
  }
};

const toggleSelectBook = (id) => {
  const idx = selectedBooks.value.indexOf(id);
  if (idx > -1) selectedBooks.value.splice(idx, 1);
  else selectedBooks.value.push(id);
};

const deleteSelectedBooks = async () => {
  const batch = writeBatch(db);
  selectedBooks.value.forEach(id => batch.delete(doc(db, "books", id)));
  await batch.commit();
  selectedBooks.value = [];
  showDeleteModal.value = false;
};

// --- Lifecycle ---
let clockInterval;
onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  // Unified listeners
  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "borrowers"), (s) => borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
});

onUnmounted(() => clearInterval(clockInterval));
</script>

<style scoped>
.apple-gradient {
  background: linear-gradient(180deg, #fff 30%, rgba(255,255,255,0.2) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-enter-active, .page-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.page-enter-from { opacity: 0; transform: scale(0.98) translateY(10px); }
.page-leave-to { opacity: 0; transform: scale(1.02) translateY(-10px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>