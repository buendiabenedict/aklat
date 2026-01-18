<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40 text-left">
    
    <header class="p-6 flex justify-between items-center relative z-20">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-black text-lg shadow-[0_0_20px_rgba(37,99,235,0.4)]">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.744c0 5.548 4.075 10.14 9 10.856 4.925-.716 9-5.308 9-10.856 0-1.31-.21-2.57-.598-3.744A11.959 11.959 0 0112 2.714z" />
          </svg>
        </div>
        <div>
          <h1 class="text-sm font-bold tracking-tighter uppercase leading-none">Admin Central</h1>
          <p class="text-[10px] font-black text-blue-500 mt-1 uppercase tracking-widest">{{ currentTime }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2 bg-zinc-900 px-3 py-1.5 rounded-full border border-white/5 shadow-inner">
        <div class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
        <span class="text-[9px] font-bold uppercase tracking-widest text-zinc-400">System Live</span>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 relative z-10">
      <transition name="page" mode="out-in">
        
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6 py-4">
          <section>
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Metrics</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Dashboard</h2>
          </section>

          <div class="grid grid-cols-2 gap-3">
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Total Books</p>
              <p class="text-3xl font-bold tracking-tighter">{{ books.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Users</p>
              <p class="text-3xl font-bold tracking-tighter text-blue-500">{{ users.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">Active Loans</p>
              <p class="text-3xl font-bold tracking-tighter text-amber-500">{{ borrowers.length }}</p>
            </div>
            <div class="bg-zinc-950 border border-white/5 p-6 rounded-3xl text-center">
              <p class="text-zinc-500 text-[9px] font-bold uppercase tracking-widest mb-1">History Logs</p>
              <p class="text-3xl font-bold tracking-tighter text-zinc-400">{{ historyLogs.length }}</p>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'inventory'" key="inventory" class="py-4">
          <section class="mb-6 flex justify-between items-end">
            <div>
              <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Repository</p>
              <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Inventory</h2>
            </div>
            <div class="flex gap-2">
              <button v-if="selectedBooks.length > 0" @click="showDeleteModal = true" class="w-12 h-12 bg-red-600 text-white rounded-2xl flex items-center justify-center shadow-lg active:scale-90 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>
              </button>
              <button @click="showAddModal = true" class="w-12 h-12 bg-white text-black rounded-2xl flex items-center justify-center shadow-xl active:scale-90 transition-all">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path d="M12 4.5v15m7.5-7.5h-15" /></svg>
              </button>
            </div>
          </section>
          <div class="space-y-2">
            <div v-for="book in books" :key="book.id" @click="toggleSelectBook(book.id)" :class="selectedBooks.includes(book.id) ? 'border-blue-500 bg-blue-500/10' : 'border-white/5 bg-zinc-950'" class="p-4 rounded-xl flex items-center justify-between border transition-all cursor-pointer">
              <div class="flex items-center gap-4">
                <div class="w-4 h-4 rounded border border-zinc-700 flex items-center justify-center" :class="selectedBooks.includes(book.id) ? 'bg-blue-500 border-blue-500' : ''">
                  <svg v-if="selectedBooks.includes(book.id)" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="4"><path d="M5 13l4 4L19 7" /></svg>
                </div>
                <div>
                  <h3 class="text-sm font-bold tracking-tight uppercase leading-none">{{ book.title }}</h3>
                  <p class="text-[8px] text-zinc-600 uppercase mt-1 tracking-widest">UID: {{ book.id.slice(0,8) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'requests'" key="requests" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Queue</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Requests</h2>
          </section>
          <div v-if="pendingRequests.length === 0" class="p-16 border border-dashed border-white/10 rounded-[2rem] text-center">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">Clear Queue</p>
          </div>
          <div v-for="req in pendingRequests" :key="req.id" class="bg-zinc-950 border border-white/10 p-6 rounded-3xl mb-4">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-lg font-bold tracking-tighter uppercase leading-none">{{ req.bookTitle }}</h3>
                <p class="text-[9px] text-blue-500 font-bold uppercase tracking-widest mt-1">{{ req.userEmail }}</p>
              </div>
            </div>
            <div class="flex gap-2">
              <button @click="approveRequest(req)" class="flex-1 py-3 bg-white text-black rounded-xl font-black text-[9px] uppercase tracking-widest">Approve</button>
              <button @click="declineRequest(req.id)" class="flex-1 py-3 bg-zinc-900 text-red-500 rounded-xl font-black text-[9px] uppercase tracking-widest border border-red-500/10">Decline</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Real-time Tracking</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Borrowers</h2>
          </section>
          <div v-for="person in borrowers" :key="person.id" 
               :class="getRemainingMs(person.returnSchedule) <= 0 ? 'bg-red-600 text-white border-red-400' : 'bg-white text-black border-blue-600'"
               class="p-5 rounded-2xl mb-3 flex justify-between items-center shadow-xl border-l-[6px] transition-all duration-500">
            <div class="max-w-[60%]">
              <h3 class="text-sm font-black uppercase tracking-tighter leading-none truncate">{{ person.bookTitle }}</h3>
              <p class="text-[8px] font-bold uppercase mt-1 truncate" :class="getRemainingMs(person.returnSchedule) <= 0 ? 'text-white/70' : 'text-zinc-500'">
                {{ person.userEmail }}
              </p>
              <div class="mt-2 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full animate-ping" :class="getRemainingMs(person.returnSchedule) <= 0 ? 'bg-white' : 'bg-blue-600'"></span>
                <span class="text-[10px] font-black font-mono tracking-tighter">
                  {{ formatCountdown(person.returnSchedule) }}
                </span>
              </div>
            </div>
            <button @click="confirmReturn(person)" 
                    :class="getRemainingMs(person.returnSchedule) <= 0 ? 'bg-white text-red-600' : 'bg-black text-white'"
                    class="px-4 py-2 rounded-lg text-[8px] font-black uppercase tracking-widest shadow-lg active:scale-95 transition-all">
              Returned
            </button>
          </div>
          <div v-if="borrowers.length === 0" class="text-center py-20">
            <p class="text-zinc-800 font-bold uppercase text-[9px] tracking-[0.3em]">No Active Loans</p>
          </div>
        </div>

        <div v-else-if="activeTab === 'community'" key="community" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">User Base</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Community</h2>
          </section>
          <div class="space-y-3">
            <div v-for="user in users" :key="user.id" class="bg-zinc-950 border border-white/5 p-4 rounded-2xl flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-zinc-800 flex items-center justify-center font-bold text-blue-500 border border-white/5 uppercase">
                {{ user.email?.[0] }}
              </div>
              <div>
                <p class="text-[11px] font-black uppercase tracking-tighter">{{ user.email }}</p>
                <p class="text-[8px] font-bold uppercase tracking-widest" :class="user.role === 'admin' ? 'text-blue-500' : 'text-zinc-600'">
                  {{ user.role || 'Member' }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'logs'" key="logs" class="py-10">
          <section class="mb-6">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">History</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">System Logs</h2>
          </section>
          <div class="space-y-2">
            <div v-for="log in historyLogs" :key="log.id" class="p-4 bg-zinc-950 border border-white/5 rounded-xl flex justify-between items-center">
              <div>
                <p class="text-[10px] font-bold uppercase truncate max-w-[150px]">{{ log.bookTitle }}</p>
                <p class="text-[8px] text-zinc-500 uppercase tracking-widest font-bold">{{ log.userEmail }}</p>
              </div>
              <span class="text-[8px] px-2 py-0.5 rounded font-black uppercase tracking-widest" :class="getLogBadgeClass(log.status)">{{ log.status }}</span>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'profile'" key="profile" class="py-10 text-center">
          <section class="text-left mb-10">
            <p class="text-zinc-600 text-[9px] font-bold uppercase tracking-[0.4em] mb-1">Identity</p>
            <h2 class="text-5xl font-bold tracking-tighter uppercase apple-gradient">Profile</h2>
          </section>
          <div class="w-24 h-24 bg-blue-600 border border-blue-400 mx-auto rounded-[2.5rem] flex items-center justify-center text-3xl font-black mb-4 shadow-2xl">A</div>
          <h2 class="text-2xl font-bold tracking-tighter uppercase">{{ auth.currentUser?.email }}</h2>
          <button @click="showLogoutModal = true" class="mt-20 w-full max-w-xs py-4 bg-zinc-900 text-red-500 rounded-2xl font-black uppercase text-[10px] tracking-widest border border-red-500/10 active:bg-red-600 active:text-white transition-all">Sign Out Admin Session</button>
        </div>

      </transition>
    </main>

    <div class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 w-full max-w-[420px] px-4">
      <nav class="bg-zinc-900/80 backdrop-blur-3xl border border-white/10 rounded-full p-2 flex items-center justify-between shadow-2xl overflow-x-auto no-scrollbar">
        <button v-for="tab in ['dashboard', 'inventory', 'requests', 'borrowers', 'community', 'logs', 'profile']" :key="tab" @click="activeTab = tab" :class="activeTab === tab ? 'bg-white text-black scale-110' : 'text-zinc-600'" class="w-10 h-10 min-w-[40px] rounded-full flex items-center justify-center transition-all relative">
          <div v-if="tab === 'requests' && pendingRequests.length > 0" class="absolute -top-1 -right-1 min-w-[16px] h-4 bg-red-600 rounded-full border border-black flex items-center justify-center px-1 animate-bounce z-10 shadow-lg">
            <span class="text-[8px] font-black text-white leading-none">{{ pendingRequests.length }}</span>
          </div>
          <div v-if="tab === 'borrowers' && hasOverdue" class="absolute -top-1 -right-1 w-3 h-3 bg-red-600 rounded-full border border-black animate-pulse z-10"></div>
          
          <svg v-if="tab === 'dashboard'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25h-2.25a2.25 2.25 0 01-2.25-2.25v-2.25z" /></svg>
          <svg v-if="tab === 'inventory'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" /></svg>
          <svg v-if="tab === 'requests'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>
          <svg v-if="tab === 'borrowers'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <svg v-if="tab === 'community'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
          <svg v-if="tab === 'logs'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M8.25 6.75h12M8.25 12h12M8.25 17.25h12M3.75 6.75h.007v.008H3.75V6.75zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zM3.75 12h.007v.008H3.75V12zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm-.375 5.25h.007v.008H3.75v-.008zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" /></svg>
          <svg v-if="tab === 'profile'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
        </button>
      </nav>
    </div>

    <transition name="fade">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-8 rounded-[2.5rem] max-w-sm w-full shadow-2xl">
          <h2 class="text-xl font-bold tracking-tighter mb-6 uppercase apple-gradient text-center">Batch Initialize</h2>
          <textarea v-model="batchTitleInput" placeholder="Enter book titles (one per line)" rows="5" class="w-full bg-zinc-900 border border-white/5 rounded-2xl py-4 px-6 text-white outline-none font-bold mb-4 text-xs resize-none"></textarea>
          <button @click="batchAddBooks" :disabled="!batchTitleInput" class="w-full py-4 bg-white text-black rounded-2xl font-black uppercase text-[10px] tracking-widest active:scale-95 transition-all">Add to Repository</button>
          <button @click="showAddModal = false" class="w-full py-4 text-zinc-600 font-bold uppercase text-[9px] mt-1">Cancel Action</button>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <div class="w-16 h-16 bg-red-600/20 text-red-600 mx-auto rounded-full flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </div>
          <h3 class="text-xl font-black mb-2 uppercase tracking-tighter">Purge Data?</h3>
          <p class="text-[10px] text-zinc-500 font-bold uppercase mb-8 tracking-widest leading-relaxed">You are about to delete {{ selectedBooks.length }} selected items from the repository.</p>
          <div class="flex gap-3">
            <button @click="showDeleteModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">Abort</button>
            <button @click="deleteSelectedBooks" class="flex-1 py-4 rounded-2xl bg-red-600 text-white font-black text-[10px] uppercase">Confirm</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showReturnModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div v-if="targetBorrower" class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <div class="w-16 h-16 bg-blue-600/20 text-blue-500 mx-auto rounded-full flex items-center justify-center mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
          </div>
          <h3 class="text-xl font-black mb-2 uppercase tracking-tighter">Mark Returned?</h3>
          <p class="text-[10px] text-zinc-500 font-bold uppercase mb-8 tracking-widest leading-relaxed">
            Record return for "{{ targetBorrower.bookTitle }}" by {{ targetBorrower.userEmail }}.
          </p>
          <div class="flex gap-3">
            <button @click="showReturnModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="executeReturn" class="flex-1 py-4 rounded-2xl bg-white text-black font-black text-[10px] uppercase">Yes</button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showLogoutModal" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 backdrop-blur-2xl px-6">
        <div class="bg-zinc-950 border border-white/10 p-10 rounded-[2.5rem] max-w-xs w-full text-center">
          <h3 class="text-xl font-black mb-6 uppercase tracking-tighter leading-none">Terminate?</h3>
          <div class="flex gap-3">
            <button @click="showLogoutModal = false" class="flex-1 py-4 rounded-2xl border border-white/10 font-bold text-zinc-500 text-[10px] uppercase">No</button>
            <button @click="executeLogout" class="flex-1 py-4 rounded-2xl bg-red-600 text-white font-black text-[10px] uppercase">Yes</button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineEmits, onUnmounted } from 'vue';
import { db, auth } from './lib/firebase';
import { collection, onSnapshot, addDoc, deleteDoc, doc, updateDoc, serverTimestamp, query, orderBy, writeBatch } from "firebase/firestore";
import { signOut } from "firebase/auth";

const emit = defineEmits(['logout']);

const activeTab = ref('dashboard');
const books = ref([]);
const users = ref([]);
const notifications = ref([]);
const borrowers = ref([]);
const historyLogs = ref([]);
const selectedBooks = ref([]);

// Modals
const showAddModal = ref(false);
const showDeleteModal = ref(false);
const showReturnModal = ref(false);
const showLogoutModal = ref(false);

const targetBorrower = ref(null);
const batchTitleInput = ref('');
const currentTime = ref('');

const timerRef = ref(Date.now());
let clockInterval;

const updateClock = () => {
  const now = new Date();
  timerRef.value = now.getTime();
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour12: true, hour: '2-digit', minute: '2-digit' 
  });
};

const getRemainingMs = (schedule) => {
  if (!schedule) return 0;
  const fixedDate = schedule.replace(/-/g, '/');
  const target = new Date(fixedDate);
  target.setHours(23, 59, 59, 999); 
  const targetMs = target.getTime();
  return isNaN(targetMs) ? 0 : targetMs - timerRef.value;
};

const formatCountdown = (schedule) => {
  const diff = getRemainingMs(schedule);
  if (diff <= 0) return "EXPIRED / OVERDUE";
  const d = Math.floor(diff / (1000 * 60 * 60 * 24));
  const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const s = Math.floor((diff % (1000 * 60)) / 1000);
  return `${d}d : ${h.toString().padStart(2, '0')}h : ${m.toString().padStart(2, '0')}m : ${s.toString().padStart(2, '0')}s`;
};

const hasOverdue = computed(() => {
  return borrowers.value.some(p => getRemainingMs(p.returnSchedule) <= 0);
});

onMounted(() => {
  updateClock();
  clockInterval = setInterval(updateClock, 1000);

  onSnapshot(collection(db, "books"), (s) => books.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "users"), (s) => users.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "notifications"), orderBy("createdAt", "desc")), (s) => notifications.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(query(collection(db, "history"), orderBy("createdAt", "desc")), (s) => historyLogs.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
  onSnapshot(collection(db, "borrowers"), (s) => borrowers.value = s.docs.map(d => ({ id: d.id, ...d.data() })));
});

onUnmounted(() => {
  clearInterval(clockInterval);
});

const pendingRequests = computed(() => notifications.value.filter(r => r.status === 'pending'));

const getLogBadgeClass = (status) => {
  const s = status?.toLowerCase() || '';
  if (s.includes('approve') || s.includes('returned')) return 'text-green-500 bg-green-500/10';
  if (s.includes('decline')) return 'text-red-500 bg-red-500/10';
  return 'text-zinc-500 bg-zinc-900';
};

const batchAddBooks = async () => {
  const titles = batchTitleInput.value.split('\n').filter(t => t.trim() !== '');
  const batch = writeBatch(db);
  titles.forEach(title => {
    const docRef = doc(collection(db, "books"));
    batch.set(docRef, { title, createdAt: serverTimestamp() });
  });
  await batch.commit();
  batchTitleInput.value = '';
  showAddModal.value = false;
};

const toggleSelectBook = (id) => {
  const index = selectedBooks.value.indexOf(id);
  if (index > -1) selectedBooks.value.splice(index, 1);
  else selectedBooks.value.push(id);
};

const deleteSelectedBooks = async () => {
  const batch = writeBatch(db);
  selectedBooks.value.forEach(id => batch.delete(doc(db, "books", id)));
  await batch.commit();
  selectedBooks.value = [];
  showDeleteModal.value = false;
};

const approveRequest = async (req) => {
  // notification id is req.id
  await updateDoc(doc(db, "notifications", req.id), { status: 'approved' });
  await addDoc(collection(db, "borrowers"), { 
    ...req,
    requestId: req.id, // Save the notification/request ID for later syncing
    returnSchedule: req.returnDate, 
    status: 'approved', 
    approvedAt: serverTimestamp() 
  });
  await addDoc(collection(db, "history"), { bookTitle: req.bookTitle, userEmail: req.userEmail, status: 'approved', createdAt: serverTimestamp() });
};

const declineRequest = async (id) => {
  const req = notifications.value.find(n => n.id === id);
  await updateDoc(doc(db, "notifications", id), { status: 'declined' });
  await addDoc(collection(db, "history"), { bookTitle: req?.bookTitle, userEmail: req?.userEmail, status: 'declined', createdAt: serverTimestamp() });
};

// 🛠️ THE GHOST FIX: SYNCED RETURN LOGIC
const confirmReturn = (person) => {
  targetBorrower.value = person;
  showReturnModal.value = true;
};

const executeReturn = async () => {
  if (!targetBorrower.value) return;
  
  const { id, bookTitle, userEmail, userId, requestId } = targetBorrower.value;

  try {
    const batch = writeBatch(db);

    // 1. Tanggalin sa Admin Borrowers list
    batch.delete(doc(db, "borrowers", id));

    // 2. I-update ang STATUS ng original notification para mawala sa "Borrowed Assets"
    // Dahil ang user view ay nag-fa-filter ng "status === 'approved'"
    if (requestId) {
      batch.update(doc(db, "notifications", requestId), { 
        status: 'returned_archive' 
      });
    }

    // 3. Mag-send ng bagong notification para sa Inbox ng user
    const newNotifRef = doc(collection(db, "notifications"));
    batch.set(newNotifRef, {
      userId: userId,
      bookTitle: bookTitle,
      userEmail: userEmail,
      message: "The librarian set your book to returned.",
      status: 'returned_by_admin',
      createdAt: serverTimestamp()
    });

    // 4. Mag-add sa System Logs
    const historyRef = doc(collection(db, "history"));
    batch.set(historyRef, {
      bookTitle, 
      userEmail, 
      status: 'returned', 
      createdAt: serverTimestamp() 
    });

    // Execute all at once
    await batch.commit();

    showReturnModal.value = false;
    targetBorrower.value = null;
    
    console.log("Sync Complete: Ghost entries cleared! 👻🚫");
  } catch (error) {
    console.error("Return error:", error);
  }
};

const executeLogout = async () => {
  await signOut(auth);
  emit('logout');
};
</script>

<style scoped>
.apple-gradient {
  background: linear-gradient(180deg, #ffffff 0%, #444444 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.no-scrollbar::-webkit-scrollbar { display: none; }
.page-enter-active, .page-leave-active { transition: opacity 0.2s ease; }
.page-enter-from, .page-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>