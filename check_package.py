import json

def check_package(package_name, package_json_path="package.json", lock_json_path="package-lock.json"):
    try:
        with open(package_json_path, "r") as f:
            package_data = json.load(f)
        with open(lock_json_path, "r") as f:
            lock_data = json.load(f)

        result = {}

        # Check in package.json
        if package_name in package_data.get("dependencies", {}):
            result["package.json"] = package_data["dependencies"][package_name]
        elif package_name in package_data.get("devDependencies", {}):
            result["package.json"] = package_data["devDependencies"][package_name]

        # Check in package-lock.json (npm v7+ uses "packages")
        lock_deps = lock_data.get("dependencies", {})
        if package_name in lock_deps:
            result["package-lock.json"] = lock_deps[package_name].get("version", "unknown")

        # Also check "packages" section
        lock_packages = lock_data.get("packages", {})
        node_modules_key = f"node_modules/{package_name}"
        if node_modules_key in lock_packages:
            result["package-lock.json"] = lock_packages[node_modules_key].get("version", "unknown")

        return result if result else None

    except FileNotFoundError as e:
        return {"error": f"File not found -> {e.filename}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in package.json or package-lock.json"}


if __name__ == "__main__":
    packages_to_check = [
        "@babel/code-frame",  # will be found here
        "axios"
    ]

    for pkg in packages_to_check:
        result = check_package(pkg)
        if result:
            print(f"\033[91m{pkg}: {result}\033[0m")  # 🔴 red if found
        else:
            print(f"\033[92m{pkg}: not found\033[0m")  # 🟢 green if not found
