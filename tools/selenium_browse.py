# Seleniumでページを閲覧・HTML取得するツール
#
# 使い方:
#   起動:     py -3.14 tools/selenium_browse.py open [URL]
#   HTML取得: py -3.14 tools/selenium_browse.py html
#   URL移動:  py -3.14 tools/selenium_browse.py go <URL>
#   終了:     py -3.14 tools/selenium_browse.py close
#
# 初回はopenでブラウザを起動。以降はhtml/goで操作。
# ログインが必要なら手動でログインしてからhtmlを実行。

import sys
import time
import json
from pathlib import Path
from urllib.request import urlopen

SELENIUM_PROFILE = str(Path(__file__).parent.parent / ".selenium-profile")
OUT_PATH = Path(__file__).parent / "page_dump.html"
CDP_PORT = 9222

def open_browser(url):
    """ブラウザをリモートデバッグ付きで起動"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opts = Options()
    opts.add_argument(f"--user-data-dir={SELENIUM_PROFILE}")
    opts.add_argument(f"--remote-debugging-port={CDP_PORT}")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    print(f"[OK] ブラウザ起動: {url}")
    print(f"[INFO] ログインが必要なら手動でログインしてください。")
    print(f"[INFO] HTMLを取得: py -3.14 tools/selenium_browse.py html")

def get_driver_existing():
    """既に起動しているブラウザに接続"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opts = Options()
    opts.add_experimental_option("debuggerAddress", f"127.0.0.1:{CDP_PORT}")
    driver = webdriver.Chrome(options=opts)
    return driver

def dump_html():
    """現在のページのHTMLを取得してファイルに保存"""
    driver = get_driver_existing()
    html = driver.page_source
    current_url = driver.current_url
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] HTML保存: {OUT_PATH} ({len(html)} bytes)")
    print(f"[INFO] URL: {current_url}")

def go_url(url):
    """指定URLに移動してHTML取得"""
    driver = get_driver_existing()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    current_url = driver.current_url
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] 移動+HTML保存: {OUT_PATH} ({len(html)} bytes)")
    print(f"[INFO] URL: {current_url}")

def close_browser():
    """ブラウザを閉じる"""
    try:
        driver = get_driver_existing()
        driver.quit()
        print("[OK] ブラウザを閉じました。")
    except Exception as e:
        print(f"[INFO] ブラウザは既に閉じています: {e}")

def main():
    if len(sys.argv) < 2:
        print("使い方:")
        print("  open [URL]  - ブラウザ起動")
        print("  html        - HTML取得")
        print("  go <URL>    - URL移動+HTML取得")
        print("  close       - ブラウザ終了")
        return

    cmd = sys.argv[1]

    if cmd == "open":
        url = sys.argv[2] if len(sys.argv) > 2 else "https://appstoreconnect.apple.com/agreements"
        open_browser(url)
    elif cmd == "html":
        dump_html()
    elif cmd == "go":
        if len(sys.argv) < 3:
            print("[ERROR] URLを指定してください")
            return
        go_url(sys.argv[2])
    elif cmd == "close":
        close_browser()
    else:
        print(f"[ERROR] 不明なコマンド: {cmd}")

if __name__ == "__main__":
    main()
