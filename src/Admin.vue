<template>
  <div class="h-screen bg-zinc-950 text-white font-ios selection:bg-white/20 overflow-hidden text-left">
    
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

    <!-- UI LAYER (Only shows after welcome fade) -->
    <div v-if="contentVisible" class="animate-content-in relative h-screen flex flex-col">
      <!-- Top Header (Fixed Overlay) -->
      <header class="fixed top-0 left-0 right-0 p-6 flex justify-between items-center z-[100] bg-zinc-950/20 backdrop-blur-xl border-b border-white/5">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-zinc-900 border border-white/10 rounded-lg flex items-center justify-center text-white font-black text-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-bold tracking-tighter uppercase leading-none">Admin Central</h1>
            <p class="text-[10px] font-black text-white mt-1 uppercase tracking-widest opacity-40">{{ currentTimeDisplay }}</p>
          </div>
        </div>
        
        <div class="flex items-center gap-5">
          <!-- Social Buttons -->
          <button @click="confirmSocial('Facebook')" class="text-white opacity-40 hover:opacity-100 transition-opacity active:scale-90">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
              <path d="M22.675 0h-21.35c-.732 0-1.325.593-1.325 1.325v21.351c0 .731.593 1.324 1.325 1.324h11.495v-9.294h-3.128v-3.622h3.128v-2.671c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12v9.293h6.116c.73 0 1.323-.593 1.323-1.325v-21.35c0-.732-.593-1.325-1.325-1.325z"/>
            </svg>
          </button>
          <button @click="confirmSocial('Instagram')" class="text-white opacity-40 hover:opacity-100 transition-opacity active:scale-90">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204 013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.791-4-4s1.791-4 4-4 4 1.791 4 4-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
          </button>

          <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'text-white' : 'text-zinc-500'" class="transition-colors active:scale-90">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </button>
        </div>
      </header>

      <!-- Scrollable Content Area -->
      <main class="flex-1 overflow-y-auto pt-24 pb-32 px-6 scrollbar-hide">
        <div class="max-w-5xl mx-auto relative z-10">
        <transition name="page" mode="out-in">
          
          <!-- DASHBOARD TAB -->
          <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 py-4">
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
                <div class="flex justify-between items-center text-black">
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
          <div v-else-if="activeTab === 'inventory'" key="inventory" class="py-4">
            <section class="mb-8 flex justify-between items-end">
              <div>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Asset Management</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Inventory</h2>
              </div>
              <div class="flex gap-2">
                <button v-if="selectedBooks.length > 0" @click="showBatchDeleteModal = true" class="px-4 py-2 bg-red-600 text-[10px] font-black uppercase tracking-widest rounded-xl shadow-lg active:scale-90 transition-all">
                  Delete ({{ selectedBooks.length }})
                </button>
                <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
                </button>
              </div>
            </section>
            
            <div v-if="books.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">No Assets Registered</p>
            </div>
            <transition-group v-else name="list" tag="div" class="space-y-2">
              <div v-for="book in books" :key="book.id" 
                   @click="toggleBookSelection(book.id)"
                   :class="selectedBooks.includes(book.id) ? 'bg-zinc-800 border-white/20' : 'bg-zinc-900 border-white/5'"
                   class="p-6 border rounded-[1.5rem] flex items-center justify-between group transition-all cursor-pointer">
                <div class="flex items-center gap-4">
                   <div class="w-5 h-5 rounded-full border border-white/10 flex items-center justify-center transition-all"
                        :class="selectedBooks.includes(book.id) ? 'bg-white border-white' : ''">
                      <svg v-if="selectedBooks.includes(book.id)" class="w-3 h-3 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="4"><path d="M5 13l4 4L19 7" /></svg>
                   </div>
                   <div>
                      <h3 class="text-base font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
                      <p class="text-[8px] text-zinc-700 uppercase tracking-[0.2em] font-black mt-2">UID: {{ book.id.slice(0,10) }}</p>
                   </div>
                </div>
                <button @click.stop="confirmDelete(book)" class="w-10 h-10 flex items-center justify-center text-zinc-800 hover:text-red-500 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
              </div>
            </transition-group>
          </div>

          <!-- REQUESTS TAB -->
          <div v-else-if="activeTab === 'requests'" key="requests" class="py-10">
            <section class="mb-8">
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Queue Management</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Approvals</h2>
            </section>

            <div v-if="pendingRequests.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">Queue is Clear</p>
            </div>
            <transition-group v-else name="list" tag="div">
              <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-900 border border-white/5 p-8 rounded-[2.5rem] mb-6">
                <h3 class="text-2xl font-bold tracking-tighter uppercase leading-none mb-3">{{ req.bookTitle }}</h3>
                <p class="text-[10px] text-zinc-400 font-bold uppercase tracking-widest mb-6">{{ req.userEmail }}</p>
                <div class="flex gap-3">
                  <button @click="confirmApprove(req)" class="flex-1 py-5 bg-white text-black rounded-2xl font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all">Authorize</button>
                  <button @click="confirmDecline(req)" class="flex-1 py-5 bg-zinc-950 text-red-500 rounded-2xl font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all border border-red-500/10">Decline</button>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- BORROWERS TAB -->
          <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="py-10">
            <section class="mb-8">
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Live Tracking</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Borrowers</h2>
            </section>
            
            <div v-if="borrowers.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">No Active Loans</p>
            </div>
            <transition-group v-else name="list" tag="div">
              <div v-for="person in borrowers" :key="person.id" 
                   class="p-8 bg-zinc-900 rounded-[2.5rem] mb-4 flex justify-between items-center border border-white/5">
                <div class="flex-1">
                  <h3 class="text-lg font-black uppercase tracking-tighter mb-1 leading-none">{{ person.bookTitle }}</h3>
                  <p class="text-[10px] font-bold uppercase opacity-60 tracking-widest mb-5">{{ person.userEmail }}</p>
                </div>
                <button @click="confirmReturn(person)" 
                        class="px-8 py-5 rounded-2xl text-[10px] font-black uppercase tracking-widest bg-white text-black active:scale-95 transition-all">
                  Return
                </button>
              </div>
            </transition-group>
          </div>

          <!-- COMMUNITY TAB -->
          <div v-else-if="activeTab === 'community'" key="community" class="py-10">
            <section class="mb-8">
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">User Network</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Community</h2>
            </section>

            <div v-if="users.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">Network Offline</p>
            </div>
            <transition-group v-else name="list" tag="div" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="user in users" :key="user.id" class="p-6 bg-zinc-900 border border-white/5 rounded-[2rem] flex items-center gap-4">
                <div class="w-12 h-12 bg-zinc-950 rounded-full flex items-center justify-center text-zinc-500 border border-white/10">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                </div>
                <div class="overflow-hidden">
                  <h3 class="text-sm font-bold uppercase truncate tracking-tight">{{ user.displayName || user.email.split('@')[0] }}</h3>
                  <p class="text-[9px] text-zinc-600 font-bold uppercase truncate tracking-widest">{{ user.email }}</p>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- PROFILE TAB -->
          <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 space-y-10">
            <section>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Identity</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Profile</h2>
            </section>

            <div class="bg-zinc-900 border border-white/5 p-10 rounded-[3rem] text-center">
              <div class="w-24 h-24 bg-zinc-950 border border-white/10 rounded-full flex items-center justify-center mx-auto mb-6 text-white">
                 <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              </div>
              <h3 class="text-2xl font-black uppercase tracking-tighter mb-1">Administrator</h3>
              <p class="text-[10px] text-zinc-600 font-bold uppercase tracking-[0.2em] mb-8">Authorized Access Only</p>
              
              <!-- Profile Stats Integration -->
              <div class="grid grid-cols-2 gap-2 mb-10">
                 <div class="p-4 bg-zinc-950/50 border border-white/5 rounded-2xl">
                    <p class="text-[8px] font-black uppercase text-zinc-600 tracking-widest mb-1">Privilege</p>
                    <p class="text-xs font-bold text-white uppercase tracking-tighter">Root Level</p>
                 </div>
                 <div class="p-4 bg-zinc-950/50 border border-white/5 rounded-2xl">
                    <p class="text-[8px] font-black uppercase text-zinc-600 tracking-widest mb-1">Status</p>
                    <p class="text-xs font-bold text-emerald-500 uppercase tracking-tighter">Encrypted</p>
                 </div>
              </div>

              <button @click="showLogoutModal = true" class="w-full py-6 bg-zinc-950 text-red-500 rounded-[2rem] font-black uppercase text-[12px] tracking-widest active:scale-95 transition-all border border-red-500/10 hover:bg-red-500 hover:text-white">
                Terminate Session
              </button>
            </div>
          </div>

          <!-- HISTORY LOGS TAB -->
          <div v-else-if="activeTab === 'logs'" key="logs" class="py-10">
            <section class="mb-8 flex justify-between items-end">
              <div>
                <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Audit Record</p>
                <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">History</h2>
              </div>
              <button @click="showResetModal = true" class="text-[8px] font-black uppercase tracking-widest text-zinc-500 border border-white/5 px-4 py-2 rounded-full hover:bg-white/5">Reset</button>
            </section>

            <div v-if="historyLogs.length === 0" class="py-20 text-center">
              <p class="text-[10px] font-black uppercase tracking-[0.5em] text-zinc-800">Registry Empty</p>
            </div>
            <transition-group v-else name="list" tag="div" class="space-y-2">
              <div v-for="log in historyLogs" :key="log.id" class="p-6 bg-zinc-900 border border-white/5 rounded-[1.5rem] flex justify-between items-center transition-all">
                <div>
                  <p class="text-[11px] font-bold uppercase tracking-tight mb-1">{{ log.bookTitle }}</p>
                  <p class="text-[9px] text-zinc-600 uppercase tracking-widest font-bold">{{ log.userEmail }}</p>
                </div>
                <div class="text-right">
                  <span class="text-[8px] px-3 py-1 rounded-full font-black uppercase tracking-widest border" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
                </div>
              </div>
            </transition-group>
          </div>

          </div>

        </transition>
      </main>

      <!-- NAVIGATION BAR (Floating Overlay) -->
      <div class="fixed bottom-8 left-0 right-0 z-[100] flex justify-center px-6 pointer-events-none">
        <nav class="bg-zinc-900/60 backdrop-blur-2xl border border-white/10 rounded-[2rem] p-2 flex items-center justify-between shadow-[0_20px_50px_rgba(0,0,0,0.5)] w-full max-w-[440px] pointer-events-auto">
          <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'community', 'logs']" :key="tab" @click="activeTab = tab" 
                  :class="activeTab === tab ? 'bg-white text-black scale-95 shadow-lg' : 'text-zinc-500 hover:text-zinc-300 hover:bg-white/5'" 
                  class="w-10 h-10 rounded-xl flex items-center justify-center transition-all relative group">
            
            <svg v-if="tab === 'dashboard'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
            <svg v-if="tab === 'inventory'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
            <svg v-if="tab === 'requests'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
            <svg v-if="tab === 'borrowers'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
            <svg v-if="tab === 'community'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0" /></svg>
            <svg v-if="tab === 'logs'" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            
            <span class="text-[7px] font-black uppercase tracking-tighter mt-1 opacity-0 group-hover:opacity-100 transition-opacity absolute -bottom-4">{{ tab }}</span>

            <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute -top-1 -right-1 w-4 h-4 bg-white text-black rounded-full flex items-center justify-center text-[8px] font-black shadow-lg">
              {{ pendingRequests.length }}
            </div>
          </button>
        </nav>
      </div>
    </div>

    <!-- MODALS -->
    <transition name="fade">
      <!-- Social Confirm Modal -->
      <div v-if="showSocialModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase">External Link</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10 leading-relaxed px-4">
            Navigating to <span class="text-white">{{ activeSocial }}</span>. Protocol will continue in external application.
          </p>
          <div class="flex gap-3">
            <button @click="openSocial" class="flex-1 py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Proceed</button>
            <button @click="showSocialModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <!-- Logout Modal -->
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <div class="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          </div>
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase">End Session?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10 leading-relaxed px-4">
            Security tokens will be cleared.<br>Re-authentication required for next access.
          </p>
          <div class="flex gap-3">
            <button @click="$emit('logout')" class="flex-1 py-5 bg-red-600 text-white rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Terminate</button>
            <button @click="showLogoutModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal para sa pagdagdag ng libro -->
    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-xl px-6">
        <div class="bg-zinc-900 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-2xl font-bold tracking-tighter mb-8 uppercase text-center">Register Asset</h2>
          <div class="space-y-1.5 mb-10">
            <input v-model="newBook.title" type="text" placeholder="BOOK TITLE" class="w-full bg-zinc-950 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold placeholder:text-zinc-700 focus:border-white transition-all uppercase" />
          </div>
          <div class="flex gap-3">
            <button @click="addBook" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Register</button>
            <button @click="showAddModal = false" class="flex-1 py-5 bg-zinc-950 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { db } from './lib/firebase';
import { collection, onSnapshot, addDoc, deleteDoc, doc, updateDoc, serverTimestamp, query, orderBy, writeBatch } from "firebase/firestore";

const showWelcome = ref(true);
const contentVisible = ref(false);
const activeTab = ref('dashboard');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);
const selectedBooks = ref([]);

const showAddModal = ref(false);
const showLogoutModal = ref(false);
const showSocialModal = ref(false);
const showBatchDeleteModal = ref(false);
const showResetModal = ref(false);
const showApproveModal = ref(false);
const showDeclineModal = ref(false);
const showReturnModal = ref(false);
const showDeleteModal = ref(false);

const activeSocial = ref('');
const socialLinks = {
  Facebook: 'https://www.facebook.com/ben.benedict.31392',
  Instagram: 'https://www.instagram.com/buendia.benedict/'
};

const bookToDelete = ref(null);
const activeRequest = ref(null);
const activeReturn = ref(null);
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

const confirmSocial = (platform) => {
  activeSocial.value = platform;
  showSocialModal.value = true;
};

const openSocial = () => {
  window.open(socialLinks[activeSocial.value], '_blank');
  showSocialModal.value = false;
};

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  // Welcome Trigger
  setTimeout(() => {
    showWelcome.value = false;
  }, 2500);

  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
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

const toggleBookSelection = (id) => {
  const index = selectedBooks.value.indexOf(id);
  if (index === -1) selectedBooks.value.push(id);
  else selectedBooks.value.splice(index, 1);
};

const confirmDelete = (book) => {
  bookToDelete.value = book;
  showDeleteModal.value = true;
};

const deleteBook = async () => {
  if (!bookToDelete.value) return;
  await deleteDoc(doc(db, "books", bookToDelete.value.id));
  showDeleteModal.value = false;
};

const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s.includes('approved') || s.includes('returned')) return 'text-green-500 bg-green-500/10 border-green-500/20';
  if (s.includes('declined')) return 'text-red-500 bg-red-500/10 border-red-500/20';
  return 'text-zinc-500 border-white/5';
};

const clearLogs = async () => {
  const batch = writeBatch(db);
  historyLogs.value.forEach(l => batch.delete(doc(db, "history", l.id)));
  await batch.commit();
  showResetModal.value = false;
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

.welcome-fade-enter-active, .welcome-fade-leave-active { transition: all 1s cubic-bezier(0.65, 0, 0.35, 1); }
.welcome-fade-enter-from { opacity: 0; }
.welcome-fade-leave-to { opacity: 0; transform: translateY(-20px); }

.page-enter-active, .page-leave-active { transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.page-enter-from, .page-leave-to { opacity: 0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.list-enter-active, .list-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.list-enter-from { opacity: 0; transform: translateY(10px); }
.list-leave-to { opacity: 0; transform: scale(0.95); }
.list-move { transition: transform 0.4s ease; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>