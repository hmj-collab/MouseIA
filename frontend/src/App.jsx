import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, LayoutDashboard, Globe, Shield, Database, 
  LogOut, User as UserIcon, Activity, Settings as SettingsIcon
} from 'lucide-react';

import api from './services/api';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Projects from './components/Projects';
import Scans from './components/Scans';
import SignalsFindings from './components/SignalsFindings';
import Vulnerabilities from './components/Vulnerabilities';
import Settings from './components/Settings';

function App() {
  const [user, setUser] = useState(null);
  const [currentTab, setCurrentTab] = useState('dashboard'); // 'dashboard', 'projects', 'scans', 'signals', 'vulnerabilities'
  const [checkingAuth, setCheckingAuth] = useState(true);

  // Check auth state on mount
  useEffect(() => {
    const currentUser = api.getCurrentUser();
    if (currentUser) {
      setUser(currentUser);
    }
    setCheckingAuth(false);

    // Handle token expiration/401 global failures
    const handleAuthFailed = () => {
      setUser(null);
      setCurrentTab('dashboard');
    };

    window.addEventListener('auth-failed', handleAuthFailed);
    return () => {
      window.removeEventListener('auth-failed', handleAuthFailed);
    };
  }, []);

  const handleLoginSuccess = (loggedInUser) => {
    setUser(loggedInUser);
    setCurrentTab('dashboard');
  };

  const handleLogout = () => {
    api.logout();
    setUser(null);
    setCurrentTab('dashboard');
  };

  if (checkingAuth) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'var(--bg-primary)' }}>
        <div style={{ color: 'var(--text-secondary)' }}>Carregando Console de Segurança...</div>
      </div>
    );
  }

  // Renders the login screen if the user is not authenticated
  if (!user) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Header bar */}
      <header className="app-header">
        <a href="#" className="logo" onClick={() => setCurrentTab('dashboard')}>
          <ShieldAlert size={22} style={{ color: 'var(--color-primary)' }} />
          <span>Mouse <span>IA</span></span>
        </a>

        {/* Desktop Navigation */}
        <nav className="nav-links">
          <button 
            className={`nav-item ${currentTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentTab('dashboard')}
          >
            <LayoutDashboard size={16} /> Dashboard
          </button>
          <button 
            className={`nav-item ${currentTab === 'projects' ? 'active' : ''}`}
            onClick={() => setCurrentTab('projects')}
          >
            <Globe size={16} /> Escopo
          </button>
          <button 
            className={`nav-item ${currentTab === 'scans' ? 'active' : ''}`}
            onClick={() => setCurrentTab('scans')}
          >
            <Shield size={16} /> Varreduras
          </button>
          <button 
            className={`nav-item ${currentTab === 'signals' ? 'active' : ''}`}
            onClick={() => setCurrentTab('signals')}
          >
            <Database size={16} /> Sinais e Achados
          </button>
          <button 
            className={`nav-item ${currentTab === 'vulnerabilities' ? 'active' : ''}`}
            onClick={() => setCurrentTab('vulnerabilities')}
          >
            <ShieldAlert size={16} /> Vulnerabilidades
          </button>
          {user && user.role === 'admin' && (
            <button 
              className={`nav-item ${currentTab === 'settings' ? 'active' : ''}`}
              onClick={() => setCurrentTab('settings')}
            >
              <SettingsIcon size={16} /> Configurações
            </button>
          )}
        </nav>

        {/* User context menu */}
        <div className="user-menu">
          <div className="user-info">
            <div className="user-name" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <UserIcon size={12} style={{ color: 'var(--color-primary)' }} />
              {user.username}
            </div>
            <div className="user-role">{user.role.toUpperCase()}</div>
          </div>
          
          <button 
            className="secondary"
            onClick={handleLogout}
            style={{ padding: '0.45rem 0.85rem', fontSize: '0.75rem', display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            <LogOut size={14} /> Sair
          </button>
        </div>
      </header>

      {/* Main Console Content */}
      <main style={{ flex: 1, width: '100%', maxWidth: '1280px', margin: '0 auto', padding: '0 2rem' }}>
        {currentTab === 'dashboard' && (
          <Dashboard user={user} onNavigate={setCurrentTab} />
        )}
        {currentTab === 'projects' && (
          <Projects user={user} />
        )}
        {currentTab === 'scans' && (
          <Scans user={user} />
        )}
        {currentTab === 'signals' && (
          <SignalsFindings user={user} />
        )}
        {currentTab === 'vulnerabilities' && (
          <Vulnerabilities user={user} />
        )}
        {currentTab === 'settings' && (
          <Settings user={user} />
        )}
      </main>

      {/* Footer */}
      <footer style={{
        textAlign: 'center',
        padding: '2rem 0',
        fontSize: '0.75rem',
        color: 'var(--text-muted)',
        borderTop: '1px solid var(--border-color)',
        marginTop: '3rem'
      }}>
        Mouse IA Console &copy; 2026 - Gestão Avançada de Vulnerabilidades.
      </footer>
    </div>
  );
}

export default App;
