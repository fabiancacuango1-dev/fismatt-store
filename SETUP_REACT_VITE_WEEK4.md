# 🚀 SETUP INICIAL: REACT + VITE + FIREBASE (SEMANA 4)

**Esta es la estructura que comenzaremos SEMANA 4 (11 de abril 2026)**

---

## 📋 PRE-REQUISITOS

Antes de empezar, tener instalado:

```bash
# 1. Node.js (v18+)
node --version
v18.x.x o superior

# 2. npm
npm --version
8.x.x o superior

# 3. Git
git --version
```

Si no tienes, descargar desde:
- Node.js: https://nodejs.org/ (Descargar LTS)
- Git: https://git-scm.com/

---

## 🎯 OBJETIVO SEMANA 4

Crear estructura:

```
fismatt-platform/
├── frontend/                 # App React (Vercel)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # Firebase Functions
│   └── functions/
│
└── docs/
    └── SETUP_GUIDE.md
```

---

## 🛠️ PASO 1: CREAR PROYECTO REACT

**En terminal, ejecutar:**

```bash
# 1. Navegar a donde quieras crear el proyecto
cd ~/Documents/

# 2. Crear proyecto React con Vite
npm create vite@latest fismatt-platform -- --template react

# 3. Entrar a carpeta
cd fismatt-platform

# 4. Instalar dependencias
npm install

# 5. Instalar Tailwind CSS (para estilos)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 6. Instalar Firebase
npm install firebase

# 7. Instalar React Router (para navegación)
npm install react-router-dom
```

---

## ⚙️ PASO 2: CONFIGURAR TAILWIND CSS

**Archivo: tailwind.config.js**

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1e40af",
        secondary: "#fbbf24",
        accent: "#006ba6",
      },
    },
  },
  plugins: [],
}
```

**Archivo: src/index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-50 text-gray-900;
}

.btn-primary {
  @apply bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition;
}
```

---

## 🔥 PASO 3: CREAR PROYECTO FIREBASE

1. Ir a: https://console.firebase.google.com/
2. Click "Create Project"
3. Nombre: `fismatt-platform`
4. Enable Google Analytics: **No**
5. Click "Continue"

Una vez creado:
1. Click "Web" (icono `</>``)
2. Nombre app: `fismatt-frontend`
3. Copiar configuración (la usaremos en siguiente paso)

---

## 🔑 PASO 4: CONFIGURAR CREDENCIALES FIREBASE

**Archivo: src/services/firebase.js** (CREAR)

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "TU_API_KEY",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123xyz"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Auth
export const auth = getAuth(app);

// Initialize Firestore
export const db = getFirestore(app);

export default app;
```

⚠️ **IMPORTANTE:** 
- Reemplazar `TU_API_KEY` y valores con los de tu proyecto Firebase
- NUNCA commitear esto a GitHub sin proteger variables

---

## 📁 PASO 5: CREAR ESTRUCTURA DE CARPETAS

```bash
# Desde dentro de fismatt-platform/

# Crear carpetas base
mkdir -p src/components/{Auth,Dashboard,Products,Common}
mkdir -p src/pages
mkdir -p src/services
mkdir -p src/context
mkdir -p src/hooks
mkdir -p public/images

# Crear archivos base
touch src/components/Auth/Login.jsx
touch src/components/Auth/Register.jsx
touch src/components/Dashboard/Dashboard.jsx
touch src/pages/Landing.jsx
touch src/pages/Home.jsx
touch src/context/AuthContext.jsx
touch src/hooks/useAuth.js
```

---

## 🎬 PASO 6: CREAR APP BÁSICA

**Archivo: src/App.jsx**

```jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Landing from './pages/Landing';
import Home from './pages/Home';
import Login from './components/Auth/Login';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Home />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
```

**Archivo: src/pages/Landing.jsx**

```jsx
import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-900 flex items-center justify-center">
      <div className="text-center text-white">
        <h1 className="text-5xl font-bold mb-4">FISMATT SYSTEMS</h1>
        <p className="text-xl mb-8">Soluciones Educativas Profesionales</p>
        <Link 
          to="/login" 
          className="btn-primary bg-yellow-400 text-blue-900 hover:bg-yellow-500"
        >
          Inicia sesión
        </Link>
      </div>
    </div>
  );
}
```

---

## 🔐 PASO 7: AUTENTICACIÓN BÁSICA

**Archivo: src/context/AuthContext.jsx**

```jsx
import { createContext, useState, useEffect } from 'react';
import { auth } from '../services/firebase';
import { onAuthStateChanged } from 'firebase/auth';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
```

**Archivo: src/hooks/useAuth.js**

```javascript
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe estar dentro de AuthProvider');
  }
  return context;
}
```

---

## ✅ VERIFICACIÓN INICIAL

Una vez hecho todo, ejecutar:

```bash
# Terminal 1: Dev server
npm run dev

# Debería mostrar:
# ➜  Local:   http://localhost:5173/
# ➜  Press h + enter to show help

# Ir a http://localhost:5173 en navegador
# Debería ver página con "FISMATT SYSTEMS"
```

---

## 🐛 TROUBLESHOOTING

**Problema: "CORS error"**
```
Solución: En firebase.js, agregar:
import { connectFunctionsEmulator } from 'firebase/functions';
```

**Problema: "Firebase is not defined"**
```
Solución: Verificar import en archivo
import { initializeApp } from 'firebase/app';
```

**Problema: "tailwind no se aplica"**
```
Solución: Reinicar servidor
npm run dev
```

---

## 📦 PASO 8: PREPARAR PARA PRODUCCIÓN (Semana 5+)

Cuando esté lista la app:

```bash
# Build para producción
npm run build

# Comprobar que genera carpeta dist/
ls -la dist/
```

---

## 🔗 RECURSOS

- React Docs: https://react.dev/
- Firebase Docs: https://firebase.google.com/docs
- Vite Docs: https://vitejs.dev/
- Tailwind CSS: https://tailwindcss.com/
- React Router: https://reactrouter.com/

---

## 📅 TIMELINE REALISTA (SEMANA 4-5)

```
LUNES (Semana 4):
  - Setup React + Vite ✅
  - Configurar Tailwind
  - Crear proyecto Firebase
  - Tiempo: 2-3 horas

MARTES-MIÉRCOLES (Semana 4):
  - Implementar rutas básicas
  - Context API setup
  - Página de landing mock
  - Tiempo: 4-5 horas

JUEVES-VIERNES (Semana 4):
  - Autenticación Firebase (Email + Google)
  - Página de login/register
  - Pruebas básicas
  - Tiempo: 5-6 horas

SEMANA 5:
  - Dashboard principal
  - Home page mejorada
  - Integraciones iniciales
  - Deploy a Vercel
```

---

## 🚀 DEPLOY A VERCEL (Semana 5)

```bash
# 1. Commitear a GitHub
git add .
git commit -m "Initial React setup"
git push

# 2. Ir a vercel.com
# 3. Click "New Project"
# 4. Conectar tu repositorio GitHub
# 5. Select "fismatt-platform" folder
# 6. Click "Deploy"
# ✅ App live en: fismatt-platform.vercel.app
```

---

## 📝 NOTAS IMPORTANTES

✅ Esta es estructura **DIY-friendly** (solo necesitas terminal + VS Code)  
✅ **Firebase free tier** soporta 10,000+ usuarios sin costo  
✅ **Vercel free tier** soporta unlimited deployments  
✅ **No necesitas backend separado** (Firebase lo hace todo)  
✅ **Puedes escalara completamente gratis** hasta 100k users

---

**¿LISTO PARA SEMANA 4?**

Confirma cuando termines testimonios y estaremos listos para React.

---

**Proximos pasos hoy (6 de abril):**
1. ✅ Arma lista de 7 contactos
2. ✅ Envía mensajes WhatsApp
3. ⏳ Espera respuestas (24-48h)

