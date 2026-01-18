<template>
  <div class="bg-black min-h-screen selection:bg-white/30 overflow-hidden font-ios text-white flex items-center justify-center">
    
    <!-- INITIAL SYSTEM LOADER -->
    <transition name="loader-fade">
      <div v-if="isSystemLoading" class="fixed inset-0 z-[200] bg-black flex flex-col items-center justify-center">
        <div class="ios-spinner">
          <div v-for="i in 12" :key="i" :class="'bar' + i"></div>
        </div>
        <p class="mt-8 text-white/40 text-[10px] tracking-[0.4em] uppercase font-bold animate-pulse">Initializing AKLAT Cloud</p>
      </div>
    </transition>

    <!-- FORGOT PASSWORD MODAL -->
    <transition name="modal-fade">
      <div v-if="showForgotModal" class="fixed inset-0 z-[400] flex items-center justify-center p-6 backdrop-blur-md bg-black/40">
        <div class="bg-zinc-900 border border-white/10 p-8 rounded-[2rem] max-w-sm w-full shadow-2xl text-center space-y-6">
          <div class="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mx-auto">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <div class="space-y-2">
            <h3 class="text-xl font-semibold">Feature Unavailable</h3>
            <p class="text-zinc-500 text-sm leading-relaxed">Account recovery is currently disabled in the beta environment. Please contact your system administrator.</p>
          </div>
          <button @click="showForgotModal = false" class="w-full py-4 bg-white text-black font-bold rounded-xl active:scale-95 transition-transform">
            Understood
          </button>
        </div>
      </div>
    </transition>

    <!-- MAIN VIEWPORT TRANSITION -->
    <transition name="page-swap" mode="out-in">
      
      <!-- AUTHENTICATION VIEW -->
      <div v-if="!currentView && !isSystemLoading" key="auth" class="w-full min-h-screen relative flex items-center justify-center p-6">
        
        <!-- BACKDROP AMBIENCE: FLOATING CIRCLES & BLINKING DOTS -->
        <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
          <div class="floating-circle circle-1"></div>
          <div class="floating-circle circle-2"></div>
          <div class="floating-circle circle-3"></div>
          
          <!-- Blinking Dots Grid -->
          <div class="absolute inset-0 grid grid-cols-6 md:grid-cols-12 gap-4 p-4 opacity-20">
            <div v-for="n in 48" :key="n" class="dot-container flex items-center justify-center">
              <div class="w-1 h-1 bg-white rounded-full animate-blink" :style="{ animationDelay: (n * 0.1) + 's' }"></div>
            </div>
          </div>
          
          <div class="absolute inset-0 opacity-[0.05] bg-[url('https://grainy-gradients.vercel.app/noise.svg')]"></div>
        </div>

        <div class="relative z-10 w-full max-w-6xl flex flex-col lg:flex-row items-center justify-center gap-12 lg:gap-24">
          
          <!-- AUTH FORM CONTAINER -->
          <div class="w-full max-w-md order-2 lg:order-1">
            <div 
              class="relative backdrop-blur-3xl bg-zinc-900/40 border border-white/10 rounded-[3rem] shadow-2xl overflow-hidden transition-all duration-700 ease-[cubic-bezier(0.23,1,0.32,1)]"
              :style="{ height: containerHeight + 'px' }"
            >
              <transition name="form-morph" mode="out-in" @after-enter="updateHeight" @enter="updateHeight">
                
                <!-- SIGN UP FORM -->
                <div v-if="!isLogin" key="signup" class="auth-card p-10 md:p-12 space-y-8 flex flex-col items-center text-center w-full">
                  <header class="space-y-2">
                    <h2 class="text-3xl font-semibold text-white tracking-tight">Create Account</h2>
                    <p class="text-zinc-500 text-sm">Join the digital library network.</p>
                  </header>
                  <form @submit.prevent="handleSignup" class="space-y-4 w-full text-left">
                    <div class="space-y-3">
                      <input v-model="form.name" type="text" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Full Name" />
                      <input v-model="form.email" type="email" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Email" />
                      <input v-model="form.password" type="password" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Password" />
                    </div>
                    <button type="submit" :disabled="authLoading" class="w-full py-5 bg-white text-black font-bold rounded-2xl transition-all active:scale-[0.98] disabled:opacity-50">
                      {{ authLoading ? 'Registering...' : 'Register' }}
                    </button>
                    <p v-if="errorMsg" class="text-red-400 text-[10px] font-bold text-center uppercase tracking-widest mt-2">{{ errorMsg }}</p>
                  </form>
                  <p class="text-zinc-500 text-sm">Member? <button @click="toggleForm(true)" class="text-white font-semibold hover:underline">Log In</button></p>
                </div>

                <!-- SIGN IN FORM -->
                <div v-else key="login" class="auth-card p-10 md:p-12 space-y-8 flex flex-col items-center text-center w-full">
                  <header class="space-y-2">
                    <h2 class="text-3xl font-semibold text-white tracking-tight">Sign In</h2>
                    <p class="text-zinc-500 text-sm">Access your personal archive.</p>
                  </header>
                  <form @submit.prevent="handleLogin" class="space-y-5 w-full text-left">
                    <div class="space-y-3">
                      <input v-model="form.email" type="email" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Email" />
                      <input v-model="form.password" type="password" required class="w-full bg-white/5 border border-white/10 rounded-2xl p-5 text-white outline-none focus:border-white/40 transition-all placeholder-zinc-700" placeholder="Password" />
                    </div>
                    
                    <div class="flex justify-end">
                      <button type="button" @click="showForgotModal = true" class="text-xs text-zinc-500 hover:text-white transition-colors">Forgot Password?</button>
                    </div>

                    <button type="submit" :disabled="authLoading" class="w-full py-5 bg-white text-black font-bold rounded-2xl active:scale-[0.98] disabled:opacity-50">
                      {{ authLoading ? 'Identifying...' : 'Continue' }}
                    </button>
                    <p v-if="errorMsg" class="text-red-400 text-[10px] font-bold text-center uppercase tracking-widest mt-4">{{ errorMsg }}</p>
                  </form>
                  <p class="text-zinc-500 text-sm">New here? <button @click="toggleForm(false)" class="text-white font-semibold hover:underline">Join Now</button></p>
                </div>

              </transition>
            </div>
          </div>

          <!-- HERO TEXT -->
          <div class="w-full lg:max-w-xl text-center lg:text-left space-y-8 order-1 lg:order-2">
            <h1 class="text-7xl md:text-9xl font-bold tracking-tighter leading-[0.8] ios-gradient-text animate-reveal">AKLAT.<br/>SYSTEM.</h1>
            <p class="text-xl md:text-2xl text-zinc-400 font-medium max-w-md mx-auto lg:mx-0 animate-reveal" style="animation-delay: 0.2s">Simple. Secure. Accessible everywhere.</p>
          </div>
        </div>
      </div>

      <!-- APP VIEWS (ADMIN / USER) -->
      <Admin v-else-if="currentView === 'admin'" key="admin" class="fixed inset-0 w-full h-full z-50" @logout="handleLogout" />
      <User v-else-if="currentView === 'user'" key="user" class="fixed inset-0 w-full h-full z-50" @logout="handleLogout" />

    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue';
import Admin from './Admin.vue';
import User from './User.vue';
import { auth, db } from './lib/firebase';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from "firebase/auth";
import { doc, setDoc, serverTimestamp } from "firebase/firestore";

// UI Logic State
const currentView = ref(null);
const isSystemLoading = ref(true);
const authLoading = ref(false);
const isLogin = ref(true);
const errorMsg = ref('');
const containerHeight = ref(0);
const showForgotModal = ref(false);
const form = reactive({ name: '', email: '', password: '' });

// Update card height for smooth form morphing
const updateHeight = () => {
  nextTick(() => {
    const activeEl = document.querySelector('.auth-card');
    if (activeEl) {
      containerHeight.value = activeEl.scrollHeight;
    }
  });
};

const toggleForm = (val) => {
  errorMsg.value = '';
  isLogin.value = val;
};

const handleSignup = async () => {
  authLoading.value = true;
  errorMsg.value = "";
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, form.email, form.password);
    await setDoc(doc(db, "users", userCredential.user.uid), {
      email: form.email,
      fullName: form.name,
      role: form.email.toLowerCase().includes('admin') ? 'Admin' : 'Member',
      createdAt: serverTimestamp()
    });
  } catch (err) { 
    errorMsg.value = err.message; 
  } finally { 
    authLoading.value = false; 
    updateHeight();
  }
};

const handleLogin = async () => {
  authLoading.value = true;
  errorMsg.value = "";
  try {
    await signInWithEmailAndPassword(auth, form.email, form.password);
  } catch (err) { 
    errorMsg.value = "Invalid login credentials."; 
  } finally { 
    authLoading.value = false; 
    updateHeight();
  }
};

const handleLogout = async () => {
  await signOut(auth);
  currentView.value = null;
};

onMounted(() => {
  // Simulate system check
  setTimeout(() => {
    isSystemLoading.value = false;
    nextTick(updateHeight);
  }, 1500);

  onAuthStateChanged(auth, (user) => {
    if (user) {
      // Delay to allow fade out to be visible if desired, 
      // but here we let the mode="out-in" handle the switch smoothly
      currentView.value = user.email.toLowerCase().includes('admin') ? 'admin' : 'user';
    } else {
      currentView.value = null;
    }
    updateHeight();
  });
});
</script>

<style>
/* FONT AND THEME */
.font-ios { 
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif; 
}

.ios-gradient-text { 
  background: linear-gradient(180deg, #FFFFFF 0%, #3F3F46 100%); 
  -webkit-background-clip: text; 
  -webkit-text-fill-color: transparent; 
}

/* ANIMATIONS: SYSTEM LOADER */
.loader-fade-leave-active { transition: opacity 0.8s ease; }
.loader-fade-leave-to { opacity: 0; }

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

/* FLOATING CIRCLES BACKGROUND */
.floating-circle { position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.15; animation: float 20s infinite alternate ease-in-out; }
.circle-1 { width: 500px; height: 500px; background: white; top: -100px; left: -100px; }
.circle-2 { width: 600px; height: 600px; background: #3f3f46; bottom: -200px; right: -100px; animation-duration: 25s; }
.circle-3 { width: 300px; height: 300px; background: white; top: 40%; left: 60%; animation-duration: 15s; }

@keyframes float {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(100px, 50px) scale(1.1); }
}

@keyframes blink {
  0%, 100% { opacity: 0.1; }
  50% { opacity: 1; transform: scale(1.5); }
}
.animate-blink { animation: blink 4s infinite ease-in-out; }

/* MODAL TRANSITION */
.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1); }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; transform: scale(1.05); }

/* FORM MORPH */
.form-morph-enter-active, .form-morph-leave-active { transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1); }
.form-morph-enter-from { opacity: 0; transform: translateY(20px) scale(0.98); filter: blur(10px); }
.form-morph-leave-to { opacity: 0; transform: translateY(-20px) scale(0.98); filter: blur(10px); }

/* PAGE SWAP (AUTH TO DASHBOARD) - This handles the smooth fade out */
.page-swap-enter-active {
  transition: opacity 1s cubic-bezier(0.23, 1, 0.32, 1);
}
.page-swap-leave-active {
  transition: all 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}
.page-swap-enter-from {
  opacity: 0;
}
.page-swap-leave-to {
  opacity: 0;
  transform: scale(0.95);
  filter: blur(15px);
}

@keyframes reveal { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-reveal { opacity: 0; animation: reveal 1s cubic-bezier(0.23, 1, 0.32, 1) forwards; }
</style>