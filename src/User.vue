<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40">
    
    <header class="p-8 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-black font-black text-xl shadow-[0_0_20px_rgba(255,255,255,0.2)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <h1 class="text-xl font-bold tracking-tighter italic">AKLAT</h1>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900/50 px-4 py-2 rounded-full border border-white/5">
        <div class="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_8px_rgba(34,197,94,0.6)]"></div>
        <span class="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-400">System Online</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'home'" key="home" class="space-y-10 py-6">
          <section>
            <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-2">Interface 01</p>
            <h2 class="text-5xl font-bold tracking-tighter">Terminal Dashboard</h2>
          </section>

          <div class="grid grid-cols-2 gap-4">
            <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem]">
              <div class="text-zinc-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
              </div>
              <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-1">Stock</p>
              <p class="text-4xl font-bold tracking-tighter text-white">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem]">
              <div class="text-blue-500 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
              <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-1">Activity</p>
              <p class="text-4xl font-bold tracking-tighter text-blue-500">{{ userRequests.length }}</p>
            </div>
          </div>

          <section class="bg-white text-black p-10 rounded-[3rem] relative overflow-hidden group cursor-pointer" @click="activeTab = 'explore'">
            <div class="relative z-10">
              <h3 class="text-3xl font-black tracking-tighter mb-2">Access Archives</h3>
              <p class="text-black/60 text-sm font-medium mb-8">Click to browse our collection of curated books.</p>
              <div class="inline-flex items-center gap-2 font-black text-[10px] uppercase tracking-widest">
                Explore Now
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
              </div>
            </div>
          </section>
        </div>

        <div v-else-if="activeTab === 'explore'" key="explore" class="py-6">
          <div class="mb-12 sticky top-6 z-40">
            <div class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 p-2 rounded-2xl flex items-center shadow-2xl">
              <div class="pl-6 pr-4 text-zinc-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </div>
              <input v-model="searchQuery" type="text" placeholder="Filter index..." class="bg-transparent border-none w-full py-4 text-lg outline-none focus:ring-0 placeholder:text-zinc-800 font-bold" />
            </div>
          </div>

          <div v-if="filteredBooks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <transition-group name="list">
              <div v-for="book in filteredBooks" :key="book.id" class="group bg-zinc-950 border border-white/5 p-10 rounded-[2.5rem] hover:border-white/20 transition-all duration-500 flex flex-col justify-between h-80">
                <div>
                  <div class="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-white group-hover:text-black transition-all duration-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                  </div>
                  <h3 class="text-2xl font-bold tracking-tight mb-2 group-hover:text-zinc-300 transition-colors">{{ book.title }}</h3>
                  <p class="text-[10px] text-zinc-600 uppercase tracking-[0.3em] font-black">Digital Record</p>
                </div>
                <button @click="openBorrowModal(book)" class="w-full py-4 bg-zinc-900 text-white group-hover:bg-white group-hover:text-black rounded-xl font-black text-[10px] uppercase tracking-[0.2em] active:scale-95 transition-all">Borrow Asset</button>
              </div>
            </transition-group>
          </div>
          <div v-else class="py-20 text-center text-zinc-800 font-bold uppercase tracking-widest text-xs italic">Zero results found.</div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 space-y-8">
          <div class="text-center">
            <div class="w-24 h-24 bg-zinc-900 border border-white/10 mx-auto rounded-[2.5rem] flex items-center justify-center text-white text-3xl font-black mb-6">
              {{ auth.currentUser?.email?.[0].toUpperCase() }}
            </div>
            <h2 class="text-3xl font-bold tracking-tighter">{{ auth.currentUser?.email }}</h2>
            <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mt-3">Auth Identity</p>
          </div>

          <div class="bg-zinc-950 border border-white/5 rounded-[3rem] p-10 space-y-8 shadow-2xl">
            <div class="flex justify-between items-center border-b border-white/[0.03] pb-6">
              <span class="text-zinc-500 text-[10px] font-black uppercase tracking-widest">ID Reference</span>
              <span class="text-xs font-mono text-zinc-400">{{ auth.currentUser?.uid.substring(0, 16) }}...</span>
            </div>
            <div class="flex justify-between items-center border-b border-white/[0.03] pb-6">
              <span class="text-zinc-500 text-[10px] font-black uppercase tracking-widest">Loan Count</span>
              <span class="text-white font-black text-xl">{{ userRequests.length }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-zinc-500 text-[10px] font-black uppercase tracking-widest">System Status</span>
              <span class="text-green-500 text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full border border-green-500/20">Authorized</span>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'status'" key="status" class="py-10">
          <h2 class="text-4xl font-bold tracking-tighter mb-10">Request History</h2>
          <div class="space-y-4">
            <div v-if="userRequests.length === 0" class="p-20 border border-dashed border-white/10 rounded-[3rem] text-center text-zinc-800 font-bold uppercase tracking-widest text-xs">No entries.</div>
            <div v-for="req in userRequests" :key="req.id" class="p-10 bg-zinc-950 border border-white/5 rounded-[2.5rem] flex flex-col sm:flex-row justify-between sm:items-center gap-6">
              <div>
                <p class="font-bold text-2xl tracking-tight">{{ req.bookTitle }}</p>
                <div class="flex items-center gap-2 mt-3 text-zinc-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  <span class="text-[10px] font-bold uppercase tracking-[0.2em]">{{ req.returnSchedule }}</span>
                </div>
              </div>
              <span :class="req.status === 'approved' ? 'text-green-500' : 'text-yellow-600'" class="text-[10px] font-black uppercase tracking-[0.3em] px-6 py-2 rounded-full border border-current opacity-60">
                {{ req.status }}
              </span>
            </div>
          </div>
        </div>
      </transition>
    </main>

    <div class="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-[360px] px-6">
      <nav class="bg-zinc-900/90 backdrop-blur-3xl border border-white/10 rounded-full p-2 flex items-center justify-between shadow-2xl">
        <button @click="activeTab = 'home'" :class="activeTab === 'home' ? 'bg-white text-black' : 'text-zinc-500'" class="flex items-center justify-center w-12 h-12 rounded-full transition-all duration-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
        </button>
        <button @click="activeTab = 'explore'" :class="activeTab === 'explore' ? 'bg-white text-black' : 'text-zinc-500'" class="flex items-center justify-center w-12 h-12 rounded-full transition-all duration-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        </button>
        <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'bg-white text-black' : 'text-zinc-500'" class="flex items-center justify-center w-12 h-12 rounded-full transition-all duration-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        </button>
        <div class="w-px h-6 bg-white/10"></div>
        <button @click="showLogoutModal = true" class="flex items-center justify-center w-12 h-12 rounded-full text-zinc-600 hover:text-red-500 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-md px-6">
        <transition name="modal-pop">
          <div v-if="showModal" class="bg-zinc-950 border border-white/10 p-10 rounded-[3.5rem] max-w-sm w-full shadow-[0_0_80px_rgba(0,0,0,1)] text-center">
            <h2 class="text-3xl font-bold tracking-tighter mb-2">Loan Schedule</h2>
            <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-10">Select return date (Mon-Fri)</p>
            
            <div class="space-y-6">
              <div>
                <input 
                  type="date" 
                  v-model="returnDate" 
                  :min="minDate" 
                  @input="validateDate" 
                  class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-6 px-6 text-white outline-none appearance-none font-bold text-center" 
                />
                <p v-if="dateError" class="text-red-600 text-[9px] mt-4 font-black uppercase tracking-[0.2em]">{{ dateError }}</p>
              </div>
            </div>

            <div class="flex flex-col gap-3 mt-10">
              <button 
                @click="submitRequest" 
                :disabled="!returnDate || dateError !== ''" 
                class="w-full py-5 bg-white text-black rounded-2xl font-black uppercase text-[10px] tracking-widest disabled:opacity-20 transition-all active:scale-95 shadow-xl shadow-white/5"
              >
                Confirm Request
              </button>
              <button @click="closeModal" class="w-full py-4 text-zinc-600 font-bold uppercase text-[10px] tracking-widest hover:text-white transition-colors">
                Cancel
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-md px-6 text-center">
        <div class="bg-zinc-950 border border-white/10 p-12 rounded-[3.5rem] max-w-sm w-full shadow-2xl">
          <h3 class="text-3xl font-bold mb-3 tracking-tighter">Sign Out</h3>
          <p class="text-zinc-600 text-xs font-medium mb-10">Terminate current session?</p>
          <div class="flex gap-4">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 uppercase text-[10px]">No</button>
            <button @click="executeLogout" class="flex-1 py-4 rounded-2xl bg-red-600 text-white font-black uppercase text-[10px]">Terminate</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="slide-up">
      <div v-if="showToast" class="fixed top-12 left-1/2 -translate-x-1/2 bg-white text-black px-10 py-4 rounded-full font-black text-[10px] uppercase tracking-widest z-[150] shadow-2xl text-center min-w-[280px]">
        Success: Entry Recorded
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineEmits } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, query, orderBy, addDoc, serverTimestamp, where } from "firebase/firestore";
import { signOut } from "firebase/auth";

const emit = defineEmits(['logout']);

const books = ref([]);
const userRequests = ref([]);
const searchQuery = ref('');
const activeTab = ref('home');
const showModal = ref(false);
const showLogoutModal = ref(false);
const showToast = ref(false);
const selectedBook = ref(null);
const returnDate = ref('');
const dateError = ref('');

const minDate = computed(() => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split('T')[0];
});

onMounted(() => {
  onSnapshot(query(collection(db, "books"), orderBy("createdAt", "desc")), (s) => {
    books.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });

  if (auth.currentUser) {
    onSnapshot(query(collection(db, "notifications"), where("userId", "==", auth.currentUser.uid)), (s) => {
      userRequests.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
    });
  }
});

const filteredBooks = computed(() => books.value.filter(b => b.title.toLowerCase().includes(searchQuery.value.toLowerCase())));

const openBorrowModal = (book) => {
  selectedBook.value = book;
  showModal.value = true;
  returnDate.value = '';
  dateError.value = '';
};

const closeModal = () => {
  showModal.value = false;
  selectedBook.value = null;
};

const validateDate = () => {
  if (!returnDate.value) {
    dateError.value = "";
    return;
  }
  const [year, month, day] = returnDate.value.split('-').map(Number);
  const selected = new Date(year, month - 1, day);
  const dayOfWeek = selected.getDay();

  if (dayOfWeek === 0 || dayOfWeek === 6) {
    dateError.value = "Selected day is a weekend.";
  } else {
    dateError.value = "";
  }
};

const submitRequest = async () => {
  if (!auth.currentUser || !returnDate.value || dateError.value !== "") return;
  try {
    await addDoc(collection(db, "notifications"), {
      bookId: selectedBook.value.id,
      bookTitle: selectedBook.value.title,
      userId: auth.currentUser.uid,
      userEmail: auth.currentUser.email,
      returnSchedule: returnDate.value,
      createdAt: serverTimestamp(),
      status: 'pending'
    });
    closeModal();
    showToast.value = true;
    setTimeout(() => showToast.value = false, 3000);
  } catch (e) { console.error(e); }
};

const executeLogout = async () => {
  try {
    await signOut(auth);
    emit('logout');
  } catch (e) { emit('logout'); }
};
</script>

<style scoped>
.page-enter-active, .page-leave-active { transition: all 0.4s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }

.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from { opacity: 0; transform: scale(0.95); }

.modal-pop-enter-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.modal-pop-enter-from { opacity: 0; transform: scale(0.9) translateY(40px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.4s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-up-enter-from { opacity: 0; transform: translate(-50%, -20px); }

input[type="date"]::-webkit-calendar-picker-indicator { filter: invert(1); opacity: 0.5; cursor: pointer; }
</style>