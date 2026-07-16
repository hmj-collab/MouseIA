# Diretrizes de Segurança do Mouse IA

## 1. Objetivo

Este documento estabelece as diretrizes de segurança para o desenvolvimento, operação e evolução da plataforma Mouse IA. A proposta é proteger usuários, dados, integrações e fluxos de análise, considerando o contexto de uma solução voltada a segurança, vulnerabilidades e gestão de ativos.

## 2. Princípios gerais

- Segurança deve ser tratada como requisito desde o início do projeto.
- A plataforma deve seguir boas práticas de desenvolvimento seguro.
- Dados sensíveis devem ser protegidos em todos os pontos do ciclo de vida.
- Autenticação, autorização, auditoria, observabilidade e resiliência são fundamentais.
- O sistema deve evoluir com segurança, inclusive com novos módulos e integrações.

## 3. Segurança da arquitetura

A arquitetura do Mouse IA deve considerar:

- separação clara entre frontend, backend, banco de dados e integrações
- camadas bem definidas para reduzir riscos de acoplamento e exposição indevida
- isolamento de módulos de análise, processamento assíncrono e execução de jobs
- mecanismos de auditoria e rastreabilidade para operações críticas

## 4. Proteção de dados

### Dados sensíveis

Os seguintes dados devem receber proteção especial:

- credenciais de acesso
- tokens e chaves de API
- informações de empresas, sites e ativos
- URLs, ambientes e dados operacionais
- logs que possam conter informações sensíveis

### Regras recomendadas

- nunca armazenar segredos diretamente no código-fonte
- usar variáveis de ambiente ou gerenciadores seguros de segredos
- aplicar criptografia em dados sensíveis sempre que necessário
- evitar exposição de detalhes internos em mensagens de erro
- aplicar políticas de retenção e descarte seguro de dados

## 5. Autenticação e autorização

### Autenticação

A plataforma deve utilizar mecanismos seguros de autenticação, com foco em:

- autenticação por identidade e senha com boas práticas de segurança
- uso de tokens com expiração controlada e revogação possível
- proteção contra força bruta e uso indevido de credenciais

#### Implementação atual

O backend emite tokens JWT Bearer assinados com HS256, com expiração de uma hora. A chave deve ser fornecida pela variável de ambiente `JWT_SECRET_KEY` em qualquer ambiente compartilhado ou de produção. Na ausência dela, há uma chave padrão exclusivamente para desenvolvimento local.

Os usuários `admin` e `viewer`, ambos com a senha `password123`, existem apenas para desenvolvimento e testes; não devem ser usados em produção.

### Autorização

Todas as operações devem respeitar controle de acesso por papel e permissão, especialmente em:

- cadastro e alteração de sites
- consulta de achados, vulnerabilidades e relatórios
- acesso a dados empresariais e operacionais
- operações administrativas e de configuração

Atualmente, `admin` pode criar, alterar e excluir Sites e criar Signals e Findings. `viewer` pode consultar Sites, Signals e Findings. Todas essas rotas exigem um token Bearer válido.

## 6. Segurança de APIs

As APIs do Mouse IA devem seguir boas práticas de segurança:

- validar entrada e saída de dados
- aplicar rate limiting e proteção contra abuso
- usar HTTPS em ambientes de produção
- evitar vazamento de detalhes internos em respostas de erro
- validar permissões antes de processar qualquer ação
- usar versionamento e padrões seguros de documentação de endpoints

## 7. Segurança do backend

O backend deve seguir políticas de desenvolvimento seguro:

- evitar uso de bibliotecas desatualizadas
- validar todas as entradas recebidas
- tratar erros sem expor stack traces ou informações internas
- implementar logs seguros, sem exposição de dados sensíveis
- separar regras de negócio de integração com sistemas externos
- aplicar testes de segurança e revisão de código

## 8. Segurança do frontend

O frontend deve evitar:

- exposição de segredos em código do cliente
- armazenamento inseguro de tokens ou dados sensíveis
- uso de mecanismos inseguros para navegação ou renderização
- divulgação de informações internas por meio de erros visuais ou logs do navegador

## 9. Segurança de banco de dados

- usar conexões seguras e credenciais protegidas
- aplicar princípio do menor privilégio para usuários do banco
- evitar queries inseguras e injeção de SQL
- manter migrations e schemas bem controlados
- proteger backups e cópias de dados
- restringir acesso administrativo apenas a perfis autorizados

## 10. Segurança de integrações externas

Integrações com fontes externas como NVD, CISA KEV, repositórios e provedores de infraestrutura devem:

- validar certificados e conexões
- tratar falhas e timeouts com segurança
- limitar permissões das integrações
- registrar tentativas de acesso e erros de comunicação
- aplicar políticas de allowlist quando possível

## 11. Segurança em filas e processamento assíncrono

Processos assíncronos, como scans, análise de sinais e geração de achados, devem:

- executar com isolamento adequado
- evitar processamento não autorizado
- registrar eventos e status de execução
- proteger arquivos temporários e resultados intermediários
- garantir idempotência quando aplicável

## 12. Segurança em logs e auditoria

Logs devem ser usados para rastreabilidade e investigação, com cuidado para não expor dados sensíveis. O sistema deve registrar:

- autenticação e autorização
- criação, atualização e remoção de entidades
- processamento de scans, achados e recomendações
- falhas, exceções e eventos críticos
- alterações de configuração e permissões

## 13. Segurança em ambientes de desenvolvimento e produção

- usar ambientes separados para desenvolvimento, teste e produção
- aplicar diferentes níveis de acesso por ambiente
- manter dependências atualizadas
- revisar configurações de deploy e containers
- não expor serviços internos sem necessidade
- usar políticas de rollback e controle de mudanças

## 14. Boas práticas recomendadas

- aplicar revisão de código com foco em segurança
- usar análise estática e testes de segurança sempre que possível
- manter documentação atualizada sobre variáveis de ambiente e segredos
- revisar permissões de acesso periodicamente
- realizar avaliações de risco para mudanças e novas integrações
- tratar incidentes com processos claros e rastreáveis

## 15. Política de resposta a incidentes

Em caso de incidente, a equipe deve:

- isolar o problema rapidamente
- preservar evidências e logs relevantes
- avaliar impacto sobre usuários, dados e integrações
- corrigir a causa raiz
- documentar a ação e os aprendizados
- comunicar o incidente de forma objetiva às partes afetadas

## 16. Checklist de segurança mínimo

Antes de liberar novas versões, verificar:

- dependências atualizadas e sem vulnerabilidades conhecidas
- segredos fora do repositório
- autenticação e autorização funcionando conforme esperado
- logs sem exposição de dados sensíveis
- APIs com validação e controle de acesso
- ambiente de produção configurado corretamente

## 17. Papéis e responsabilidades

### Responsabilidade da equipe de desenvolvimento

- implementar as diretrizes de segurança no código
- revisar mudanças com foco em segurança
- manter dependências atualizadas
- reportar vulnerabilidades identificadas

### Responsabilidade da equipe de operações

- proteger ambientes de execução
- controlar acesso aos serviços e infraestrutura
- monitorar logs e incidentes
- garantir backup, recuperação e continuidade operacional

### Responsabilidade da liderança técnica

- aprovar mudanças críticas de segurança
- definir prioridades de mitigação
- garantir alinhamento entre desenvolvimento, operações e compliance

## 18. Políticas de acesso por ambiente

### Desenvolvimento

- acesso restrito a desenvolvedores autorizados
- uso de credenciais individuais
- dados sintéticos ou mockados sempre que possível

### Teste

- acesso limitado à equipe envolvida
- ambiente isolado de produção
- dados de teste sem informações reais sensíveis

### Produção

- acesso estritamente controlado
- autenticação multifator quando possível
- auditoria de acessos e alterações
- separação entre funções operacionais e administrativas

## 19. Política de senha e segredos

- senhas devem ser longas, únicas e armazenadas de forma segura
- segredos devem ser gerenciados por ferramentas específicas
- chaves de API não devem ser compartilhadas por canais inseguros
- rotação periódica de credenciais deve ser considerada

## 20. Ameaças e mitigação

### Ameaças comuns

- acesso não autorizado a contas e endpoints
- exposição de segredos em repositórios ou logs
- falhas de validação que permitam injeção ou manipulação de dados
- uso indevido de integrações externas
- indisponibilidade causada por falhas de configuração ou dependências

### Mitigações esperadas

- controle rigoroso de acesso e autenticação
- revisão e validação de entradas e permissões
- monitoramento de logs, falhas e eventos críticos
- uso de ambientes isolados e políticas de rollback
- atualização contínua de dependências e infraestrutura

## 21. Métricas de segurança

A equipe deve acompanhar indicadores como:

- número de vulnerabilidades abertas
- tempo de correção de incidentes
- cobertura de testes e revisão de código
- taxa de sucesso de autenticação e recuperação de acesso
- frequência de atualização de dependências

## 22. Resumo

A segurança do Mouse IA deve ser tratada como uma responsabilidade transversal em toda a plataforma. Desde a modelagem de dados até a integração com fontes externas, cada camada deve ser construída com foco em proteção, rastreabilidade e resiliência.
