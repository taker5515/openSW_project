import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAQv74D7OvPPU3wBuuQI51V3xpb8CsuDp8",
  authDomain: "ten-opso-project-id.firebaseapp.com",
  projectId: "ten-opso-project-id",
  storageBucket: "ten-opso-project-id.firebasestorage.app",
  messagingSenderId: "718383659879",
  appId: "1:718383659879:web:34539c7e57a244fcfb4dc2"
};


const app = getApps().length === 0
  ? initializeApp(firebaseConfig)
  : getApp();

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();