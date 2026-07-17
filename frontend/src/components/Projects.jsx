import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Plus, Trash2, Edit2, Globe, Building2, X, Check } from 'lucide-react';
import api from '../services/api';

export default function Projects({ user }) {
  const isAdmin = user && user.role === 'admin';
  const [loading, setLoading] = useState(true);
  const [projects, setProjects] = useState([]);
  const [organizations, setOrganizations] = useState([]);

  // Modals / Forms States
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [projectForm, setProjectForm] = useState({ id: null, name: '', description: '', tags: '', organization_id: '' });

  const [showOrganizationModal, setShowOrganizationModal] = useState(false);
  const [organizationForm, setOrganizationForm] = useState({ id: null, name: '', domain: '', description: '', is_active: true });

  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('projects'); // 'projects' or 'organizations'

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [projectsData, organizationsData] = await Promise.all([
        api.getProjects(),
        api.getOrganizations()
      ]);
      setProjects(projectsData);
      setOrganizations(organizationsData);
    } catch (err) {
      setError('Erro ao carregar dados do backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Projects Handlers
  const handleProjectSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const tagsArray = projectForm.tags 
        ? projectForm.tags.split(',').map(t => t.trim()).filter(Boolean) 
        : [];
      
      const payload = {
        name: projectForm.name,
        description: projectForm.description || null,
        tags: tagsArray,
        organization_id: projectForm.organization_id ? Number(projectForm.organization_id) : null
      };

      if (projectForm.id) {
        await api.updateProject(projectForm.id, payload);
      } else {
        await api.createProject(payload);
      }
      setShowProjectModal(false);
      loadData();
    } catch (err) {
      setError(err.message || 'Erro ao salvar projeto.');
    }
  };

  const handleEditProject = (project) => {
    setProjectForm({
      id: project.id,
      name: project.name,
      description: project.description || '',
      tags: project.tags ? project.tags.join(', ') : '',
      organization_id: project.organization_id || ''
    });
    setShowProjectModal(true);
  };

  const handleDeleteProject = async (id) => {
    if (!window.confirm('Tem certeza de que deseja deletar este projeto?')) return;
    try {
      await api.deleteProject(id);
      loadData();
    } catch (err) {
      alert(err.message || 'Erro ao deletar projeto.');
    }
  };

  // Organizations Handlers
  const handleOrganizationSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const payload = {
        name: organizationForm.name,
        domain: organizationForm.domain || null,
        description: organizationForm.description || null,
        is_active: organizationForm.is_active
      };

      if (organizationForm.id) {
        await api.updateOrganization(organizationForm.id, payload);
      } else {
        await api.createOrganization(payload);
      }
      setShowOrganizationModal(false);
      loadData();
    } catch (err) {
      setError(err.message || 'Erro ao salvar organização.');
    }
  };

  const handleEditOrganization = (org) => {
    setOrganizationForm({
      id: org.id,
      name: org.name,
      domain: org.domain || '',
      description: org.description || '',
      is_active: org.is_active
    });
    setShowOrganizationModal(true);
  };

  const handleDeleteOrganization = async (id) => {
    if (!window.confirm('Tem certeza de que deseja deletar esta organização? Isso pode impactar projetos e ativos vinculados.')) return;
    try {
      await api.deleteOrganization(id);
      loadData();
    } catch (err) {
      alert(err.message || 'Erro ao deletar organização.');
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
            Gerencie organizações e projetos cadastrados na sua superfície de ataque.
          </p>
        </div>
        
        {/* Buttons for Admin */}
        {isAdmin && (
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button className="primary" onClick={() => {
              setProjectForm({ id: null, name: '', description: '', tags: '', organization_id: '' });
              setShowProjectModal(true);
            }}>
              <Plus size={18} /> Adicionar Projeto
            </button>
            <button className="secondary" onClick={() => {
              setOrganizationForm({ id: null, name: '', domain: '', description: '', is_active: true });
              setShowOrganizationModal(true);
            }}>
              <Plus size={18} /> Nova Organização
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
          style={{ borderBottom: activeTab === 'projects' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('projects')}
        >
          <Globe size={18} /> Projetos ({projects.length})
        </button>
        <button
          className="nav-item"
          style={{ borderBottom: activeTab === 'organizations' ? '2px solid var(--color-primary)' : 'none', borderRadius: 0, paddingBottom: '0.75rem' }}
          onClick={() => setActiveTab('organizations')}
        >
          <Building2 size={18} /> Organizações ({organizations.length})
        </button>
      </div>

      {activeTab === 'projects' ? (
        /* PROJECTS LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {projects.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhum projeto cadastrado ainda.
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>Descrição</th>
                    <th>Organização</th>
                    <th>Tags</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {projects.map(project => {
                    const org = organizations.find(o => o.id === project.organization_id);
                    return (
                      <tr key={project.id}>
                        <td style={{ fontWeight: 600 }}>{project.name}</td>
                        <td style={{ color: 'var(--text-secondary)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {project.description || <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Sem descrição</span>}
                        </td>
                        <td>
                          {org ? (
                            <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <Building2 size={14} style={{ color: 'var(--text-muted)' }} /> {org.name}
                            </span>
                          ) : (
                            <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Nenhuma</span>
                          )}
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
                            {project.tags && project.tags.map((tag, idx) => (
                              <span key={idx} className="badge info" style={{ fontSize: '0.65rem' }}>
                                {tag}
                              </span>
                            ))}
                          </div>
                        </td>
                        <td>
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="secondary" style={{ padding: '0.4rem' }} onClick={() => handleEditProject(project)}>
                              <Edit2 size={14} />
                            </button>
                            {isAdmin && (
                              <button className="secondary" style={{ padding: '0.4rem', color: 'var(--color-danger)' }} onClick={() => handleDeleteProject(project.id)}>
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
        /* ORGANIZATIONS LIST */
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          {organizations.length === 0 ? (
            <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhuma organização cadastrada ainda.
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
                  {organizations.map(org => (
                    <tr key={org.id}>
                      <td style={{ fontWeight: 600 }}>{org.name}</td>
                      <td>{org.domain || <span style={{ color: 'var(--text-muted)' }}>-</span>}</td>
                      <td style={{ color: 'var(--text-secondary)', maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {org.description || <span style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Sem descrição</span>}
                      </td>
                      <td>
                        <span className={`badge ${org.is_active ? 'success' : 'medium'}`} style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                          {org.is_active ? <Check size={10} /> : <X size={10} />}
                          {org.is_active ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button className="secondary" style={{ padding: '0.4rem' }} onClick={() => handleEditOrganization(org)}>
                            <Edit2 size={14} />
                          </button>
                          {isAdmin && (
                            <button className="secondary" style={{ padding: '0.4rem', color: 'var(--color-danger)' }} onClick={() => handleDeleteOrganization(org.id)}>
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

      {/* PROJECTS MODAL */}
      {showProjectModal && createPortal(
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
                {projectForm.id ? 'Editar Projeto' : 'Adicionar Novo Projeto'}
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setShowProjectModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleProjectSubmit}>
              <div className="form-group">
                <label>Nome do Projeto</label>
                <input
                  type="text"
                  placeholder="Ex: E-commerce Principal"
                  value={projectForm.name}
                  onChange={(e) => setProjectForm({ ...projectForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Organização Vinculada</label>
                <select
                  value={projectForm.organization_id}
                  onChange={(e) => setProjectForm({ ...projectForm, organization_id: e.target.value })}
                >
                  <option value="">-- Nenhuma --</option>
                  {organizations.map(o => (
                    <option key={o.id} value={o.id}>{o.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Tags (Separadas por vírgula)</label>
                <input
                  type="text"
                  placeholder="producao, principal, wordpress"
                  value={projectForm.tags}
                  onChange={(e) => setProjectForm({ ...projectForm, tags: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Descrição</label>
                <textarea
                  rows="3"
                  placeholder="Detalhes ou observações sobre este projeto..."
                  value={projectForm.description}
                  onChange={(e) => setProjectForm({ ...projectForm, description: e.target.value })}
                ></textarea>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem' }}>
                <button type="button" className="secondary" onClick={() => setShowProjectModal(false)}>Cancelar</button>
                <button type="submit" className="primary">Salvar</button>
              </div>
            </form>
          </div>
        </div>,
        document.body
      )}

      {/* ORGANIZATIONS MODAL */}
      {showOrganizationModal && createPortal(
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
                {organizationForm.id ? 'Editar Organização' : 'Adicionar Nova Organização'}
              </h2>
              <button className="secondary" style={{ padding: '4px', border: 'none' }} onClick={() => setShowOrganizationModal(false)}>
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleOrganizationSubmit}>
              <div className="form-group">
                <label>Nome da Organização</label>
                <input
                  type="text"
                  placeholder="Ex: Grupo Alpha SA"
                  value={organizationForm.name}
                  onChange={(e) => setOrganizationForm({ ...organizationForm, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label>Domínio Corporativo</label>
                <input
                  type="text"
                  placeholder="Ex: grupoalpha.com"
                  value={organizationForm.domain}
                  onChange={(e) => setOrganizationForm({ ...organizationForm, domain: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label>Descrição</label>
                <textarea
                  rows="3"
                  placeholder="Informações adicionais da organização..."
                  value={organizationForm.description}
                  onChange={(e) => setOrganizationForm({ ...organizationForm, description: e.target.value })}
                ></textarea>
              </div>

              <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '1rem' }}>
                <input
                  id="is_active"
                  type="checkbox"
                  checked={organizationForm.is_active}
                  onChange={(e) => setOrganizationForm({ ...organizationForm, is_active: e.target.checked })}
                  style={{ width: 'auto', display: 'inline' }}
                />
                <label htmlFor="is_active" style={{ display: 'inline', margin: 0, textTransform: 'none' }}>Organização Ativa</label>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem' }}>
                <button type="button" className="secondary" onClick={() => setShowOrganizationModal(false)}>Cancelar</button>
                <button type="submit" className="primary">Salvar</button>
              </div>
            </form>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
}
