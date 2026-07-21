import React, { useState, useEffect } from 'react';
import { 
  ShieldAlert, Activity, Globe, Database, Play, CheckCircle, 
  AlertCircle, AlertOctagon, Server, Clock, Download
} from 'lucide-react';
import api from '../services/api';

export default function Dashboard({ user, onNavigate }) {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    projects: 0,
    assets: 0,
    scans: 0,
    signals: 0,
    findings: 0,
    findingsBySeverity: { critical: 0, high: 0, medium: 0, low: 0, info: 0 },
    recentScans: [],
    recentFindings: [],
    avgRiskScore: 0.0,
    avgMttrHours: 0.0,
    slaCompliancePct: 100.0
  });

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [projects, assets, scans, signals, findings, metrics] = await Promise.all([
        api.getProjects(),
        api.getAssets(),
        api.getScans(),
        api.getSignals(),
        api.getFindings(),
        api.getDashboardMetrics()
      ]);

      // Calculate severity counts
      const counts = { critical: 0, high: 0, medium: 0, low: 0, info: 0 };
      findings.forEach(f => {
        const sev = (f.severity || 'info').toLowerCase();
        if (counts[sev] !== undefined) {
          counts[sev]++;
        } else {
          counts.info++;
        }
      });

      setStats({
        projects: projects.length,
        assets: assets.length,
        scans: scans.length,
        signals: signals.length,
        findings: findings.length,
        findingsBySeverity: counts,
        recentScans: scans.slice(0, 5),
        recentFindings: findings.slice(0, 5),
        avgRiskScore: metrics.avg_risk_score,
        avgMttrHours: metrics.avg_mttr_hours,
        slaCompliancePct: metrics.sla_compliance_pct
      });
    } catch (error) {
      console.error("Erro ao carregar dados do Dashboard", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleExportCSV = async () => {
    try {
      await api.downloadVulnerabilitiesCSV();
    } catch (error) {
      alert('Erro ao exportar relatório CSV.');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <div style={{ color: 'var(--text-secondary)' }}>Carregando estatísticas do console...</div>
      </div>
    );
  }

  const severityData = [
    { name: 'Crítica', key: 'critical', color: 'var(--color-critical)', icon: <AlertOctagon size={20} /> },
    { name: 'Alta', key: 'high', color: 'var(--color-danger)', icon: <AlertCircle size={20} /> },
    { name: 'Média', key: 'medium', color: 'var(--color-warning)', icon: <ShieldAlert size={20} /> },
    { name: 'Baixa', key: 'low', color: 'var(--color-primary)', icon: <Activity size={20} /> },
    { name: 'Info', key: 'info', color: 'var(--color-info)', icon: <Server size={20} /> },
  ];

  return (
    <div className="animate-fade-in" style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.25rem' }}>Dashboard Geral</h1>
          <p style={{ color: 'var(--text-secondary)' }}>
            Visão consolidada da superfície de ataque e ameaças detectadas.
          </p>
        </div>
        
        <button className="secondary" onClick={handleExportCSV} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Download size={16} /> Exportar CSV (Geral)
        </button>
      </div>

      {/* Main Stats Cards Grid */}
      <div className="grid-cols-4" style={{ marginBottom: '2rem' }}>
        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--color-primary)', padding: '0.75rem', borderRadius: '10px' }}>
            <Globe size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Projetos</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>{stats.projects}</div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--color-success)', padding: '0.75rem', borderRadius: '10px' }}>
            <Database size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Ativos Monitorados</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>{stats.assets}</div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(14, 165, 233, 0.1)', color: 'var(--color-info)', padding: '0.75rem', borderRadius: '10px' }}>
            <Play size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Varreduras Realizadas</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>{stats.scans}</div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--color-danger)', padding: '0.75rem', borderRadius: '10px' }}>
            <ShieldAlert size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Total de Achados</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>{stats.findings}</div>
          </div>
        </div>
      </div>

      {/* SLA & Governance Section */}
      <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' }}>Governança e Nível de Serviço</h3>
      <div className="grid-cols-3" style={{ marginBottom: '2.5rem' }}>
        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(245, 158, 11, 0.1)', color: 'var(--color-warning)', padding: '0.75rem', borderRadius: '10px' }}>
            <Activity size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Risk Score Médio</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>{stats.avgRiskScore || '0.0'}</div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(139, 92, 246, 0.1)', color: 'var(--color-secondary)', padding: '0.75rem', borderRadius: '10px' }}>
            <Clock size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>MTTR (Tempo de Resposta)</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>
              {stats.avgMttrHours > 0 ? `${stats.avgMttrHours}h` : 'Sem dados'}
            </div>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--color-success)', padding: '0.75rem', borderRadius: '10px' }}>
            <CheckCircle size={24} />
          </div>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>Conformidade com SLA</div>
            <div style={{ fontSize: '1.75rem', fontWeight: 700, lineHeight: 1.2 }}>{stats.slaCompliancePct}%</div>
          </div>
        </div>
      </div>

      {/* Severities distribution row */}
      <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' }}>Distribuição de Severidade do Risco</h3>
      <div className="grid-cols-5" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2.5rem' }}>
        {severityData.map(item => {
          const count = stats.findingsBySeverity[item.key] || 0;
          return (
            <div key={item.key} className="glass-card" style={{
              padding: '1.25rem',
              display: 'flex',
              flexDirection: 'column',
              borderLeft: `4px solid ${item.color}`
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', color: item.color }}>
                <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)' }}>{item.name}</span>
                {item.icon}
              </div>
              <div style={{ fontSize: '2rem', fontWeight: 700, lineHeight: 1 }}>{count}</div>
            </div>
          );
        })}
      </div>

      {/* Two Column details grid */}
      <div className="grid-cols-2">
        {/* Column 1: Recent Scans */}
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 600 }}>Varreduras Recentes</h3>
            <button className="secondary" onClick={() => onNavigate('scans')} style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem' }}>Ver todas</button>
          </div>
          {stats.recentScans.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', textAlign: 'center', padding: '2rem 0' }}>
              Nenhum scan registrado.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {stats.recentScans.map(scan => (
                <div key={scan.id} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.75rem 1rem',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px'
                }}>
                  <div>
                    <div style={{ fontSize: '0.875rem', fontWeight: 600 }}>Tipo: {scan.scan_type.toUpperCase()}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      Iniciado em: {scan.started_at ? api.formatDate(scan.started_at) : 'N/A'}
                    </div>
                  </div>
                  <span className={`badge ${scan.status === 'completed' ? 'success' : scan.status === 'running' ? 'info' : 'medium'}`}>
                    {scan.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Column 2: Recent Findings */}
        <div className="glass-card" style={{ padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: 600 }}>Últimos Detectados</h3>
            <button className="secondary" onClick={() => onNavigate('signals')} style={{ padding: '0.35rem 0.75rem', fontSize: '0.75rem' }}>Ver todos</button>
          </div>
          {stats.recentFindings.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem', textAlign: 'center', padding: '2rem 0' }}>
              Nenhum achado registrado.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {stats.recentFindings.map(finding => (
                <div key={finding.id} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.75rem 1rem',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px'
                }}>
                  <div style={{ maxWidth: '75%' }}>
                    <div style={{ fontSize: '0.875rem', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {finding.title}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {finding.description}
                    </div>
                  </div>
                  <span className={`badge ${(finding.severity || 'info').toLowerCase()}`}>
                    {finding.severity}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
