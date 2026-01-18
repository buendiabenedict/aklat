<template>
  <div class="fixed inset-0 bg-black text-white font-ios flex overflow-hidden w-full h-full">
    
    <transition name="fade">
      <div v-if="showWelcome" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center">
        <p class="text-zinc-600 uppercase tracking-[0.6em] text-[10px] mb-4 animate-pulse">Personal Access Granted</p>
        <h2 class="text-5xl font-bold tracking-tighter">Welcome to Your Library</h2>
      </div>
    </transition>

    <aside 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']" 
      class="w-72 h-full border-r border-white/10 bg-zinc-950 z-50 flex flex-col transition-all duration-700 ease-in-out shrink-0"
    >
      <div class="h-28 flex items-center px-8 overflow-hidden">
        <div class="w-8 h-8 bg-white rounded-lg shrink-0 shadow-[0_0_15px_rgba(255,255,255,0.2)]"></div>
        <h1 class="ml-4 text-xs font-black tracking-widest uppercase text-white">Aklat Student</h1>
      </div>

      <nav class="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
        <button v-for="item in navItems" :key="item.name" @click="activeTab = item.id"
          class="w-full flex items-center h-14 rounded-xl px-4 transition-all duration-200"
          :class="activeTab === item.id ? 'bg-white text-black' : 'text-zinc-500 hover:text-white'">
          <div class="w-6 h-6 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" :d="item.path" /></svg>
          </div>
          <span class="ml-4 font-bold text-sm tracking-tight whitespace-nowrap">{{ item.name }}</span>
        </button>
      </nav>

      <div class="p-6 border-t border-white/5 space-y-4">
        <div class="flex items-center gap-3 px-2">
          <div class="relative flex h-2 w-2">
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"></span>
            <span :class="dbStatus === 'online' ? 'bg-green-500' : 'bg-red-500'" class="relative inline-flex rounded-full h-2 w-2"></span>
          </div>
          <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-500 whitespace-nowrap">Cloud Sync: {{ dbStatus }}</p>
        </div>

        <button @click="showLogoutModal = true" class="w-full h-14 flex items-center justify-center rounded-xl text-red-500 hover:bg-red-500/10 transition-all group">
          <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          <span class="ml-3 font-bold text-xs uppercase tracking-widest whitespace-nowrap">Sign Out</span>
        </button>
      </div>
    </aside>

    <main 
      :class="[showWelcome ? 'opacity-5' : 'opacity-100']"
      class="flex-1 h-full overflow-y-auto p-8 md:p-16 relative z-10 transition-opacity duration-1000 bg-black"
    >
      <header class="mb-16 flex justify-between items-start">
        <div>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3 flex items-center gap-2">
            {{ currentTime }} 
            <span class="w-1 h-1 bg-zinc-800 rounded-full"></span> 
            Personal Portal
          </p>
          <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab === 'inventory' ? 'My Library' : activeTab }}</h2>
        </div>
        
        <div v-if="activeTab === 'inventory'">
          <button @click="showAddBookModal = true" class="bg-white text-black px-8 py-4 rounded-xl font-bold hover:bg-zinc-200 transition-all flex items-center gap-2 active:scale-95 shadow-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" /></svg>
            Add to My List
          </button>
        </div>
      </header>

      <transition name="fade" mode="out-in">
        <div v-if="activeTab === 'home'" :key="'home'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950 group hover:border-white/30 transition-all">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">My Total Books</h3>
            <p class="text-3xl font-bold tracking-tighter">{{ myBooks.length }}</p>
          </div>
          <div class="p-8 border border-white/10 rounded-2xl bg-zinc-950 group hover:border-white/30 transition-all">
            <h3 class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest mb-4">Account Status</h3>
            <p class="text-3xl font-bold tracking-tighter text-green-500">Active Member</p>
          </div>
        </div>

        <section v-else-if="activeTab === 'inventory'" :key="'inventory'" class="space-y-8">
          <div class="relative w-full max-w-xl">
             <input v-model="searchQuery" type="text" placeholder="Search my collection..." class="bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white w-full outline-none focus:border-white/30 transition-all" />
          </div>
          
          <div v-if="myBooks.length === 0" class="p-20 text-center border border-dashed border-white/10 rounded-3xl">
             <p class="text-zinc-500">Your library is empty. Start adding some books! 📚</p>
          </div>

          <div v-else class="border border-white/10 rounded-2xl overflow-hidden bg-zinc-950">
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
                    <button @click="confirmDelete(book.id)" class="text-zinc-500 hover:text-red-500 font-bold text-[10px] uppercase tracking-widest transition-colors">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div v-else-if="activeTab === 'settings'" :key="'settings'" class="p-10 border border-white/10 rounded-2xl text-zinc-500">
           Email: {{ currentUserEmail }} <br/>
           Access Level: Student <br/>
           Sync Status: Verified 🛡️
        </div>
      </transition>
    </main>

    <transition name="fade">
      <div v-if="showAddBookModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-lg w-full">
          <h3 class="text-2xl font-bold mb-6 tracking-tighter text-white">Add New Book</h3>
          <div class="space-y-4 mb-8">
            <label class="text-[10px] uppercase tracking-widest text-zinc-600 font-black">Title</label>
            <input v-model="newBookTitle" @keyup.enter="addBook" type="text" placeholder="What are you reading?" class="w-full bg-zinc-900 border border-white/10 rounded-xl py-4 px-6 text-white outline-none focus:border-white/40 transition-all"/>
          </div>
          <div class="flex gap-3">
            <button @click="showAddBookModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold text-white hover:bg-white/5 transition-all">Cancel</button>
            <button @click="addBook" class="flex-1 py-4 rounded-xl bg-white text-black font-bold hover:bg-zinc-200 transition-all active:scale-95">Add</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-sm w-full text-center text-white">
          <h3 class="text-2xl font-bold mb-2 tracking-tighter">Sign Out?</h3>
          <p class="text-zinc-500 text-sm mb-8 font-medium">Your progress is saved to the cloud.</p>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold hover:bg-white/5">Cancel</button>
            <button @click="$emit('logout')" class="flex-1 py-4 rounded-xl bg-red-600 font-bold hover:bg-red-700">Logout</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-3xl max-w-sm w-full text-center text-white">
          <h3 class="text-2xl font-bold mb-2 tracking-tighter">Remove Book?</h3>
          <p class="text-zinc-500 text-sm mb-8 font-medium">This will be removed from your personal collection.</p>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 py-4 rounded-xl border border-white/10 font-bold hover:bg-white/5">Cancel</button>
            <button @click="deleteBook" class="flex-1 py-4 rounded-xl bg-red-600 font-bold hover:bg-red-700">Confirm</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, addDoc, deleteDoc, doc, onSnapshot, query, where, orderBy, serverTimestamp } from "firebase/firestore";

// State
const myBooks = ref([]);
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
const currentUserEmail = ref(auth.currentUser?.email || '');

const navItems = [
  { id: 'home', name: 'Dashboard', path: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { id: 'inventory', name: 'My Library', path: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253' },
  { id: 'settings', name: 'My Account', path: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z' }
];

// Computed search
const filteredBooks = computed(() => {
  if (!searchQuery.value) return myBooks.value;
  return myBooks.value.filter(book => book.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
});

// FUNCTIONS
const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit', second: '2-digit' });
};

// LOAD USER SPECIFIC DATA
const loadMyData = () => {
  const user = auth.currentUser;
  if (!user) return;

  // KEY: We only query books where 'ownerId' matches the current user's UID
  const q = query(
    collection(db, "personal_books"), 
    where("ownerId", "==", user.uid),
    orderBy("createdAt", "desc")
  );

  onSnapshot(q, (snapshot) => {
    myBooks.value = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  }, (error) => { 
    console.error(error);
    dbStatus.value = 'offline'; 
  });
};

const addBook = async () => {
  if (!newBookTitle.value.trim()) return;
  const user = auth.currentUser;
  
  try {
    await addDoc(collection(db, "personal_books"), { 
      title: newBookTitle.value, 
      ownerId: user.uid, // Linking the book to the user
      createdAt: serverTimestamp() 
    });
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
    await deleteDoc(doc(db, "personal_books", bookToDelete.value));
    showDeleteModal.value = false;
    bookToDelete.value = null;
  } catch (err) { alert(err.message); }
};

let timeInterval;
onMounted(() => {
  loadMyData();
  updateTime();
  timeInterval = setInterval(updateTime, 1000);
  setTimeout(() => { showWelcome.value = false; }, 3000);
});

onUnmounted(() => {
  clearInterval(timeInterval);
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>