<template>
  <div class="fixed inset-0 bg-black text-white font-ios flex overflow-hidden w-full h-full">
    
    <transition name="fade">
      <div v-if="showWelcome" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center">
        <p class="text-zinc-600 uppercase tracking-[0.6em] text-[10px] mb-4 animate-pulse">Library Access Granted</p>
        <h2 class="text-5xl font-bold tracking-tighter">Welcome to AKLAT</h2>
      </div>
    </transition>

    <aside 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']" 
      class="w-72 h-full border-r border-white/10 bg-zinc-950 z-50 flex flex-col transition-all duration-700 ease-in-out shrink-0"
    >
      <div class="h-28 flex items-center px-8 overflow-hidden">
        <div class="w-8 h-8 bg-white rounded-lg shrink-0 shadow-[0_0_15px_rgba(255,255,255,0.2)]"></div>
        <h1 class="ml-4 text-xs font-black tracking-widest uppercase text-white">Aklat Student</h1>
      </div>

      <nav class="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
        <button v-for="item in navItems" :key="item.name" @click="activeTab = item.id"
          class="w-full flex items-center h-14 rounded-xl px-4 transition-all duration-200"
          :class="activeTab === item.id ? 'bg-white text-black' : 'text-zinc-500 hover:text-white'">
          <div class="w-6 h-6 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" :d="item.path" /></svg>
          </div>
          <span class="ml-4 font-bold text-sm tracking-tight">{{ item.name }}</span>
        </button>
      </nav>

      <div class="p-6 border-t border-white/5 space-y-4">
        <div class="flex items-center gap-3 px-2">
          <div class="relative flex h-2 w-2">
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"></span>
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="relative inline-flex rounded-full h-2 w-2"></span>
          </div>
          <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-500 whitespace-nowrap">Cloud: {{ dbStatus }}</p>
        </div>

        <button @click="showLogoutModal = true" class="w-full h-14 flex items-center justify-center rounded-xl text-red-500 hover:bg-red-500/10 transition-all group">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          <span class="ml-3 font-bold text-xs uppercase tracking-widest">Sign Out</span>
        </button>
      </div>
    </aside>

    <main 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']"
      class="flex-1 h-full overflow-y-auto p-8 md:p-16 relative z-10 transition-opacity duration-1000 bg-black"
    >
      <header class="mb-16">
        <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3 flex items-center gap-2">
          {{ currentTime }} 
          <span class="w-1 h-1 bg-zinc-800 rounded-full"></span> 
          System Connected
        </p>
        <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab === 'inventory' ? 'Browse Library' : activeTab }}</h2>
      </header>

      <transition name="fade" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Total Books Available</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ allBooks.length }}</p>
          </div>
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Your Identity</h3>
            <p class="text-xl font-bold tracking-tighter text-white truncate">{{ currentUserEmail }}</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'" class="space-y-8">
          <div class="relative w-full max-w-xl">
             <input v-model="searchQuery" type="text" placeholder="Search for a book title..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white w-full outline-none focus:border-white/30 transition-all" />
          </div>
          
          <div class="border border-white/10 rounded-2xl overflow-hidden bg-zinc-950">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="text-zinc-600 text-[10px] font-black uppercase tracking-[0.3em] border-b border-white/5">
                  <th class="p-8">Book Information</th>
                  <th class="p-8 text-right">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/[0.03]">
                <tr v-for="book in filteredBooks" :key="book.id" class="hover:bg-white/[0.02] transition-colors">
                  <td class="p-8 font-medium tracking-tight text-zinc-200">{{ book.title }}</td>
                  <td class="p-8 text-right">
                    <span class="text-[10px] font-bold uppercase tracking-[0.2em] px-3 py-1 bg-green-500/10 text-green-500 rounded-full border border-green-500/20">Available</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div v-else-if="activeTab === 'settings'" :key="'settings'" class="p-10 border border-white/10 rounded-2xl text-zinc-500 leading-relaxed">
           <p class="text-white font-bold mb-4">Account Information</p>
           Email: {{ currentUserEmail }} <br/>
           Access: Student (Read-Only) <br/>
           Location: Global Library Sync 🌍
        </div>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-sm w-full text-center text-white">
          <h3 class="text-2xl font-bold mb-2 tracking-tighter">Sign Out?</h3>
          <p class="text-zinc-500 text-sm mb-8">Come back soon to discover more books.</p>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold hover:bg-white/5">Cancel</button>
            <button @click="$emit('logout')" class="flex-1 py-4 rounded-xl bg-red-600 font-bold hover:bg-red-700">Logout</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, query, orderBy } from "firebase/firestore";

// State
const allBooks = ref([]);
const activeTab = ref('home');
const showWelcome = ref(true);
const showLogoutModal = ref(false);
const searchQuery = ref('');
const currentTime = ref('');
const dbStatus = ref('online');
const currentUserEmail = ref(auth.currentUser?.email || 'Student');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'Browse Library', path: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
  { id: 'settings', name: 'Settings', path: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' }
];

const filteredBooks = computed(() => {
  if (!searchQuery.value) return allBooks.value;
  return allBooks.value.filter(book => book.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
});

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit' });
};

// Fixed Database Status Sync
const syncData = () => {
  // Listen to global books collection (Read-Only for users)
  const q = query(collection(db, "books"), orderBy("createdAt", "desc"));
  
  const unsubscribe = onSnapshot(q, (snapshot) => {
    allBooks.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    dbStatus.value = 'online';
  }, (error) => {
    console.error("Firestore sync error:", error);
    dbStatus.value = 'offline';
  });

  return unsubscribe;
};

let timeInterval;
let firestoreUnsubscribe;

onMounted(() => {
  firestoreUnsubscribe = syncData();
  updateTime();
  timeInterval = setInterval(updateTime, 1000);
  
  // Browser-level connection check
  window.addEventListener('online', () => dbStatus.value = 'online');
  window.addEventListener('offline', () => dbStatus.value = 'offline');
  
  setTimeout(() => { showWelcome.value = false; }, 3000);
});

onUnmounted(() => {
  clearInterval(timeInterval);
  if (firestoreUnsubscribe) firestoreUnsubscribe();
  window.removeEventListener('online', () => dbStatus.value = 'online');
  window.removeEventListener('offline', () => dbStatus.value = 'offline');
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>