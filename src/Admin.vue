<template>
  <div class="min-h-screen bg-black text-white font-ios selection:bg-white/20 overflow-x-hidden pb-40">
    <!-- Header -->
    <header class="px-6 py-4 sticky top-0 z-50 bg-black/80 backdrop-blur-xl border-b border-white/5">
      <div class="max-w-5xl mx-auto flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="logo-glow w-10 h-10 bg-blue-600/20 rounded-xl flex items-center justify-center border border-blue-500/30">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/>
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-bold tracking-tighter uppercase italic">Admin</h1>
            <p class="text-xs font-semibold text-blue-400/80 mt-0.5 uppercase tracking-wider">{{ currentTimeDisplay }}</p>
          </div>
        </div>
        
        <div class="flex items-center gap-3">
          <div class="status-indicator px-3 py-1.5 rounded-full border border-green-500/20 bg-green-500/5">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-xs font-bold uppercase tracking-wider text-green-400">Live</span>
            </div>
          </div>
          <button @click="$emit('logout')" class="p-2 text-zinc-400 hover:text-red-400 transition-colors rounded-lg hover:bg-white/5">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-5xl mx-auto px-6 py-4">
      <transition name="fade-slide" mode="out-in">
        <!-- Dashboard -->
        <div v-if="activeTab === 'dashboard'" key="dashboard" class="space-y-6">
          <section>
            <h2 class="text-4xl font-bold tracking-tight uppercase gradient-text italic mb-2">Overview</h2>
            <p class="text-xs text-zinc-500 font-semibold uppercase tracking-wider">System Metrics</p>
          </section>

          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <MetricCard 
              label="Inventory"
              :value="books.length"
              color="text-white"
              :trend="books.length > 0 ? '+' : '0'"
              icon="📚"
            />
            <MetricCard 
              label="Active Users"
              :value="users.length"
              color="text-blue-400"
              :trend="users.length > 5 ? '+' : '0'"
              icon="👥"
            />
            <MetricCard 
              label="Active Loans"
              :value="borrowers.length"
              color="text-amber-400"
              :trend="borrowers.length > 0 ? '+' : '0'"
              icon="📖"
            />
            <MetricCard 
              label="History Logs"
              :value="historyLogs.length"
              color="text-zinc-400"
              @click="activeTab = 'logs'"
              icon="📊"
              clickable
            />
          </div>

          <!-- Pending Requests Banner -->
          <transition name="scale">
            <div v-if="pendingRequests.length > 0" 
                 @click="activeTab = 'requests'"
                 class="pending-requests-banner p-6 rounded-2xl cursor-pointer transform transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]">
              <div class="flex items-center justify-between">
                <div>
                  <div class="flex items-center gap-2 mb-2">
                    <div class="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                    <h3 class="text-lg font-bold uppercase tracking-tight">Action Required</h3>
                  </div>
                  <p class="text-sm text-white/70">{{ pendingRequests.length }} pending request(s)</p>
                </div>
                <div class="badge-count w-12 h-12 bg-white/10 backdrop-blur-sm rounded-xl flex items-center justify-center text-xl font-bold border border-white/20">
                  {{ pendingRequests.length }}
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- Inventory -->
        <div v-else-if="activeTab === 'inventory'" key="inventory" class="space-y-6">
          <section class="flex justify-between items-center">
            <div>
              <h2 class="text-4xl font-bold tracking-tight uppercase gradient-text italic mb-2">Inventory</h2>
              <p class="text-xs text-zinc-500 font-semibold uppercase tracking-wider">Asset Management</p>
            </div>
            <div class="flex gap-2">
              <ActionButton 
                v-if="selectedBooks.length > 0"
                @click="showDeleteModal = true"
                color="red"
                icon="🗑️"
                label="Delete"
                :badge="selectedBooks.length"
              />
              <ActionButton 
                @click="showAddModal = true"
                color="white"
                icon="➕"
                label="Add"
              />
            </div>
          </section>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <BookCard 
              v-for="book in books"
              :key="book.id"
              :book="book"
              :selected="selectedBooks.includes(book.id)"
              @click="toggleSelectBook(book.id)"
            />
          </div>
        </div>

        <!-- Requests -->
        <div v-else-if="activeTab === 'requests'" key="requests" class="space-y-6">
          <section>
            <h2 class="text-4xl font-bold tracking-tight uppercase gradient-text italic mb-2">Approvals</h2>
            <p class="text-xs text-zinc-500 font-semibold uppercase tracking-wider">Queue Management</p>
          </section>

          <div v-if="pendingRequests.length === 0" class="empty-state">
            <div class="text-center py-16">
              <div class="text-6xl mb-4 opacity-20">📭</div>
              <p class="text-lg font-semibold text-zinc-600 mb-2">No Pending Requests</p>
              <p class="text-sm text-zinc-500">All caught up! Check back later.</p>
            </div>
          </div>

          <div class="space-y-4">
            <RequestCard 
              v-for="req in pendingRequests"
              :key="req.id"
              :request="req"
              @approve="approveRequest(req)"
              @decline="declineRequest(req.id)"
            />
          </div>
        </div>

        <!-- Borrowers -->
        <div v-else-if="activeTab === 'borrowers'" key="borrowers" class="space-y-6">
          <section>
            <h2 class="text-4xl font-bold tracking-tight uppercase gradient-text italic mb-2">Borrowers</h2>
            <p class="text-xs text-zinc-500 font-semibold uppercase tracking-wider">Live Tracking</p>
          </section>

          <div class="space-y-3">
            <BorrowerCard 
              v-for="person in borrowers"
              :key="person.id"
              :borrower="person"
              :overdue="isOverdue(person.returnSchedule)"
              @return="markAsReturned(person)"
            />
          </div>
        </div>

        <!-- Logs -->
        <div v-else-if="activeTab === 'logs'" key="logs" class="space-y-6">
          <section class="flex justify-between items-center">
            <div>
              <h2 class="text-4xl font-bold tracking-tight uppercase gradient-text italic mb-2">History</h2>
              <p class="text-xs text-zinc-500 font-semibold uppercase tracking-wider">Audit Record</p>
            </div>
            <ActionButton 
              @click="clearHistory"
              color="red"
              icon="🧹"
              label="Clear"
              outline
            />
          </section>

          <div class="space-y-3">
            <LogCard 
              v-for="log in historyLogs"
              :key="log.id"
              :log="log"
            />
          </div>
        </div>

      </transition>
    </main>

    <!-- Bottom Navigation -->
    <BottomNav 
      :activeTab="activeTab"
      :pendingCount="pendingRequests.length"
      @tab-change="activeTab = $event"
    />

    <!-- Modals -->
    <AddBookModal 
      v-if="showAddModal"
      v-model="newBook.title"
      @submit="addBook"
      @close="showAddModal = false"
    />

    <DeleteModal 
      v-if="showDeleteModal"
      :count="selectedBooks.length"
      @confirm="deleteSelectedBooks"
      @close="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { 
  collection, 
  onSnapshot, 
  addDoc, 
  deleteDoc, 
  doc, 
  updateDoc, 
  serverTimestamp, 
  query, 
  orderBy, 
  writeBatch 
} from "firebase/firestore"
import { db } from './lib/firebase'

// Components
import MetricCard from './components/MetricCard.vue'
import BookCard from './components/BookCard.vue'
import RequestCard from './components/RequestCard.vue'
import BorrowerCard from './components/BorrowerCard.vue'
import LogCard from './components/LogCard.vue'
import BottomNav from './components/BottomNav.vue'
import AddBookModal from './components/AddBookModal.vue'
import DeleteModal from './components/DeleteModal.vue'
import ActionButton from './components/ActionButton.vue'

const emit = defineEmits(['logout'])

// State
const activeTab = ref('dashboard')
const books = ref([])
const users = ref([])
const notifications = ref([])
const borrowers = ref([])
const historyLogs = ref([])
const selectedBooks = ref([])
const showAddModal = ref(false)
const showDeleteModal = ref(false)
const newBook = ref({ title: '' })
const currentTimeDisplay = ref('')

// Computed
const pendingRequests = computed(() => 
  notifications.value.filter(r => r.status === 'pending')
)

// Clock
let clockInterval

const updateClock = () => {
  const now = new Date()
  currentTimeDisplay.value = now.toLocaleTimeString('en-US', { 
    hour12: true, 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Utility Functions
const isOverdue = (schedule) => {
  if (!schedule) return false
  const now = new Date()
  const target = new Date(schedule.replace(/-/g, '/'))
  target.setHours(7, 30, 0, 0)
  return now.getTime() > target.getTime()
}

// CRUD Operations
const toggleSelectBook = (id) => {
  const index = selectedBooks.value.indexOf(id)
  if (index > -1) {
    selectedBooks.value.splice(index, 1)
  } else {
    selectedBooks.value.push(id)
  }
}

const addBook = async () => {
  if (!newBook.value.title.trim()) return
  await addDoc(collection(db, "books"), { 
    title: newBook.value.title.toUpperCase(), 
    createdAt: serverTimestamp() 
  })
  newBook.value.title = ''
  showAddModal.value = false
}

const deleteSelectedBooks = async () => {
  const batch = writeBatch(db)
  selectedBooks.value.forEach(id => batch.delete(doc(db, "books", id)))
  await batch.commit()
  selectedBooks.value = []
  showDeleteModal.value = false
}

const approveRequest = async (req) => {
  await updateDoc(doc(db, "notifications", req.id), { status: 'approved' })
  await addDoc(collection(db, "borrowers"), { 
    ...req, 
    status: 'active', 
    approvedAt: serverTimestamp() 
  })
  await addDoc(collection(db, "history"), { 
    ...req, 
    status: 'approved', 
    createdAt: serverTimestamp() 
  })
}

const declineRequest = async (id) => {
  await updateDoc(doc(db, "notifications", id), { status: 'declined' })
  await addDoc(collection(db, "history"), { 
    id, 
    status: 'declined', 
    createdAt: serverTimestamp() 
  })
}

const markAsReturned = async (person) => {
  await addDoc(collection(db, "history"), { 
    ...person, 
    status: 'returned', 
    createdAt: serverTimestamp() 
  })
  await deleteDoc(doc(db, "borrowers", person.id))
}

const clearHistory = async () => {
  if (confirm("Are you sure you want to clear all history logs?")) {
    const batch = writeBatch(db)
    historyLogs.value.forEach(log => batch.delete(doc(db, "history", log.id)))
    await batch.commit()
  }
}

// Lifecycle
onMounted(() => {
  updateClock()
  clockInterval = setInterval(updateClock, 1000)

  // Real-time listeners
  const unsubscribeBooks = onSnapshot(collection(db, "books"), 
    (snapshot) => books.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  )
  const unsubscribeUsers = onSnapshot(collection(db, "users"), 
    (snapshot) => users.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  )
  const unsubscribeNotifications = onSnapshot(
    query(collection(db, "notifications"), orderBy("createdAt", "desc")), 
    (snapshot) => notifications.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  )
  const unsubscribeHistory = onSnapshot(
    query(collection(db, "history"), orderBy("createdAt", "desc")), 
    (snapshot) => historyLogs.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  )
  const unsubscribeBorrowers = onSnapshot(collection(db, "borrowers"), 
    (snapshot) => borrowers.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  )

  // Cleanup function
  onUnmounted(() => {
    clearInterval(clockInterval)
    unsubscribeBooks()
    unsubscribeUsers()
    unsubscribeNotifications()
    unsubscribeHistory()
    unsubscribeBorrowers()
  })
})
</script>

<style scoped>
/* Gradient Text */
.gradient-text {
  background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Pending Requests Banner */
.pending-requests-banner {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(79, 70, 229, 0.3);
}

/* Logo Glow Effect */
.logo-glow {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

/* Badge Count Animation */
.badge-count {
  animation: float 3s ease-in-out infinite;
}

/* Empty State */
.empty-state {
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
}

/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>