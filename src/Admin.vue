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
          <h1 class="text-sm font-bold tracking-tighter uppercase leading-none italic">Admin Central</h1>
          <p class="text-[10px] font-black text-blue-500 mt-1 uppercase tracking-widest">{{ currentTimeDisplay }}</p>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-2 bg-zinc-900 px-3 py-1.5 rounded-full border border-white/5">
          <div class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
          <span class="text-[9px] font-bold uppercase tracking-widest text-zinc-400">System Live</span>
        </div>
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
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient italic leading-none">Overview</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem] hover:border-white/10 transition-colors group">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 italic">Inventory</p>
              <p class="text-4xl font-bold tracking-tighter group-hover:scale-105 transition-transform duration-500">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem]">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 italic">Active Users</p>
              <p class="text-4xl font-bold tracking-tighter text-blue-500">{{ users.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem]">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 italic">Active Loans</p>
              <p class="text-4xl font-bold tracking-tighter text-amber-500">{{ borrowers.length }}</p>
            </div>
            <div @click="activeTab = 'logs'" class="bg-zinc-900 border border-white/10 p-6 rounded-[2rem] cursor-pointer active:scale-95 transition-all">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 italic">History Logs</p>
              <p class="text-4xl font-bold tracking-tighter text-zinc-400">{{ historyLogs.length }}</p>
            </div>
          </div>

          <section v-if="pendingRequests.length > 0" @click="activeTab = 'requests'" 
                   class="bg-blue-600 p-8 rounded-[2.5rem] cursor-pointer hover:bg-blue-500 transition-all relative overflow-hidden active:scale-[0.98]">
             <div class="relative z-10 text-black flex justify-between items-center">
               <div>
                 <h3 class="text-2xl font-black tracking-tighter mb-1 italic uppercase">Incoming Requests</h3>
                 <p class="text-black/60 text-[10px] tracking-widest font-bold uppercase">{{ pendingRequests.length }} assets awaiting authorization</p>
               </div>
               <div class="w-14 h-14 bg-black text-white rounded-2xl flex items-center justify-center font-black text-xl shadow-2xl animate-bounce">
                 {{ pendingRequests.length }}
               </div>
             </div>
          </section>
        </div>

        <div v-else-if="activeTab === 'inventory'" key="inventory" class="py-4">
          <section class="mb-8 flex justify-between items-end">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Asset Management</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient italic leading-none">Inventory</h2>
            </div>
            <div class="flex gap-2">
              <button v-if="selectedBooks.length > 0" @click="showDeleteModal = true" class="w-12 h-12 bg-red-600 text-white rounded-2xl flex items-center justify-center shadow-lg active:scale-90 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
              <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
              </button>
            </div>
          </section>
          
          <div class="space-y-2">
            <div v-for="book in books" :key="book.id" @click="toggleSelectBook(book.id)" 
                 :class="selectedBooks.includes(book.id) ? 'border-blue-600 bg-blue-600/10 scale-[0.98]' : 'border-white/5 bg-zinc-950'" 
                 class="p-6 rounded-[1.5rem] flex items-center justify-between border transition-all cursor-pointer">
              <div class="flex items-center gap-5">
                <div class="w-6 h-6 rounded-lg border-2 border-zinc-800 flex items-center justify-center transition-colors" :class="selectedBooks.includes(book.id) ? 'bg-blue-600 border-blue-600' : ''">
                   <svg v-if="selectedBooks.includes(book.id)" xmlns="http://www.w3.org/2000/center" class="w-4 h-4 text-white" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                </div>
                <div>
                  <h3 class="text-base font-bold tracking-tight uppercase italic leading-none">{{ book.title }}</h3>
                  <p class="text-[8px] text-zinc-600 uppercase mt-1.5 tracking-widest font-black">Asset UID: {{ book.id.slice(0,12) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'requests'" key="requests" class="py-10">
          <section class="mb-8">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Queue Management</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient italic leading-none">Approvals</h2>
          </section>

          <div v-if="pendingRequests.length === 0" class="p-24 border border-dashed border-white/5 rounded-[3rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[10px] tracking-[0.5em]">No Pending Actions</p>
          </div>

          <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-950 border border-white/5 p-8 rounded-[2.5rem] mb-6 shadow-2xl">
            <div class="mb-8">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <p class="text-[8px] text-zinc-500 font-black uppercase tracking-widest">Awaiting Confirmation</p>
              </div>
              <h3 class="text-2xl font-bold tracking-tighter uppercase italic leading-none mb-3">{{ req.bookTitle }}</h3>
              <p class="text-[10px] text-blue-500 font-bold uppercase tracking-widest">{{ req.userEmail }}</p>
              
              <div class="mt-6 flex items-center gap-3 bg-zinc-900 w-max px-4 py-2 rounded-2xl border border-white/5">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                <span class="text-[10px] font-bold text-zinc-300 uppercase tracking-widest">Return: {{ req.returnSchedule }}</span>
              </div>
            </div>
            <div class="flex gap-3">
              <button @click="approveRequest(req)" class="flex-[2] py-5 bg-white text-black rounded-[1.5rem] font-black text-[11px] uppercase tracking-[0.2em] active:scale-95 transition-all">Authorize</button>
              <button @click="declineRequest(req.id)" class="flex-1 py-5 bg-zinc-900 text-red-500 rounded-[1.5rem] font-black text-[11px] uppercase tracking-[0.2em] border border-red-500/10 active:scale-95 transition-all">Decline</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="py-10">
          <section class="mb-8">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Live Tracking</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient italic leading-none">Borrowers</h2>
          </section>
          
          <div v-for="person in borrowers" :key="person.id" 
               :class="isOverdue(person.returnSchedule) ? 'overdue-card' : 'standard-card'"
               class="p-8 rounded-[2.5rem] mb-4 flex justify-between items-center border shadow-2xl relative overflow-hidden transition-all group">
            
            <div class="relative z-10 flex-1">
              <div class="flex items-center gap-2 mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white/40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <h3 class="text-lg font-black uppercase tracking-tighter leading-none italic">{{ person.bookTitle }}</h3>
              </div>
              <p class="text-[10px] font-bold uppercase opacity-60 tracking-widest mb-6">{{ person.userEmail }}</p>
              
              <div class="flex items-center gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-[13px] font-bold font-mono tracking-tighter uppercase text-white/90">
                  {{ person.returnSchedule }} <span class="text-blue-500">— 07:30 AM</span>
                </span>
              </div>
            </div>

            <button @click="markAsReturned(person)" 
                    class="relative z-10 px-8 py-5 rounded-[1.5rem] text-[10px] font-black uppercase tracking-widest transition-all
                           bg-white text-black hover:bg-zinc-200 active:scale-95 shadow-2xl">
              Return
            </button>
          </div>
        </div>

        <div v-else-if="activeTab === 'logs'" key="logs" class="py-10">
          <section class="mb-8 flex justify-between items-end">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Audit Record</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient italic leading-none">History</h2>
            </div>
            <button @click="clearHistory" class="text-[9px] font-black uppercase tracking-[0.2em] text-red-500 bg-red-500/10 px-5 py-2.5 rounded-full border border-red-500/20 active:opacity-50 transition-all italic">Wipe Database</button>
          </section>
          
          <div class="space-y-3">
            <div v-for="log in historyLogs" :key="log.id" class="p-6 bg-zinc-950 border border-white/5 rounded-[1.5rem] flex justify-between items-center transition-all hover:bg-zinc-900/50">
              <div>
                <p class="text-[11px] font-bold uppercase tracking-tight italic mb-0.5">{{ log.bookTitle }}</p>
                <p class="text-[9px] text-zinc-500 uppercase tracking-widest font-black">{{ log.userEmail }}</p>
              </div>
              <div class="text-right">
                <span class="text-[8px] px-3 py-1 rounded-full font-black uppercase tracking-widest inline-block mb-1.5" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
                <p class="text-[8px] text-zinc-700 font-mono font-bold">{{ formatTimestamp(log.createdAt) }}</p>
              </div>
            </div>
          </div>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-[440px] px-6">
      <nav class="bg-zinc-900/70 backdrop-blur-3xl border border-white/10 rounded-[2rem] p-2 flex items-center justify-between shadow-[0_25px_50px_-12px_rgba(0,0,0,0.8)]">
        <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'logs']" :key="tab" @click="activeTab = tab" 
                :class="activeTab === tab ? 'bg-white text-black shadow-2xl scale-110' : 'text-zinc-600 hover:text-zinc-300'" 
                class="w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-500 relative group">
          
          <svg v-if="tab === 'dashboard'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          <svg v-if="tab === 'inventory'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
          <svg v-if="tab === 'requests'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          <svg v-if="tab === 'borrowers'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          <svg v-if="tab === 'logs'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          
          <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-blue-600 rounded-full flex items-center justify-center text-[10px] font-black text-white border-2 border-black animate-pulse shadow-lg">{{ pendingRequests.length }}</div>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-3xl font-bold tracking-tighter mb-8 uppercase italic apple-gradient">Add Asset</h2>
          <div class="space-y-4 mb-10">
            <input v-model="newBook.title" type="text" placeholder="Entry Title" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold placeholder:text-zinc-700 focus:border-blue-600 transition-all uppercase italic" @keyup.enter="addBook" />
          </div>
          <div class="flex gap-3">
            <button @click="addBook" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Submit Entry</button>
            <button @click="showAddModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Abort</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-xs w-full text-center shadow-2xl">
          <div class="w-20 h-20 bg-red-600/10 text-red-600 mx-auto rounded-3xl flex items-center justify-center mb-6 border border-red-600/20">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </div>
          <h3 class="text-2xl font-black mb-2 uppercase italic tracking-tighter">De-register?</h3>
          <p class="text-zinc-500 text-[10px] uppercase font-bold tracking-widest mb-10">Permanent deletion of {{ selectedBooks.length }} item(s).</p>
          <div class="flex flex-col gap-3">
            <button @click="deleteSelectedBooks" class="w-full py-5 bg-red-600 text-white rounded-2xl font-black uppercase text-[11px] tracking-[0.2em] active:scale-95 transition-all shadow-xl shadow-red-600/20">Purge Selected</button>
            <button @click="showDeleteModal = false" class="w-full py-5 text-zinc-600 font-bold uppercase text-[10px] tracking-widest active:opacity-50">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, defineEmits } from 'vue';
import { db } from './lib/firebase';
import { collection, onSnapshot, addDoc, deleteDoc, doc, updateDoc, serverTimestamp, query, orderBy, writeBatch } from "firebase/firestore";

const emit = defineEmits(['logout']);
const activeTab = ref('dashboard');
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

let clockInterval;

const updateClock = () => {
  const now = new Date();
  currentTimeDisplay.value = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' });
};

const isOverdue = (schedule) => {
  if (!schedule) return false;
  const now = new Date();
  const target = new Date(schedule.replace(/-/g, '/'));
  target.setHours(7, 30, 0, 0); 
  return now.getTime() > target.getTime();
};

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  // Real-time Database Sync
  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => historyLogs.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "borrowers"), (s) => borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
});

onUnmounted(() => clearInterval(clockInterval));

// Computed
const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

// Logic Functions
const toggleSelectBook = (id) => {
  const index = selectedBooks.value.indexOf(id);
  if (index > -1) selectedBooks.value.splice(index, 1);
  else selectedBooks.value.push(id);
};

const addBook = async () => {
  if (!newBook.value.title.trim()) return;
  await addDoc(collection(db, "books"), { title: newBook.value.title.toUpperCase(), createdAt: serverTimestamp() });
  newBook.value.title = '';
  showAddModal.value = false;
};

const deleteSelectedBooks = async () => {
  const batch = writeBatch(db);
  selectedBooks.value.forEach(id => batch.delete(doc(db, "books", id)));
  await batch.commit();
  selectedBooks.value = [];
  showDeleteModal.value = false;
};

const approveRequest = async (req) => {
  await updateDoc(doc(db, "notifications", req.id), { status: 'approved' });
  await addDoc(collection(db, "borrowers"), { ...req, status: 'active', approvedAt: serverTimestamp() });
  await addDoc(collection(db, "history"), { ...req, status: 'approved', createdAt: serverTimestamp() });
};

const declineRequest = async (id) => {
  await updateDoc(doc(db, "notifications", id), { status: 'declined' });
  await addDoc(collection(db, "history"), { id, status: 'declined', createdAt: serverTimestamp() });
};

const markAsReturned = async (person) => {
  await addDoc(collection(db, "history"), { ...person, status: 'returned', createdAt: serverTimestamp() });
  await deleteDoc(doc(db, "borrowers", person.id));
};

// UI Helpers
const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s.includes('approved') || s.includes('returned')) return 'text-green-500 bg-green-500/10 border-green-500/20';
  if (s.includes('declined')) return 'text-red-500 bg-red-500/10 border-red-500/20';
  return 'text-zinc-500 bg-zinc-900 border-white/5';
};

const formatTimestamp = (ts) => {
  if (!ts) return '...';
  return new Date(ts.seconds * 1000).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' });
};

const clearHistory = async () => {
  if (confirm("Are you sure you want to clear all history logs?")) {
     const batch = writeBatch(db);
     historyLogs.value.forEach(log => batch.delete(doc(db, "history", log.id)));
     await batch.commit();
  }
};
</script>

<style scoped>
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.standard-card { background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%); border-color: rgba(255,255,255,0.08); }
.overdue-card { background: linear-gradient(145deg, rgba(220,38,38,0.1) 0%, rgba(220,38,38,0.05) 100%); border-color: rgba(220,38,38,0.3); }

.page-enter-active, .page-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.4s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>