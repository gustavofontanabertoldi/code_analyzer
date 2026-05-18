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