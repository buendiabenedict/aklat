<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden">
    
    <header class="relative h-[40vh] flex flex-col items-center justify-center px-6 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-zinc-900/50 to-black z-0"></div>
      
      <transition name="fade-up" appear>
        <div class="relative z-10 text-center">
          <div class="w-16 h-1 bg-white mx-auto mb-8 rounded-full"></div>
          <h1 class="text-6xl md:text-8xl font-bold tracking-tighter mb-4 italic">AKLAT</h1>
          <p class="text-zinc-500 uppercase tracking-[0.5em] text-[10px] md:text-xs">Digital Library Terminal v2.0</p>
        </div>
      </transition>
    </header>

    <main class="max-w-7xl mx-auto px-6 pb-24 relative z-10">
      
      <transition name="fade" appear>
        <div class="mb-12 sticky top-8 z-40">
          <div class="bg-zinc-950/80 backdrop-blur-xl border border-white/10 p-2 rounded-2xl flex items-center shadow-2xl">
            <div class="pl-6 pr-4 text-zinc-500">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search by title..." 
              class="bg-transparent border-none w-full py-4 text-lg outline-none focus:ring-0 placeholder:text-zinc-700"
            />
          </div>
        </div>
      </transition>

      <div v-if="filteredBooks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <transition-group name="list">
          <div 
            v-for="book in filteredBooks" 
            :key="book.id"
            class="group bg-zinc-950 border border-white/5 p-8 rounded-[2.5rem] hover:border-white/20 transition-all duration-500 hover:scale-[1.02] flex flex-col justify-between h-80"
          >
            <div>
              <div class="flex justify-between items-start mb-6">
                <div class="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center text-2xl group-hover:bg-white group-hover:text-black transition-all duration-500">📖</div>
                <span class="text-[10px] font-black uppercase tracking-widest text-zinc-600 group-hover:text-zinc-400">Available</span>
              </div>
              <h3 class="text-2xl font-bold tracking-tight leading-tight mb-2">{{ book.title }}</h3>
            </div>

            <button 
              @click="openBorrowModal(book)"
              class="w-full py-4 bg-white text-black rounded-2xl font-black text-xs uppercase tracking-widest active:scale-95 transition-all opacity-0 group-hover:opacity-100 translate-y-4 group-hover:translate-y-0 duration-300"
            >
              Request Borrow
            </button>
          </div>
        </transition-group>
      </div>

      <transition name="fade">
        <div v-if="filteredBooks.length === 0" class="py-40 text-center">
          <p class="text-zinc-600 italic text-xl">No books found in the archives.</p>
        </div>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-md px-6">
        <transition name="modal-pop">
          <div v-if="showModal" class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-lg w-full shadow-2xl">
            <h2 class="text-3xl font-bold tracking-tighter mb-2">Request Details</h2>
            <p class="text-zinc-500 text-sm mb-8">Confirm your return schedule for <span class="text-white italic">"{{ selectedBook?.title }}"</span></p>
            
            <div class="space-y-6">
              <div>
                <label class="text-[10px] font-black uppercase tracking-widest text-zinc-500 block mb-3">Return Date (Mon-Fri Only)</label>
                <input 
                  type="date" 
                  v-model="returnDate" 
                  :min="minDate"
                  @change="validateDate"
                  class="w-full bg-zinc-900 border border-white/10 rounded-2xl py-5 px-6 text-white outline-none focus:border-white/30 transition-all appearance-none"
                />
                <p v-if="dateError" class="text-red-500 text-[10px] mt-2 font-bold uppercase tracking-widest">{{ dateError }}</p>
              </div>

              <div>
                <label class="text-[10px] font-black uppercase tracking-widest text-zinc-500 block mb-3">Return Time</label>
                <input 
                  type="time" 
                  v-model="returnTime"
                  class="w-full bg-zinc-900 border border-white/10 rounded-2xl py-5 px-6 text-white outline-none focus:border-white/30 transition-all appearance-none"
                />
              </div>
            </div>

            <div class="flex gap-4 mt-12">
              <button @click="closeModal" class="flex-1 py-5 rounded-2xl border border-white/10 font-bold text-zinc-500 hover:text-white transition-all">Cancel</button>
              <button 
                @click="submitRequest" 
                :disabled="!returnDate || !returnTime || dateError"
                class="flex-1 py-5 rounded-2xl bg-white text-black font-black uppercase text-xs tracking-widest active:scale-95 disabled:opacity-20 transition-all"
              >
                Send Request
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>

    <transition name="slide-up">
      <div v-if="showToast" class="fixed bottom-12 left-1/2 -translate-x-1/2 bg-white text-black px-8 py-4 rounded-full font-black text-xs uppercase tracking-widest z-[150] shadow-2xl">
        Request Sent Successfully! 🚀
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, query, orderBy, addDoc, serverTimestamp } from "firebase/firestore";

// State
const books = ref([]);
const searchQuery = ref('');
const showModal = ref(false);
const showToast = ref(false);
const selectedBook = ref(null);

// Form State
const returnDate = ref('');
const returnTime = ref('');
const dateError = ref('');

// Min Date calculation (Tomorrow)
const minDate = computed(() => {
  const today = new Date();
  today.setDate(today.getDate() + 1);
  return today.toISOString().split('T')[0];
});

// Load Data
onMounted(() => {
  const q = query(collection(db, "books"), orderBy("createdAt", "desc"));
  onSnapshot(q, (snapshot) => {
    books.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  });
});

const filteredBooks = computed(() => {
  return books.value.filter(book => 
    book.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Handlers
const openBorrowModal = (book) => {
  selectedBook.ref = book; // In case needed for display
  selectedBook.value = book;
  showModal.value = true;
  returnDate.value = '';
  returnTime.value = '';
  dateError.value = '';
};

const closeModal = () => {
  showModal.value = false;
  selectedBook.value = null;
};

const validateDate = () => {
  if (!returnDate.value) return;
  const date = new Date(returnDate.value);
  const day = date.getUTCDay(); // 0 = Sun, 6 = Sat
  
  if (day === 0 || day === 6) {
    dateError.value = "Weekends are not available for return.";
  } else {
    dateError.value = "";
  }
};

const submitRequest = async () => {
  if (!auth.currentUser) {
    alert("Please sign in first!");
    return;
  }

  try {
    await addDoc(collection(db, "notifications"), {
      bookId: selectedBook.value.id,
      bookTitle: selectedBook.value.title,
      userId: auth.currentUser.uid,
      userEmail: auth.currentUser.email,
      returnSchedule: `${returnDate.value} at ${returnTime.value}`,
      createdAt: serverTimestamp(),
      status: 'pending'
    });

    closeModal();
    showToast.value = true;
    setTimeout(() => showToast.value = false, 3000);
  } catch (error) {
    console.error("Error sending request:", error);
  }
};
</script>

<style scoped>
/* Base Fade Animation */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.6s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Hero Fade Up */
.fade-up-enter-active {
  transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(40px);
}

/* List/Grid Animations */
.list-enter-active, .list-leave-active {
  transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}
.list-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}
.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Modal Pop Animation */
.modal-pop-enter-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.modal-pop-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

/* Slide Up Toast */
.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-enter-from {
  opacity: 0;
  transform: translate(-50%, 40px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}

/* Custom styles for native pickers to look a bit better in dark mode */
input[type="date"]::-webkit-calendar-picker-indicator,
input[type="time"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}
</style>