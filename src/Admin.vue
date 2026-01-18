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
          
          <span v-if="item.id === 'notifications' && notifications.length > 0" class="absolute right-4 w-5 h-5 bg-red-600 text-white text-[10px] rounded-full flex items-center justify-center animate-bounce">
            {{ notifications.length }}
          </span>
        </button>
      </nav>

      <div class="p-6 border-t border-white/5 space-y-4">
        <div class="flex items-center gap-3 px-2">
          <div class="relative flex h-2 w-2">
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"></span>
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="relative inline-flex rounded-full h-2 w-2"></span>
          </div>
          <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-500">DB: {{ dbStatus }}</p>
        </div>
        <button @click="showLogoutModal = true" class="w-full h-14 flex items-center justify-center rounded-xl text-red-500 hover:bg-red-500/10 transition-all">
          <span class="font-bold text-xs uppercase tracking-widest">Sign Out</span>
        </button>
      </div>
    </aside>

    <main 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']"
      class="flex-1 h-full overflow-y-auto p-8 md:p-16 relative z-10 bg-black"
    >
      <header class="mb-16">
        <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3">{{ currentTime }} • System Ledger</p>
        <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab.replace('_', ' ') }}</h2>
      </header>

      <transition name="fade" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="stat in stats" :key="stat.label" class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">{{ stat.label }}</h3>
            <p class="text-3xl font-bold tracking-tighter" :class="stat.color">{{ stat.value }}</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'notifications'" :key="'notifications'">
          <div v-if="notifications.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">No pending requests.</div>
          <transition-group name="list" tag="div" class="space-y-4">
            <div v-for="notif in notifications" :key="notif.id" class="p-6 border border-white/20 rounded-2xl bg-zinc-950 flex justify-between items-center">
              <div class="flex gap-4 items-center">
                <div class="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center font-bold">{{ notif.userEmail[0].toUpperCase() }}</div>
                <div>
                  <p class="text-sm font-bold">{{ notif.userEmail }} <span class="text-zinc-500 font-normal">requested</span> {{ notif.bookTitle }}</p>
                  <p class="text-[10px] text-zinc-600 uppercase tracking-widest font-black mt-1">Awaiting Action</p>
                </div>
              </div>
              <div class="flex gap-3">
                <button @click="handleAction(notif, 'approved')" class="px-6 py-2 bg-white text-black text-[10px] font-black uppercase rounded-lg hover:bg-zinc-200">Approve</button>
                <button @click="handleAction(notif, 'rejected')" class="px-6 py-2 border border-white/10 text-white text-[10px] font-black uppercase rounded-lg hover:bg-white/5">Decline</button>
              </div>
            </div>
          </transition-group>
        </section>

        <section v-else-if="activeTab === 'borrowed'" :key="'borrowed'">
          <div v-if="borrowers.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">No active loans.</div>
          <transition-group name="list" tag="div" class="space-y-4">
            <div v-for="item in borrowers" :key="item.id" class="p-6 border border-blue-500/10 rounded-2xl bg-zinc-950 flex justify-between items-center">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-blue-600/10 text-blue-500 rounded-lg flex items-center justify-center">📖</div>
                <div>
                  <p class="text-sm font-bold text-white">{{ item.bookTitle }}</p>
                  <p class="text-[10px] text-zinc-500 uppercase tracking-widest">{{ item.userEmail }}</p>
                </div>
              </div>
              <button @click="handleReturn(item)" class="px-6 py-2 bg-blue-600 text-white text-[10px] font-black uppercase rounded-lg hover:bg-blue-500 shadow-lg active:scale-95 transition-all">Mark as Returned</button>
            </div>
          </transition-group>
        </section>

        <section v-else-if="activeTab === 'history'" :key="'history'">
          <div v-if="history.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">Log is empty.</div>
          <transition-group name="list" tag="div" class="space-y-3">
            <div v-for="log in history" :key="log.id" class="p-5 border border-white/5 rounded-2xl bg-zinc-950/40 flex justify-between items-center hover:bg-zinc-900/50 transition-colors">
              <div class="flex items-center gap-5">
                <div :class="log.status === 'returned' ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'" class="w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold shadow-inner">
                  {{ log.status === 'returned' ? '✓' : '✕' }}
                </div>
                <div>
                  <p class="text-sm font-bold text-zinc-200">{{ log.bookTitle }}</p>
                  <p class="text-[10px] text-zinc-500 uppercase tracking-widest font-medium">{{ log.userEmail }}</p>
                </div>
              </div>
              <div class="text-right">
                <span :class="log.status === 'returned' ? 'text-green-500' : 'text-red-500'" class="text-[9px] font-black uppercase tracking-[0.2em] border border-white/5 px-3 py-1 rounded-full bg-black/50">
                  {{ log.status }}
                </span>
                <p class="text-[9px] text-zinc-600 mt-2 font-bold uppercase tracking-tighter">
                  {{ log.timestamp ? formatLogTime(log.timestamp) : 'Just now' }}
                </p>
              </div>
            </div>
          </transition-group>
        </section>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'">
          <div class="flex gap-4 mb-8">
            <input v-model="searchQuery" type="text" placeholder="Search books..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white flex-1 outline-none focus:border-white/30 transition-all" />
            <button @click="showAddBookModal = true" class="bg-white text-black px-8 py-4 rounded-xl font-bold active:scale-95 transition-all">Add Book</button>
          </div>
          <div class="border border-white/10 rounded-2xl overflow-hidden bg-zinc-950">
            <table class="w-full text-left">
              <transition-group name="list" tag="tbody" class="divide-y divide-white/[0.03]">
                <tr v-for="book in filteredBooks" :key="book.id" class="hover:bg-white/[0.02]">
                  <td class="p-8 font-medium">{{ book.title }}</td>
                  <td class="p-8 text-right"><button @click="confirmDelete(book.id)" class="text-red-500/50 hover:text-red-500 text-[10px] font-bold uppercase tracking-widest">Remove</button></td>
                </tr>
              </transition-group>
            </table>
          </div>
        </section>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showAddBookModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-sm px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-lg w-full">
          <h3 class="text-2xl font-bold mb-6 tracking-tighter italic">Register Book</h3>
          <input v-model="newBookTitle" @keyup.enter="addBook" type="text" placeholder="Title..." class="w-full bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white mb-8 outline-none focus:border-white/40"/>
          <div class="flex gap-3">
            <button @click="showAddBookModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white">Cancel</button>
            <button @click="addBook" class="flex-1 py-4 rounded-xl bg-white text-black font-black">Add to DB</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { db } from './lib/firebase';
import { collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy, serverTimestamp } from "firebase/firestore";

// State
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const history = ref([]);
const activeTab = ref('home');
const showWelcome = ref(true);
const showLogoutModal = ref(false);
const showAddBookModal = ref(false);
const newBookTitle = ref('');
const searchQuery = ref('');
const currentTime = ref('');
const dbStatus = ref('online');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'Inventory', path: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'notifications', name: 'Requests', path: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' },
  { id: 'borrowed', name: 'Borrowers', path: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197' },
  { id: 'history', name: 'History Logs', path: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' }
];

const stats = computed(() => [
  { label: 'Books', value: books.value.length, color: 'text-white' },
  { label: 'New Requests', value: notifications.value.length, color: 'text-red-500' },
  { label: 'Active Loans', value: borrowers.value.length, color: 'text-blue-500' },
  { label: 'Logged Entries', value: history.value.length, color: 'text-zinc-500' }
]);

const loadData = () => {
  onSnapshot(query(collection(db, "books"), orderBy("createdAt", "desc")), (s) => books.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(collection(db, "notifications"), (s) => notifications.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(collection(db, "borrowers"), (s) => borrowers.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(query(collection(db, "history"), orderBy("timestamp", "desc")), (s) => {
    history.value = s.docs.map(d => ({id: d.id, ...d.data()}));
    dbStatus.value = 'online';
  }, () => dbStatus.value = 'offline');
};

const handleAction = async (notif, status) => {
  const data = { ...notif, status, timestamp: new Date().toISOString() };
  delete data.id;

  try {
    if (status === 'approved') {
      await addDoc(collection(db, "borrowers"), data);
    } else {
      await addDoc(collection(db, "history"), data);
    }
    await deleteDoc(doc(db, "notifications", notif.id));
  } catch (err) { console.error(err); }
};

const handleReturn = async (borrower) => {
  const data = { ...borrower, status: 'returned', timestamp: new Date().toISOString() };
  delete data.id;

  try {
    await addDoc(collection(db, "history"), data);
    await deleteDoc(doc(db, "borrowers", borrower.id));
  } catch (err) { console.error(err); }
};

const formatLogTime = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleString('en-US', { 
    month: 'short', day: 'numeric', 
    hour: '2-digit', minute: '2-digit', 
    hour12: true 
  });
};

const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));
const updateTime = () => { currentTime.value = new Date().toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' }); };

let timer;
onMounted(() => { loadData(); updateTime(); timer = setInterval(updateTime, 1000); setTimeout(() => showWelcome.value = false, 3000); });
onUnmounted(() => clearInterval(timer));

const addBook = async () => { if (!newBookTitle.value.trim()) return; await addDoc(collection(db, "books"), { title: newBookTitle.value, createdAt: serverTimestamp() }); newBookTitle.value = ''; showAddBookModal.value = false; };
const confirmDelete = async (id) => { await deleteDoc(doc(db, "books", id)); };
</script>

<style scoped>
/* Page Fade */
.fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* List Animations (Fade In, Fade Out, Slide) */
.list-enter-active, .list-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* Ensure items don't jump when others are leaving */
.list-move {
  transition: transform 0.5s ease;
}
</style>