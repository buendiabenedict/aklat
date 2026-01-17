<template>
  <div class="min-h-screen bg-black text-white font-ios relative overflow-hidden flex">
    
    <div class="absolute inset-0 z-0 pointer-events-none">
      <div class="orb orb-1"></div>
      <div class="absolute inset-0 opacity-[0.03] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]"></div>
    </div>

    <aside :class="isSidebarCollapsed ? 'w-20' : 'w-72'" class="h-screen border-r border-white/10 bg-zinc-950/50 backdrop-blur-3xl z-50 flex flex-col transition-[width] duration-500 ease-in-out relative shrink-0">
      <button @click="isSidebarCollapsed = !isSidebarCollapsed" class="absolute -right-3 top-10 bg-white text-black rounded-full p-1.5 z-[60] shadow-xl hover:scale-110 transition-transform">
        <svg class="w-3 h-3" :class="isSidebarCollapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M15 19l-7-7 7-7" /></svg>
      </button>

      <div class="h-28 flex items-center px-6 overflow-hidden">
        <div class="w-8 h-8 bg-white rounded-xl shrink-0 shadow-[0_0_20px_rgba(255,255,255,0.3)]"></div>
        <transition name="fade">
          <h1 v-if="!isSidebarCollapsed" class="ml-4 text-sm font-black tracking-widest ios-gradient-text uppercase">Librarian Panel</h1>
        </transition>
      </div>

      <nav class="flex-1 px-3 space-y-2 mt-4">
        <button v-for="item in navItems" :key="item.name" @click="activeTab = item.id"
          class="w-full flex items-center h-14 rounded-2xl transition-all duration-300"
          :class="[ activeTab === item.id ? 'bg-white text-black shadow-lg' : 'text-zinc-500 hover:bg-white/5 hover:text-white', isSidebarCollapsed ? 'justify-center' : 'px-4' ]">
          <div class="w-6 h-6 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" :d="item.path" /></svg>
          </div>
          <transition name="fade">
            <span v-if="!isSidebarCollapsed" class="ml-4 font-bold text-sm tracking-tight whitespace-nowrap">{{ item.name }}</span>
          </transition>
        </button>
      </nav>

      <div class="p-3 border-t border-white/5">
        <button @click="$emit('logout')" class="w-full h-14 flex items-center justify-center rounded-2xl text-red-500 hover:bg-red-500/10 transition-all group">
          <svg class="w-6 h-6 shrink-0 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          <span v-if="!isSidebarCollapsed" class="ml-3 font-bold text-xs uppercase tracking-widest">Sign Out</span>
        </button>
      </div>
    </aside>

    <main class="flex-1 h-screen overflow-y-auto p-8 md:p-16 relative z-10 custom-scrollbar">
      <header class="mb-16 flex justify-between items-end">
        <div>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-[0.4em] mb-3">System Online • Firebase Firestore</p>
          <h2 class="text-6xl font-bold tracking-tighter capitalize">{{ activeTab }}</h2>
        </div>
        <div class="text-right">
          <p class="text-white font-bold text-2xl tracking-tighter">{{ books.length }}</p>
          <p class="text-zinc-600 text-[10px] font-bold uppercase tracking-widest">Total Books</p>
        </div>
      </header>

      <section v-if="activeTab === 'inventory'" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div class="flex flex-col md:flex-row gap-4">
          <input 
            v-model="newBookTitle" 
            @keyup.enter="addBook"
            type="text" 
            placeholder="Search or add new book title..." 
            class="bg-zinc-900/50 border border-white/10 rounded-[1.5rem] py-5 px-8 text-white w-full max-w-xl outline-none focus:border-white/30 focus:bg-zinc-900 transition-all shadow-inner" 
          />
          <button @click="addBook" :disabled="isProcessing" class="bg-white text-black px-10 rounded-[1.5rem] font-bold hover:bg-zinc-200 transition-all active:scale-95 disabled:opacity-50">
            {{ isProcessing ? 'Adding...' : 'Add to Collection' }}
          </button>
        </div>

        <div class="bg-zinc-900/30 border border-white/10 rounded-[2.5rem] overflow-hidden backdrop-blur-md">
          <table class="w-full text-left">
            <thead>
              <tr class="text-zinc-600 text-[10px] font-black uppercase tracking-[0.3em] border-b border-white/5">
                <th class="p-10">Book Identity</th>
                <th class="p-10">Date Added</th>
                <th class="p-10 text-right">Control</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/[0.03]">
              <tr v-for="book in books" :key="book.id" class="group hover:bg-white/[0.02] transition-colors">
                <td class="p-10">
                  <div class="flex items-center gap-4">
                    <div class="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
                    <span class="text-lg font-medium tracking-tight">{{ book.title }}</span>
                  </div>
                </td>
                <td class="p-10 text-zinc-500 text-sm font-medium">
                  {{ book.createdAt?.toDate().toLocaleDateString() || 'Just now' }}
                </td>
                <td class="p-10 text-right">
                  <button @click="deleteBook(book.id)" class="opacity-0 group-hover:opacity-100 bg-red-500/10 text-red-500 px-4 py-2 rounded-xl text-[10px] font-bold uppercase tracking-widest hover:bg-red-500 hover:text-white transition-all">
                    Remove
                  </button>
                </td>
              </tr>
              <tr v-if="books.length === 0">
                <td colspan="3" class="p-20 text-center text-zinc-600 font-bold uppercase tracking-[0.5em] text-xs">
                  Library is empty
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { db } from './lib/firebase';
import { 
  collection, 
  addDoc, 
  deleteDoc, 
  doc, 
  onSnapshot, 
  query, 
  orderBy, 
  serverTimestamp 
} from "firebase/firestore";

const books = ref([]);
const activeTab = ref('inventory');
const newBookTitle = ref('');
const isSidebarCollapsed = ref(false);
const isProcessing = ref(false);

const navItems = [
  { id: 'inventory', name: 'Inventory', path: 'M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4' },
  { id: 'borrows', name: 'Records', path: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' }
];

// REAL-TIME LISTENER: Kusa itong mag-uupdate kapag may nabago sa Firestore
const loadBooks = () => {
  const q = query(collection(db, "books"), orderBy("createdAt", "desc"));
  onSnapshot(q, (snapshot) => {
    books.value = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  });
};

const addBook = async () => {
  if (!newBookTitle.value.trim() || isProcessing.value) return;
  
  isProcessing.value = true;
  try {
    await addDoc(collection(db, "books"), {
      title: newBookTitle.value,
      createdAt: serverTimestamp() // Time mula sa Google server
    });
    newBookTitle.value = '';
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    isProcessing.value = false;
  }
};

const deleteBook = async (id) => {
  if (!confirm("Are you sure you want to remove this book?")) return;
  try {
    await deleteDoc(doc(db, "books", id));
  } catch (err) {
    alert(err.message);
  }
};

onMounted(loadBooks);
</script>

<style scoped>
.orb { position: absolute; width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, #ffffff 0%, transparent 70%); filter: blur(140px); opacity: 0.05; top: -200px; right: -200px; }
.ios-gradient-text { background: linear-gradient(to right, #fff, #666); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 10px; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>