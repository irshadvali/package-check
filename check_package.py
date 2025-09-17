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

        # Check in package-lock.json
        if package_name in lock_data.get("dependencies", {}):
            dep_info = lock_data["dependencies"][package_name]
            result["package-lock.json"] = dep_info.get("version", "unknown")

        return result if result else None

    except FileNotFoundError as e:
        return {"error": f"File not found -> {e.filename}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in package.json or package-lock.json"}


if __name__ == "__main__":
    packages_to_check = [
        "angulartics2",
        "@ctrl/deluge",
        "@ctrl/golang-template",
        "@ctrl/magnet-link",
        "@ctrl/ngx-codemirror",
        "@ctrl/ngx-csv",
        "@ctrl/ngx-emoji-mart",
        "@ctrl/ngx-rightclick",
        "@ctrl/qbittorrent",
        "@ctrl/react-adsense",
        "@ctrl/shared-torrent",
        "@ctrl/tinycolor",
        "@ctrl/torrent-file",
        "@ctrl/transmission",
        "@ctrl/ts-base32",
        "encounter-playground",
        "json-rules-engine-simplified",
        "koa2-swagger-ui",
        "@nativescript-community/gesturehandler",
        "@nativescript-community/sentry",
        "@nativescript-community/text",
        "@nativescript-community/ui-collectionview",
        "@nativescript-community/ui-drawer",
        "@nativescript-community/ui-image",
        "@nativescript-community/ui-material-bottomsheet",
        "@nativescript-community/ui-material-core",
        "@nativescript-community/ui-material-core-tabs",
        "ngx-color",
        "ngx-toastr",
        "ngx-trend",
        "react-complaint-image",
        "react-jsonschema-form-conditionals",
        "react-jsonschema-form-extras",
        "rxnt-authentication",
        "rxnt-healthchecks-nestjs",
        "rxnt-kue",
        "swc-plugin-component-annotate",
        "ts-gaussian",
        "axios",
    ]

    for pkg in packages_to_check:
        result = check_package(pkg)
        if result:
            print(f"\033[91m{pkg}: {result}\033[0m")  # 🔴 red if found
        else:
            print(f"\033[92m{pkg}: not found\033[0m")  # 🟢 green if not found
