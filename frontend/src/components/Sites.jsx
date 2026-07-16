import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Edit2, Globe, Building2, ExternalLink, X, Check } from 'lucide-react';
import api from '../services/api';

export default function Sites({ user }) {
  const isAdmin = user && user.role === 'admin';
  const [loading, setLoading] = useState(true);
  const [sites, setSites] = useState([]);
  const [companies, setCompanies] = useState([]);

  // Modals / Forms States
  const [showSiteModal, setShowSiteModal] = useState(false);
  const [siteForm, setSiteForm] = useState({ id: null, name: '', url: '', description: '', tags: '', company_id: '' });

  const [showCompanyModal, setShowCompanyModal] = useState(false);
  const [companyForm, setCompanyForm] = useState({ id: null, name: '', domain: '', description: '', is_active: true });

  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('sites'); // 'sites' or 'companies'

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [sitesData, companiesData] = await Promise.all([
        api.getSites(),
        api.getCompanies()
      ]);
      setSites(sitesData);
      setCompanies(companiesData);
    } catch (err) {
      setError('Erro ao carregar dados do backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Sites Handlers
  const handleSiteSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const tagsArray = siteForm.tags 
        ? siteForm.tags.split(',').map(t => t.trim()).filter(Boolean) 
        : [];
      
      const payload = {
        name: siteForm.name,
        url: siteForm.url,
        description: siteForm.description || null,
        tags: tagsArray,
        company_id: siteForm.company_id ? Number(siteForm.company_id) : null
      };

      if (siteForm.id) {
        await api.updateSite(siteForm.id, payload);
      } else {
        await api.createSite(payload);
      }
      setShowSiteModal(false);
      loadData();
    } catch (err) {
      setError(err.message || 'Erro ao salvar site.');
    }
  };

  const handleEditSite = (site) => {
    setSiteForm({
      id: site.id,
      name: site.name,
      url: site.url,
      description: site.description || '',
      tags: site.tags ? site.tags.join(', ') : '',
      company_id: site.company_id || ''
    });
    setShowSiteModal(true);
  };

  const handleDeleteSite = async (id) => {
    if (!window.confirm('Tem certeza de que deseja deletar este site?')) return;
    try {
      await api.deleteSite(id);
      loadData();
    } catch (err) {
      alert(err.message || 'Erro ao deletar site.');
    }
  };

  // Companies Handlers
  const handleCompanySubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const payload = {
        name: companyForm.name,
        domain: companyForm.domain || null,
        description: companyForm.description || null,
        is_active: companyForm.is_active
      };

      if (companyForm.id) {
        await api.updateCompany(companyForm.id, payload);
      } else {
        await api.createCompany(payload);
      }
      setShowCompanyModal(false);
      loadData();
    } catch (err) {
      setError(err.message || 'Erro ao salvar empresa.');
    }
  };

  const handleEditCompany = (company) => {
    setCompanyForm({
      id: company.id,
      name: company.name,
      domain: company.domain || '',
      description: company.description || '',
      is_active: company.is_active
    });
    setShowCompanyModal(true);
  };

  const handleDeleteCompany = async (id) => {
    if (!window.confirm('Tem certeza de que deseja deletar esta empresa? Isso pode impactar sites e ativos vinculados.')) return;
    try {
      await api.deleteCompany(id);
      loadData();
    } catch (err) {
      alert(err.message || 'Erro ao deletar empresa.');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div style={{ color: 'var(--text-secondary)' }}>Carregando dados...</div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.25rem' }}>Gestão de Escopo</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Gerencie sites e empresas cadastrados na sua superfície de ataque.
          </p>
        </div>
        
        {/* Buttons for Admin */}
        {isAdmin && (
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button className="primary" onClick={() => {
              setSiteForm({ id: null, name: '', url: '', description: '', tags: '', company_id: '' });
              setShowSiteModal(true);
            }}>
              <Plus size={18} /> Adicionar Site
            </button>
            <button className="secondary" onClick={() => {
              setCompanyForm({ id: null, name: '', domain: '', description: '', is_active: true });
              setShowCompanyModal(true);
            }}>
              <Plus size={18} /> Nova Empresa
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
          style={{ borderBottom: activeTab === 'sites' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('sites')}
        >
          <Globe size={18} /> Sites ({sites.length})
        </button>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'companies' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('companies')}
        >
          <Building2 size={18} /> Empresas ({companies.length})
        </button>
      </div>

      {activeTab === 'sites' ? (
        /* SITES LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {sites.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhum site cadastrado ainda.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>URL</th>
                    <th>Empresa</th>
                    <th>Tags</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {sites.map(site => {
                    const company = companies.find(c => c.id === site.company_id);
                    return (
                      <tr key={site.id}>
                        <td style={{ fontWeight: 600 }}>{site.name}</td>
                        <td>
                          <a href={site.url} target="_blank" rel="noopener noreferrer" style={{
                            color: 'var(--color-primary)',
                            textDecoration: 'none',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '4px'
                          }}>
                            {site.url} <ExternalLink size={12} />
                          </a>
                        </td>
                        <td>
                          {company ? (
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <Building2 size={14} style={{ color: 'var(--text-muted)' }} /> {company.name}
                            </span>
                          ) : (
                            <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Nenhuma</span>
                          )}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                            {site.tags && site.tags.map((tag, idx) => (
                              <span key={idx} className="badge info" style={{ fontSize: '0.65rem' }}>
                                {tag}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="secondary" style={{ padding: '0.4rem' }} onClick={() => handleEditSite(site)}>
                              <Edit2 size={14} />
                            </button>
                            {isAdmin && (
                              <button className="secondary" style={{ padding: '0.4rem', color: 'var(--color-danger)' }} onClick={() => handleDeleteSite(site.id)}>
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
        /* COMPANIES LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {companies.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhuma empresa cadastrada ainda.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Domínio</th>
                    <th>Descrição</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {companies.map(company => (
                    <tr key={company.id}>
                      <td style={{ fontWeight: 600 }}>{company.name}</td>
                      <td>{company.domain || <span style={{ color: 'var(--text-muted)' }}>-</span>}</td>
                      <td style={{ color: 'var(--text-secondary)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {company.description || <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Sem descrição</span>}
                      </td>
                      <td>
                        <span className={`badge ${company.is_active ? 'success' : 'medium'}`} style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                          {company.is_active ? <Check size={10} /> : <X size={10} />}
                          {company.is_active ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button className="secondary" style={{ padding: '0.4rem' }} onClick={() => handleEditCompany(company)}>
                            <Edit2 size={14} />
                          </button>
                          {isAdmin && (
                            <button className="secondary" style={{ padding: '0.4rem', color: 'var(--color-danger)' }} onClick={() => handleDeleteCompany(company.id)}>
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
      )}

      {/* SITES MODAL */}
      {showSiteModal && (
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
                {siteForm.id ? 'Editar Site' : 'Adicionar Novo Site'}
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setShowSiteModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleSiteSubmit}>
              <div className="form-group">
                <label>Nome do Site</label>
                <input
                  type="text"
                  placeholder="Ex: E-commerce Principal"
                  value={siteForm.name}
                  onChange={(e) => setSiteForm({ ...siteForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>URL (Endereço)</label>
                <input
                  type="url"
                  placeholder="https://meusite.com"
                  value={siteForm.url}
                  onChange={(e) => setSiteForm({ ...siteForm, url: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Empresa Vinculada</label>
                <select
                  value={siteForm.company_id}
                  onChange={(e) => setSiteForm({ ...siteForm, company_id: e.target.value })}
                >
                  <option value="">-- Nenhuma --</option>
                  {companies.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Tags (Separadas por vírgula)</label>
                <input
                  type="text"
                  placeholder="producao, principal, wordpress"
                  value={siteForm.tags}
                  onChange={(e) => setSiteForm({ ...siteForm, tags: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Descrição</label>
                <textarea
                  rows="3"
                  placeholder="Detalhes ou observações sobre este site..."
                  value={siteForm.description}
                  onChange={(e) => setSiteForm({ ...siteForm, description: e.target.value })}
                ></textarea>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem' }}>
                <button type="button" className="secondary" onClick={() => setShowSiteModal(false)}>Cancelar</button>
                <button type="submit" className="primary">Salvar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* COMPANIES MODAL */}
      {showCompanyModal && (
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
                {companyForm.id ? 'Editar Empresa' : 'Adicionar Nova Empresa'}
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setShowCompanyModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleCompanySubmit}>
              <div className="form-group">
                <label>Nome da Empresa</label>
                <input
                  type="text"
                  placeholder="Ex: Grupo Alpha SA"
                  value={companyForm.name}
                  onChange={(e) => setCompanyForm({ ...companyForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Domínio Corporativo</label>
                <input
                  type="text"
                  placeholder="Ex: grupoalpha.com"
                  value={companyForm.domain}
                  onChange={(e) => setCompanyForm({ ...companyForm, domain: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Descrição</label>
                <textarea
                  rows="3"
                  placeholder="Informações adicionais da empresa..."
                  value={companyForm.description}
                  onChange={(e) => setCompanyForm({ ...companyForm, description: e.target.value })}
                ></textarea>
              </div>

              <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '1rem' }}>
                <input
                  id="is_active"
                  type="checkbox"
                  checked={companyForm.is_active}
                  onChange={(e) => setCompanyForm({ ...companyForm, is_active: e.target.checked })}
                  style={{ width: 'auto', display: 'inline' }}
                />
                <label htmlFor="is_active" style={{ display: 'inline', margin: 0, textTransform: 'none' }}>Empresa Ativa</label>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem' }}>
                <button type="button" className="secondary" onClick={() => setShowCompanyModal(false)}>Cancelar</button>
                <button type="submit" className="primary">Salvar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
