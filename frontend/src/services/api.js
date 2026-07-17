const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
  getToken() {
    return localStorage.getItem('token');
  }

  setToken(token) {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  getCurrentUser() {
    const token = this.getToken();
    if (!token) return null;
    try {
      // Decode JWT payload (standard Base64 decode)
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      return null;
    }
  }

  logout() {
    this.setToken(null);
  }

  async request(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    const config = {
      ...options,
      headers,
    };

    const url = `${API_BASE_URL}${endpoint}`;

    try {
      const response = await fetch(url, config);
      if (response.status === 401) {
        this.logout();
        window.dispatchEvent(new Event('auth-failed'));
      }
      
      if (response.status === 204) {
        return true;
      }

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Erro na requisição à API.');
      }
      return data;
    } catch (error) {
      console.error(`API Error on ${endpoint}:`, error);
      throw error;
    }
  }

  // Auth Endpoints
  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setToken(data.access_token);
    return this.getCurrentUser();
  }

  async register(username, email, password, role = 'viewer') {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, role }),
    });
  }

  // Organizations Endpoints
  async getOrganizations() {
    return this.request('/organizations');
  }

  async getOrganization(id) {
    return this.request(`/organizations/${id}`);
  }

  async createOrganization(organizationData) {
    return this.request('/organizations', {
      method: 'POST',
      body: JSON.stringify(organizationData),
    });
  }

  async updateOrganization(id, organizationData) {
    return this.request(`/organizations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(organizationData),
    });
  }

  async deleteOrganization(id) {
    return this.request(`/organizations/${id}`, {
      method: 'DELETE',
    });
  }

  // Projects Endpoints
  async getProjects() {
    return this.request('/projects');
  }

  async getProject(id) {
    return this.request(`/projects/${id}`);
  }

  async createProject(projectData) {
    return this.request('/projects', {
      method: 'POST',
      body: JSON.stringify(projectData),
    });
  }

  async updateProject(id, projectData) {
    return this.request(`/projects/${id}`, {
      method: 'PUT',
      body: JSON.stringify(projectData),
    });
  }

  async deleteProject(id) {
    return this.request(`/projects/${id}`, {
      method: 'DELETE',
    });
  }

  // Assets Endpoints
  async getAssets(organizationId = null, projectId = null) {
    let query = '';
    const params = [];
    if (organizationId) params.push(`organization_id=${organizationId}`);
    if (projectId) params.push(`project_id=${projectId}`);
    if (params.length) query = `?${params.join('&')}`;

    return this.request(`/assets${query}`);
  }

  async createAsset(assetData) {
    return this.request('/assets', {
      method: 'POST',
      body: JSON.stringify(assetData),
    });
  }

  async updateAsset(id, assetData) {
    return this.request(`/assets/${id}`, {
      method: 'PUT',
      body: JSON.stringify(assetData),
    });
  }

  async deleteAsset(id) {
    return this.request(`/assets/${id}`, {
      method: 'DELETE',
    });
  }

  // Scans Endpoints
  async getScans(projectId = null, assetId = null) {
    let query = '';
    const params = [];
    if (projectId) params.push(`project_id=${projectId}`);
    if (assetId) params.push(`asset_id=${assetId}`);
    if (params.length) query = `?${params.join('&')}`;

    return this.request(`/scans${query}`);
  }

  async createScan(scanData) {
    return this.request('/scans', {
      method: 'POST',
      body: JSON.stringify(scanData),
    });
  }

  async updateScan(id, scanData) {
    return this.request(`/scans/${id}`, {
      method: 'PUT',
      body: JSON.stringify(scanData),
    });
  }

  async deleteScan(id) {
    return this.request(`/scans/${id}`, {
      method: 'DELETE',
    });
  }

  async launchScan(id) {
    return this.request(`/scans/${id}/launch`, {
      method: 'POST',
    });
  }

  // Signals Endpoints
  async getSignals() {
    return this.request('/signals');
  }

  async createSignal(signalData) {
    return this.request('/signals', {
      method: 'POST',
      body: JSON.stringify(signalData),
    });
  }

  // Findings Endpoints
  async getFindings() {
    return this.request('/findings');
  }

  async createFinding(findingData) {
    return this.request('/findings', {
      method: 'POST',
      body: JSON.stringify(findingData),
    });
  }

  // Vulnerabilities Endpoints
  async getVulnerabilities(assetId = null) {
    const query = assetId ? `?asset_id=${assetId}` : '';
    return this.request(`/vulnerabilities${query}`);
  }

  async getVulnerability(id) {
    return this.request(`/vulnerabilities/${id}`);
  }

  async updateVulnerability(id, vulnData) {
    return this.request(`/vulnerabilities/${id}`, {
      method: 'PUT',
      body: JSON.stringify(vulnData),
    });
  }

  async deleteVulnerability(id) {
    return this.request(`/vulnerabilities/${id}`, {
      method: 'DELETE',
    });
  }

  async getAiAnalysis(id) {
    return this.request(`/vulnerabilities/${id}/ai-analysis`, {
      method: 'POST',
    });
  }


  // Recommendations Endpoints
  async getRecommendations(vulnerabilityId = null) {
    const query = vulnerabilityId ? `?vulnerability_id=${vulnerabilityId}` : '';
    return this.request(`/recommendations${query}`);
  }

  async getRecommendation(id) {
    return this.request(`/recommendations/${id}`);
  }

  async updateRecommendation(id, recData) {
    return this.request(`/recommendations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(recData),
    });
  }

  async deleteRecommendation(id) {
    return this.request(`/recommendations/${id}`, {
      method: 'DELETE',
    });
  }
}

export const api = new ApiService();
export default api;
