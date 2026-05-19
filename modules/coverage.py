import subprocess
import os
import xml.etree.ElementTree as ET

def run_coverage_analysis(repo_path):
    print("Iniciando análise de cobertura com JaCoCo...")
    
    #Executa o Maven no repositório alvo para rodar os testes e gerar o report
    try:
        cmd = ["mvn", "clean", "test", "jacoco:report"]
        subprocess.run(cmd, cwd=repo_path, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Aviso: Falha ao rodar os testes do Maven ou o JaCoCo não está configurado no alvo.")
        return None

    #Path padrão onde o JaCoCo gera o relatório XML
    xml_path = os.path.join(repo_path, "target", "site", "jacoco", "jacoco.xml")
    
    if not os.path.exists(xml_path):
        print("Relatório jacoco.xml não encontrado.")
        return None

    #Parseia o XML para extrair os dados reais
    results = {}
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Percorre cada classe (arquivo) descrita no relatório do JaCoCo
    for package in root.findall("package"):
        for sourcefile in package.findall("sourcefile"):
            file_name = sourcefile.get("name")
            
            #Procura pelo contador de linhas (LINE)
            line_counter = sourcefile.find("counter[@type='LINE']")
            
            if line_counter is not None:
                missed = int(line_counter.get("missed"))
                covered = int(line_counter.get("covered"))
                total = missed + covered
                
                #Calcula a porcentagem real de linhas cobertas
                coverage_percent = (covered / total) * 100 if total > 0 else 0.0
                
                results[file_name] = {
                    "covered_lines": covered,
                    "total_lines": total,
                    "percentage": coverage_percent
                }

    return results