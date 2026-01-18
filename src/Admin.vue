<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40 text-left">
    
    <!-- Top Header -->
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-lg shadow-[0_0_20px_rgba(37,99,235,0.4)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
          </svg>
        </div>
        <div>
          <h1 class="text-sm font-bold tracking-tighter uppercase leading-none">Admin Central</h1>
          <p class="text-[10px] font-black text-blue-500 mt-1 uppercase tracking-widest">{{ currentTimeDisplay }}</p>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <button @click="activeTab = 'profile'" :class="activeTab === 'profile' ? 'text-white' : 'text-zinc-500'" class="transition-colors active:scale-90">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </button>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <!-- DASHBOARD TAB -->
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 py-4">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Metrics</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Overview</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem] transition-all hover:border-white/10">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Inventory</p>
              <p class="text-4xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-[2rem] transition-all hover:border-white/10">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Loans</p>
              <p class="text-4xl font-bold tracking-tighter text-amber-500">{{ borrowers.length }}</p>
            </div>
            <div @click="activeTab = 'community'" class="col-span-2 bg-zinc-950 border border-white/5 p-6 rounded-[2rem] transition-all hover:border-white/10 cursor-pointer group">
              <div class="flex justify-between items-center">
                <div>
                  <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1 group-hover:text-blue-500 transition-colors">Registered Users</p>
                  <p class="text-4xl font-bold tracking-tighter">{{ users.length }}</p>
                </div>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-zinc-800 group-hover:text-white transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0" /></svg>
              </div>
            </div>
          </div>
          
          <transition name="fade">
            <div @click="activeTab = 'requests'" v-if="pendingRequests.length > 0" class="bg-blue-600 p-8 rounded-[2.5rem] cursor-pointer active:scale-[0.98] transition-all shadow-xl shadow-blue-900/20">
              <div class="flex justify-between items-center text-black">
                <div>
                  <h3 class="text-2xl font-black tracking-tighter uppercase mb-1">Pending Requests</h3>
                  <p class="text-[10px] font-bold uppercase tracking-widest opacity-60">{{ pendingRequests.length }} authorizations required</p>
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
            <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4v16m8-8H4" /></svg>
            </button>
          </section>
          
          <transition-group name="list" tag="div" class="space-y-2">
            <div v-for="book in books" :key="book.id" class="p-6 bg-zinc-950 border border-white/5 rounded-[1.5rem] flex items-center justify-between group transition-all hover:bg-zinc-900/50">
              <div>
                <h3 class="text-base font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
                <p class="text-[8px] text-zinc-700 uppercase tracking-[0.2em] font-black mt-2">UID: {{ book.id.slice(0,10) }}</p>
              </div>
              <button @click="confirmDelete(book)" class="w-10 h-10 flex items-center justify-center text-zinc-800 hover:text-red-500 transition-colors active:scale-90">
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

          <div v-if="pendingRequests.length === 0" class="p-20 text-center border border-dashed border-white/5 rounded-[3rem]">
            <p class="text-zinc-800 font-bold uppercase text-[10px] tracking-[0.5em]">No Pending Requests</p>
          </div>

          <transition-group name="list" tag="div">
            <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-950 border border-white/5 p-8 rounded-[2.5rem] mb-6 shadow-2xl">
              <h3 class="text-2xl font-bold tracking-tighter uppercase leading-none mb-3">{{ req.bookTitle }}</h3>
              <p class="text-[10px] text-blue-500 font-bold uppercase tracking-widest mb-6">{{ req.userEmail }}</p>
              <div class="bg-zinc-900/50 p-4 rounded-2xl mb-8 border border-white/5">
                <p class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-1">Return Protocol</p>
                <p class="text-sm font-black text-white uppercase">{{ req.returnSchedule }} — 07:30 AM</p>
              </div>
              <div class="flex gap-3">
                <button @click="confirmApprove(req)" class="flex-1 py-5 bg-white text-black rounded-2xl font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all">Authorize</button>
                <button @click="declineRequest(req.id)" class="flex-1 py-5 bg-zinc-900 text-red-500 rounded-2xl font-black text-[10px] uppercase tracking-widest active:scale-95 transition-all border border-red-500/10">Decline</button>
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
          
          <div v-if="borrowers.length === 0" class="p-20 text-center border border-dashed border-white/5 rounded-[3rem]">
            <p class="text-zinc-800 font-bold uppercase text-[10px] tracking-[0.5em]">Zero Active Loans</p>
          </div>

          <transition-group name="list" tag="div">
            <div v-for="person in borrowers" :key="person.id" 
                 class="p-8 bg-zinc-950 rounded-[2.5rem] mb-4 flex justify-between items-center border border-white/5 shadow-xl transition-all">
              <div class="flex-1">
                <h3 class="text-lg font-black uppercase tracking-tighter mb-1 leading-none">{{ person.bookTitle }}</h3>
                <p class="text-[10px] font-bold uppercase opacity-60 tracking-widest mb-5">{{ person.userEmail }}</p>
                <p class="text-[11px] font-mono font-bold text-blue-500 uppercase tracking-tighter">Due: {{ person.returnSchedule }} — 07:30 AM</p>
              </div>
              <button @click="confirmReturn(person)" 
                      class="px-8 py-5 rounded-2xl text-[10px] font-black uppercase tracking-widest bg-white text-black active:scale-95 transition-all shadow-lg shadow-white/5">
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

          <div v-if="users.length === 0" class="p-20 text-center border border-dashed border-white/5 rounded-[3rem]">
            <p class="text-zinc-800 font-bold uppercase text-[10px] tracking-[0.5em]">No registered users</p>
          </div>

          <transition-group name="list" tag="div" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="user in users" :key="user.id" class="p-6 bg-zinc-950 border border-white/5 rounded-[2rem] flex items-center gap-4 transition-all hover:bg-zinc-900/50">
              <div class="w-12 h-12 bg-zinc-900 rounded-full flex items-center justify-center text-zinc-500 border border-white/10">
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
        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10">
          <section class="mb-12">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Identity</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient leading-none">Profile</h2>
          </section>

          <div class="bg-zinc-950 border border-white/5 p-10 rounded-[3rem] text-center">
            <div class="w-24 h-24 bg-blue-600/10 border border-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
               <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
            </div>
            <h3 class="text-2xl font-black uppercase tracking-tighter mb-1">Administrator</h3>
            <p class="text-[10px] text-zinc-600 font-bold uppercase tracking-[0.2em] mb-12">Authorized Access Only</p>
            
            <button @click="$emit('logout')" class="w-full py-6 bg-zinc-900 text-red-500 rounded-[2rem] font-black uppercase text-[12px] tracking-widest active:scale-95 transition-all border border-red-500/10 hover:bg-red-500 hover:text-white">
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
            <button @click="showResetModal = true" class="text-[8px] font-black uppercase tracking-widest text-zinc-500 border border-white/5 px-4 py-2 rounded-full active:opacity-50 transition-all hover:bg-white/5">Reset</button>
          </section>

          <transition-group name="list" tag="div" class="space-y-2">
            <div v-for="log in historyLogs" :key="log.id" class="p-6 bg-zinc-950 border border-white/5 rounded-[1.5rem] flex justify-between items-center transition-all">
              <div>
                <p class="text-[11px] font-bold uppercase tracking-tight mb-1">{{ log.bookTitle }}</p>
                <p class="text-[9px] text-zinc-600 uppercase tracking-widest font-bold">{{ log.userEmail }}</p>
              </div>
              <div class="text-right">
                <span class="text-[8px] px-3 py-1 rounded-full font-black uppercase tracking-widest border" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
                <p class="text-[7px] text-zinc-800 font-mono mt-1 font-bold">{{ formatTimestamp(log.createdAt) }}</p>
              </div>
            </div>
          </transition-group>
        </div>

      </transition>
    </main>

    <!-- COMPACT NAVIGATION BAR -->
    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 w-full max-w-[360px] px-6">
      <nav class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-full p-1 flex items-center justify-between shadow-2xl">
        <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'community', 'logs']" :key="tab" @click="activeTab = tab" 
                :class="activeTab === tab ? 'bg-white text-black shadow-lg scale-95' : 'text-zinc-500 hover:text-zinc-300'" 
                class="w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 relative">
          
          <svg v-if="tab === 'dashboard'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          <svg v-if="tab === 'inventory'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
          <svg v-if="tab === 'requests'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          <svg v-if="tab === 'borrowers'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
          <svg v-if="tab === 'community'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0" /></svg>
          <svg v-if="tab === 'logs'" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          
          <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute -top-0.5 -right-0.5 w-3.5 h-3.5 bg-blue-600 rounded-full border-2 border-black flex items-center justify-center text-[7px] font-black text-white">
            {{ pendingRequests.length }}
          </div>
        </button>
      </nav>
    </div>

    <!-- MODAL: ADD BOOK -->
    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 backdrop-blur-xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-3xl font-bold tracking-tighter mb-8 uppercase apple-gradient leading-none">Add Asset</h2>
          <div class="space-y-1.5 mb-10">
            <label class="text-[9px] font-black uppercase tracking-[0.3em] text-zinc-600 ml-2">Label Identity</label>
            <input v-model="newBook.title" type="text" placeholder="BOOK TITLE" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-5 px-6 text-white outline-none font-bold placeholder:text-zinc-700 focus:border-white transition-all uppercase" @keyup.enter="addBook" />
          </div>
          <div class="flex gap-3">
            <button @click="addBook" class="flex-[2] py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Register</button>
            <button @click="showAddModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL: APPROVE CONFIRMATION -->
    <transition name="fade">
      <div v-if="showApproveModal" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/90 backdrop-blur-xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <div class="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M5 13l4 4L19 7" /></svg>
          </div>
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase leading-none">Authorize?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10 leading-relaxed px-4">
            granting access to<br>
            <span class="text-white">{{ activeRequest?.userEmail }}</span>
          </p>
          <div class="flex gap-3">
            <button @click="approveRequest(activeRequest)" class="flex-1 py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Approve</button>
            <button @click="showApproveModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL: RETURN CONFIRMATION -->
    <transition name="fade">
      <div v-if="showReturnModal" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/90 backdrop-blur-xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <div class="w-16 h-16 bg-amber-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          </div>
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase leading-none">Confirm Return?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10 leading-relaxed px-4">
            Checking in<br>
            <span class="text-white">{{ activeReturn?.bookTitle }}</span>
          </p>
          <div class="flex gap-3">
            <button @click="markAsReturned(activeReturn)" class="flex-1 py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Process</button>
            <button @click="showReturnModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL: DELETE CONFIRMATION -->
    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/90 backdrop-blur-xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <div class="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase leading-none">Delete Asset?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10 leading-relaxed px-4">
            You are about to permanently remove<br>
            <span class="text-white">{{ bookToDelete?.title }}</span>
          </p>
          <div class="flex gap-3">
            <button @click="deleteBook" class="flex-1 py-5 bg-red-600 text-white rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Delete</button>
            <button @click="showDeleteModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- MODAL: RESET HISTORY CONFIRMATION -->
    <transition name="fade">
      <div v-if="showResetModal" class="fixed inset-0 z-[110] flex items-center justify-center bg-black/90 backdrop-blur-xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[3rem] max-w-sm w-full shadow-2xl text-center">
          <div class="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86 7.717l.547 1.022M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707" /></svg>
          </div>
          <h2 class="text-2xl font-bold tracking-tighter mb-2 uppercase leading-none">Clear Logs?</h2>
          <p class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mb-10 leading-relaxed px-4">
            This will perform a system wipe on<br>
            all transaction history.
          </p>
          <div class="flex gap-3">
            <button @click="clearLogs" class="flex-1 py-5 bg-white text-black rounded-2xl font-black uppercase text-[11px] tracking-widest active:scale-95 transition-all">Clear All</button>
            <button @click="showResetModal = false" class="flex-1 py-5 bg-zinc-900 text-zinc-500 rounded-2xl font-bold uppercase text-[11px] active:scale-95 transition-all">Cancel</button>
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

const activeTab = ref('dashboard');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);

const showAddModal = ref(false);
const showDeleteModal = ref(false);
const showResetModal = ref(false);
const showApproveModal = ref(false);
const showReturnModal = ref(false);

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

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

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

const confirmApprove = (req) => {
  activeRequest.value = req;
  showApproveModal.value = true;
};

const approveRequest = async (req) => {
  await updateDoc(doc(db, "notifications", req.id), { status: 'approved' });
  await addDoc(collection(db, "borrowers"), { 
    bookTitle: req.bookTitle,
    userId: req.userId,
    userEmail: req.userEmail,
    returnSchedule: req.returnSchedule,
    status: 'active', 
    approvedAt: serverTimestamp(),
    createdAt: serverTimestamp()
  });
  await addDoc(collection(db, "history"), { 
    bookTitle: req.bookTitle,
    userEmail: req.userEmail,
    status: 'approved', 
    createdAt: serverTimestamp() 
  });
  showApproveModal.value = false;
  activeRequest.value = null;
};

const declineRequest = async (id) => {
  await updateDoc(doc(db, "notifications", id), { status: 'declined' });
};

const confirmReturn = (person) => {
  activeReturn.value = person;
  showReturnModal.value = true;
};

const markAsReturned = async (person) => {
  try {
    await addDoc(collection(db, "history"), {
      bookTitle: person.bookTitle,
      userEmail: person.userEmail,
      userId: person.userId,
      returnSchedule: person.returnSchedule,
      status: 'returned',
      createdAt: serverTimestamp()
    });
    await deleteDoc(doc(db, "borrowers", person.id));
    showReturnModal.value = false;
    activeReturn.value = null;
  } catch (err) {
    console.error("Return operation failed:", err);
  }
};

const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s.includes('approved') || s.includes('returned')) return 'text-green-500 bg-green-500/10 border-green-500/20';
  if (s.includes('declined')) return 'text-red-500 bg-red-500/10 border-red-500/20';
  return 'text-zinc-500 border-white/5';
};

const formatTimestamp = (ts) => {
  if (!ts) return 'just now';
  return new Date(ts.seconds * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

const clearLogs = async () => {
  const batch = writeBatch(db);
  historyLogs.value.forEach(l => batch.delete(doc(db, "history", l.id)));
  await batch.commit();
  showResetModal.value = false;
}
</script>

<style scoped>
.apple-gradient { background: linear-gradient(180deg, #ffffff 0%, #444444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

/* Page Transitions */
.page-enter-active, .page-leave-active { transition: opacity 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.page-enter-from, .page-leave-to { opacity: 0; }

/* Simple Fade */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* List Item Animations */
.list-enter-active, .list-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.list-enter-from { opacity: 0; transform: translateY(10px); }
.list-leave-to { opacity: 0; transform: scale(0.95); }
.list-move { transition: transform 0.4s ease; }
</style>