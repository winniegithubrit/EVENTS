// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCJhsFT2JVmefSjAM8Wml5rrAM6W1uuUyY",
  authDomain: "events-planner-1ea45.firebaseapp.com",
  projectId: "events-planner-1ea45",
  storageBucket: "events-planner-1ea45.appspot.com",
  messagingSenderId: "543441083389",
  appId: "1:543441083389:web:fd55145c24ee62251c9794",
  measurementId: "G-HQC7ZLLXMB"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// npm install -g firebase-tools
// npm install firebase