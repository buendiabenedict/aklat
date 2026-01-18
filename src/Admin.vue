<template>
  <!-- Main Container: Uses System Black for OLED depth -->
  <div class="min-h-screen bg-black text-white font-sans selection:bg-blue-500/30 overflow-x-hidden pb-32">
    
    <!-- iOS Status Bar / Header -->
    <header class="sticky top-0 z-40 bg-black/70 backdrop-blur-md px-6 pt-12 pb-4 flex justify-between items-end border-b border-white/5">
      <div>
        <p class="text-[11px] font-semibold text-zinc-500 uppercase tracking-[0.15em] leading-none mb-1">System Controller</p>
        <h1 class="text-3xl font-bold tracking-tight">Admin</h1>
      </div>
      <div class="flex items-center gap-4 mb-1">
        <div class="flex flex-col items-end">
          <span class="text-[10px] font-bold text-blue-500 tracking-tighter uppercase">Signal Active</span>
          <span class="text-[12px] font-medium text-zinc-400 tabular-nums">{{ currentTimeDisplay }}</span>
        </div>
        <button @click="$emit('logout')" class="w-10 h-10 bg-zinc-800/50 rounded-full flex items-center justify-center active:scale-90 transition-transform">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-zinc-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
        </button>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 mt-6">
      <transition name="ios-page" mode="out-in">
        
        <!-- DASHBOARD TAB -->
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-8">
          <!-- Widget Grid -->
          <div class="grid grid-cols-2 gap-4">
            <div class="ios-widget bg-zinc-900/50 p-5 rounded-[2.2rem] border border-white/5 relative overflow-hidden">
              <div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
              </div>
              <p class="text-[34px] font-semibold tracking-tight leading-none mb-1">{{ books.length }}</p>
              <p class="text-[12px] font-semibold text-zinc-500 uppercase tracking-wide">Total Assets</p>
            </div>

            <div class="ios-widget bg-zinc-900/50 p-5 rounded-[2.2rem] border border-white/5">
              <div class="w-8 h-8 rounded-full bg-orange-500/10 flex items-center justify-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              </div>
              <p class="text-[34px] font-semibold tracking-tight leading-none mb-1">{{ borrowers.length }}</p>
              <p class="text-[12px] font-semibold text-zinc-500 uppercase tracking-wide">Active Loans</p>
            </div>
          </div>

          <!-- Notification Center Style -->
          <section v-if="pendingRequests.length > 0">
            <h2 class="px-2 text-[13px] font-semibold text-zinc-500 uppercase tracking-wider mb-3">Pending Authorization</h2>
            <div v-for="req in pendingRequests" :key="req.id" @click="activeTab = 'requests'" 
                 class="group active:scale-[0.97] transition-all duration-200 bg-zinc-900/40 backdrop-blur-xl border border-white/5 p-5 rounded-3xl mb-3 flex items-center justify-between">
              <div>
                <p class="text-[15px] font-semibold leading-tight">{{ req.bookTitle }}</p>
                <p class="text-[13px] text-zinc-500">{{ req.userEmail.split('@')[0] }}</p>
              </div>
              <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M9 5l7 7-7 7" /></svg>
              </div>
            </div>
          </section>
        </div>

        <!-- INVENTORY TAB (Settings style list) -->
        <div v-else-if="activeTab === 'inventory'" key="inventory">
          <div class="flex justify-between items-center mb-6 px-2">
            <h2 class="text-2xl font-bold tracking-tight">Inventory</h2>
            <div class="flex gap-3">
               <button v-if="selectedBooks.length" @click="showDeleteModal = true" class="text-red-500 font-medium text-sm px-3 py-1 bg-red-500/10 rounded-full">Delete</button>
               <button @click="showAddModal = true" class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center active:scale-90 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
              </button>
            </div>
          </div>

          <div class="bg-zinc-900/50 rounded-2xl overflow-hidden border border-white/5">
            <div v-for="(book, index) in books" :key="book.id" 
                 @click="toggleSelectBook(book.id)"
                 class="relative flex items-center gap-4 px-5 py-4 active:bg-zinc-800 transition-colors cursor-pointer group">
              <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all" 
                   :class="selectedBooks.includes(book.id) ? 'bg-blue-500 border-blue-500' : 'border-zinc-700'">
                <svg v-if="selectedBooks.includes(book.id)" xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 text-white" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
              </div>
              <div class="flex-1">
                <p class="text-[16px] font-medium tracking-tight">{{ book.title }}</p>
                <p class="text-[11px] text-zinc-500 uppercase tracking-widest font-mono">ID: {{ book.id.slice(-6) }}</p>
              </div>
              <!-- Inset Divider -->
              <div v-if="index !== books.length - 1" class="absolute bottom-0 left-14 right-0 h-[0.5px] bg-white/5"></div>
            </div>
          </div>
        </div>

        <!-- BORROWERS TAB -->
        <div v-else-if="activeTab === 'borrowers'" key="borrowers">
          <h2 class="text-2xl font-bold tracking-tight mb-6 px-2">Active Loans</h2>
          <div class="space-y-4">
            <div v-for="person in borrowers" :key="person.id" 
                 class="bg-zinc-900/40 border border-white/5 p-5 rounded-[2rem] flex items-center justify-between">
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <div v-if="isOverdue(person.returnSchedule)" class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                  <h3 class="text-[17px] font-semibold tracking-tight">{{ person.bookTitle }}</h3>
                </div>
                <p class="text-[13px] text-zinc-400">{{ person.userEmail }}</p>
                <div class="flex items-center gap-1.5 pt-1">
                  <span class="text-[11px] font-bold px-2 py-0.5 rounded-md" :class="isOverdue(person.returnSchedule) ? 'bg-red-500/10 text-red-500' : 'bg-zinc-800 text-zinc-400'">
                    Due: {{ person.returnSchedule }}
                  </span>
                </div>
              </div>
              <button @click="markAsReturned(person)" class="bg-white text-black text-[13px] font-bold px-5 py-2.5 rounded-full active:scale-90 transition-transform">
                Return
              </button>
            </div>
          </div>
        </div>

      </transition>
    </main>

    <!-- Native-style Bottom Tab Bar -->
    <nav class="fixed bottom-0 left-0 right-0 z-50">
      <div class="bg-zinc-900/80 backdrop-blur-2xl border-t border-white/10 pb-8 pt-2 px-6 flex justify-between items-center">
        <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'logs']" 
                :key="tab" @click="activeTab = tab" 
                :class="activeTab === tab ? 'text-blue-500' : 'text-zinc-500'"
                class="flex flex-col items-center gap-1 transition-colors duration-300">
          <div class="relative">
            <svg v-if="tab === 'dashboard'" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            <svg v-if="tab === 'inventory'" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z"/></svg>
            <svg v-if="tab === 'requests'" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/></svg>
            <svg v-if="tab === 'borrowers'" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/></svg>
            <svg v-if="tab === 'logs'" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/></svg>
            
            <span v-if="tab === 'requests' && pendingRequests.length" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-[9px] font-black flex items-center justify-center text-white border-2 border-zinc-900">
              {{ pendingRequests.length }}
            </span>
          </div>
          <span class="text-[10px] font-medium capitalize">{{ tab }}</span>
        </button>
      </div>
    </nav>

    <!-- iOS style Alert/Modal -->
    <transition name="ios-modal">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center px-6">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showAddModal = false"></div>
        <div class="bg-zinc-900 border border-white/10 rounded-[2rem] w-full max-w-sm overflow-hidden shadow-2xl relative z-10">
          <div class="p-6 text-center border-b border-white/5">
            <h3 class="text-[17px] font-semibold mb-1">New Asset</h3>
            <p class="text-[13px] text-zinc-400">Enter the title of the new inventory item.</p>
            <input v-model="newBook.title" type="text" autofocus class="w-full mt-4 bg-zinc-800 border-none rounded-xl px-4 py-3 text-white outline-none focus:ring-2 ring-blue-500/50" placeholder="Title" />
          </div>
          <div class="flex">
            <button @click="showAddModal = false" class="flex-1 py-4 text-blue-500 font-medium active:bg-white/5 border-r border-white/5">Cancel</button>
            <button @click="addBook" class="flex-1 py-4 text-blue-500 font-bold active:bg-white/5">Add</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
// ... logic remains identical to your current script ...
// (Refer to original script for logic functions)
</script>

<style scoped>
/* SF Pro like tracking */
h1, h2, h3 {
  letter-spacing: -0.022em;
}

/* iOS Page Transitions */
.ios-page-enter-active, .ios-page-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.ios-page-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.ios-page-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* iOS Modal Transitions */
.ios-modal-enter-active, .ios-modal-leave-active {
  transition: opacity 0.3s ease;
}
.ios-modal-enter-active .bg-zinc-900 {
  animation: ios-zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.ios-modal-enter-from { opacity: 0; }

@keyframes ios-zoom {
  from { opacity: 0; transform: scale(1.1); }
  to { opacity: 1; transform: scale(1); }
}

/* Custom Inset Grouping styles */
.ios-widget {
  box-shadow: 0 10px 20px -5px rgba(0,0,0,0.3);
}

/* Hide scrollbar */
::-webkit-scrollbar {
  display: none;
}
</style>