import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { 
  ShieldAlert, ShieldCheck, CheckCircle2, AlertOctagon, AlertTriangle, 
  Trash2, RefreshCw, X, ShieldAlert as VulnerabilityIcon, FileText, Check
} from 'lucide-react';
import api from '../services/api';

export default function Vulnerabilities({ user }) {
  const isAdmin = user && user.role === 'admin';
  const [loading, setLoading] = useState(true);
  
  // Data States
  const [vulnerabilities, setVulnerabilities] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [assets, setAssets] = useState([]);

  // Filter States
  const [activeTab, setActiveTab] = useState('vulnerabilities'); // 'vulnerabilities' or 'recommendations'
  const [severityFilter, setSeverityFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Selected Detail Modal
  const [selectedVuln, setSelectedVuln] = useState(null);
  const [linkedRecs, setLinkedRecs] = useState([]);
  const [updatingStatus, setUpdatingStatus] = useState(null); // Track ID being updated

  const loadData = async () => {
    setLoading(true);
    try {
      const [vulnsData, recsData, assetsData] = await Promise.all([
        api.getVulnerabilities(),
        api.getRecommendations(),
        api.getAssets()
      ]);
      setVulnerabilities(vulnsData);
      setRecommendations(recsData);
      setAssets(assetsData);
    } catch (err) {
      console.error("Erro ao carregar vulnerabilidades e recomendações", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getAssetValue = (assetId) => {
    if (!assetId) return 'Nenhum';
    const asset = assets.find(a => a.id === assetId);
    return asset ? asset.value : `Ativo #${assetId}`;
  };

  const getCvssColor = (score) => {
    if (!score) return 'var(--text-muted)';
    if (score >= 9.0) return 'var(--color-critical)'; // Critical
    if (score >= 7.0) return 'var(--color-danger)';   // High
    if (score >= 4.0) return 'var(--color-warning)';  // Medium
    return 'var(--color-success)';                     // Low
  };

  const getPriorityColor = (prio) => {
    const p = prio.toLowerCase();
    if (p === 'critical' || p === 'high') return 'var(--color-danger)';
    if (p === 'medium') return 'var(--color-warning)';
    return 'var(--color-primary)';
  };

  const handleVulnClick = async (vuln) => {
    setSelectedVuln(vuln);
    // Find recommendations linked to this vulnerability ID
    const recs = recommendations.filter(r => r.vulnerability_id === vuln.id);
    setLinkedRecs(recs);
  };

  const handleUpdateVulnStatus = async (vulnId, newStatus) => {
    setUpdatingStatus(vulnId);
    try {
      const updated = await api.updateVulnerability(vulnId, { status: newStatus });
      
      // Update local states
      setVulnerabilities(prev => prev.map(v => v.id === vulnId ? updated : v));
      if (selectedVuln && selectedVuln.id === vulnId) {
        setSelectedVuln(updated);
      }
    } catch (err) {
      alert("Erro ao atualizar status: " + (err.message || err));
    } finally {
      setUpdatingStatus(null);
    }
  };

  const handleUpdateRecStatus = async (recId, newStatus) => {
    try {
      const updated = await api.updateRecommendation(recId, { status: newStatus });
      setRecommendations(prev => prev.map(r => r.id === recId ? updated : r));
      
      // Update modal list if open
      setLinkedRecs(prev => prev.map(r => r.id === recId ? updated : r));
    } catch (err) {
      alert("Erro ao atualizar recomendação: " + (err.message || err));
    }
  };

  const handleDeleteVuln = async (id) => {
    if (!window.confirm("Deseja realmente remover o registro desta vulnerabilidade? Recomendações associadas também serão apagadas.")) return;
    try {
      await api.deleteVulnerability(id);
      setSelectedVuln(null);
      loadData();
    } catch (err) {
      alert("Erro ao deletar: " + (err.message || err));
    }
  };

  // Filters
  const filteredVulns = vulnerabilities.filter(v => {
    const matchSev = severityFilter ? (v.severity || '').toLowerCase() === severityFilter.toLowerCase() : true;
    const matchStatus = statusFilter ? (v.status || '').toLowerCase() === statusFilter.toLowerCase() : true;
    return matchSev && matchStatus;
  });

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div style={{ color: 'var(--text-secondary)' }}>Carregando central de vulnerabilidades...</div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.25rem' }}>Análise e Mitigação</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Consulte as vulnerabilidades técnicas correlacionadas e execute planos de recomendação.
          </p>
        </div>
        <button className="secondary" onClick={loadData}>
          <RefreshCw size={14} /> Atualizar
        </button>
      </div>

      {/* Filter Toolbar */}
      <div className="glass-card" style={{ padding: '1.25rem', marginBottom: '1.5rem', display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Filtrar:</span>
        
        <div style={{ minWidth: '150px' }}>
          <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)} style={{ padding: '0.45rem', fontSize: '0.8rem' }}>
            <option value="">-- Severidade --</option>
            <option value="critical">Crítica</option>
            <option value="high">Alta</option>
            <option value="medium">Média</option>
            <option value="low">Baixa</option>
          </select>
        </div>

        <div style={{ minWidth: '150px' }}>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} style={{ padding: '0.45rem', fontSize: '0.8rem' }}>
            <option value="">-- Status --</option>
            <option value="open">Aberto (Open)</option>
            <option value="mitigated">Mitigado (Mitigated)</option>
            <option value="accepted">Aceito (Accepted)</option>
            <option value="resolved">Resolvido (Resolved)</option>
          </select>
        </div>

        {(severityFilter || statusFilter) && (
          <button className="secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem', border: 'none' }} onClick={() => { setSeverityFilter(''); setStatusFilter(''); }}>
            Limpar Filtros
          </button>
        )}
      </div>

      {/* Navigation tabs */}
      <div style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid var(--border-color)', marginBottom: '1.5rem', paddingBottom: '1px' }}>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'vulnerabilities' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('vulnerabilities')}
        >
          <VulnerabilityIcon size={18} /> Vulnerabilidades ({filteredVulns.length})
        </button>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'recommendations' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('recommendations')}
        >
          <FileText size={18} /> Recomendações de Ação ({recommendations.length})
        </button>
      </div>

      {activeTab === 'vulnerabilities' ? (
        /* VULNERABILITIES LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {filteredVulns.length === 0 ? (
            <div style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem', color: 'var(--color-primary)' }}>Nenhuma vulnerabilidade detectada ainda</div>
              <p style={{ maxWidth: '500px', margin: '0 auto 1.5rem', fontSize: '0.875rem', lineHeight: '1.5', color: 'var(--text-muted)' }}>
                As vulnerabilidades são geradas dinamicamente após a execução de uma varredura. Vá até a aba "Varreduras" e clique em "Iniciar" para analisar um site em escopo.
              </p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>CVE ID</th>
                    <th>Título</th>
                    <th>Alvo (Ativo)</th>
                    <th>Score CVSS</th>
                    <th>Severidade</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredVulns.map(vuln => (
                    <tr key={vuln.id}>
                      <td style={{ fontFamily: 'monospace', fontWeight: 600 }}>
                        {vuln.cve_id ? (
                          <span style={{ color: 'var(--color-primary)' }}>{vuln.cve_id}</span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>Mapeamento-Local</span>
                        )}
                      </td>
                      <td style={{ fontWeight: 600, maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {vuln.title}
                      </td>
                      <td>
                        <span style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                          {getAssetValue(vuln.asset_id)}
                        </span>
                      </td>
                      <td>
                        {vuln.cvss_score ? (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ fontWeight: 700, color: getCvssColor(vuln.cvss_score) }}>{vuln.cvss_score.toFixed(1)}</span>
                            <div style={{ width: '60px', height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                              <div style={{ 
                                width: `${vuln.cvss_score * 10}%`, 
                                height: '100%', 
                                background: getCvssColor(vuln.cvss_score) 
                              }}></div>
                            </div>
                          </div>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>-</span>
                        )}
                      </td>
                      <td>
                        <span className={`badge ${(vuln.severity || 'info').toLowerCase()}`}>
                          {vuln.severity}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${
                          vuln.status === 'resolved' || vuln.status === 'mitigated' ? 'success' : 
                          vuln.status === 'accepted' ? 'info' : 'high'
                        }`}>
                          {vuln.status}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button className="primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.75rem' }} onClick={() => handleVulnClick(vuln)}>
                            Analisar
                          </button>
                          {isAdmin && (
                            <button className="secondary" style={{ padding: '0.4rem', color: 'var(--color-danger)' }} onClick={() => handleDeleteVuln(vuln.id)}>
                              <Trash2 size={14} />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : (
        /* RECOMMENDATIONS LIST */
        <div className="grid-cols-2">
          {recommendations.length === 0 ? (
            <div className="glass-card" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-secondary)', gridColumn: 'span 2' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '0.5rem', color: 'var(--color-success)' }}>Nenhuma recomendação de mitigação ativa</div>
              <p style={{ maxWidth: '500px', margin: '0 auto', fontSize: '0.875rem', lineHeight: '1.5', color: 'var(--text-muted)' }}>
                Os planos de ação com recomendações prioritárias serão exibidos aqui assim que vulnerabilidades forem identificadas durante os escaneamentos ativos.
              </p>
            </div>
          ) : (
            recommendations.map(rec => (
              <div key={rec.id} className="glass-card animate-fade-in" style={{
                padding: '1.5rem',
                borderLeft: `4px solid ${getPriorityColor(rec.priority)}`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                    <span className="badge" style={{
                      background: 'rgba(255,255,255,0.03)',
                      color: getPriorityColor(rec.priority),
                      borderColor: getPriorityColor(rec.priority)
                    }}>
                      Prioridade: {rec.priority.toUpperCase()}
                    </span>
                    <span className={`badge ${rec.status === 'done' ? 'success' : 'medium'}`}>
                      {rec.status}
                    </span>
                  </div>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem' }}>{rec.title}</h3>
                  <pre style={{
                    background: 'rgba(0,0,0,0.2)',
                    padding: '0.85rem',
                    borderRadius: '6px',
                    fontSize: '0.75rem',
                    color: 'var(--text-secondary)',
                    whiteSpace: 'pre-wrap',
                    fontFamily: 'inherit',
                    lineHeight: '1.4',
                    marginBottom: '1rem'
                  }}>{rec.description}</pre>
                </div>

                {isAdmin && (
                  <div style={{ display: 'flex', gap: '0.5rem', borderTop: '1px solid var(--border-color)', paddingTop: '0.75rem', justifyContent: 'flex-end' }}>
                    {rec.status !== 'done' ? (
                      <button 
                        className="primary" 
                        style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', display: 'inline-flex', alignItems: 'center', gap: '4px' }}
                        onClick={() => handleUpdateRecStatus(rec.id, 'done')}
                      >
                        <Check size={12} /> Marcar como Resolvido
                      </button>
                    ) : (
                      <button 
                        className="secondary" 
                        style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem' }}
                        onClick={() => handleUpdateRecStatus(rec.id, 'open')}
                      >
                        Reabrir Recomendação
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {/* DETAIL MODAL */}
      {selectedVuln && createPortal(
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(4px)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
        }}>
          <div className="glass-card animate-fade-in" style={{
            width: '90%', maxWidth: '650px', padding: '2rem', border: '1px solid rgba(255, 255, 255, 0.1)', maxHeight: '90vh', overflowY: 'auto'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem', marginBottom: '1.5rem' }}>
              <div>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0 }}>
                  {selectedVuln.cve_id ? `${selectedVuln.cve_id} - ` : ''}{selectedVuln.title}
                </h2>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'monospace', marginTop: '4px' }}>
                  ID Vulnerabilidade: #{selectedVuln.id} | Alvo: {getAssetValue(selectedVuln.asset_id)}
                </div>
              </div>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setSelectedVuln(null)}>
                <X size={20} />
              </button>
            </div>

            {/* Vuln Specs */}
            <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Severidade</div>
                <span className={`badge ${(selectedVuln.severity || 'info').toLowerCase()}`}>{selectedVuln.severity}</span>
              </div>
              
              {selectedVuln.cvss_score && (
                <div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>CVSS Score</div>
                  <span style={{ fontWeight: 700, color: getCvssColor(selectedVuln.cvss_score) }}>{selectedVuln.cvss_score.toFixed(1)} / 10.0</span>
                </div>
              )}

              <div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.25rem' }}>Status da Ameaça</div>
                <span className={`badge ${
                  selectedVuln.status === 'resolved' || selectedVuln.status === 'mitigated' ? 'success' : 
                  selectedVuln.status === 'accepted' ? 'info' : 'high'
                }`}>{selectedVuln.status}</span>
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.35rem' }}>Descrição Técnica</div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: '1.5', margin: 0 }}>
                {selectedVuln.description || 'Nenhuma descrição detalhada disponível.'}
              </p>
            </div>

            {/* Status updates for Admin */}
            {isAdmin && (
              <div className="glass-card" style={{ padding: '1rem', background: 'rgba(255,255,255,0.01)', border: '1px solid var(--border-color)', marginBottom: '1.5rem' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, marginBottom: '0.5rem' }}>Alterar Status de Análise (Ações de Triagem)</div>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  <button 
                    className="secondary" 
                    style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: selectedVuln.status === 'open' ? 'var(--color-danger)' : '' }}
                    disabled={updatingStatus !== null}
                    onClick={() => handleUpdateVulnStatus(selectedVuln.id, 'open')}
                  >
                    Abrir (Open)
                  </button>
                  <button 
                    className="secondary" 
                    style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: selectedVuln.status === 'mitigated' ? 'var(--color-success)' : '' }}
                    disabled={updatingStatus !== null}
                    onClick={() => handleUpdateVulnStatus(selectedVuln.id, 'mitigated')}
                  >
                    Mitigar (Mitigated)
                  </button>
                  <button 
                    className="secondary" 
                    style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: selectedVuln.status === 'accepted' ? 'var(--color-primary)' : '' }}
                    disabled={updatingStatus !== null}
                    onClick={() => handleUpdateVulnStatus(selectedVuln.id, 'accepted')}
                  >
                    Aceitar Risco (Accepted)
                  </button>
                  <button 
                    className="secondary" 
                    style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem', borderColor: selectedVuln.status === 'resolved' ? 'var(--color-success)' : '' }}
                    disabled={updatingStatus !== null}
                    onClick={() => handleUpdateVulnStatus(selectedVuln.id, 'resolved')}
                  >
                    Resolver (Resolved)
                  </button>
                </div>
              </div>
            )}

            {/* Recommendations Sub-section */}
            <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1.25rem' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <ShieldCheck size={18} style={{ color: 'var(--color-success)' }} /> Recomendações de Mitigação Vinculadas
              </h3>

              {linkedRecs.length === 0 ? (
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                  Nenhuma recomendação vinculada a esta vulnerabilidade.
                </p>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {linkedRecs.map(rec => (
                    <div key={rec.id} style={{
                      padding: '1rem',
                      background: 'rgba(255, 255, 255, 0.02)',
                      border: '1px solid var(--border-color)',
                      borderRadius: '8px',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.5rem'
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{rec.title}</span>
                        <span className={`badge ${rec.status === 'done' ? 'success' : 'medium'}`}>{rec.status}</span>
                      </div>
                      <pre style={{
                        background: 'rgba(0,0,0,0.1)',
                        padding: '0.75rem',
                        borderRadius: '4px',
                        fontSize: '0.75rem',
                        color: 'var(--text-secondary)',
                        whiteSpace: 'pre-wrap',
                        fontFamily: 'inherit',
                        lineHeight: '1.4',
                        margin: 0
                      }}>{rec.description}</pre>

                      {isAdmin && rec.status !== 'done' && (
                        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.25rem' }}>
                          <button 
                            className="primary" 
                            style={{ padding: '0.25rem 0.65rem', fontSize: '0.7rem', display: 'inline-flex', alignItems: 'center', gap: '4px' }}
                            onClick={() => handleUpdateRecStatus(rec.id, 'done')}
                          >
                            <Check size={10} /> Concluir Mitigação
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
              <button className="primary" onClick={() => setSelectedVuln(null)}>Fechar Painel</button>
            </div>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
}
