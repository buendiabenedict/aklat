<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40 text-left">
    
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-lg shadow-[0_0_20px_rgba(37,99,235,0.4)]">
          <span class="text-[10px] tracking-tighter">AC</span>
        </div>
        <div>
          <h1 class="text-sm font-bold tracking-tighter uppercase leading-none">Admin Central</h1>
          <p class="text-[10px] font-black text-blue-500 mt-1 uppercase tracking-widest">{{ currentTimeDisplay }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900 px-3 py-1.5 rounded-full border border-white/5 shadow-inner">
        <div class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
        <span class="text-[9px] font-bold uppercase tracking-widest text-zinc-400">System Live</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 py-4">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Metrics</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Dashboard</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Total Books</p>
              <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Users</p>
              <p class="text-3xl font-bold tracking-tighter text-blue-500">{{ users.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Loans</p>
              <p class="text-3xl font-bold tracking-tighter text-amber-500">{{ borrowers.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">History Logs</p>
              <p class="text-3xl font-bold tracking-tighter text-zinc-400">{{ historyLogs.length }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'inventory'" key="inventory" class="py-4">
          <section class="mb-6 flex justify-between items-end">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Repository</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Inventory</h2>
            </div>
            <div class="flex gap-2">
              <button v-if="selectedBooks.length > 0" @click="showDeleteModal = true" class="w-12 h-12 bg-red-600 text-white rounded-2xl flex items-center justify-center shadow-lg active:scale-90 transition-all">
                DEL
              </button>
              <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
                ADD
              </button>
            </div>
          </section>
          <div class="space-y-2">
            <div v-for="book in books" :key="book.id" @click="toggleSelectBook(book.id)" :class="selectedBooks.includes(book.id) ? 'border-blue-500 bg-blue-500/10' : 'border-white/5 bg-zinc-950'" class="p-4 rounded-xl flex items-center justify-between border transition-all cursor-pointer">
              <div class="flex items-center gap-4">
                <div class="w-4 h-4 rounded border border-zinc-700 flex items-center justify-center" :class="selectedBooks.includes(book.id) ? 'bg-blue-500 border-blue-500' : ''"></div>
                <div>
                  <h3 class="text-sm font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
                  <p class="text-[8px] text-zinc-600 uppercase mt-1 tracking-widest">UID: {{ book.id.slice(0,8) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'requests'" key="requests" class="py-10">
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
                <p class="text-[8px] text-zinc-500 font-bold uppercase mt-2 tracking-widest">Date: {{ req.returnDate }}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <button @click="approveRequest(req)" class="flex-1 py-3 bg-white text-black rounded-xl font-black text-[9px] uppercase tracking-widest">Approve</button>
              <button @click="declineRequest(req.id)" class="flex-1 py-3 bg-zinc-900 text-red-500 rounded-xl font-black text-[9px] uppercase tracking-widest border border-red-500/10">Decline</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Active Tracker</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Borrowers</h2>
          </section>
          <div v-for="person in borrowers" :key="person.id" 
               :class="isOverdue(person.returnSchedule) ? 'overdue-card' : 'standard-card'"
               class="p-6 rounded-[2rem] mb-4 flex justify-between items-center border shadow-2xl relative overflow-hidden transition-all group">
            
            <div class="relative z-10 flex-1">
              <h3 class="text-sm font-black uppercase tracking-tight leading-none mb-1">{{ person.bookTitle }}</h3>
              <p class="text-[9px] font-bold uppercase opacity-60 tracking-widest mb-4">{{ person.userEmail }}</p>
              
              <div class="flex items-center gap-4">
                <div class="flex flex-col">
                  <span class="text-[8px] font-bold uppercase opacity-40 tracking-widest mb-0.5">Deadline</span>
                  <span class="text-[12px] font-bold font-mono tracking-tighter uppercase">
                    {{ person.returnSchedule }} — 07:30 AM
                  </span>
                </div>
                <div v-if="isOverdue(person.returnSchedule)" class="px-2 py-0.5 rounded-full bg-red-500 text-white text-[8px] font-black uppercase tracking-tighter animate-pulse">
                  OVERDUE
                </div>
              </div>
            </div>

            <button @click="confirmReturn(person)" 
                    class="relative z-10 px-6 py-3 rounded-full text-[9px] font-black uppercase tracking-widest transition-all
                           bg-white/10 hover:bg-white hover:text-black border border-white/10 backdrop-blur-sm">
              Return
            </button>
          </div>

          <div v-if="borrowers.length === 0" class="text-center py-20">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">No Active Records</p>
          </div>
        </div>

        <div v-else-if="activeTab === 'community'" key="community" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">User Base</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Community</h2>
          </section>
          <div class="space-y-3">
            <div v-for="user in users" :key="user.id" class="bg-zinc-950 border border-white/5 p-4 rounded-2xl flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center font-bold text-blue-500 border border-white/5 uppercase">
                {{ user.email?.[0] }}
              </div>
              <div>
                <p class="text-[11px] font-black uppercase tracking-tighter">{{ user.email }}</p>
                <p class="text-[8px] font-bold uppercase tracking-widest" :class="user.role === 'admin' ? 'text-blue-500' : 'text-zinc-600'">
                  {{ user.role || 'Member' }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'logs'" key="logs" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">History</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">System Logs</h2>
          </section>
          <div class="space-y-2">
            <div v-for="log in historyLogs" :key="log.id" class="p-4 bg-zinc-950 border border-white/5 rounded-xl flex justify-between items-center">
              <div>
                <p class="text-[10px] font-bold uppercase truncate max-w-[150px]">{{ log.bookTitle }}</p>
                <p class="text-[8px] text-zinc-500 uppercase tracking-widest font-bold">{{ log.userEmail }}</p>
              </div>
              <span class="text-[8px] px-2 py-0.5 rounded font-black uppercase tracking-widest" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 text-center">
          <section class="text-left mb-10">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Identity</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Profile</h2>
          </section>
          <div class="w-24 h-24 bg-blue-600 border border-blue-400 mx-auto rounded-[2.5rem] flex items-center justify-center text-3xl font-black mb-4 shadow-2xl">A</div>
          <h2 class="text-2xl font-bold tracking-tighter uppercase">{{ auth.currentUser?.email }}</h2>
          <button @click="showLogoutModal = true" class="mt-20 w-full max-w-xs py-4 bg-zinc-900 text-red-500 rounded-2xl font-black uppercase text-[10px] tracking-widest border border-red-500/10 active:bg-red-600 active:text-white transition-all">Sign Out Admin</button>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 w-full max-w-[450px] px-4">
      <nav class="bg-zinc-900/60 backdrop-blur-3xl border border-white/10 rounded-full p-2 flex items-center justify-between shadow-2xl">
        <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'community', 'logs', 'profile']" :key="tab" @click="activeTab = tab" :class="activeTab === tab ? 'bg-white text-black scale-110 shadow-lg' : 'text-zinc-500 hover:text-white'" class="w-10 h-10 min-w-[40px] rounded-full flex items-center justify-center transition-all relative">
          <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute -top-1 -right-1 w-3 h-3 bg-red-600 rounded-full border border-black animate-pulse z-10"></div>
          <div v-if="tab === 'borrowers' && hasOverdue" class="absolute -top-1 -right-1 w-2 h-2 bg-red-600 rounded-full z-10 animate-ping"></div>
          <span class="text-[8px] font-black uppercase">{{ tab.slice(0, 3) }}</span>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showReturnModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div v-if="targetBorrower" class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-8 uppercase tracking-tighter">Confirm Return?</h3>
          <div class="flex gap-3">
            <button @click="showReturnModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="executeReturn" class="flex-1 py-4 rounded-2xl bg-white text-black font-black text-[10px] uppercase">Yes</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-xl font-bold tracking-tighter mb-6 uppercase apple-gradient text-center">Inventory</h2>
          <textarea v-model="batchTitleInput" placeholder="Titles..." rows="5" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-4 px-6 text-white outline-none font-bold mb-4 text-xs resize-none"></textarea>
          <button @click="batchAddBooks" :disabled="!batchTitleInput" class="w-full py-4 bg-white text-black rounded-2xl font-black uppercase text-[10px] tracking-widest active:scale-95 transition-all">Submit</button>
          <button @click="showAddModal = false" class="w-full py-4 text-zinc-600 font-bold uppercase text-[9px] mt-1">Cancel</button>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-6 uppercase tracking-tighter">Delete?</h3>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="deleteSelectedBooks" class="flex-1 py-4 rounded-2xl bg-red-600 text-white font-black text-[10px] uppercase">Yes</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-6 uppercase tracking-tighter">Terminate?</h3>
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
import { ref, onMounted, computed, defineEmits, onUnmounted } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, addDoc, deleteDoc, doc, updateDoc, serverTimestamp, query, orderBy, writeBatch } from "firebase/firestore";
import { signOut } from "firebase/auth";

const emit = defineEmits(['logout']);

const activeTab = ref('dashboard');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);
const selectedBooks = ref([]);

// Modals
const showAddModal = ref(false);
const showDeleteModal = ref(false);
const showReturnModal = ref(false);
const showLogoutModal = ref(false);

const targetBorrower = ref(null);
const batchTitleInput = ref('');
const currentTimeDisplay = ref('');

let clockInterval;

// STATUS CHECKER
const isOverdue = (schedule) => {
  if (!schedule) return false;
  const now = new Date();
  const target = new Date(schedule.replace(/-/g, '/'));
  target.setHours(7, 30, 0, 0); 
  return now.getTime() > target.getTime();
};

const hasOverdue = computed(() => borrowers.value.some(p => isOverdue(p.returnSchedule)));

const updateClock = () => {
  const now = new Date();
  currentTimeDisplay.value = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' });
};

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => historyLogs.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "borrowers"), (s) => borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
});

onUnmounted(() => clearInterval(clockInterval));

const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s.includes('approve') || s.includes('returned')) return 'text-green-500 bg-green-500/10';
  if (s.includes('decline')) return 'text-red-500 bg-red-500/10';
  return 'text-zinc-500 bg-zinc-900';
};

const batchAddBooks = async () => {
  const titles = batchTitleInput.value.split('\n').filter(t => t.trim() !== '');
  const batch = writeBatch(db);
  titles.forEach(title => {
    const docRef = doc(collection(db, "books"));
    batch.set(docRef, { title, createdAt: serverTimestamp() });
  });
  await batch.commit();
  batchTitleInput.value = '';
  showAddModal.value = false;
};

const toggleSelectBook = (id) => {
  const idx = selectedBooks.value.indexOf(id);
  if (idx > -1) selectedBooks.value.splice(idx, 1);
  else selectedBooks.value.push(id);
};

const deleteSelectedBooks = async () => {
  const batch = writeBatch(db);
  selectedBooks.value.forEach(id => {
    batch.delete(doc(db, "books", id));
  });
  await batch.commit();
  selectedBooks.value = [];
  showDeleteModal.value = false;
};

const approveRequest = async (req) => {
  try {
    await updateDoc(doc(db, "notifications", req.id), { 
      status: 'approved',
      message: `Approved: Due ${req.returnDate} @ 7:30 AM.`,
      approvedAt: serverTimestamp() 
    });
    await addDoc(collection(db, "borrowers"), {
      bookTitle: req.bookTitle,
      userEmail: req.userEmail,
      userId: req.userId,
      originalRequestId: req.id,
      returnSchedule: req.returnDate,
      status: 'active',
      approvedAt: serverTimestamp()
    });
    await addDoc(collection(db, "history"), {
      bookTitle: req.bookTitle,
      userEmail: req.userEmail,
      status: 'approved',
      createdAt: serverTimestamp()
    });
  } catch (err) {
    console.error("Approve Error:", err);
  }
};

const declineRequest = async (id) => {
  const req = notifications.value.find(n => n.id === id);
  await updateDoc(doc(db, "notifications", id), { status: 'declined' });
  await addDoc(collection(db, "history"), { 
    bookTitle: req?.bookTitle, 
    userEmail: req?.userEmail, 
    status: 'declined', 
    createdAt: serverTimestamp() 
  });
};

const confirmReturn = (person) => {
  targetBorrower.value = person;
  showReturnModal.value = true;
};

const executeReturn = async () => {
  if (!targetBorrower.value) return;
  const { id, bookTitle, userEmail, userId, originalRequestId } = targetBorrower.value;
  try {
    await deleteDoc(doc(db, "borrowers", id));
    if (originalRequestId) await updateDoc(doc(db, "notifications", originalRequestId), { status: 'returned_archive' });
    await addDoc(collection(db, "notifications"), {
      userId, bookTitle, userEmail,
      message: `Return recorded for ${bookTitle}`,
      status: 'returned_by_admin',
      createdAt: serverTimestamp()
    });
    await addDoc(collection(db, "history"), { bookTitle, userEmail, status: 'returned', createdAt: serverTimestamp() });
    showReturnModal.value = false;
    targetBorrower.value = null;
  } catch (err) {
    console.error("Return Error:", err);
  }
};

const executeLogout = async () => {
  await signOut(auth);
  emit('logout');
};
</script>

<style scoped>
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

/* 🍎 iOS MINIMALIST GRADIENTS FOR BORROWERS PAGE */
.standard-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
  border-color: rgba(255,255,255,0.08);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.overdue-card {
  background: linear-gradient(145deg, rgba(220,38,38,0.1) 0%, rgba(220,38,38,0.05) 100%);
  border-color: rgba(220,38,38,0.3);
  box-shadow: 0 20px 40px rgba(220,38,38,0.15);
}

.page-enter-active, .page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>