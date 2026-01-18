<template>
  <div class="min-h-screen bg-zinc-950 text-white font-ios selection:bg-white/20 overflow-x-hidden text-left">
    
    <!-- WELCOME SEQUENCE -->
    <transition name="welcome-fade" @after-leave="onWelcomeFinished">
      <div v-if="showWelcome" class="fixed inset-0 z-[300] bg-zinc-950 flex flex-col items-center justify-center p-6">
        <div class="text-center">
          <p class="text-[10px] font-black text-white uppercase tracking-[0.5em] mb-4 animate-pulse opacity-50">System Initialized</p>
          <h1 class="text-4xl md:text-6xl font-bold tracking-tighter uppercase apple-gradient mb-2">Access Granted</h1>
          <h2 class="text-2xl md:text-4xl font-black tracking-tighter uppercase opacity-20">Administrator</h2>
        </div>
      </div>
    </transition>

    <!-- UI LAYER -->
    <div v-if="contentVisible" class="animate-content-in relative min-h-screen">
      
      <!-- NAVIGATION BAR (Fixed Floating Overlay) -->
      <!-- 'fixed' handles the overlay behavior so it stays on top of all pages regardless of scroll -->
      <div class="fixed bottom-8 left-0 right-0 z-[100] flex justify-center px-6 pointer-events-none">
        <nav class="bg-zinc-900/80 backdrop-blur-2xl border border-white/10 rounded-full p-2 flex items-center justify-between shadow-[0_25px_50px_-12px_rgba(0,0,0,0.8)] w-full max-w-md pointer-events-auto">
          <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'community', 'logs']" 
                  :key="tab" @click="activeTab = tab" 
                  :class="activeTab === tab ? 'bg-white text-black scale-95 shadow-lg' : 'text-zinc-500 hover:text-zinc-300'" 
                  class="w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 relative group">
            
            <svg v-if="tab === 'dashboard'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
            <svg v-if="tab === 'inventory'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
            <svg v-if="tab === 'requests'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
            <svg v-if="tab === 'borrowers'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
            <svg v-if="tab === 'community'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0" /></svg>
            <svg v-if="tab === 'logs'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            
            <!-- Badge for pending -->
            <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center text-[10px] font-black border-2 border-zinc-900">
              {{ pendingRequests.length }}
            </div>
          </button>
        </nav>
      </div>

      <!-- Top Header -->
      <header class="p-6 flex justify-between items-center relative z-20">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-zinc-900 border border-white/10 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-bold tracking-tighter uppercase leading-none">Admin Central</h1>
            <p class="text-[10px] font-black text-white mt-1 uppercase tracking-widest opacity-40">{{ currentTimeDisplay }}</p>
          </div>
        </div>
        
        <div class="flex items-center gap-4">
          <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'text-white' : 'text-zinc-500'" class="transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </button>
        </div>
      </header>

      <main class="max-w-5xl mx-auto px-6 pb-40 relative z-10">
        <transition name="page" mode="out-in">
          
          <!-- DASHBOARD TAB -->
          <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 pt-4">
            <section>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Metrics</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Overview</h2>
            </section>

            <div class="grid grid-cols-2 gap-3">
              <div class="bg-zinc-900 border border-white/5 p-6 rounded-[2rem]">
                <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Inventory</p>
                <p class="text-4xl font-bold tracking-tighter">{{ books.length }}</p>
                <p class="text-[8px] font-bold text-zinc-600 uppercase mt-2">Asset Count</p>
              </div>
              <div class="bg-zinc-900 border border-white/5 p-6 rounded-[2rem]">
                <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Loans</p>
                <p class="text-4xl font-bold tracking-tighter text-amber-500">{{ borrowers.length }}</p>
                <p class="text-[8px] font-bold text-zinc-600 uppercase mt-2">Active Sessions</p>
              </div>
              <div class="bg-zinc-900 border border-white/5 p-6 rounded-[2rem] col-span-2">
                <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Community Strength</p>
                <p class="text-4xl font-bold tracking-tighter">{{ users.length }}</p>
                <p class="text-[8px] font-bold text-zinc-600 uppercase mt-2">Registered Members</p>
              </div>
            </div>
            
            <transition name="fade">
              <div @click="activeTab = 'requests'" v-if="pendingRequests.length > 0" class="bg-white p-8 rounded-[2.5rem] cursor-pointer active:scale-[0.98] transition-all">
                <div class="flex justify-between items-center">
                  <div>
                    <h3 class="text-2xl font-black tracking-tighter uppercase mb-1 text-black">Action Required</h3>
                    <p class="text-[10px] font-bold uppercase tracking-widest opacity-60 text-black">{{ pendingRequests.length }} authorizations pending</p>
                  </div>
                  <div class="w-12 h-12 bg-black text-white rounded-2xl flex items-center justify-center font-black">
                    {{ pendingRequests.length }}
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- INVENTORY TAB -->
          <div v-else-if="activeTab === 'inventory'" key="inventory" class="pt-4">
            <section class="mb-8 flex justify-between items-end">
              <div>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Asset Management</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Inventory</h2>
              </div>
              <div class="flex gap-2">
                <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
                </button>
              </div>
            </section>
            
            <div v-if="books.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">No Assets Registered</p>
            </div>
            
            <transition-group name="list" tag="div" class="space-y-3">
              <div v-for="book in books" :key="book.id" 
                   class="p-6 bg-zinc-900 border border-white/5 rounded-[1.8rem] flex items-center justify-between group transition-all">
                <div class="flex items-center gap-4">
                   <div class="w-10 h-10 bg-zinc-950 rounded-xl flex items-center justify-center text-zinc-700 border border-white/5">
                      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                   </div>
                   <div>
                      <h3 class="text-base font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
                      <p class="text-[8px] text-zinc-700 uppercase tracking-[0.2em] font-black mt-2">UID: {{ book.id.slice(0,10) }}</p>
                   </div>
                </div>
                <button @click="confirmDelete(book)" class="w-10 h-10 flex items-center justify-center text-zinc-800 hover:text-red-500 transition-colors active:scale-90">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
              </div>
            </transition-group>
          </div>

          <!-- REQUESTS TAB -->
          <div v-else-if="activeTab === 'requests'" key="requests" class="pt-4">
            <section class="mb-8">
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Queue Management</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Approvals</h2>
            </section>

            <div v-if="pendingRequests.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">Queue is Clear</p>
            </div>
            <transition-group name="list" tag="div" class="space-y-4">
              <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-900 border border-white/5 p-8 rounded-[2.5rem]">
                <h3 class="text-xl font-bold tracking-tighter uppercase mb-1">{{ req.bookTitle }}</h3>
                <p class="text-[10px] text-zinc-400 font-bold uppercase tracking-widest mb-6">{{ req.userEmail }}</p>
                <div class="flex gap-3">
                  <button @click="handleApproval(req, true)" class="flex-1 py-4 bg-white text-black rounded-2xl font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all">Authorize</button>
                  <button @click="handleApproval(req, false)" class="flex-1 py-4 bg-zinc-950 text-red-500 rounded-2xl font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all border border-red-500/10">Decline</button>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- BORROWERS TAB -->
          <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="pt-4">
            <section class="mb-8">
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Live Tracking</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Borrowers</h2>
            </section>
            
            <div v-if="borrowers.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">No Active Loans</p>
            </div>
            <transition-group name="list" tag="div" class="space-y-3">
              <div v-for="person in borrowers" :key="person.id" 
                   class="p-6 bg-zinc-900 rounded-[2rem] flex justify-between items-center border border-white/5">
                <div class="flex-1">
                  <h3 class="text-base font-black uppercase tracking-tight mb-1">{{ person.bookTitle }}</h3>
                  <p class="text-[9px] font-bold uppercase opacity-40 tracking-widest">{{ person.userEmail }}</p>
                </div>
                <button @click="handleReturn(person)" 
                        class="px-6 py-3 rounded-xl text-[10px] font-black uppercase tracking-widest bg-white text-black active:scale-95 transition-all">
                  Return
                </button>
              </div>
            </transition-group>
          </div>

          <!-- COMMUNITY TAB -->
          <div v-else-if="activeTab === 'community'" key="community" class="pt-4">
            <section class="mb-8">
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">User Network</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Community</h2>
            </section>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="user in users" :key="user.id" class="p-6 bg-zinc-900 border border-white/5 rounded-[2rem] flex items-center gap-4">
                <div class="w-12 h-12 bg-zinc-950 rounded-full flex items-center justify-center text-zinc-500 border border-white/10">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                </div>
                <div class="overflow-hidden">
                  <h3 class="text-sm font-bold uppercase truncate tracking-tight">{{ user.displayName || user.email.split('@')[0] }}</h3>
                  <p class="text-[9px] text-zinc-600 font-bold uppercase truncate tracking-widest">{{ user.email }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- PROFILE TAB -->
          <div v-else-if="activeTab === 'profile'" key="profile" class="pt-4 space-y-8">
            <section>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Identity</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Profile</h2>
            </section>

            <div class="bg-zinc-900 border border-white/5 p-10 rounded-[3rem] text-center">
              <div class="w-24 h-24 bg-zinc-950 border border-white/10 rounded-full flex items-center justify-center mx-auto mb-6 text-white">
                 <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </div>
              <h3 class="text-2xl font-black uppercase tracking-tighter mb-1">Administrator</h3>
              <p class="text-[10px] text-zinc-600 font-bold uppercase tracking-[0.2em] mb-8">System Access Node</p>
              
              <div class="grid grid-cols-2 gap-2 mb-10">
                 <div class="p-5 bg-zinc-950/50 border border-white/5 rounded-[1.5rem]">
                    <p class="text-[8px] font-black uppercase text-zinc-600 tracking-widest mb-1">Access Tier</p>
                    <p class="text-xs font-bold text-white uppercase tracking-tighter">Level Root</p>
                 </div>
                 <div class="p-5 bg-zinc-950/50 border border-white/5 rounded-[1.5rem]">
                    <p class="text-[8px] font-black uppercase text-zinc-600 tracking-widest mb-1">Signal Status</p>
                    <p class="text-xs font-bold text-emerald-500 uppercase tracking-tighter">Secure</p>
                 </div>
              </div>

              <button @click="showLogoutModal = true" class="w-full py-6 bg-red-600/10 text-red-500 rounded-[2rem] font-black uppercase text-[12px] tracking-widest active:scale-95 transition-all border border-red-500/20">
                Log Out System
              </button>
            </div>
          </div>

          <!-- HISTORY TAB -->
          <div v-else-if="activeTab === 'logs'" key="logs" class="pt-4">
            <section class="mb-8 flex justify-between items-end">
              <div>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Audit Record</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">History</h2>
              </div>
            </section>

            <div v-if="historyLogs.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">No Logs Found</p>
            </div>
            <div class="space-y-2">
              <div v-for="log in historyLogs" :key="log.id" class="p-6 bg-zinc-900 border border-white/5 rounded-[1.5rem] flex justify-between items-center">
                <div>
                  <p class="text-[12px] font-bold uppercase tracking-tight mb-1">{{ log.bookTitle }}</p>
                  <p class="text-[9px] text-zinc-600 uppercase tracking-widest font-bold">{{ log.userEmail }}</p>
                </div>
                <span class="text-[8px] px-3 py-1 rounded-full font-black uppercase tracking-widest border" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
              </div>
            </div>
          </div>

        </transition>
      </main>
    </div>

    <!-- MODALS -->
    <transition name="fade">
      <!-- Add Book Modal -->
      <div v-if="showAddModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-2xl font-bold tracking-tighter mb-8 uppercase text-center">Add New Asset</h2>
          <div class="space-y-4 mb-10">
            <input v-model="newBook.title" type="text" placeholder="BOOK TITLE" class="w-full bg-zinc-950 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold placeholder:text-zinc-700 focus:border-white transition-all uppercase" />
          </div>
          <div class="flex gap-3">
            <button @click="addBook" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Create</button>
            <button @click="showAddModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Back</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <!-- Logout Modal -->
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase">Log Out?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10">Session data will be cleared.</p>
          <div class="flex gap-3">
            <button @click="$emit('logout')" class="flex-1 py-5 bg-red-600 text-white rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Confirm</button>
            <button @click="showLogoutModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Delete Confirmation Modal -->
    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase">Delete Asset?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10">This action cannot be undone.</p>
          <div class="flex gap-3">
            <button @click="deleteBook" class="flex-1 py-5 bg-red-600 text-white rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Delete</button>
            <button @click="showDeleteModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Abort</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { db } from './lib/firebase';
import { 
  collection, onSnapshot, addDoc, deleteDoc, doc, 
  updateDoc, serverTimestamp, query, orderBy, setDoc 
} from "firebase/firestore";

const showWelcome = ref(true);
const contentVisible = ref(false);
const activeTab = ref('dashboard');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);

const showAddModal = ref(false);
const showLogoutModal = ref(false);
const showDeleteModal = ref(false);

const bookToDelete = ref(null);
const newBook = ref({ title: '' });
const currentTimeDisplay = ref('');

let clockInterval;
const updateClock = () => {
  const now = new Date();
  currentTimeDisplay.value = now.toLocaleTimeString('en-US', { hour12: true, hour: '2-digit', minute: '2-digit' });
};

const onWelcomeFinished = () => {
  contentVisible.value = true;
};

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  setTimeout(() => { showWelcome.value = false; }, 2000);

  onSnapshot(query(collection(db, "books"), orderBy("createdAt", "desc")), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => {
    notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => {
    historyLogs.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });
  onSnapshot(collection(db, "borrowers"), (s) => {
    borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() }));
  });
});

onUnmounted(() => clearInterval(clockInterval));

const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

const addBook = async () => {
  if (!newBook.value.title.trim()) return;
  await addDoc(collection(db, "books"), { 
    title: newBook.value.title.toUpperCase(), 
    createdAt: serverTimestamp() 
  });
  newBook.value.title = '';
  showAddModal.value = false;
};

const confirmDelete = (book) => {
  bookToDelete.value = book;
  showDeleteModal.value = true;
};

const deleteBook = async () => {
  if (!bookToDelete.value) return;
  await deleteDoc(doc(db, "books", bookToDelete.value.id));
  showDeleteModal.value = false;
  bookToDelete.value = null;
};

const handleApproval = async (req, isApproved) => {
  const status = isApproved ? 'approved' : 'declined';
  
  // Update Notification
  await updateDoc(doc(db, "notifications", req.id), { status });

  // Update History
  await addDoc(collection(db, "history"), {
    bookTitle: req.bookTitle,
    userEmail: req.userEmail,
    userId: req.userId,
    status: status,
    createdAt: serverTimestamp()
  });

  if (isApproved) {
    // Add to active borrowers
    await addDoc(collection(db, "borrowers"), {
      bookId: req.bookId,
      bookTitle: req.bookTitle,
      userEmail: req.userEmail,
      userId: req.userId,
      borrowedAt: serverTimestamp()
    });
  }
};

const handleReturn = async (person) => {
  // Add to history
  await addDoc(collection(db, "history"), {
    bookTitle: person.bookTitle,
    userEmail: person.userEmail,
    userId: person.userId,
    status: 'returned',
    createdAt: serverTimestamp()
  });

  // Remove from borrowers
  await deleteDoc(doc(db, "borrowers", person.id));
};

const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s === 'approved' || s === 'returned') return 'text-emerald-500 bg-emerald-500/10 border-emerald-500/20';
  if (s === 'declined') return 'text-red-500 bg-red-500/10 border-red-500/20';
  return 'text-zinc-500 border-white/5';
};
</script>

<style scoped>
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

@keyframes contentIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-content-in {
  animation: contentIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

.welcome-fade-leave-active { transition: all 0.8s cubic-bezier(0.65, 0, 0.35, 1); }
.welcome-fade-leave-to { opacity: 0; transform: scale(1.1); filter: blur(20px); }

.page-enter-active, .page-leave-active { transition: all 0.3s ease; }
.page-enter-from { opacity: 0; transform: translateY(5px); }
.page-leave-to { opacity: 0; transform: translateY(-5px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.list-enter-active, .list-leave-active { transition: all 0.4s ease; }
.list-enter-from { opacity: 0; transform: translateX(-10px); }
.list-leave-to { opacity: 0; transform: scale(0.95); }
</style>