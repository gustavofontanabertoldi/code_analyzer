import os
import xml.etree.ElementTree as ET

def detect_spring_boot_version(repo_path):
    pom_path = os.path.join(repo_path, "pom.xml")

    if not os.path.exists(pom_path):
        return None
    
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()

        namespace = {
            "m":"http://maven.apache.org/POM/4.0.0"
        }

        parent = root.find("m:parent", namespace)

        if parent is not None:
            group_id = parent.find("m:groupId", namespace)
            artifact_id = parent.find("m:artifactId", namespace)
            version = parent.find("m:version", namespace)

            if (
                group_id is not None
                and artifact_id is not None
                and version is not None
            ):
                if(
                    group_id.text == "org.springframework.boot"
                    and "spring-boot" in artifact_id.text
                ):
                    return version.text
        
        return None
    except Exception as e:
        print(f"Erro detectactando versão spring: {e}")
        return None
    
def choose_java_version(spring_version):

    if spring_version is None:
        return 17
    
    major = int(spring_version.split(".")[0])

    if major == 1:
        return 8
    
    if major == 2:
        minor = int(spring_version.split(".")[1])
        if minor <= 4:
            return 11
        return 17
    
    if major >= 3:
        return 21
    
    return 17

def detect_database_usage(repo_path):

    suspects = [
        "mysql",
        "postgresql",
        "spring-boot-starter-data-jpa",
        "hibernate"
    ]

    # -------------------------
    # Verifica pom.xml
    # -------------------------

    pom_path = os.path.join(repo_path, "pom.xml")

    if os.path.exists(pom_path):
        try:
            with open(pom_path, "r", encoding="utf-8") as f:
                pom_content = f.read().lower()
            
            for suspect in suspects:
                if suspect in pom_content:
                    return True
            
        except Exception as e:
            print(f"Erro lendo pom.xml: {e}")
        
    # -------------------------
    # Verifica application.properties
    # -------------------------

    properties_path = os.path.join(
        repo_path,
        "src",
        "main",
        "resources",
        "application.properties"
    )

    if os.path.exists(properties_path):
        try:
            with open(properties_path, "r", encoding="utf-8") as f:
                content = f.read().lower()

            db_signals = [
                "spring.datasource.url",
                "spring.datasource.username",
                "spring.jpa.hibernate",
                "ddl-auto"
            ]

            for signal in db_signals:
                if signal in content:
                    return True
        except Exception as e:
            print(f"Erro lendo aplications.properties: {e}")
    
    # -------------------------
    # Verifica application.yml
    # -------------------------

    yml_path = os.path.join(
        repo_path,
        "src",
        "main",
        "resources",
        "application.yml"
    )

    if os.path.exists(yml_path):
        try:
            with open(yml_path, "r", encoding="utf-8") as f:
                yml_content = f.read().lower()

            yml_signals = [
                "datasource:",
                "hibernate:",
                "ddl-auto:"
            ]

            for signal in yml_signals:
                if signal in yml_content:
                    return True
        except Exception as e:
            print(f"Erro lendo application.yml: {e}")
    
    return False