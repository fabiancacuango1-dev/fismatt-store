╔════════════════════════════════════════════════════════════════════════════════╗
║                    💻 GUÍA DE IMPLEMENTACIÓN — PASO 1 💻                      ║
║                     Setup del Proyecto React + Firebase                       ║
╚════════════════════════════════════════════════════════════════════════════════╝


════════════════════════════════════════════════════════════════════════════════
                         PRE-REQUISITOS
════════════════════════════════════════════════════════════════════════════════

Necesitas tenerinstallado:

✅ Node.js v18+ (npm o yarn)
✅ Git
✅ Cuenta en Firebase (gratuita en https://firebase.google.com)
✅ Cuenta en Vercel (gratuita en https://vercel.com)


════════════════════════════════════════════════════════════════════════════════
                         PASO 1: CREAR PROYECTO REACT + VITE
════════════════════════════════════════════════════════════════════════════════

En terminal:

cd ~
npm create vite@latest fismatt-app -- --template react
cd fismatt-app


Proyecto creado con estructura:

fismatt-app/
├── public/
├── src/
│  ├── App.jsx
│  ├── App.css
│  ├── main.jsx
│  └── index.css
├── package.json
├── vite.config.js
└── .gitignore

Instalar dependencias:

npm install

# Base:
npm install react-router-dom@latest
npm install -D tailwindcss postcss autoprefixer
npm install firebase
npm install zustand (alternativa a Context si prefieres)
npm install @headlessui/react


════════════════════════════════════════════════════════════════════════════════
                         PASO 2: CONFIGURAR TAILWIND CSS
════════════════════════════════════════════════════════════════════════════════

Inicializar Tailwind:

npx tailwindcss init -p

Editar tailwind.config.js:

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1e40af',
        'primary-dark': '#1e3a8a',
        secondary: '#fbbf24',
        accent: '#006ba6',
        dark: '#0f172a',
        'dark-light': '#1e293b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

Editar src/index.css:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
  @apply antialiased;
}

html {
  @apply scroll-smooth;
}

body {
  @apply bg-dark text-white;
}
```


════════════════════════════════════════════════════════════════════════════════
                         PASO 3: CONFIGURAR FIREBASE
════════════════════════════════════════════════════════════════════════════════

1. Ve a https://console.firebase.google.com
2. Click "Crear proyecto"
3. Nombre: "fismatt-saas"
4. Desactiva Google Analytics
5. Click "Crear proyecto"

Espera a que se cree, luego:

6. Click en el proyecto
7. Va a Settings (engranaje)
8. Ve a pestaña "Tus apps"
9. Click "Agregar app" → Web
10. Nombre: "fismatt-app"
11. Click "Registrar app"

Te dará config tipo:

```javascript
const firebaseConfig = {
  apiKey: "AIz...",
  authDomain: "fismatt-saas.firebaseapp.com",
  projectId: "fismatt-saas",
  storageBucket: "fismatt-saas.appspot.com",
  messagingSenderId: "...",
  appId: "...",
  measurementId: "..."
};
```

GUARDA ESTA CONFIG


════════════════════════════════════════════════════════════════════════════════
                         PASO 4: CREAR ARCHIVO FIREBASE
════════════════════════════════════════════════════════════════════════════════

Crear: src/services/firebase.js

```javascript
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey: "TU_API_KEY",
  authDomain: "fismatt-saas.firebaseapp.com",
  projectId: "fismatt-saas",
  storageBucket: "fismatt-saas.appspot.com",
  messagingSenderId: "TU_SENDER_ID",
  appId: "TU_APP_ID",
  measurementId: "TU_MEASUREMENT_ID"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);

// Servicios
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);

export default app;
```

⚠️ IMPORTANTE: NUNCA commites claves reales a Git
Usa .env:

Crear .env:

```
VITE_FIREBASE_API_KEY=TU_API_KEY
VITE_FIREBASE_AUTH_DOMAIN=fismatt-saas.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=fismatt-saas
VITE_FIREBASE_STORAGE_BUCKET=fismatt-saas.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=TU_SENDER_ID
VITE_FIREBASE_APP_ID=TU_APP_ID
VITE_FIREBASE_MEASUREMENT_ID=TU_MEASUREMENT_ID
```

Luego editar firebase.js para usar variables:

```javascript
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
};
```

Agregar .env a .gitignore (ya debe estar)


════════════════════════════════════════════════════════════════════════════════
                         PASO 5: CREAR CONTEXT PARA AUTENTICACIÓN
════════════════════════════════════════════════════════════════════════════════

Crear: src/context/AuthContext.jsx

```javascript
import { createContext, useState, useEffect } from 'react';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { auth } from '../services/firebase';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    }, (err) => {
      setError(err.message);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const logout = async () => {
    try {
      await signOut(auth);
      setUser(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

Crear hook: src/hooks/useAuth.js

```javascript
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  return context;
}
```


════════════════════════════════════════════════════════════════════════════════
                         PASO 6: CREAR RUTAS BÁSICAS
════════════════════════════════════════════════════════════════════════════════

Crear: src/App.jsx

```javascript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';

// Páginas públicas
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';

// Páginas privadas
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Profile from './pages/Profile';

// Componentes
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <div className="flex items-center justify-center h-screen">Cargando...</div>;
  if (!user) return <Navigate to="/login" />;

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Rutas públicas */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Rutas privadas */}
          <Route
            path="/app/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/app/productos"
            element={
              <ProtectedRoute>
                <Products />
              </ProtectedRoute>
            }
          />
          <Route
            path="/app/perfil"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />

          {/* 404 */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
```


════════════════════════════════════════════════════════════════════════════════
                         PASO 7: CREAR LANDING PAGE BÁSICA
════════════════════════════════════════════════════════════════════════════════

Crear: src/pages/Landing.jsx

```javascript
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-b from-dark to-dark-light">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 w-full z-50 bg-dark/80 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">FS</span>
            </div>
            <span className="text-xl font-bold text-white">FISMATT</span>
          </div>

          <div className="flex gap-4">
            {user ? (
              <>
                <Link to="/app/dashboard" className="px-4 py-2 text-white hover:text-secondary transition">
                  Dashboard
                </Link>
              </>
            ) : (
              <>
                <Link to="/login" className="px-4 py-2 text-white hover:text-secondary transition">
                  Iniciar sesión
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition"
                >
                  Registrarse
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero */}
      <div className="pt-32 pb-20 px-4 text-center">
        <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white">
          Gestión Educativa Inteligente
        </h1>
        <p className="text-xl text-gray-400 mb-8">
          Plataforma centralizada para docentes ecuatorianos. Evalúa, gestiona y optimiza tu trabajo académico.
        </p>

        {!user && (
          <Link
            to="/register"
            className="inline-block px-8 py-3 bg-gradient-to-r from-primary to-accent text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-primary/50 transition"
          >
            Comienza Gratis
          </Link>
        )}
      </div>

      {/* Características */}
      <div className="max-w-7xl mx-auto px-4 py-20 grid md:grid-cols-3 gap-8">
        <div className="p-6 border border-primary/20 rounded-xl hover:border-primary/50 transition">
          <h3 className="text-xl font-bold mb-2">INEVAL-PRO</h3>
          <p className="text-gray-400">Preparación completa para la evaluación docente 2026</p>
        </div>
        <div className="p-6 border border-secondary/20 rounded-xl hover:border-secondary/50 transition">
          <h3 className="text-xl font-bold mb-2">Minduc</h3>
          <p className="text-gray-400">Importación y gestión de calificaciones automática</p>
        </div>
        <div className="p-6 border border-accent/20 rounded-xl hover:border-accent/50 transition">
          <h3 className="text-xl font-bold mb-2">EduHorarios</h3>
          <p className="text-gray-400">Gestión intelligent de horarios y disponibilidad</p>
        </div>
      </div>
    </div>
  );
}
```


════════════════════════════════════════════════════════════════════════════════
                         PASO 8: PROBAR LOCALMENTE
════════════════════════════════════════════════════════════════════════════════

npm run dev

Se abrirá en http://localhost:5173

Deberías ver:
- Landing page
- Navbar con links de login/register
- Botón "Comienza Gratis"
- Cards de productos


════════════════════════════════════════════════════════════════════════════════
                         PRÓXIMO PASO: Crear Login y Register
════════════════════════════════════════════════════════════════════════════════

Lo haremos en el próximo documento: IMPLEMENTACION_PASO_2_AUTH.md

Continuaremos con:
□ Página de Login
□ Página de Registro
□ Gestión de contraseñas
□ Google Sign-In
□ Validaciones
□ Error handling


════════════════════════════════════════════════════════════════════════════════

CHECKLIST DE ESTE PASO:

□ Node.js v18+ instalado
□ Proyecto React creado con Vite
□ Tailwind CSS configurado
□ Firebase project creado
□ Configuración Firebase en .env
□ AuthContext creado
□ Rutas básicas funcionando
□ Landing page visible en localhost:5173

Si todo está ✅, pasamos al PASO 2: Autenticación

════════════════════════════════════════════════════════════════════════════════
