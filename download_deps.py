import urllib.request
import json
import os
import ssl
import sys

# Repositories known to host OCP WASM builds
REPOS = [
    "yeicor-3d/OCP.wasm",
    "CadQuery/ocp-build-system",
    "yeicor-3d/yet-another-cad-viewer"
]

DEST_DIR = "web"
DEST_FILE = os.path.join(DEST_DIR, "cadquery_ocp.whl")

def get_wasm_assets():
    print("🔎 Scanning GitHub for available OCP WASM wheels...")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    found_assets = []
    
    for repo in REPOS:
        print(f"   Checking {repo}...")
        url = f"https://api.github.com/repos/{repo}/releases"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response:
                releases = json.loads(response.read())
                
                for release in releases:
                    for asset in release.get('assets', []):
                        name = asset['name']
                        # We are looking for .whl files that mention 'emscripten' or 'wasm'
                        if name.endswith('.whl') and ('emscripten' in name or 'wasm' in name):
                            found_assets.append({
                                'name': name,
                                'url': asset['browser_download_url'],
                                'repo': repo,
                                'tag': release['tag_name'],
                                'size': asset['size'] / (1024*1024)
                            })
        except Exception as e:
            print(f"   ⚠️  Could not access {repo}: {e}")

    return found_assets

def download_asset(url):
    print(f"\n⬇️  Downloading from:\n   {url}")
    
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, context=ctx) as response:
            with open(DEST_FILE, 'wb') as out_file:
                total_size = int(response.info().get('Content-Length', 0))
                block_size = 1024 * 1024 # 1MB chunks
                downloaded = 0
                
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    out_file.write(buffer)
                    
                    # Simple progress bar
                    if total_size > 0:
                        percent = int(downloaded * 100 / total_size)
                        print(f"   {percent}% ({downloaded//(1024*1024)}MB)", end='\r')
                    else:
                        print(f"   {downloaded//(1024*1024)}MB downloaded", end='\r')
                        
        print(f"\n✅ Success! Saved to {os.path.abspath(DEST_FILE)}")
        print("🚀 You can now run 'python run_web.py'")
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")

def main():
    assets = get_wasm_assets()
    
    if not assets:
        print("\n❌ No WASM wheels found! This is very unusual.")
        print("It might be a temporary GitHub API limit or network issue.")
        sys.exit(1)

    print("\n✅ Found the following wheels:")
    print(f"{'#':<3} {'Size (MB)':<10} {'Filename'}")
    print("-" * 60)
    
    # Filter for Python 3.11 (cp311) as it's the most stable for Pyodide right now
    # You can remove this filter if you want to see everything
    recommended = [a for a in assets if 'cp311' in a['name']]
    others = [a for a in assets if 'cp311' not in a['name']]
    
    display_list = recommended + others
    
    for i, asset in enumerate(display_list):
        prefix = "⭐" if asset in recommended else "  "
        print(f"{i+1:<3} {asset['size']:<10.1f} {prefix} {asset['name']}")

    print("-" * 60)
    selection = input("\nEnter the number to download (default 1): ").strip()
    
    if not selection:
        choice = 0
    else:
        try:
            choice = int(selection) - 1
        except ValueError:
            print("Invalid selection.")
            sys.exit(1)

    if 0 <= choice < len(display_list):
        target = display_list[choice]
        download_asset(target['url'])
    else:
        print("Invalid number.")

if __name__ == "__main__":
    main()