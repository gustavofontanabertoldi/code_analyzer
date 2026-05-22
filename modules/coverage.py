import os
import subprocess
import xml.etree.ElementTree as ET

from config import TEMP_DIR
from utils.project_detector import validate_java_compatibility


MAVEN_NAMESPACE = "http://maven.apache.org/POM/4.0.0"
MAVEN_NS = {"m": MAVEN_NAMESPACE}
MAVEN_TAG = f"{{{MAVEN_NAMESPACE}}}"


def inject_jacoco_if_missing(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")
    if not os.path.exists(pom_path):
        return

    try:
        ET.register_namespace("", MAVEN_NAMESPACE)
        tree = ET.parse(pom_path)
        root = tree.getroot()

        pom_str = ET.tostring(root, encoding="utf-8").decode("utf-8").lower()
        if "jacoco" in pom_str:
            print("[INFO] JaCoCo ja esta configurado ou mencionado no pom.xml do alvo.")
            return

        print("[CONFIG] JaCoCo nao detectado no alvo. Injetando plugin dinamicamente...")

        build_node = root.find("m:build", MAVEN_NS)
        if build_node is None:
            build_node = ET.SubElement(root, f"{MAVEN_TAG}build")

        plugins_node = build_node.find("m:plugins", MAVEN_NS)
        if plugins_node is None:
            plugins_node = ET.SubElement(build_node, f"{MAVEN_TAG}plugins")

        plugin_node = ET.SubElement(plugins_node, f"{MAVEN_TAG}plugin")
        group_id = ET.SubElement(plugin_node, f"{MAVEN_TAG}groupId")
        group_id.text = "org.jacoco"
        artifact_id = ET.SubElement(plugin_node, f"{MAVEN_TAG}artifactId")
        artifact_id.text = "jacoco-maven-plugin"
        version = ET.SubElement(plugin_node, f"{MAVEN_TAG}version")
        version.text = "0.8.12"

        executions = ET.SubElement(plugin_node, f"{MAVEN_TAG}executions")
        prepare_execution = ET.SubElement(executions, f"{MAVEN_TAG}execution")
        prepare_goals = ET.SubElement(prepare_execution, f"{MAVEN_TAG}goals")
        prepare_goal = ET.SubElement(prepare_goals, f"{MAVEN_TAG}goal")
        prepare_goal.text = "prepare-agent"

        report_execution = ET.SubElement(executions, f"{MAVEN_TAG}execution")
        report_id = ET.SubElement(report_execution, f"{MAVEN_TAG}id")
        report_id.text = "report"
        report_phase = ET.SubElement(report_execution, f"{MAVEN_TAG}phase")
        report_phase.text = "test"
        report_goals = ET.SubElement(report_execution, f"{MAVEN_TAG}goals")
        report_goal = ET.SubElement(report_goals, f"{MAVEN_TAG}goal")
        report_goal.text = "report"

        tree.write(pom_path, encoding="utf-8", xml_declaration=True)
        print("[SUCESSO] Plugin JaCoCo injetado com sucesso no pom.xml.")
    except Exception as e:
        print(f"[AVISO] Falha ao tentar injetar JaCoCo dinamicamente: {e}")


def run_coverage_analysis(repo_path):
    print("Iniciando analise de cobertura com JaCoCo...")

    java_ok, required_java, current_java = validate_java_compatibility(repo_path)
    if not java_ok:
        print(
            "Cobertura ignorada: o projeto exige "
            f"Java {required_java}, mas o Java atual e {current_java}."
        )
        return None

    inject_jacoco_if_missing(repo_path)

    os.makedirs(TEMP_DIR, exist_ok=True)
    log_path = os.path.join(TEMP_DIR, "coverage.log")

    try:
        cmd = ["mvn", "clean", "test", "jacoco:report"]
        with open(log_path, "w", encoding="utf-8") as log_file:
            subprocess.run(
                cmd,
                cwd=repo_path,
                shell=True,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                check=True,
            )
    except subprocess.CalledProcessError:
        print("\n[AVISO] O Maven retornou um codigo de erro durante os testes.")
        print("Tentando verificar se o relatorio foi gerado mesmo assim...")
        print(f"Consulte o log em: {log_path}")

    xml_path = os.path.join(repo_path, "target", "site", "jacoco", "jacoco.xml")

    if not os.path.exists(xml_path):
        print("[ERRO] Relatorio jacoco.xml nao foi gerado.")
        print(f"Consulte o log em: {log_path}")
        return None

    results = {}
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for package in root.findall("package"):
            for sourcefile in package.findall("sourcefile"):
                file_name = sourcefile.get("name")
                line_counter = sourcefile.find("counter[@type='LINE']")

                if line_counter is not None:
                    missed = int(line_counter.get("missed"))
                    covered = int(line_counter.get("covered"))
                    total = missed + covered
                    coverage_percent = (covered / total) * 100 if total > 0 else 0.0

                    results[file_name] = {
                        "covered_lines": covered,
                        "total_lines": total,
                        "percentage": coverage_percent,
                    }
        return results
    except Exception as e:
        print(f"[ERRO] Falha ao ler o XML do JaCoCo: {e}")
        return None
