import React, { useState } from 'react';
import { Shield, Key, Mail, User, LogIn, UserPlus, Eye, EyeOff } from 'lucide-react';
import api from '../services/api';

export default function Login({ onLoginSuccess }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setLoading(true);

    try {
      if (isRegister) {
        await api.register(username, email, password, 'viewer');
        setSuccessMsg('Cadastro realizado com sucesso! Faça login.');
        setIsRegister(false);
        setPassword('');
      } else {
        const user = await api.login(username, password);
        onLoginSuccess(user);
      }
    } catch (err) {
      setError(err.message || 'Erro ao realizar operação.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 'calc(100vh - 64px)',
      padding: '2rem 1rem'
    }}>
      <div className="glass-card animate-fade-in" style={{
        width: '100%',
        maxWidth: '420px',
        padding: '2.5rem 2rem',
        border: '1px solid rgba(255, 255, 255, 0.08)'
      }}>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '2rem' }}>
          <div style={{
            background: 'rgba(59, 130, 246, 0.1)',
            border: '1px solid rgba(59, 130, 246, 0.2)',
            borderRadius: '12px',
            padding: '0.75rem',
            marginBottom: '1rem',
            color: 'var(--color-primary)',
            boxShadow: 'var(--glow-shadow)'
          }}>
            <Shield size={36} />
          </div>
          <h2 style={{ fontSize: '1.75rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            {isRegister ? 'Nova Conta' : 'Acesso ao Console'}
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', textAlign: 'center' }}>
            {isRegister 
              ? 'Crie sua credencial para visualizar a segurança dos ativos' 
              : 'Gestão Inteligente de Vulnerabilidades e Superfícies de Ataque'}
          </p>
        </div>

        {error && (
          <div style={{
            background: 'var(--color-danger-glow)',
            border: '1px solid var(--color-danger)',
            color: '#fca5a5',
            padding: '0.75rem 1rem',
            borderRadius: '8px',
            fontSize: '0.875rem',
            marginBottom: '1.25rem',
            textAlign: 'center'
          }}>
            {error}
          </div>
        )}

        {successMsg && (
          <div style={{
            background: 'var(--color-success-glow)',
            border: '1px solid var(--color-success)',
            color: '#6ee7b7',
            padding: '0.75rem 1rem',
            borderRadius: '8px',
            fontSize: '0.875rem',
            marginBottom: '1.25rem',
            textAlign: 'center'
          }}>
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <div style={{ position: 'relative' }}>
              <input
                id="username"
                type="text"
                placeholder="Ex: admin"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={{ paddingLeft: '2.5rem' }}
              />
              <User size={16} style={{
                position: 'absolute',
                left: '0.85rem',
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'var(--text-muted)'
              }} />
            </div>
          </div>

          {isRegister && (
            <div className="form-group">
              <label htmlFor="email">E-mail</label>
              <div style={{ position: 'relative' }}>
                <input
                  id="email"
                  type="email"
                  placeholder="seuemail@provedor.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  style={{ paddingLeft: '2.5rem' }}
                />
                <Mail size={16} style={{
                  position: 'absolute',
                  left: '0.85rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: 'var(--text-muted)'
                }} />
              </div>
            </div>
          )}

          <div className="form-group" style={{ marginBottom: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <label htmlFor="password" style={{ marginBottom: 0 }}>Senha</label>
            </div>
            <div style={{ position: 'relative' }}>
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ paddingLeft: '2.5rem', paddingRight: '2.5rem' }}
              />
              <Key size={16} style={{
                position: 'absolute',
                left: '0.85rem',
                top: '50%',
                transform: 'translateY(-50%)',
                color: 'var(--text-muted)'
              }} />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '0.5rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'transparent',
                  border: 'none',
                  padding: '4px',
                  color: 'var(--text-muted)',
                  cursor: 'pointer'
                }}
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="primary"
            disabled={loading}
            style={{ width: '100%', padding: '0.75rem', display: 'flex', justifyContent: 'center', marginBottom: '1.5rem' }}
          >
            {loading ? (
              'Processando...'
            ) : isRegister ? (
              <>
                <UserPlus size={18} /> Criar Conta
              </>
            ) : (
              <>
                <LogIn size={18} /> Entrar no Console
              </>
            )}
          </button>
        </form>

        <div style={{
          textAlign: 'center',
          borderTop: '1px solid var(--border-color)',
          paddingTop: '1.5rem',
          fontSize: '0.875rem',
          color: 'var(--text-secondary)'
        }}>
          {isRegister ? (
            <>
              Já possui uma credencial?{' '}
              <button
                onClick={() => { setIsRegister(false); setError(''); }}
                style={{ background: 'transparent', border: 'none', color: 'var(--color-primary)', display: 'inline', fontWeight: 600, padding: 0 }}
              >
                Entrar
              </button>
            </>
          ) : (
            <>
              Novo no console?{' '}
              <button
                onClick={() => { setIsRegister(true); setError(''); }}
                style={{ background: 'transparent', border: 'none', color: 'var(--color-primary)', display: 'inline', fontWeight: 600, padding: 0 }}
              >
                Cadastre-se
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
