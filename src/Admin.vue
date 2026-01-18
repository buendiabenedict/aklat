<template>
  <div class="fixed inset-0 bg-black text-white font-ios flex overflow-hidden w-full h-full">
    
    <transition name="fade">
      <div v-if="showWelcome" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center">
        <p class="text-zinc-600 uppercase tracking-[0.6em] text-[10px] mb-4 animate-pulse">System Access Granted</p>
        <h2 class="text-5xl font-bold tracking-tighter">Welcome, Admin</h2>
      </div>
    </transition>

    <aside 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']" 
      class="w-72 h-full border-r border-white/10 bg-zinc-950 z-50 flex flex-col transition-all duration-700 shrink-0"
    >
      <div class="h-28 flex items-center px-8 overflow-hidden">
        <div class="w-8 h-8 bg-white rounded-lg shrink-0 shadow-[0_0_15px_rgba(255,255,255,0.2)]"></div>
        <h1 class="ml-4 text-xs font-black tracking-widest uppercase text-white">Aklat Admin</h1>
      </div>

      <nav class="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
        <button v-for="item in navItems" :key="item.name" @click="activeTab = item.id"
          class="w-full flex items-center h-14 rounded-xl px-4 transition-all duration-200 relative"
          :class="activeTab === item.id ? 'bg-white text-black' : 'text-zinc-500 hover:text-white'">
          <div class="w-6 h-6 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" :d="item.path" /></svg>
          </div>
          <span class="ml-4 font-bold text-sm tracking-tight">{{ item.name }}</span>
          
          <span v-if="item.id === 'notifications' && pendingCount > 0" class="absolute right-4 w-5 h-5 bg-red-600 text-white text-[10px] rounded-full flex items-center justify-center animate-bounce">
            {{ pendingCount }}
          </span>
        </button>
      </nav>

      <div class="p-6 border-t border-white/5 space-y-4">
        <div class="flex items-center gap-3 px-2">
          <div class="relative flex h-2 w-2">
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"></span>
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="relative inline-flex rounded-full h-2 w-2"></span>
          </div>
          <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-500 whitespace-nowrap">DB: {{ dbStatus }}</p>
        </div>
        <button @click="showLogoutModal = true" class="w-full h-14 flex items-center justify-center rounded-xl text-red-500 hover:bg-red-500/10 transition-all group">
          <span class="font-bold text-xs uppercase tracking-widest">Sign Out</span>
        </button>
      </div>
    </aside>

    <main 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']"
      class="flex-1 h-full overflow-y-auto p-8 md:p-16 relative z-10 bg-black"
    >
      <header class="mb-16 flex justify-between items-start">
        <div>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3">{{ currentTime }} • Control Center</p>
          <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab === 'borrowed' ? 'Borrowed Books' : activeTab }}</h2>
        </div>
        <div v-if="activeTab === 'inventory'">
          <button @click="showAddBookModal = true" class="bg-white text-black px-8 py-4 rounded-xl font-bold hover:bg-zinc-200 transition-all shadow-xl active:scale-95">Add New Book</button>
        </div>
      </header>

      <transition name="fade" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Total Inventory</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
          </div>
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Total Users</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ users.length }}</p>
          </div>
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Pending Requests</h3>
            <p class="text-3xl font-bold tracking-tighter text-red-500">{{ pendingCount }}</p>
          </div>
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Currently Borrowed</h3>
            <p class="text-3xl font-bold tracking-tighter text-blue-500">{{ approvedCount }}</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'" class="space-y-8">
          <input v-model="searchQuery" type="text" placeholder="Search book titles..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white w-full max-w-xl outline-none focus:border-white/30" />
          <div class="border border-white/10 rounded-2xl overflow-hidden bg-zinc-950 shadow-2xl">
            <table class="w-full text-left">
              <thead>
                <tr class="text-zinc-600 text-[10px] font-black uppercase tracking-[0.3em] border-b border-white/5">
                  <th class="p-8">Book Name</th>
                  <th class="p-8 text-right">Management</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/[0.03]">
                <tr v-for="book in filteredBooks" :key="book.id" class="hover:bg-white/[0.02]">
                  <td class="p-8 font-medium tracking-tight text-zinc-200">{{ book.title }}</td>
                  <td class="p-8 text-right">
                    <button @click="confirmDelete(book.id)" class="text-red-500/40 hover:text-red-500 font-bold text-[10px] uppercase tracking-widest transition-all">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section v-else-if="activeTab === 'borrowed'" :key="'borrowed'" class="space-y-4">
          <div v-if="approvedRequests.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">
            No active borrowed books. 📖
          </div>
          <div v-for="item in approvedRequests" :key="item.id" class="p-8 border border-white/10 rounded-2xl bg-zinc-950 flex justify-between items-center group">
            <div class="flex items-center gap-6">
              <div class="w-12 h-12 bg-blue-500/10 text-blue-500 rounded-xl flex items-center justify-center font-black border border-blue-500/20">
                {{ item.userEmail[0].toUpperCase() }}
              </div>
              <div>
                <h4 class="text-white font-bold tracking-tight text-lg">{{ item.bookTitle }}</h4>
                <p class="text-zinc-500 text-xs mt-1">Borrowed by: <span class="text-zinc-300 font-medium">{{ item.userEmail }}</span></p>
              </div>
            </div>
            <div class="text-right">
              <span class="text-[10px] font-black uppercase tracking-[0.2em] px-4 py-2 bg-blue-500/10 text-blue-500 border border-blue-500/20 rounded-full">On Loan</span>
              <p class="text-[9px] text-zinc-600 mt-3 font-bold uppercase tracking-widest">Return Pending</p>
            </div>
          </div>
        </section>

        <section v-else-if="activeTab === 'notifications'" :key="'notifications'" class="space-y-4">
          <div v-if="notifications.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">
            No new notifications.
          </div>
          <div v-for="notif in notifications" :key="notif.id" 
            class="p-6 border rounded-2xl bg-zinc-950 flex justify-between items-center transition-all"
            :class="notif.status === 'pending' ? 'border-white/20' : 'border-white/5 opacity-40'"
          >
            <div class="flex gap-4 items-center">
              <div class="w-10 h-10 rounded-full bg-zinc-900 border border-white/10 flex items-center justify-center text-white font-bold">
                {{ notif.userEmail[0].toUpperCase() }}
              </div>
              <div>
                <p class="text-sm font-bold tracking-tight text-zinc-200">
                  <span class="text-zinc-500 font-normal">{{ notif.userEmail }}</span> wants to borrow 
                  <span class="italic text-white">"{{ notif.bookTitle }}"</span>
                </p>
                <p class="text-[10px] text-zinc-600 uppercase tracking-widest font-black mt-1">{{ notif.status }}</p>
              </div>
            </div>
            <div class="flex gap-3" v-if="notif.status === 'pending'">
              <button @click="updateNotifStatus(notif.id, 'approved')" class="px-6 py-2 bg-white text-black text-[10px] font-black uppercase tracking-widest rounded-lg hover:bg-zinc-200 transition-all">Approve</button>
              <button @click="updateNotifStatus(notif.id, 'rejected')" class="px-6 py-2 border border-white/10 text-white text-[10px] font-black uppercase tracking-widest rounded-lg hover:bg-white/5 transition-all">Decline</button>
            </div>
            <span v-else class="text-[10px] text-zinc-700 font-bold uppercase tracking-widest">{{ notif.status }}</span>
          </div>
        </section>

        <section v-else-if="activeTab === 'community'" :key="'community'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="user in users" :key="user.id" class="p-6 border border-white/10 rounded-2xl bg-zinc-950 flex items-center gap-4 hover:border-white/30 transition-all">
            <div class="w-10 h-10 bg-white text-black rounded-full flex items-center justify-center font-black shadow-lg">{{ user.email[0].toUpperCase() }}</div>
            <div class="min-w-0">
              <p class="font-bold truncate text-sm text-white">{{ user.email }}</p>
              <p class="text-[9px] text-zinc-600 uppercase tracking-widest font-bold">{{ user.role || 'Member' }}</p>
            </div>
          </div>
        </section>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showAddBookModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6 backdrop-blur-sm">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-lg w-full shadow-2xl">
          <h3 class="text-3xl font-bold mb-8 tracking-tighter">Register New Book</h3>
          <input v-model="newBookTitle" @keyup.enter="addBook" type="text" placeholder="Enter book title..." class="w-full bg-zinc-900 border border-white/10 rounded-2xl py-5 px-6 text-white mb-8 outline-none focus:border-white/40"/>
          <div class="flex gap-3">
            <button @click="showAddBookModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white hover:bg-white/5 transition-all">Cancel</button>
            <button @click="addBook" class="flex-1 py-4 rounded-xl bg-white text-black font-black hover:bg-zinc-200 transition-all">Add to System</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6 backdrop-blur-sm">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2rem] max-w-sm w-full text-center">
          <h3 class="text-2xl font-bold mb-8 tracking-tighter">Sign Out?</h3>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold">Cancel</button>
            <button @click="$emit('logout')" class="flex-1 py-4 rounded-xl bg-red-600 font-bold">Logout</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6 backdrop-blur-sm">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2rem] max-w-sm w-full text-center">
          <h3 class="text-2xl font-bold mb-8 tracking-tighter text-red-500">Delete Permanently?</h3>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white">Cancel</button>
            <button @click="deleteBook" class="flex-1 py-4 rounded-xl bg-red-600 font-black">Delete</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { db } from './lib/firebase';
import { collection, addDoc, deleteDoc, updateDoc, doc, onSnapshot, query, orderBy, serverTimestamp } from "firebase/firestore";

// State
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const activeTab = ref('home');
const showWelcome = ref(true);
const showLogoutModal = ref(false);
const showDeleteModal = ref(false);
const showAddBookModal = ref(false);
const bookToDelete = ref(null);
const newBookTitle = ref('');
const searchQuery = ref('');
const currentTime = ref('');
const dbStatus = ref('online');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'Inventory', path: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'borrowed', name: 'Current Borrowers', path: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
  { id: 'community', name: 'Community', path: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0' },
  { id: 'notifications', name: 'Notifications', path: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' }
];

// Computed
const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));
const pendingCount = computed(() => notifications.value.filter(n => n.status === 'pending').length);
const approvedCount = computed(() => approvedRequests.value.length);
const approvedRequests = computed(() => notifications.value.filter(n => n.status === 'approved'));

// Actions
const updateTime = () => {
  currentTime.value = new Date().toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit' });
};

const loadData = () => {
  onSnapshot(query(collection(db, "books"), orderBy("createdAt", "desc")), (s) => books.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => {
    notifications.value = s.docs.map(d => ({id: d.id, ...d.data()}));
    dbStatus.value = 'online';
  }, () => dbStatus.value = 'offline');
};

const addBook = async () => {
  if (!newBookTitle.value.trim()) return;
  await addDoc(collection(db, "books"), { title: newBookTitle.value, createdAt: serverTimestamp() });
  newBookTitle.value = ''; showAddBookModal.value = false;
};

const confirmDelete = (id) => { bookToDelete.value = id; showDeleteModal.value = true; };
const deleteBook = async () => { await deleteDoc(doc(db, "books", bookToDelete.value)); showDeleteModal.value = false; };

const updateNotifStatus = async (id, newStatus) => {
  await updateDoc(doc(db, "notifications", id), { status: newStatus });
};

let timer;
onMounted(() => {
  loadData();
  updateTime();
  timer = setInterval(updateTime, 1000);
  setTimeout(() => showWelcome.value = false, 3000);
});
onUnmounted(() => clearInterval(timer));
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>