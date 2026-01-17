<template>
  <div class="bg-black min-h-screen selection:bg-white/30 overflow-hidden font-ios text-white">
    
    <transition name="loader-fade">
      <div v-if="isSystemLoading" class="fixed inset-0 z-[200] bg-black flex flex-col items-center justify-center">
        <div class="ios-spinner">
          <div v-for="i in 12" :key="i" :class="'bar' + i"></div>
        </div>
        <p class="mt-8 text-white/40 text-[10px] tracking-[0.4em] uppercase font-bold animate-pulse">Initializing AKLAT</p>
      </div>
    </transition>

    <transition name="page-swap" mode="out-in">
      <div v-if="!currentView && !isSystemLoading" key="auth" class="min-h-screen w-full relative flex items-center justify-center p-6 md:p-12">
        
        <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
          <div class="orb orb-1"></div>
          <div class="orb orb-2"></div>
          <div class="absolute inset-0 opacity-[0.05] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]"></div>
        </div>

        <div class="relative z-10 w-full max-w-6xl flex flex-col lg:flex-row items-center justify-between gap-12 lg:gap-24 animate-reveal">
          
          <div class="w-full max-w-md">
            <div 
              class="relative backdrop-blur-3xl bg-zinc-900/40 border border-white/10 rounded-[3rem] shadow-2xl overflow-hidden transition-all duration-700 ease-[cubic-bezier(0.23,1,0.32,1)]"
              :style="{ height: containerHeight + 'px' }"
            >
              <transition name="form-fade" mode="out-in" @before-leave="beforeLeave" @enter="enter">
                
                <div v-if="!isLogin" key="signup" class="p-10 md:p-12 space-y-8 flex flex-col">
                  <header class="space-y-2">
                    <h2 class="text-3xl font-semibold text-white tracking-tight">Register</h2>
                    <p class="text-zinc-500 text-sm">Join the AKLAT library system.</p>
                  </header>
                  
                  <form @submit.prevent="handleSignup" class="space-y-4">
                    <input v-model="form.name" type="text" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Full Name" />
                    <input v-model="form.email" type="email" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Email Address" />
                    <input v-model="form.password" type="password" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Password" />
                    <button type="submit" :disabled="authLoading" class="w-full py-5 bg-white text-black font-bold rounded-2xl transition-all active:scale-[0.98]">
                      {{ authLoading ? 'Registering...' : 'Create Account' }}
                    </button>
                    <p v-if="errorMsg" class="text-red-400 text-[10px] font-bold text-center uppercase tracking-widest mt-2">{{ errorMsg }}</p>
                  </form>
                  
                  <p class="text-center text-zinc-500 text-sm">
                    Already a member? <button @click="isLogin = true; errorMsg = ''" class="text-white font-semibold hover:underline">Log In</button>
                  </p>
                </div>

                <div v-else key="login" class="p-10 md:p-12 space-y-8 flex flex-col">
                  <header class="space-y-2">
                    <h2 class="text-3xl font-semibold text-white tracking-tight">Welcome</h2>
                    <p class="text-zinc-500 text-sm">Sign in to access the library.</p>
                  </header>
                  
                  <form @submit.prevent="handleLogin" class="space-y-5">
                    <input v-model="form.email" type="email" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Email" />
                    <input v-model="form.password" type="password" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Password" />
                    <button type="submit" :disabled="authLoading" class="w-full py-5 bg-white text-black font-bold rounded-2xl active:scale-[0.98]">
                      {{ authLoading ? 'Verifying...' : 'Sign In' }}
                    </button>
                    <p v-if="errorMsg" class="text-white text-[10px] font-bold text-center uppercase tracking-widest mt-4">{{ errorMsg }}</p>
                  </form>

                  <p class="text-center text-zinc-500 text-sm">
                    Don't have an account? <button @click="isLogin = false; errorMsg = ''" class="text-white font-semibold hover:underline">Join Now</button>
                  </p>
                </div>

              </transition>
            </div>
          </div>

          <div class="w-full lg:max-w-xl text-center lg:text-left space-y-8">
            <h1 class="text-6xl md:text-8xl font-bold tracking-tight leading-[0.9] ios-gradient-text">AKLAT.<br/>SYSTEM.</h1>
            <p class="text-xl md:text-2xl text-zinc-400 font-medium max-w-md mx-auto lg:mx-0">Simple. Secure. Accessible everywhere.</p>
            <div class="flex items-center justify-center lg:justify-start gap-4 text-zinc-600 font-bold text-[10px] uppercase tracking-[0.4em]">
              <span>v.1.0.0 Stable</span>
              <span class="w-1 h-1 bg-white rounded-full"></span>
              <span>Firebase Cloud</span>
            </div>
          </div>

        </div>
      </div>

      <Admin v-else-if="currentView === 'admin'" key="admin" @logout="handleLogout" />
      
      <div v-else-if="currentView === 'user'" key="user-view" class="h-screen flex flex-col items-center justify-center text-white bg-black p-6">
        <div class="text-center space-y-8">
          <p class="text-zinc-600 uppercase tracking-[0.6em] text-[10px] mb-4 animate-pulse">Access Granted</p>
          <h1 class="text-6xl font-bold tracking-tighter uppercase">Student Dashboard</h1>
          <p class="text-zinc-500 max-w-sm mx-auto">Welcome to the AKLAT library collection. You can now browse and manage your reading list.</p>
          <button @click="handleLogout" class="px-12 py-4 border border-white/20 rounded-full hover:bg-white hover:text-black transition-all font-bold uppercase tracking-widest text-xs">Logout</button>
        </div>
      </div>

    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue';
import Admin from './Admin.vue';
import { auth, db } from './lib/firebase'; // Added 'db' for Firestore
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged 
} from "firebase/auth";
import { doc, setDoc, serverTimestamp } from "firebase/firestore"; // Added for saving users

const currentView = ref(null);
const isSystemLoading = ref(true);
const authLoading = ref(false);
const isLogin = ref(true);
const errorMsg = ref('');
const containerHeight = ref(600);
const form = reactive({ name: '', email: '', password: '' });

// Transitions
const beforeLeave = (el) => { el.style.width = el.offsetWidth + 'px'; el.style.position = 'absolute'; };
const enter = (el) => { nextTick(() => { containerHeight.value = el.offsetHeight; }); };

// Firebase Actions

const saveUserToDatabase = async (user, name = null) => {
  // Sinisave ang user sa 'users' collection para lumitaw sa Community tab
  try {
    const is_admin = user.email.includes('admin');
    await setDoc(doc(db, "users", user.uid), {
      email: user.email,
      fullName: name || user.displayName || 'New Member',
      role: is_admin ? 'Admin' : 'Member',
      lastLogin: serverTimestamp()
    }, { merge: true });
  } catch (e) {
    console.error("Error saving user: ", e);
  }
};

const handleSignup = async () => {
  authLoading.value = true;
  errorMsg.value = "";
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, form.email, form.password);
    // Pagka-rehistro, i-save agad sa Database
    await saveUserToDatabase(userCredential.user, form.name);
    alert("Success! Your account is created.");
    isLogin.value = true;
  } catch (err) {
    errorMsg.value = err.message;
  } finally { authLoading.value = false; }
};

const handleLogin = async () => {
  authLoading.value = true;
  errorMsg.value = "";
  try {
    const userCredential = await signInWithEmailAndPassword(auth, form.email, form.password);
    // Pagka-login, i-update ang record sa Database
    await saveUserToDatabase(userCredential.user);
    const user = userCredential.user;
    currentView.value = user.email.includes('admin') ? 'admin' : 'user';
  } catch (err) {
    errorMsg.value = "Invalid email or password.";
  } finally { authLoading.value = false; }
};

const handleLogout = async () => {
  await signOut(auth);
  currentView.value = null;
};

onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      currentView.value = user.email.includes('admin') ? 'admin' : 'user';
    }
  });

  setTimeout(() => { 
    isSystemLoading.value = false;
    nextTick(() => {
      const activeEl = document.querySelector('.p-10');
      if (activeEl) containerHeight.value = activeEl.offsetHeight;
    });
  }, 2500);
});
</script>

<style>
.font-ios { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif; }
.ios-gradient-text { background: linear-gradient(180deg, #FFFFFF 0%, #A1A1AA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.ios-spinner { position: relative; width: 32px; height: 32px; }
.ios-spinner div { position: absolute; left: 46%; top: 10%; width: 8%; height: 25%; background: white; border-radius: 50px; opacity: 0.1; animation: ios-fade 1s linear infinite; }
@keyframes ios-fade { from { opacity: 1; } to { opacity: 0.1; } }
.bar1 { transform: rotate(0deg) translate(0, -100%); animation-delay: 0s !important; }
.bar2 { transform: rotate(30deg) translate(0, -100%); animation-delay: -0.916s !important; }
.bar3 { transform: rotate(60deg) translate(0, -100%); animation-delay: -0.833s !important; }
.bar4 { transform: rotate(90deg) translate(0, -100%); animation-delay: -0.75s !important; }
.bar5 { transform: rotate(120deg) translate(0, -100%); animation-delay: -0.666s !important; }
.bar6 { transform: rotate(150deg) translate(0, -100%); animation-delay: -0.583s !important; }
.bar7 { transform: rotate(180deg) translate(0, -100%); animation-delay: -0.5s !important; }
.bar8 { transform: rotate(210deg) translate(0, -100%); animation-delay: -0.416s !important; }
.bar9 { transform: rotate(240deg) translate(0, -100%); animation-delay: -0.333s !important; }
.bar10 { transform: rotate(270deg) translate(0, -100%); animation-delay: -0.25s !important; }
.bar11 { transform: rotate(300deg) translate(0, -100%); animation-delay: -0.166s !important; }
.bar12 { transform: rotate(330deg) translate(0, -100%); animation-delay: -0.083s !important; }

/* Transitions */
.orb { position: absolute; border-radius: 50%; filter: blur(140px); opacity: 0.15; pointer-events: none; }
.orb-1 { width: 800px; height: 800px; background: radial-gradient(circle, #ffffff 0%, transparent 70%); top: -400px; left: -200px; }
.orb-2 { width: 600px; height: 600px; background: radial-gradient(circle, #52525b 0%, transparent 70%); bottom: -300px; right: -100px; }
.loader-fade-leave-active { transition: opacity 0.6s ease; }
.loader-fade-leave-to { opacity: 0; }
.page-swap-enter-active, .page-swap-leave-active { transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1); }
.page-swap-enter-from { opacity: 0; filter: blur(10px); }
.form-fade-enter-active { transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1) 0.1s; }
.form-fade-leave-active { transition: all 0.3s ease; }
.form-fade-enter-from { opacity: 0; transform: translateY(15px); }
.form-fade-leave-to { opacity: 0; transform: translateY(-15px); }
@keyframes reveal { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
.animate-reveal { animation: reveal 1.2s cubic-bezier(0.23, 1, 0.32, 1) forwards; }
</style>