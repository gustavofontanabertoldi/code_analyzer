import os
from jinja2 import Template

def generate_results(results, duplications, benchmark, latency, coverage):    
    total_cbo = 0
    max_complexity = 0
    cleaned_results = []
    
    for r in results:
        total_cbo += r['cbo']
        for m in r['complexity']:
            if m['complexity'] > max_complexity:
                max_complexity = m['complexity']
        
        cleaned_results.append({
            "file_full": r['file'],
            "file_short": os.path.basename(r['file']),
            "cbo": r['cbo'],
            "complexity": r['complexity']
        })
                
    avg_cbo = total_cbo / len(results) if results else 0

    total_covered = 0
    total_lines = 0
    if coverage and isinstance(coverage, dict):
        for data in coverage.values():
            total_covered += data['covered_lines']
            total_lines += data['total_lines']
    general_coverage = (total_covered / total_lines) * 100 if total_lines > 0 else 0

    # Critérios de Falha Baseados no Enunciado do Blind Test
    motivos_falha = []
    if avg_cbo > 8: 
        motivos_falha.append("Excesso de acoplamento entre classes (CBO médio elevado)")
    if max_complexity > 20:
        motivos_falha.append("Alta complexidade ciclomática encontrada em métodos críticos")
    if general_coverage < 60: 
        motivos_falha.append("Falta de testes automatizados abrangentes no sistema")

    if motivos_falha:
        status_global = "REPROVADO NA ISO/IEC 25010"
        diagnostico = f"Este código falha na conformidade devido a: {', '.join(motivos_falha)}."
        cor_status = "#dc3545"
    else:
        status_global = "APROVADO"
        diagnostico = "O repositório atende aos critérios mínimos de manutenibilidade e testabilidade avaliados."
        cor_status = "#28a745"

    # Template HTML com correções definitivas de grid e alinhamento
    html_template = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Parecer de Conformidade - ISO/IEC 25010</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f8f9fa; color: #333; }
            .container { max-width: 1100px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h1, h2, h3 { color: #0056b3; border-bottom: 2px solid #dee2e6; padding-bottom: 8px; }
            .status-box { padding: 20px; border-radius: 6px; color: white; font-weight: bold; font-size: 1.2em; margin-bottom: 30px; }
            
            /* Tabela com larguras controladas via CSS clássico */
            table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 30px; background: white; }
            th, td { border: 1px solid #dee2e6; padding: 12px; text-align: left; vertical-align: top; }
            
            th { background-color: #f1f3f5; color: #495057; font-weight: 600; }
            tr:nth-child(even) { background-color: #f8f9fa; }
            
            /* Badges inline robustas */
            .badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; display: inline-block; margin-left: 6px; text-transform: uppercase; }
            .badge-baixo { background-color: #d4edda; color: #155724; }
            .badge-medio { background-color: #fff3cd; color: #856404; }
            .badge-alto { background-color: #f8d7da; color: #721c24; }
            .badge-instavel { background-color: #343a40; color: white; }
            
            /* Container do método em formato de bloco limpo */
            .method-item { margin-bottom: 8px; background: #fdfdfd; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #0056b3; }
            .file-path { font-size: 0.75em; color: #888; display: block; font-weight: normal; margin-top: 4px; word-break: break-all; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Relatório de Auditoria Técnica</h1>
            <p><strong>Norma de Referência:</strong> ISO/IEC 25010 (Manutenibilidade, Eficiência e Confiabilidade)</p>
            
            <div class="status-box" style="background-color: {{ cor_status }};">
                Status Final: {{ status_global }}<br>
                <span style="font-weight: normal; font-size: 0.9em;">{{ diagnostico }}</span>
            </div>

            <h2>Módulo I: Análise de Manutenibilidade (Estática)</h2>
            <p><strong>Duplicações de Código (DRY):</strong> {{ duplications }} bloco(s) idêntico(s) detectado(s).</p>
            
            <h3>Métricas por Arquivo (Complexidade Ciclomática e CBO)</h3>
            <table>
                <thead>
                    <tr>
                        <th style="width: 40%;">Arquivo</th>
                        <th style="width: 15%; text-align: center;">CBO (Acoplamento)</th>
                        <th style="width: 45%;">Métodos Analisados e Complexidade (McCabe)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for file in cleaned_results %}
                    <tr>
                        <td>
                            <strong style="font-size: 1.05em; color: #212529;">{{ file.file_short }}</strong>
                            <span class="file-path">{{ file.file_full }}</span>
                        </td>
                        <td style="text-align: center; font-size: 1.2em; font-weight: bold; color: #495057;">
                            {{ file.cbo }}
                        </td>
                        <td>
                            {% for m in file.complexity %}
                            <div class="method-item">
                                <strong>•</strong> <code>{{ m.method }}</code>: {{ m.complexity }}
                                <span class="badge badge-{{ m.status.strip().lower() }}">{{ m.status.strip() }}</span>
                            </div>
                            {% else %}
                            <span style="color: #8c96a0; font-style: italic; font-size: 0.95em;">Nenhum método detectado ou classe pura de dados.</span>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

            <h2>Módulo II: Eficiência de Desempenho (Dinâmica)</h2>
            <p><strong>Benchmark de Rotas Críticas:</strong> {{ benchmark if benchmark else 'Nenhum dado coletado.' }}</p>
            
            <h3>Comportamento da Latência sob Estresse</h3>
            <table>
                <thead>
                    <tr>
                        <th>Carga (Requisições)</th>
                        <th>Tempo Médio por Req.</th>
                        <th>% de Degradação (Aumento de Latência)</th>
                    </tr>
                </thead>
                <tbody>
                    {% if latency %}
                        {% for load, data in latency.items() %}
                        <tr>
                            <td><strong>{{ load }}</strong></td>
                            <td>{{ "%.4f"|format(data.avg_time) }}s</td>
                            <td>
                                {% if load == 100 or load == '100' %}
                                    <span class="badge badge-baixo">Carga Base</span>
                                {% else %}
                                    <span class="badge badge-alto">+{{ "%.2f"|format(data.percent_increase) }}%</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    {% else %}
                        <tr><td colspan="3" style="color: #6c757d; font-style: italic;">Nenhum teste de carga executado devido a salvaguardas de infraestrutura.</td></tr>
                    {% endif %}
                </tbody>
            </table>

            <h2>Módulo III: Confiabilidade e Testabilidade</h2>
            <h3>Cobertura de Linhas Real (JaCoCo)</h3>
            <p><strong>Cobertura Geral do Repositório:</strong> <span class="badge {% if general_coverage >= 60 %}badge-baixo{% else %}badge-alto{% endif %}">{{ "%.2f"|format(general_coverage) }}%</span></p>
            
            <table>
                <thead>
                    <tr>
                        <th>Arquivo Java</th>
                        <th>Linhas Cobertas / Totais</th>
                        <th>Porcentagem</th>
                    </tr>
                </thead>
                <tbody>
                    {% if coverage and coverage is mapping %}
                        {% for file_name, data in coverage.items() %}
                        <tr>
                            <td><code>{{ file_name }}</code></td>
                            <td>{{ data.covered_lines }} / {{ data.total_lines }}</td>
                            <td><strong>{{ "%.2f"|format(data.percentage) }}%</strong></td>
                        </tr>
                        {% endfor %}
                    {% else %}
                        <tr><td colspan="3" style="color: #6c757d; font-style: italic;">Nenhum dado do JaCoCo disponível (Fallback acionado com sucesso).</td></tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    template = Template(html_template)
    rendered_html = template.render(
        cleaned_results=cleaned_results,
        duplications=duplications,
        benchmark=benchmark,
        latency=latency,
        coverage=coverage,
        status_global=status_global,
        diagnostico=diagnostico,
        cor_status=cor_status,
        general_coverage=general_coverage
    )

    output_path = "dashboard_qualidade.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    print(f"\n[SUCESSO] Relatório Técnico HTML gerado com sucesso em: {os.path.abspath(output_path)}")