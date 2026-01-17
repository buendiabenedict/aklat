<template>
  <div class="min-h-screen bg-black text-white font-ios flex overflow-hidden">
    
    <aside :class="isSidebarCollapsed ? 'w-20' : 'w-72'" class="h-screen border-r border-white/10 bg-zinc-950 z-50 flex flex-col transition-[width] duration-300 ease-in-out relative shrink-0">
      <button @click="isSidebarCollapsed = !isSidebarCollapsed" class="absolute -right-3 top-10 bg-white text-black rounded-full p-1.5 z-[60] hover:scale-110 transition-transform">
        <svg class="w-3 h-3" :class="isSidebarCollapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M15 19l-7-7 7-7" /></svg>
      </button>

      <div class="h-28 flex items-center px-6 overflow-hidden">
        <div class="w-8 h-8 bg-white rounded-lg shrink-0"></div>
        <transition name="fade">
          <h1 v-if="!isSidebarCollapsed" class="ml-4 text-xs font-black tracking-widest uppercase text-white">Aklat Admin</h1>
        </transition>
      </div>

      <nav class="flex-1 px-3 space-y-2 mt-4">
        <button v-for="item in navItems" :key="item.name" @click="activeTab = item.id"
          class="w-full flex items-center h-14 rounded-xl transition-all duration-200"
          :class="[ activeTab === item.id ? 'bg-white text-black' : 'text-zinc-500 hover:text-white', isSidebarCollapsed ? 'justify-center' : 'px-4' ]">
          <div class="w-6 h-6 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" :d="item.path" /></svg>
          </div>
          <transition name="fade">
            <span v-if="!isSidebarCollapsed" class="ml-4 font-bold text-sm tracking-tight whitespace-nowrap">{{ item.name }}</span>
          </transition>
        </button>
      </nav>

      <div class="p-3 border-t border-white/5">
        <button @click="showLogoutModal = true" class="w-full h-14 flex items-center justify-center rounded-xl text-red-500 hover:bg-red-500/10 transition-all group">
          <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          <span v-if="!isSidebarCollapsed" class="ml-3 font-bold text-xs uppercase tracking-widest">Sign Out</span>
        </button>
      </div>
    </aside>

    <main class="flex-1 h-screen overflow-y-auto p-8 md:p-16 relative z-10">
      
      <transition name="fade">
        <div v-if="showWelcome" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center">
          <p class="text-zinc-500 uppercase tracking-[0.5em] text-xs mb-4">Access Granted</p>
          <h2 class="text-5xl font-bold tracking-tighter">Welcome, Admin</h2>
        </div>
      </transition>

      <header class="mb-16 flex justify-between items-end">
        <div>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3">System Online</p>
          <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab }}</h2>
        </div>
        <div v-if="activeTab === 'inventory'" class="text-right">
          <p class="text-white font-bold text-4xl tracking-tighter">{{ filteredBooks.length }}</p>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest">Total Books</p>
        </div>
      </header>

      <transition name="fade" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="i in 3" :key="i" class="p-8 border border-white/10 rounded-2xl bg-zinc-900/50">
            <h3 class="text-zinc-500 text-xs font-bold uppercase tracking-widest mb-4">Quick Stat {{ i }}</h3>
            <p class="text-3xl font-bold">--</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'" class="space-y-8">
          <div class="flex flex-col md:flex-row gap-4 items-center">
            <div class="relative w-full max-w-xl">
              <input v-model="searchQuery" type="text" placeholder="Search books..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white w-full outline-none focus:border-white/30" />
            </div>
            <div class="flex gap-2 w-full md:w-auto">
              <input v-model="newBookTitle" @keyup.enter="addBook" type="text" placeholder="New Title" class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white w-full md:w-64 outline-none focus:border-white/30" />
              <button @click="addBook" class="bg-white text-black px-8 rounded-xl font-bold hover:bg-zinc-200">Add</button>
            </div>
          </div>
          <div class="border border-white/10 rounded-2xl overflow-hidden bg-zinc-900/50">
            <table class="w-full text-left">
              <thead>
                <tr class="text-zinc-600 text-[10px] font-black uppercase tracking-[0.3em] border-b border-white/5">
                  <th class="p-8">Book Identity</th>
                  <th class="p-8 text-right">Control</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/[0.03]">
                <tr v-for="book in filteredBooks" :key="book.id" class="hover:bg-white/[0.02]">
                  <td class="p-8 font-medium">{{ book.title }}</td>
                  <td class="p-8 text-right">
                    <button @click="deleteBook(book.id)" class="text-red-500 font-bold text-xs uppercase tracking-widest">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div v-else-if="activeTab === 'settings'" :key="'settings'" class="p-10 border border-white/10 rounded-2xl">
          <p class="text-zinc-500">System Preferences & Configuration</p>
        </div>

        <div v-else-if="activeTab === 'notifications'" :key="'notifications'" class="p-10 border border-white/10 rounded-2xl">
          <p class="text-zinc-500">No new alerts at this time.</p>
        </div>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/90 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-sm w-full text-center">
          <h3 class="text-2xl font-bold mb-2">Sign Out?</h3>
          <p class="text-zinc-500 text-sm mb-8">Are you sure you want to end your session?</p>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold">Cancel</button>
            <button @click="$emit('logout')" class="flex-1 py-4 rounded-xl bg-red-600 text-white font-bold">Logout</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { db } from './lib/firebase';
import { collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy, serverTimestamp } from "firebase/firestore";

const books = ref([]);
const activeTab = ref('home'); // Default page is Home
const showWelcome = ref(true); // Welcome text active on start
const showLogoutModal = ref(false);
const isSidebarCollapsed = ref(false);
const newBookTitle = ref('');
const searchQuery = ref('');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'Inventory', path: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'notifications', name: 'Alerts', path: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' },
  { id: 'settings', name: 'Settings', path: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }
];

const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value;
  return books.value.filter(book => book.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
});

const loadBooks = () => {
  const q = query(collection(db, "books"), orderBy("createdAt", "desc"));
  onSnapshot(q, (snapshot) => {
    books.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  });
};

const addBook = async () => {
  if (!newBookTitle.value.trim()) return;
  try {
    await addDoc(collection(db, "books"), { title: newBookTitle.value, createdAt: serverTimestamp() });
    newBookTitle.value = '';
  } catch (err) { alert(err.message); }
};

const deleteBook = async (id) => {
  if (confirm("Delete book?")) await deleteDoc(doc(db, "books", id));
};

onMounted(() => {
  loadBooks();
  // Welcome screen timer: 2.5 seconds
  setTimeout(() => { showWelcome.value = false; }, 2500);
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>