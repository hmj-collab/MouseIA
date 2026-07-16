import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { 
  Play, RefreshCw, Trash2, Database, ShieldAlert, Plus, X, Globe,
  Shield, CheckCircle, Clock, AlertTriangle, ExternalLink
} from 'lucide-react';
import api from '../services/api';

export default function Scans({ user }) {
  const isAdmin = user && user.role === 'admin';
  const [loading, setLoading] = useState(true);
  
  // Data States
  const [assets, setAssets] = useState([]);
  const [scans, setScans] = useState([]);
  const [sites, setSites] = useState([]);
  const [companies, setCompanies] = useState([]);

  // Modals / Forms States
  const [showAssetModal, setShowAssetModal] = useState(false);
  const [assetForm, setAssetForm] = useState({ id: null, name: '', asset_type: 'url', value: '', description: '', company_id: '', site_id: '' });

  const [showScanModal, setShowScanModal] = useState(false);
  const [scanForm, setScanForm] = useState({ id: null, scan_type: 'wordpress', description: '', asset_id: '', site_id: '' });

  const [activeTab, setActiveTab] = useState('scans'); // 'scans' or 'assets'
  const [error, setError] = useState('');
  const [runningScans, setRunningScans] = useState({}); // Track currently running scan executions

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [assetsData, scansData, sitesData, companiesData] = await Promise.all([
        api.getAssets(),
        api.getScans(),
        api.getSites(),
        api.getCompanies()
      ]);
      setAssets(assetsData);
      setScans(scansData);
      setSites(sitesData);
      setCompanies(companiesData);
    } catch (err) {
      setError('Erro ao carregar dados do console.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Asset handlers
  const handleAssetSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const payload = {
        name: assetForm.name,
        asset_type: assetForm.asset_type,
        value: assetForm.value,
        description: assetForm.description || null,
        company_id: assetForm.company_id ? Number(assetForm.company_id) : null,
        site_id: assetForm.site_id ? Number(assetForm.site_id) : null,
        is_active: true
      };

      if (assetForm.id) {
        await api.updateAsset(assetForm.id, payload);
      } else {
        await api.createAsset(payload);
      }
      setShowAssetModal(false);
      loadData();
    } catch (err) {
      setError(err.message || 'Erro ao salvar ativo.');
    }
  };

  const handleEditAsset = (asset) => {
    setAssetForm({
      id: asset.id,
      name: asset.name,
      asset_type: asset.asset_type,
      value: asset.value,
      description: asset.description || '',
      company_id: asset.company_id || '',
      site_id: asset.site_id || ''
    });
    setShowAssetModal(true);
  };

  const handleDeleteAsset = async (id) => {
    if (!window.confirm('Deseja realmente remover este ativo? Scans associados podem falhar.')) return;
    try {
      await api.deleteAsset(id);
      loadData();
    } catch (err) {
      alert(err.message || 'Erro ao deletar ativo.');
    }
  };

  // Scan handlers
  const handleScanSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const payload = {
        scan_type: scanForm.scan_type,
        status: 'pending',
        description: scanForm.description || null,
        asset_id: scanForm.asset_id ? Number(scanForm.asset_id) : null,
        site_id: scanForm.site_id ? Number(scanForm.site_id) : null
      };

      await api.createScan(payload);
      setShowScanModal(false);
      loadData();
    } catch (err) {
      setError(err.message || 'Erro ao agendar varredura.');
    }
  };

  const handleLaunchScan = async (scanId) => {
    setError('');
    setRunningScans(prev => ({ ...prev, [scanId]: true }));
    try {
      await api.launchScan(scanId);
      loadData();
    } catch (err) {
      setError(`Erro ao executar varredura #${scanId}: ` + (err.message || 'Erro de conexão.'));
    } finally {
      setRunningScans(prev => {
        const copy = { ...prev };
        delete copy[scanId];
        return copy;
      });
    }
  };

  const handleDeleteScan = async (id) => {
    if (!window.confirm('Tem certeza de que deseja remover o histórico desta varredura?')) return;
    try {
      await api.deleteScan(id);
      loadData();
    } catch (err) {
      alert(err.message || 'Erro ao remover varredura.');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div style={{ color: 'var(--text-secondary)' }}>Carregando infraestrutura de scans...</div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.25rem' }}>Varreduras e Ativos</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Monitore a infraestrutura técnica e execute testes automatizados de vulnerabilidades.
          </p>
        </div>

        {isAdmin && (
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button className="primary" onClick={() => {
              setScanForm({ id: null, scan_type: 'wordpress', description: '', asset_id: '', site_id: '' });
              setShowScanModal(true);
            }}>
              <Play size={18} style={{ transform: 'rotate(0deg)' }} /> Executar Novo Scan
            </button>
            <button className="secondary" onClick={() => {
              setAssetForm({ id: null, name: '', asset_type: 'url', value: '', description: '', company_id: '', site_id: '' });
              setShowAssetModal(true);
            }}>
              <Plus size={18} /> Novo Ativo
            </button>
          </div>
        )}
      </div>

      {error && (
        <div style={{
          background: 'var(--color-danger-glow)',
          border: '1px solid var(--color-danger)',
          color: '#fca5a5',
          padding: '0.75rem 1rem',
          borderRadius: '8px',
          fontSize: '0.875rem',
          marginBottom: '1.5rem'
        }}>
          {error}
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid var(--border-color)', marginBottom: '1.5rem', paddingBottom: '1px' }}>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'scans' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('scans')}
        >
          <Shield size={18} /> Varreduras ({scans.length})
        </button>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'assets' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('assets')}
        >
          <Database size={18} /> Ativos Digitais ({assets.length})
        </button>
      </div>

      {activeTab === 'scans' ? (
        /* SCANS LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {scans.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhuma varredura agendada ou executada ainda.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Tipo</th>
                    <th>Alvo</th>
                    <th>Status</th>
                    <th>Executado em</th>
                    <th>Descrição / Logs</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {scans.map(scan => {
                    const site = sites.find(s => s.id === scan.site_id);
                    const asset = assets.find(a => a.id === scan.asset_id);
                    const targetName = site ? `Site: ${site.name}` : asset ? `Ativo: ${asset.name}` : 'Nenhum';
                    const targetVal = site ? site.url : asset ? asset.value : null;

                    const isRunning = runningScans[scan.id];

                    return (
                      <tr key={scan.id}>
                        <td style={{ color: 'var(--text-muted)', fontWeight: 600 }}>#{scan.id}</td>
                        <td style={{ fontWeight: 600 }}>
                          <span className="badge info">{scan.scan_type}</span>
                        </td>
                        <td>
                          <div>
                            <div style={{ fontWeight: 500 }}>{targetName}</div>
                            {targetVal && (
                              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                {targetVal} <ExternalLink size={10} />
                              </div>
                            )}
                          </div>
                        </td>
                        <td>
                          <span className={`badge ${
                            scan.status === 'completed' ? 'success' : 
                            scan.status === 'running' ? 'info' : 
                            scan.status === 'failed' ? 'high' : 'medium'
                          }`} style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                            {scan.status === 'completed' && <CheckCircle size={10} />}
                            {scan.status === 'running' && <Clock size={10} />}
                            {scan.status === 'failed' && <AlertTriangle size={10} />}
                            {scan.status}
                          </span>
                        </td>
                        <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                          {scan.started_at ? new Date(scan.started_at).toLocaleString() : <span style={{ color: 'var(--text-muted)' }}>Pendente</span>}
                        </td>
                        <td style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {scan.description || <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Sem logs</span>}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            {isAdmin && (
                              <button 
                                className="primary" 
                                style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem' }} 
                                onClick={() => handleLaunchScan(scan.id)}
                                disabled={isRunning || scan.status === 'running'}
                              >
                                {isRunning ? (
                                  <RefreshCw size={12} className="spin" style={{ animation: 'spin 1s linear infinite' }} />
                                ) : (
                                  <Play size={12} />
                                )}
                                Iniciar
                              </button>
                            )}
                            {isAdmin && (
                              <button 
                                className="secondary" 
                                style={{ padding: '0.4rem', color: 'var(--color-danger)' }} 
                                onClick={() => handleDeleteScan(scan.id)}
                              >
                                <Trash2 size={14} />
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : (
        /* ASSETS LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {assets.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhum ativo técnico registrado ainda.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Tipo</th>
                    <th>Valor do Ativo</th>
                    <th>Site Relacionado</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {assets.map(asset => {
                    const site = sites.find(s => s.id === asset.site_id);
                    return (
                      <tr key={asset.id}>
                        <td style={{ fontWeight: 600 }}>{asset.name}</td>
                        <td>
                          <span className="badge info">{asset.asset_type}</span>
                        </td>
                        <td style={{ fontFamily: 'monospace', color: 'var(--text-secondary)' }}>
                          {asset.value}
                        </td>
                        <td>
                          {site ? (
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <Globe size={14} style={{ color: 'var(--text-muted)' }} /> {site.name}
                            </span>
                          ) : (
                            <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Nenhum</span>
                          )}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="secondary" style={{ padding: '0.4rem' }} onClick={() => handleEditAsset(asset)}>
                              <Trash2 size={14} style={{ display: 'none' }} /> Editar
                            </button>
                            {isAdmin && (
                              <button className="secondary" style={{ padding: '0.4rem', color: 'var(--color-danger)' }} onClick={() => handleDeleteAsset(asset.id)}>
                                <Trash2 size={14} />
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ASSET MODAL */}
      {showAssetModal && createPortal(
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <div className="glass-card animate-fade-in" style={{
            width: '100%', maxWidth: '500px', padding: '2rem', border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>
                {assetForm.id ? 'Editar Ativo' : 'Adicionar Novo Ativo'}
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setShowAssetModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleAssetSubmit}>
              <div className="form-group">
                <label>Nome do Ativo</label>
                <input
                  type="text"
                  placeholder="Ex: Servidor de Homologação"
                  value={assetForm.name}
                  onChange={(e) => setAssetForm({ ...assetForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Tipo de Ativo</label>
                <select
                  value={assetForm.asset_type}
                  onChange={(e) => setAssetForm({ ...assetForm, asset_type: e.target.value })}
                >
                  <option value="url">URL (Endereço Web)</option>
                  <option value="domain">Domínio / DNS</option>
                  <option value="ip">IP / Endpoint Técnico</option>
                  <option value="host">Host / Servidor</option>
                  <option value="other">Outro</option>
                </select>
              </div>

              <div className="form-group">
                <label>Valor (IP/URL/Domínio)</label>
                <input
                  type="text"
                  placeholder="Ex: 192.168.1.100 ou api.meusite.com"
                  value={assetForm.value}
                  onChange={(e) => setAssetForm({ ...assetForm, value: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Empresa Relacionada</label>
                <select
                  value={assetForm.company_id}
                  onChange={(e) => setAssetForm({ ...assetForm, company_id: e.target.value })}
                >
                  <option value="">-- Nenhuma --</option>
                  {companies.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Site Relacionado</label>
                <select
                  value={assetForm.site_id}
                  onChange={(e) => setAssetForm({ ...assetForm, site_id: e.target.value })}
                >
                  <option value="">-- Nenhum --</option>
                  {sites.map(s => (
                    <option key={s.id} value={s.id}>{s.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Descrição</label>
                <textarea
                  rows="3"
                  placeholder="Informações adicionais do ativo..."
                  value={assetForm.description}
                  onChange={(e) => setAssetForm({ ...assetForm, description: e.target.value })}
                ></textarea>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem' }}>
                <button type="button" className="secondary" onClick={() => setShowAssetModal(false)}>Cancelar</button>
                <button type="submit" className="primary">Salvar</button>
              </div>
            </form>
          </div>
        </div>,
        document.body
      )}

      {/* SCAN MODAL */}
      {showScanModal && createPortal(
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <div className="glass-card animate-fade-in" style={{
            width: '100%', maxWidth: '500px', padding: '2rem', border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>
                Agendar Nova Varredura
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setShowScanModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleScanSubmit}>
              <div className="form-group">
                <label>Tipo de Varredura</label>
                <select
                  value={scanForm.scan_type}
                  onChange={(e) => setScanForm({ ...scanForm, scan_type: e.target.value })}
                >
                  <option value="wordpress">WordPress Analysis (Security Headers & WP Version)</option>
                  <option value="headers">HTTP Security Headers Check</option>
                  <option value="port-scan">Port Scanning (Basic)</option>
                  <option value="tls-ssl">TLS/SSL Configuration Check</option>
                </select>
              </div>

              <div style={{ borderTop: '1px solid var(--border-color)', margin: '1.5rem 0', paddingTop: '1rem' }}>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                  Escolha um Site **OU** um Ativo para ser o alvo do escopo desta varredura:
                </p>
                
                <div className="form-group">
                  <label>Alvo: Site</label>
                  <select
                    value={scanForm.site_id}
                    disabled={scanForm.asset_id !== ''}
                    onChange={(e) => setScanForm({ ...scanForm, site_id: e.target.value })}
                  >
                    <option value="">-- Escolher Site --</option>
                    {sites.map(s => (
                      <option key={s.id} value={s.id}>{s.name} ({s.url})</option>
                    ))}
                  </select>
                </div>

                <div style={{ textAlign: 'center', margin: '0.5rem 0', color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>OU</div>

                <div className="form-group">
                  <label>Alvo: Ativo Técnico</label>
                  <select
                    value={scanForm.asset_id}
                    disabled={scanForm.site_id !== ''}
                    onChange={(e) => setScanForm({ ...scanForm, asset_id: e.target.value })}
                  >
                    <option value="">-- Escolher Ativo --</option>
                    {assets.map(a => (
                      <option key={a.id} value={a.id}>{a.name} ({a.value})</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Descrição / Meta</label>
                <textarea
                  rows="3"
                  placeholder="Objetivos do scan..."
                  value={scanForm.description}
                  onChange={(e) => setScanForm({ ...scanForm, description: e.target.value })}
                ></textarea>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem' }}>
                <button type="button" className="secondary" onClick={() => setShowScanModal(false)}>Cancelar</button>
                <button type="submit" className="primary">Confirmar Agendamento</button>
              </div>
            </form>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
}
