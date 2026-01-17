<template>
  <div class="min-h-screen bg-black text-white font-ios flex overflow-hidden relative">
    
    <transition name="fade">
      <div v-if="showWelcome" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center">
        <p class="text-zinc-600 uppercase tracking-[0.6em] text-[10px] mb-4 animate-pulse">System Access Granted</p>
        <h2 class="text-5xl font-bold tracking-tighter">Welcome, Admin</h2>
      </div>
    </transition>

    <aside 
      :class="[isSidebarCollapsed ? 'w-20' : 'w-72', showWelcome ? 'opacity-5' : 'opacity-100']" 
      class="h-screen border-r border-white/10 bg-zinc-950 z-50 flex flex-col transition-all duration-700 ease-in-out relative shrink-0"
    >
      <button @click="isSidebarCollapsed = !isSidebarCollapsed" class="absolute -right-3 top-10 bg-white text-black rounded-full p-1.5 z-[60] hover:scale-110 transition-transform shadow-xl border border-black/10">
        <svg class="w-3 h-3" :class="isSidebarCollapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M15 19l-7-7 7-7" /></svg>
      </button>

      <div class="h-28 flex items-center px-6 overflow-hidden">
        <div class="w-8 h-8 bg-white rounded-lg shrink-0 shadow-[0_0_15px_rgba(255,255,255,0.2)]"></div>
        <transition name="fade">
          <h1 v-if="!isSidebarCollapsed" class="ml-4 text-xs font-black tracking-widest uppercase text-white tracking-widest">Aklat Admin</h1>
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

    <main 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']"
      class="flex-1 h-screen overflow-y-auto p-8 md:p-16 relative z-10 transition-opacity duration-1000"
    >
      <header class="mb-16 flex justify-between items-end">
        <div>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3">System Online</p>
          <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab }}</h2>
        </div>
        
        <div v-if="activeTab === 'inventory'">
          <button @click="showAddBookModal = true" class="bg-white text-black px-8 py-4 rounded-xl font-bold hover:bg-zinc-200 transition-all flex items-center gap-2 active:scale-95 shadow-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" /></svg>
            Add New Book
          </button>
        </div>
      </header>

      <transition name="fade" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Books In Catalog</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
          </div>
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Community Members</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ users.length }}</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'" class="space-y-8">
          <div class="relative w-full max-w-xl">
             <input v-model="searchQuery" type="text" placeholder="Search library inventory..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white w-full outline-none focus:border-white/30 transition-all" />
          </div>
          <div class="border border-white/10 rounded-2xl overflow-hidden bg-zinc-950">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="text-zinc-600 text-[10px] font-black uppercase tracking-[0.3em] border-b border-white/5">
                  <th class="p-8">Book Title</th>
                  <th class="p-8 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/[0.03]">
                <tr v-for="book in filteredBooks" :key="book.id" class="hover:bg-white/[0.02] transition-colors">
                  <td class="p-8 font-medium tracking-tight">{{ book.title }}</td>
                  <td class="p-8 text-right">
                    <button @click="confirmDelete(book.id)" class="text-red-500/50 hover:text-red-500 font-bold text-[10px] uppercase tracking-widest transition-colors">Remove</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section v-else-if="activeTab === 'community'" :key="'community'" class="space-y-8">
          <div v-if="users.length === 0" class="p-20 text-center border border-dashed border-white/10 rounded-3xl">
            <p class="text-zinc-600 uppercase tracking-widest text-xs font-bold mb-2">No database entries</p>
            <p class="text-zinc-400">Login records will appear here once users start signing in.</p>
          </div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="user in users" :key="user.id" class="p-6 border border-white/10 rounded-2xl bg-zinc-950 flex items-center gap-4 group hover:border-white/20 transition-all">
              <div class="w-12 h-12 bg-zinc-900 rounded-full flex items-center justify-center font-bold text-lg border border-white/5 group-hover:bg-white group-hover:text-black transition-all">
                {{ user.email ? user.email[0].toUpperCase() : 'U' }}
              </div>
              <div class="overflow-hidden">
                <p class="font-bold truncate">{{ user.email }}</p>
                <p class="text-[10px] text-zinc-600 uppercase tracking-widest font-black">{{ user.role || 'Member' }}</p>
              </div>
            </div>
          </div>
        </section>

        <div v-else-if="activeTab === 'settings'" :key="'settings'" class="p-10 border border-white/10 rounded-2xl text-zinc-500">
           System Settings: Cloud Deployment v1.0.2
        </div>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showAddBookModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-lg w-full">
          <h3 class="text-2xl font-bold mb-6 tracking-tighter text-white">Add New Book</h3>
          <div class="space-y-4 mb-8">
            <label class="text-[10px] uppercase tracking-widest text-zinc-600 font-black">Book Title</label>
            <input 
              v-model="newBookTitle" 
              @keyup.enter="addBook" 
              type="text" 
              placeholder="e.g. Noli Me Tangere" 
              class="w-full bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white outline-none focus:border-white/40 transition-all"
            />
          </div>
          <div class="flex gap-3">
            <button @click="showAddBookModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white hover:bg-white/5 transition-all">Cancel</button>
            <button @click="addBook" class="flex-1 py-4 rounded-xl bg-white text-black font-bold hover:bg-zinc-200 transition-all active:scale-95">Save to Catalog</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-sm w-full text-center">
          <h3 class="text-2xl font-bold mb-2 tracking-tighter text-white">Sign Out?</h3>
          <p class="text-zinc-500 text-sm mb-8 font-medium text-center">This will end your librarian session.</p>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white hover:bg-white/5">Cancel</button>
            <button @click="$emit('logout')" class="flex-1 py-4 rounded-xl bg-red-600 text-white font-bold hover:bg-red-700">Logout</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-sm w-full text-center">
          <div class="w-16 h-16 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </div>
          <h3 class="text-2xl font-bold mb-2 tracking-tighter text-white">Delete Book?</h3>
          <p class="text-zinc-500 text-sm mb-8 font-medium">This cannot be undone.</p>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white hover:bg-white/5">Cancel</button>
            <button @click="deleteBook" class="flex-1 py-4 rounded-xl bg-red-600 text-white font-bold hover:bg-red-700">Confirm Delete</button>
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

// State
const books = ref([]);
const users = ref([]);
const activeTab = ref('home');
const showWelcome = ref(true);
const showLogoutModal = ref(false);
const showDeleteModal = ref(false);
const showAddBookModal = ref(false);
const bookToDelete = ref(null);
const isSidebarCollapsed = ref(false);
const newBookTitle = ref('');
const searchQuery = ref('');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'Inventory', path: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'community', name: 'Community', path: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' },
  { id: 'settings', name: 'Settings', path: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }
];

const filteredBooks = computed(() => {
  if (!searchQuery.value) return books.value;
  return books.value.filter(book => book.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
});

// REAL-TIME LISTENERS
const loadData = () => {
  // Load Books
  onSnapshot(query(collection(db, "books"), orderBy("createdAt", "desc")), (snapshot) => {
    books.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  });

  // Load Users
  onSnapshot(collection(db, "users"), (snapshot) => {
    users.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  });
};

const addBook = async () => {
  if (!newBookTitle.value.trim()) return;
  try {
    await addDoc(collection(db, "books"), { title: newBookTitle.value, createdAt: serverTimestamp() });
    newBookTitle.value = '';
    showAddBookModal.value = false;
  } catch (err) { alert(err.message); }
};

const confirmDelete = (id) => {
  bookToDelete.value = id;
  showDeleteModal.value = true;
};

const deleteBook = async () => {
  if (!bookToDelete.value) return;
  try {
    await deleteDoc(doc(db, "books", bookToDelete.value));
    showDeleteModal.value = false;
    bookToDelete.value = null;
  } catch (err) { alert(err.message); }
};

onMounted(() => {
  loadData();
  setTimeout(() => { showWelcome.value = false; }, 3000);
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>