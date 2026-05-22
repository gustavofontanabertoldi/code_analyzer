import os
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass


MAVEN_NAMESPACE = "http://maven.apache.org/POM/4.0.0"
MAVEN_NS = {"m": MAVEN_NAMESPACE}
MAVEN_TAG = f"{{{MAVEN_NAMESPACE}}}"


@dataclass
class DatabaseDetection:
    has_database: bool = False
    source: str | None = None
    trigger: str | None = None


def detect_spring_boot_version(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")
    if not os.path.exists(pom_path):
        return None

    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        parent = root.find("m:parent", MAVEN_NS)
        if parent is not None:
            group_id = parent.find("m:groupId", MAVEN_NS)
            artifact_id = parent.find("m:artifactId", MAVEN_NS)
            version = parent.find("m:version", MAVEN_NS)
            if group_id is not None and artifact_id is not None and version is not None:
                artifact_text = artifact_id.text or ""
                if group_id.text == "org.springframework.boot" and "spring-boot" in artifact_text:
                    return version.text

        properties = root.find("m:properties", MAVEN_NS)
        if properties is not None:
            spring_version = properties.find("m:spring-boot.version", MAVEN_NS)
            if spring_version is not None:
                return spring_version.text

        return None
    except Exception as e:
        print(f"Erro detectando versao Spring: {e}")
        return None


def _parse_pom(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")
    if not os.path.exists(pom_path):
        return None

    try:
        return ET.parse(pom_path).getroot()
    except Exception as e:
        print(f"Erro lendo pom.xml: {e}")
        return None


def _pom_text(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")
    if not os.path.exists(pom_path):
        return ""

    try:
        with open(pom_path, "r", encoding="utf-8") as f:
            return f.read().lower()
    except Exception as e:
        print(f"Erro lendo pom.xml: {e}")
        return ""


def detect_project_framework(repo_path):
    pom_content = _pom_text(repo_path)
    if "quarkus-maven-plugin" in pom_content or "<packaging>quarkus</packaging>" in pom_content:
        return "quarkus"
    if "spring-boot-maven-plugin" in pom_content or "spring-boot-starter" in pom_content:
        return "spring-boot"
    return "maven"


def _pom_property(root, property_name):
    if root is None:
        return None

    properties = root.find("m:properties", MAVEN_NS)
    if properties is None:
        return None

    element = properties.find(f"m:{property_name}", MAVEN_NS)
    if element is not None and element.text:
        return element.text.strip()
    return None


def detect_required_java_version(repo_path):
    root = _parse_pom(repo_path)
    candidates = [
        _pom_property(root, "maven.compiler.release"),
        _pom_property(root, "java.version"),
        _pom_property(root, "maven.compiler.target"),
        _pom_property(root, "maven.compiler.source"),
    ]

    for candidate in candidates:
        if not candidate:
            continue
        match = re.match(r"^(?:1\.)?(\d+)", candidate)
        if match:
            return int(match.group(1))

    return None


def detect_current_java_version():
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            check=False,
        )
        output = f"{result.stdout}\n{result.stderr}"
        match = re.search(r'version "(\d+)(?:\.(\d+))?', output)
        if not match:
            return None
        major = int(match.group(1))
        if major == 1 and match.group(2):
            return int(match.group(2))
        return major
    except Exception as e:
        print(f"Erro detectando Java atual: {e}")
        return None


def validate_java_compatibility(repo_path):
    required = detect_required_java_version(repo_path)
    current = detect_current_java_version()

    if required is None or current is None:
        return True, required, current

    return current >= required, required, current


def choose_java_version(spring_version):
    if spring_version is None:
        return 17

    match = re.match(r"^(\d+)(?:\.(\d+))?", spring_version.strip())
    if not match:
        print(f"[AVISO] Versao Spring inesperada ({spring_version}). Usando Java 17.")
        return 17

    major = int(match.group(1))
    minor = int(match.group(2) or 0)

    if major == 1:
        return 8
    if major == 2 and minor <= 4:
        return 11
    if major == 2:
        return 17
    if major >= 3:
        return 17

    return 17


def _resources_dir(repo_path):
    return os.path.join(repo_path, "src", "main", "resources")


def _read_lower(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().lower()


def _read_properties(path):
    properties = {}
    if not os.path.exists(path):
        return properties

    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                properties[key.strip()] = value.strip()
    except Exception as e:
        print(f"Erro lendo propriedades em {path}: {e}")

    return properties


def detect_active_profile(repo_path):
    env_profile = os.environ.get("SPRING_PROFILES_ACTIVE")
    if env_profile:
        return env_profile.split(",")[0].strip()

    application_path = os.path.join(_resources_dir(repo_path), "application.properties")
    properties = _read_properties(application_path)
    profile = properties.get("spring.profiles.active")
    if profile:
        return profile.split(",")[0].strip()

    return None


def detect_server_port(repo_path):
    resources_dir = _resources_dir(repo_path)
    port = "8080"

    application_path = os.path.join(resources_dir, "application.properties")
    base_properties = _read_properties(application_path)
    if base_properties.get("server.port"):
        port = base_properties["server.port"]

    profile = detect_active_profile(repo_path)
    if profile:
        profile_path = os.path.join(resources_dir, f"application-{profile}.properties")
        profile_properties = _read_properties(profile_path)
        if profile_properties.get("server.port"):
            port = profile_properties["server.port"]

    return port


def detect_server_url(repo_path):
    port = detect_server_port(repo_path)
    return f"http://localhost:{port}"


def _find_database_signal_in_config(resources_dir):
    db_signals = [
        "spring.datasource.url",
        "spring.datasource.username",
        "spring.jpa.hibernate",
        "ddl-auto",
        "datasource:",
        "hibernate:",
    ]

    config_names = [
        "application.properties",
        "application.yml",
        "application.yaml",
        "application-dev.properties",
        "application-dev.yml",
        "application-dev.yaml",
        "application-test.properties",
        "application-test.yml",
        "application-test.yaml",
    ]

    for config_name in config_names:
        config_path = os.path.join(resources_dir, config_name)
        if not os.path.exists(config_path):
            continue

        try:
            content = _read_lower(config_path)
            for signal in db_signals:
                if signal in content:
                    return DatabaseDetection(True, config_name, signal)
        except Exception as e:
            print(f"Erro lendo {config_name}: {e}")

    return DatabaseDetection()


def _find_database_signal_in_pom(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")
    if not os.path.exists(pom_path):
        return DatabaseDetection()

    drivers = [
        "mysql",
        "postgresql",
        "oracle",
        "sqlserver",
        "mariadb",
        "spring-boot-starter-data-jpa",
        "spring-boot-starter-jdbc",
    ]

    try:
        pom_content = _read_lower(pom_path)
        for driver in drivers:
            if driver in pom_content:
                return DatabaseDetection(True, "pom.xml", driver)
    except Exception as e:
        print(f"Erro lendo pom.xml: {e}")

    return DatabaseDetection()


def detect_database_usage(repo_path):
    resources_dir = _resources_dir(repo_path)
    config_detection = _find_database_signal_in_config(resources_dir)
    if config_detection.has_database:
        print(
            "[DETECTOR] Banco encontrado em "
            f"{config_detection.source} (gatilho: '{config_detection.trigger}')."
        )
        return config_detection

    pom_detection = _find_database_signal_in_pom(repo_path)
    if pom_detection.has_database:
        print(
            "[DETECTOR] Banco encontrado em "
            f"{pom_detection.source} (gatilho: '{pom_detection.trigger}')."
        )
        return pom_detection

    return DatabaseDetection()


def _write_h2_properties(resources_dir):
    os.makedirs(resources_dir, exist_ok=True)
    properties_path = os.path.join(resources_dir, "application-test.properties")
    h2_properties = [
        "# Configuracoes de teste injetadas pelo auditor",
        "spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;MODE=MySQL",
        "spring.datasource.driverClassName=org.h2.Driver",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.database-platform=org.hibernate.dialect.H2Dialect",
        "spring.h2.console.enabled=false",
        "spring.jpa.hibernate.ddl-auto=update",
        "",
    ]

    with open(properties_path, "w", encoding="utf-8") as f:
        f.write("\n".join(h2_properties))


def _ensure_h2_dependency(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")
    if not os.path.exists(pom_path):
        print("[AVISO] pom.xml nao encontrado. Nao foi possivel injetar H2.")
        return False

    ET.register_namespace("", MAVEN_NAMESPACE)
    tree = ET.parse(pom_path)
    root = tree.getroot()
    pom_str = ET.tostring(root, encoding="utf-8").decode("utf-8").lower()
    if "com.h2database" in pom_str:
        return True

    dependencies_node = root.find("m:dependencies", MAVEN_NS)
    if dependencies_node is None:
        dependencies_node = ET.SubElement(root, f"{MAVEN_TAG}dependencies")

    dependency_node = ET.SubElement(dependencies_node, f"{MAVEN_TAG}dependency")
    group_id = ET.SubElement(dependency_node, f"{MAVEN_TAG}groupId")
    group_id.text = "com.h2database"
    artifact_id = ET.SubElement(dependency_node, f"{MAVEN_TAG}artifactId")
    artifact_id.text = "h2"
    scope = ET.SubElement(dependency_node, f"{MAVEN_TAG}scope")
    scope.text = "runtime"

    tree.write(pom_path, encoding="utf-8", xml_declaration=True)
    print("[SUCESSO] Dependencia do H2 injetada no pom.xml.")
    return True


def prepare_h2_test_database(repo_path):
    """
    Prepara um perfil de teste com H2 sem apagar as configuracoes originais.
    """
    print("[INFRA] Preparando Banco de Dados H2 em memoria para testes...")

    try:
        _write_h2_properties(_resources_dir(repo_path))
        return _ensure_h2_dependency(repo_path)
    except Exception as e:
        print(f"[AVISO] Erro preparando H2 para testes: {e}")
        return False


def force_h2_in_memory_database(repo_path):
    return prepare_h2_test_database(repo_path)
