import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { ShieldAlert, AlertTriangle, AlertCircle, RefreshCw, Server, HelpCircle, Eye } from 'lucide-react';
import api from '../services/api';

export default function SignalsFindings({ user }) {
  const [loading, setLoading] = useState(true);
  const [signals, setSignals] = useState([]);
  const [findings, setFindings] = useState([]);
  const [sites, setSites] = useState([]);

  // Filtering / Tabs
  const [activeTab, setActiveTab] = useState('findings'); // 'findings' or 'signals'
  const [severityFilter, setSeverityFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Selected Detail Modal
  const [selectedItem, setSelectedItem] = useState(null);
  const [selectedType, setSelectedType] = useState(''); // 'signal' or 'finding'

  const loadData = async () => {
    setLoading(true);
    try {
      const [signalsData, findingsData, sitesData] = await Promise.all([
        api.getSignals(),
        api.getFindings(),
        api.getSites()
      ]);
      setSignals(signalsData);
      setFindings(findingsData);
      setSites(sitesData);
    } catch (err) {
      console.error("Erro ao carregar sinais e achados", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getSeverityIcon = (sev) => {
    const s = (sev || 'info').toLowerCase();
    if (s === 'critical' || s === 'high') return <AlertOctagon size={16} style={{ color: 'var(--color-danger)' }} />;
    if (s === 'medium') return <AlertTriangle size={16} style={{ color: 'var(--color-warning)' }} />;
    return <AlertCircle size={16} style={{ color: 'var(--color-primary)' }} />;
  };

  const getSiteName = (siteId) => {
    if (!siteId) return 'Nenhum';
    const site = sites.find(s => s.id === siteId);
    return site ? site.name : `Site #${siteId}`;
  };

  // Filter lists
  const filteredFindings = findings.filter(f => {
    const matchSev = severityFilter ? (f.severity || '').toLowerCase() === severityFilter.toLowerCase() : true;
    const matchStatus = statusFilter ? (f.status || '').toLowerCase() === statusFilter.toLowerCase() : true;
    return matchSev && matchStatus;
  });

  const filteredSignals = signals.filter(s => {
    const matchSev = severityFilter ? (s.severity || '').toLowerCase() === severityFilter.toLowerCase() : true;
    return matchSev;
  });

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div style={{ color: 'var(--text-secondary)' }}>Carregando dados de ameaças...</div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.25rem' }}>Análise de Ameaças</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Consulte a lista detalhada de eventos de segurança detectados e achados estruturados.
          </p>
        </div>
        <button className="secondary" onClick={loadData}>
          <RefreshCw size={14} /> Atualizar
        </button>
      </div>

      {/* Filter Toolbar */}
      <div className="glass-card" style={{ padding: '1.25rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Filtrar:</span>
        </div>
        
        {/* Severity filter */}
        <div style={{ minWidth: '150px' }}>
          <select 
            value={severityFilter} 
            onChange={(e) => setSeverityFilter(e.target.value)}
            style={{ padding: '0.45rem', fontSize: '0.8rem' }}
          >
            <option value="">-- Severidade --</option>
            <option value="critical">Crítica</option>
            <option value="high">Alta</option>
            <option value="medium">Média</option>
            <option value="low">Baixa</option>
            <option value="info">Informativa</option>
          </select>
        </div>

        {/* Status filter (only for Findings) */}
        {activeTab === 'findings' && (
          <div style={{ minWidth: '150px' }}>
            <select 
              value={statusFilter} 
              onChange={(e) => setStatusFilter(e.target.value)}
              style={{ padding: '0.45rem', fontSize: '0.8rem' }}
            >
              <option value="">-- Status --</option>
              <option value="open">Aberto (Open)</option>
              <option value="mitigated">Mitigado (Mitigated)</option>
              <option value="accepted">Aceito (Accepted)</option>
              <option value="resolved">Resolvido (Resolved)</option>
            </select>
          </div>
        )}

        {(severityFilter || statusFilter) && (
          <button 
            className="secondary" 
            style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem', border: 'none' }}
            onClick={() => { setSeverityFilter(''); setStatusFilter(''); }}
          >
            Limpar Filtros
          </button>
        )}
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid var(--border-color)', marginBottom: '1.5rem', paddingBottom: '1px' }}>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'findings' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('findings')}
        >
          <ShieldAlert size={18} /> Achados Estruturados ({filteredFindings.length})
        </button>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'signals' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('signals')}
        >
          <Server size={18} /> Sinais Brutos ({filteredSignals.length})
        </button>
      </div>

      {activeTab === 'findings' ? (
        /* FINDINGS LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {filteredFindings.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhum achado estruturado encontrado para os filtros atuais.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>Título</th>
                    <th>Descrição</th>
                    <th>Severidade</th>
                    <th>Status</th>
                    <th>Sinal Vinculado</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFindings.map(finding => (
                    <tr key={finding.id}>
                      <td style={{ fontWeight: 600, maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {finding.title}
                      </td>
                      <td style={{ color: 'var(--text-secondary)', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {finding.description || <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Sem descrição</span>}
                      </td>
                      <td>
                        <span className={`badge ${(finding.severity || 'info').toLowerCase()}`}>
                          {finding.severity}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${
                          finding.status === 'resolved' || finding.status === 'mitigated' ? 'success' : 
                          finding.status === 'accepted' ? 'info' : 'high'
                        }`}>
                          {finding.status}
                        </span>
                      </td>
                      <td style={{ color: 'var(--text-muted)' }}>
                        {finding.signal_id ? `Sinal #${finding.signal_id}` : 'Manual/Nenhum'}
                      </td>
                      <td>
                        <button className="secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem' }} onClick={() => {
                          setSelectedItem(finding);
                          setSelectedType('finding');
                        }}>
                          <Eye size={12} /> Detalhes
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : (
        /* SIGNALS LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {filteredSignals.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhum sinal bruto encontrado para os filtros atuais.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Origem</th>
                    <th>Tipo</th>
                    <th>Descrição</th>
                    <th>Severidade</th>
                    <th>Confiança</th>
                    <th>Site Alvo</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSignals.map(signal => (
                    <tr key={signal.id}>
                      <td style={{ color: 'var(--text-muted)', fontWeight: 600 }}>#{signal.id}</td>
                      <td>
                        <span className="badge info">{signal.source}</span>
                      </td>
                      <td style={{ fontFamily: 'monospace', fontWeight: 500 }}>{signal.signal_type}</td>
                      <td style={{ color: 'var(--text-secondary)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {signal.description}
                      </td>
                      <td>
                        <span className={`badge ${(signal.severity || 'info').toLowerCase()}`}>
                          {signal.severity}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span style={{ fontWeight: 600 }}>{signal.confidence}%</span>
                          <div style={{ width: '40px', height: '4px', background: 'rgba(255,255,255,0.05)', borderRadius: '2px', overflow: 'hidden' }}>
                            <div style={{ width: `${signal.confidence}%`, height: '100%', background: 'var(--color-success)' }}></div>
                          </div>
                        </div>
                      </td>
                      <td>{getSiteName(signal.site_id)}</td>
                      <td>
                        <button className="secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem' }} onClick={() => {
                          setSelectedItem(signal);
                          setSelectedType('signal');
                        }}>
                          <Eye size={12} /> Detalhes
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* DETAIL MODAL */}
      {selectedItem && createPortal(
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <div className="glass-card animate-fade-in" style={{
            width: '100%', maxWidth: '600px', padding: '2rem', border: '1px solid rgba(255, 255, 255, 0.1)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>
                {selectedType === 'finding' ? `Detalhes do Achado #${selectedItem.id}` : `Detalhes do Sinal #${selectedItem.id}`}
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setSelectedItem(null)}>
                <X size={20} />
              </button>
            </div>

            {selectedType === 'finding' ? (
              /* FINDING DETAILS */
              <div>
                <div style={{ marginBottom: '1.25rem' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Título</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 600 }}>{selectedItem.title}</div>
                </div>

                <div style={{ display: 'flex', gap: '2rem', marginBottom: '1.25rem' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Severidade</div>
                    <span className={`badge ${(selectedItem.severity || 'info').toLowerCase()}`}>{selectedItem.severity}</span>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Status</div>
                    <span className={`badge ${selectedItem.status === 'resolved' || selectedItem.status === 'mitigated' ? 'success' : 'high'}`}>{selectedItem.status}</span>
                  </div>
                  {selectedItem.signal_id && (
                    <div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Sinal Vinculado</div>
                      <span className="badge info">#{selectedItem.signal_id}</span>
                    </div>
                  )}
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Descrição e Detalhes Técnicos</div>
                  <pre style={{
                    background: 'rgba(0,0,0,0.3)',
                    padding: '1rem',
                    borderRadius: '8px',
                    border: '1px solid var(--border-color)',
                    fontSize: '0.85rem',
                    whiteSpace: 'pre-wrap',
                    color: 'var(--text-primary)',
                    fontFamily: 'monospace'
                  }}>{selectedItem.description || 'Sem descrição.'}</pre>
                </div>
              </div>
            ) : (
              /* SIGNAL DETAILS */
              <div>
                <div style={{ display: 'flex', gap: '2rem', marginBottom: '1.25rem' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Código / Tipo</div>
                    <div style={{ fontFamily: 'monospace', fontWeight: 600 }}>{selectedItem.signal_type}</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Origem (Source)</div>
                    <span className="badge info">{selectedItem.source}</span>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '2rem', marginBottom: '1.25rem' }}>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Severidade</div>
                    <span className={`badge ${(selectedItem.severity || 'info').toLowerCase()}`}>{selectedItem.severity}</span>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Confiança</div>
                    <div style={{ fontWeight: 700 }}>{selectedItem.confidence}%</div>
                  </div>
                  <div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Site</div>
                    <div>{getSiteName(selectedItem.site_id)}</div>
                  </div>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Evidência Coletada</div>
                  <pre style={{
                    background: 'rgba(0,0,0,0.3)',
                    padding: '1rem',
                    borderRadius: '8px',
                    border: '1px solid var(--border-color)',
                    fontSize: '0.85rem',
                    whiteSpace: 'pre-wrap',
                    color: 'var(--text-primary)',
                    fontFamily: 'monospace'
                  }}>{selectedItem.description}</pre>
                </div>
              </div>
            )}

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
              <button className="primary" onClick={() => setSelectedItem(null)}>Fechar</button>
            </div>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
}
