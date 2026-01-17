import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCrdBvykX353xlUIc7XycqT6LOH53sf7es",
  authDomain: "aklatsystem.firebaseapp.com",
  projectId: "aklatsystem",
  storageBucket: "aklatsystem.firebasestorage.app",
  messagingSenderId: "980250524225",
  appId: "1:980250524225:web:47fe9ec960e756cc5324c0",
  measurementId: "G-GWN4K475GK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// I-export natin ang kailangan natin para sa Auth at Database
export const auth = getAuth(app);
export const db = getFirestore(app);