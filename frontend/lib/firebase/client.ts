import { getApps, initializeApp, type FirebaseOptions } from "firebase/app"
import { getAuth } from "firebase/auth"

const firebaseConfig: FirebaseOptions = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
}

if (!firebaseConfig.apiKey || !firebaseConfig.projectId) {
  throw new Error(
    "Firebase client config is missing. Copy .env.local.example to .env.local and fill in the NEXT_PUBLIC_FIREBASE_* values from your Firebase project settings."
  )
}

export const firebaseApp = getApps().length
  ? getApps()[0]!
  : initializeApp(firebaseConfig)

export const firebaseAuth = getAuth(firebaseApp)
