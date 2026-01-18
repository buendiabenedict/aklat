<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-32">
    
    <header class="relative h-[35vh] flex flex-col items-center justify-center px-6 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-zinc-900/40 to-black z-0"></div>
      
      <transition name="fade-up" appear>
        <div class="relative z-10 text-center">
          <div class="w-12 h-1 bg-white mx-auto mb-6 rounded-full opacity-50"></div>
          <h1 class="text-7xl font-bold tracking-tighter mb-2 italic">AKLAT</h1>
          <p class="text-zinc-500 uppercase tracking-[0.4em] text-[10px]">Public Library Access</p>
        </div>
      </transition>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      
      <transition name="page" mode="out-in">
        <div v-if="activeTab === 'explore'" key="explore">
          <div class="mb-10 sticky top-6 z-40">
            <div class="bg-zinc-900/50 backdrop-blur-2xl border border-white/10 p-1.5 rounded-2xl flex items-center shadow-2xl">
              <div class="pl-5 pr-3 text-zinc-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </div>
              <input v-model="searchQuery" type="text" placeholder="Find your next read..." class="bg-transparent border-none w-full py-4 text-base outline-none focus:ring-0 placeholder:text-zinc-700" />
            </div>
          </div>

          <div v-if="filteredBooks.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <transition-group name="list">
              <div v-for="book in filteredBooks" :key="book.id" class="group bg-zinc-950 border border-white/5 p-8 rounded-[2rem] hover:border-white/20 transition-all duration-500 flex flex-col justify-between h-72">
                <div>
                  <div class="w-10 h-10 bg-white/5 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white group-hover:text-black transition-all">📖</div>
                  <h3 class="text-xl font-bold tracking-tight mb-1">{{ book.title }}</h3>
                  <p class="text-[10px] text-zinc-600 uppercase tracking-widest">General Collection</p>
                </div>
                <button @click="openBorrowModal(book)" class="w-full py-4 bg-zinc-900 text-white group-hover:bg-white group-hover:text-black rounded-xl font-black text-[10px] uppercase tracking-[0.2em] active:scale-95 transition-all">Request Borrow</button>
              </div>
            </transition-group>
          </div>
          <div v-else class="py-20 text-center text-zinc-700 italic">No matches found.</div>
        </div>

        <div v-else-if="activeTab === 'status'" key="status" class="py-10">
          <h2 class="text-4xl font-bold tracking-tighter mb-8">My Requests</h2>
          <div class="space-y-4">
            <div v-if="userRequests.length === 0" class="p-10 border border-dashed border-white/10 rounded-3xl text-center text-zinc-600 italic">No active requests found.</div>
            <div v-for="req in userRequests" :key="req.id" class="p-6 bg-zinc-950 border border-white/5 rounded-2xl flex justify-between items-center">
              <div>
                <p class="font-bold text-lg">{{ req.bookTitle }}</p>
                <p class="text-[10px] text-zinc-500 uppercase tracking-widest mt-1">Due: {{ req.returnSchedule }}</p>
              </div>
              <span :class="req.status === 'approved' ? 'text-green-500' : 'text-yellow-500'" class="text-[10px] font-black uppercase tracking-widest">{{ req.status }}</span>
            </div>
          </div>
        </div>
      </transition>
    </main>

    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 w-full max-w-[320px] px-4">
      <nav class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-full p-2 flex items-center justify-around shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
        <button @click="activeTab = 'explore'" :class="activeTab === 'explore' ? 'bg-white text-black' : 'text-zinc-500'" class="flex items-center justify-center w-14 h-14 rounded-full transition-all duration-500">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        </button>
        <button @click="activeTab = 'status'" :class="activeTab === 'status' ? 'bg-white text-black' : 'text-zinc-500'" class="flex items-center justify-center w-14 h-14 rounded-full transition-all duration-500 relative">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
          <span v-if="userRequests.length > 0" class="absolute top-3 right-3 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center bg-black/90 backdrop-blur-md px-4 pb-10 sm:pb-0">
        <transition name="modal-pop">
          <div v-if="showModal" class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem] max-w-sm w-full">
            <h2 class="text-3xl font-bold tracking-tighter mb-6">Return Schedule</h2>
            <div class="space-y-6">
              <div>
                <label class="text-[10px] font-black uppercase tracking-widest text-zinc-600 block mb-2">Select Weekday</label>
                <input type="date" v-model="returnDate" :min="minDate" @change="validateDate" class="w-full bg-zinc-900 border border-white/5 rounded-xl py-4 px-5 text-white outline-none focus:border-white/20 appearance-none" />
                <p v-if="dateError" class="text-red-500 text-[9px] mt-2 font-bold uppercase tracking-widest">{{ dateError }}</p>
              </div>
              <div>
                <label class="text-[10px] font-black uppercase tracking-widest text-zinc-600 block mb-2">Preferred Time</label>
                <input type="time" v-model="returnTime" class="w-full bg-zinc-900 border border-white/5 rounded-xl py-4 px-5 text-white outline-none focus:border-white/20 appearance-none" />
              </div>
            </div>
            <div class="flex gap-3 mt-10">
              <button @click="closeModal" class="flex-1 py-4 text-zinc-500 font-bold text-xs uppercase tracking-widest">Cancel</button>
              <button @click="submitRequest" :disabled="!returnDate || !returnTime || dateError" class="flex-1 py-4 bg-white text-black rounded-xl font-black text-xs uppercase tracking-widest disabled:opacity-10 transition-all">Submit</button>
            </div>
          </div>
        </transition>
      </div>
    </transition>

    <transition name="slide-up">
      <div v-if="showToast" class="fixed top-12 left-1/2 -translate-x-1/2 bg-white text-black px-6 py-3 rounded-full font-black text-[10px] uppercase tracking-widest z-[150] shadow-2xl">
        Request Sent 🚀
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, query, orderBy, addDoc, serverTimestamp, where } from "firebase/firestore";

const books = ref([]);
const userRequests = ref([]);
const searchQuery = ref('');
const activeTab = ref('explore');
const showModal = ref(false);
const showToast = ref(false);
const selectedBook = ref(null);
const returnDate = ref('');
const returnTime = ref('');
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
  dateError.value = '';
};

const closeModal = () => {
  showModal.value = false;
  selectedBook.value = null;
};

const validateDate = () => {
  if (!returnDate.value) return;
  const d = new Date(returnDate.value).getUTCDay();
  dateError.value = (d === 0 || d === 6) ? "Weekends not allowed" : "";
};

const submitRequest = async () => {
  if (!auth.currentUser) return;
  try {
    await addDoc(collection(db, "notifications"), {
      bookId: selectedBook.value.id,
      bookTitle: selectedBook.value.title,
      userId: auth.currentUser.uid,
      userEmail: auth.currentUser.email,
      returnSchedule: `${returnDate.value} @ ${returnTime.value}`,
      createdAt: serverTimestamp(),
      status: 'pending'
    });
    closeModal();
    showToast.value = true;
    setTimeout(() => showToast.value = false, 3000);
  } catch (e) { console.error(e); }
};
</script>

<style scoped>
/* Page & List Transitions */
.page-enter-active, .page-leave-active { transition: all 0.4s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }

.list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from { opacity: 0; transform: scale(0.95); }

.modal-pop-enter-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.modal-pop-enter-from { opacity: 0; transform: translateY(100%) scale(0.9); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.4s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-up-enter-from { opacity: 0; transform: translate(-50%, -20px); }

input[type="date"]::-webkit-calendar-picker-indicator,
input[type="time"]::-webkit-calendar-picker-indicator { filter: invert(1); opacity: 0.5; }
</style>