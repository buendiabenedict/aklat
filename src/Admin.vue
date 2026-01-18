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
          <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-500 whitespace-nowrap">DB: {{ dbStatus }}</p>
        </div>
        <button @click="showLogoutModal = true" class="w-full h-14 flex items-center justify-center rounded-xl text-red-500 hover:bg-red-500/10 transition-all active:scale-95">
          <span class="font-bold text-xs uppercase tracking-widest">Sign Out</span>
        </button>
      </div>
    </aside>

    <main 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']"
      class="flex-1 h-full overflow-y-auto p-8 md:p-16 relative z-10 bg-black"
    >
      <header class="mb-16 flex justify-between items-start">
        <transition name="fade" mode="out-in">
          <div :key="activeTab">
            <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3">{{ currentTime }} • Secure Terminal</p>
            <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab.replace('_', ' ') }}</h2>
          </div>
        </transition>
      </header>

      <transition name="page" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="stat in stats" :key="stat.label" class="p-8 border border-white/10 rounded-2xl bg-zinc-950">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4" :class="stat.color">{{ stat.label }}</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ stat.value }}</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'" class="space-y-4">
          <div class="flex flex-col md:flex-row gap-4 mb-8">
            <input v-model="searchQuery" type="text" placeholder="Filter library..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white flex-1 outline-none focus:border-white/30 transition-all" />
            
            <div class="flex gap-2">
              <button @click="toggleSelectMode" :class="isSelectMode ? 'bg-zinc-800 text-white border-white/20' : 'bg-white/5 text-zinc-400 border-white/5'" class="px-6 py-4 rounded-xl font-bold border transition-all text-xs uppercase tracking-widest">
                {{ isSelectMode ? 'Cancel Selection' : 'Select Books' }}
              </button>
              
              <button v-if="!isSelectMode" @click="showAddBookModal = true" class="bg-white text-black px-8 py-4 rounded-xl font-bold text-xs uppercase tracking-widest active:scale-95 transition-all">
                New Entry
              </button>

              <button v-else @click="confirmBulkDelete" :disabled="selectedBooks.length === 0" :class="selectedBooks.length > 0 ? 'bg-red-600 opacity-100' : 'bg-red-900/50 opacity-50 cursor-not-allowed'" class="bg-red-600 text-white px-8 py-4 rounded-xl font-bold text-xs uppercase tracking-widest active:scale-95 transition-all">
                Delete ({{ selectedBooks.length }})
              </button>
            </div>
          </div>

          <div class="border border-white/10 rounded-3xl overflow-hidden bg-zinc-950 shadow-2xl">
            <table class="w-full text-left">
              <transition-group tag="tbody" name="list" class="divide-y divide-white/[0.03]">
                <tr v-for="book in filteredBooks" :key="book.id" 
                    @click="isSelectMode ? toggleBookSelection(book.id) : null"
                    :class="[isSelectMode ? 'cursor-pointer' : '', selectedBooks.includes(book.id) ? 'bg-white/[0.05]' : '']"
                    class="hover:bg-white/[0.02] transition-colors group">
                  
                  <td v-if="isSelectMode" class="pl-8 w-10">
                    <div :class="selectedBooks.includes(book.id) ? 'bg-blue-500 border-blue-500' : 'border-white/20'" class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all">
                      <div v-if="selectedBooks.includes(book.id)" class="w-2 h-2 bg-white rounded-full"></div>
                    </div>
                  </td>

                  <td class="p-8 font-medium">
                    <span :class="selectedBooks.includes(book.id) ? 'text-blue-400' : 'text-white'" class="transition-colors">{{ book.title }}</span>
                  </td>
                  
                  <td class="p-8 text-right">
                    <button v-if="!isSelectMode" @click.stop="confirmSingleDelete(book)" class="text-red-500/50 hover:text-red-500 text-[10px] font-black uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all">Remove</button>
                    <span v-else class="text-zinc-700 text-[10px] font-black uppercase tracking-widest">Select Mode</span>
                  </td>
                </tr>
              </transition-group>
            </table>
          </div>
        </section>

        <section v-else-if="activeTab === 'notifications'" :key="'notifications'" class="space-y-4">
           <div v-if="notifications.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">No pending requests.</div>
          <transition-group name="list">
            <div v-for="notif in notifications" :key="notif.id" class="p-6 border border-white/20 rounded-2xl bg-zinc-950 flex justify-between items-center mb-4">
              <div class="flex gap-4 items-center">
                <div class="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center font-bold">{{ notif.userEmail[0].toUpperCase() }}</div>
                <div>
                  <p class="text-sm font-bold"><span class="text-zinc-500 font-normal">{{ notif.userEmail }}</span> requested <span class="text-white italic">"{{ notif.bookTitle }}"</span></p>
                  <p class="text-[9px] text-zinc-600 uppercase mt-1">Requested: {{ formatTimestamp(notif.createdAt) }}</p>
                </div>
              </div>
              <div class="flex gap-3">
                <button @click="handleAction(notif, 'approved')" class="px-6 py-2 bg-white text-black text-[10px] font-black uppercase rounded-lg">Approve</button>
                <button @click="handleAction(notif, 'rejected')" class="px-6 py-2 border border-white/10 text-[10px] font-black uppercase rounded-lg">Decline</button>
              </div>
            </div>
          </transition-group>
        </section>

        <section v-else-if="activeTab === 'borrowed'" :key="'borrowed'" class="space-y-4">
          <div v-if="borrowers.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">No active loans.</div>
          <transition-group name="list">
            <div v-for="item in borrowers" :key="item.id" class="p-6 border border-blue-500/10 rounded-2xl bg-zinc-950 flex justify-between items-center mb-4">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-blue-600/10 text-blue-500 rounded-lg flex items-center justify-center font-bold">📖</div>
                <div>
                  <p class="text-sm font-bold">{{ item.bookTitle }}</p>
                  <p class="text-[9px] text-zinc-500 uppercase">On loan to {{ item.userEmail }}</p>
                </div>
              </div>
              <button @click="handleReturn(item)" class="px-6 py-2 bg-blue-600 text-white text-[10px] font-black uppercase rounded-lg hover:bg-blue-500">Mark as Returned</button>
            </div>
          </transition-group>
        </section>

        <section v-else-if="activeTab === 'history'" :key="'history'" class="space-y-4">
          <div v-if="history.length === 0" class="p-20 text-center text-zinc-600 italic border border-dashed border-white/10 rounded-3xl">History is empty.</div>
          <transition-group name="list">
            <div v-for="log in history" :key="log.id" class="p-5 border border-white/5 rounded-2xl bg-zinc-950/50 flex justify-between items-center mb-4 opacity-75">
              <div class="flex items-center gap-4">
                <span :class="log.status === 'returned' ? 'text-green-500' : 'text-red-500'" class="text-xs">●</span>
                <div>
                  <p class="text-sm font-medium text-zinc-300">{{ log.bookTitle }}</p>
                  <p class="text-[9px] text-zinc-600 uppercase">{{ log.userEmail }}</p>
                  <p class="text-[8px] text-zinc-500 italic mt-1">Status: {{ log.status }} on {{ formatTimestamp(log.actionDate) }}</p>
                </div>
              </div>
            </div>
          </transition-group>
        </section>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[250] flex items-center justify-center bg-black/95 px-6 backdrop-blur-md">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2rem] max-w-sm w-full text-center">
          <div class="w-16 h-16 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center mx-auto mb-6 text-2xl">⚠️</div>
          <h3 class="text-2xl font-bold mb-2 tracking-tighter">Are you sure?</h3>
          <p class="text-zinc-500 text-sm mb-8">You are about to delete {{ deleteTargetCount }} book(s). This action is permanent.</p>
          <div class="flex gap-3">
            <button @click="closeDeleteModal" class="flex-1 py-4 rounded-xl border border-white/10 font-bold">Cancel</button>
            <button @click="executeDeletion" class="flex-1 py-4 rounded-xl bg-red-600 text-white font-black">Confirm Delete</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6 backdrop-blur-sm">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2rem] max-w-sm w-full text-center shadow-2xl">
          <h3 class="text-2xl font-bold mb-2 tracking-tighter text-white">Sign Out?</h3>
          <p class="text-zinc-500 text-sm mb-8">Babalik ka sa login screen, pre.</p>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-zinc-400">Cancel</button>
            <button @click="executeLogout" class="flex-1 py-4 rounded-xl bg-red-600 text-white font-black">Confirm</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showAddBookModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6 backdrop-blur-sm">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-lg w-full">
          <h3 class="text-2xl font-bold mb-6 tracking-tighter italic">Register Book</h3>
          <input v-model="newBookTitle" @keyup.enter="addBook" type="text" placeholder="Title..." class="w-full bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white mb-8 outline-none focus:border-white/40"/>
          <div class="flex gap-3">
            <button @click="showAddBookModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold">Cancel</button>
            <button @click="addBook" class="flex-1 py-4 rounded-xl bg-white text-black font-black">Save to DB</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, defineEmits } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy, serverTimestamp, writeBatch } from "firebase/firestore";
import { signOut } from "firebase/auth";

const emit = defineEmits(['logout']);

// State
const books = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const history = ref([]);
const activeTab = ref('home');
const showWelcome = ref(true);
const showAddBookModal = ref(false);
const showLogoutModal = ref(false);
const showDeleteModal = ref(false);

// Multi-delete State
const isSelectMode = ref(false);
const selectedBooks = ref([]);
const singleDeleteId = ref(null);

const newBookTitle = ref('');
const searchQuery = ref('');
const currentTime = ref('');
const dbStatus = ref('online');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'Inventory', path: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'notifications', name: 'Requests', path: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' },
  { id: 'borrowed', name: 'Borrowers', path: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197' },
  { id: 'history', name: 'Logs', path: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' }
];

// Selection Handlers
const toggleSelectMode = () => {
  isSelectMode.value = !isSelectMode.value;
  selectedBooks.value = [];
};

const toggleBookSelection = (id) => {
  const index = selectedBooks.value.indexOf(id);
  if (index > -1) selectedBooks.value.splice(index, 1);
  else selectedBooks.value.push(id);
};

const confirmSingleDelete = (book) => {
  singleDeleteId.value = book.id;
  showDeleteModal.value = true;
};

const confirmBulkDelete = () => {
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  singleDeleteId.value = null;
};

const deleteTargetCount = computed(() => {
  return singleDeleteId.value ? 1 : selectedBooks.value.length;
});

const executeDeletion = async () => {
  try {
    if (singleDeleteId.value) {
      await deleteDoc(doc(db, "books", singleDeleteId.value));
    } else {
      const batch = writeBatch(db);
      selectedBooks.value.forEach(id => {
        batch.delete(doc(db, "books", id));
      });
      await batch.commit();
    }
    
    // Reset state after delete
    isSelectMode.value = false;
    selectedBooks.value = [];
    closeDeleteModal();
  } catch (err) { console.error("Deletion failed:", err); }
};

// Data Logic
const stats = computed(() => [
  { label: 'Books', value: books.value.length, color: '' },
  { label: 'Pending', value: notifications.value.length, color: 'text-red-500' },
  { label: 'Loans', value: borrowers.value.length, color: 'text-blue-500' },
  { label: 'History', value: history.value.length, color: 'text-zinc-500' }
]);

const formatTimestamp = (ts) => {
  if (!ts) return 'Now';
  const date = ts.toDate ? ts.toDate() : new Date(ts);
  return date.toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
};

const executeLogout = async () => {
  try {
    if (auth) await signOut(auth);
    emit('logout');
    showLogoutModal.value = false;
  } catch (error) { emit('logout'); }
};

const loadData = () => {
  onSnapshot(query(collection(db, "books"), orderBy("createdAt", "desc")), (s) => books.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(collection(db, "notifications"), (s) => notifications.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(collection(db, "borrowers"), (s) => borrowers.value = s.docs.map(d => ({id: d.id, ...d.data()})));
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => {
    history.value = s.docs.map(d => ({id: d.id, ...d.data()}));
    dbStatus.value = 'online';
  }, () => dbStatus.value = 'offline');
};

const handleAction = async (notif, status) => {
  const data = { ...notif, status, actionDate: serverTimestamp() };
  delete data.id;
  try {
    if (status === 'approved') {
      data.approvedAt = serverTimestamp();
      await addDoc(collection(db, "borrowers"), data);
    } else {
      await addDoc(collection(db, "history"), data);
    }
    await deleteDoc(doc(db, "notifications", notif.id));
  } catch (err) { console.error(err); }
};

const handleReturn = async (borrower) => {
  const data = { ...borrower, status: 'returned', actionDate: serverTimestamp() };
  delete data.id;
  try {
    await addDoc(collection(db, "history"), data);
    await deleteDoc(doc(db, "borrowers", borrower.id));
  } catch (err) { console.error(err); }
};

const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));
const updateTime = () => { currentTime.value = new Date().toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' }); };

let timer;
onMounted(() => { loadData(); updateTime(); timer = setInterval(updateTime, 1000); setTimeout(() => showWelcome.value = false, 3000); });
onUnmounted(() => clearInterval(timer));

const addBook = async () => { if (!newBookTitle.value.trim()) return; await addDoc(collection(db, "books"), { title: newBookTitle.value, createdAt: serverTimestamp() }); newBookTitle.value = ''; showAddBookModal.value = false; };
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.page-enter-active, .page-leave-active { transition: all 0.4s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }
.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from { opacity: 0; transform: translateX(-20px); }
.list-leave-to { opacity: 0; transform: translateX(20px); }
</style>