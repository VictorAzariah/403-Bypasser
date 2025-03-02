# 403-Bypasser
🚀 A security tool designed to bypass 403 Forbidden responses and check archived URLs from the Wayback Machine.

# Manual
## Installation

This command will clone the GitHub repository into the folder `403-Bypasser`:

```bash
git clone https://github.com/VictorAzariah/403-Bypasser
```

Use this command to enter the `403-Bypasser` folder:

```bash
cd 403-Bypasser
```

This command will install the required python packages to run `403-Bypasser` tool:

```bash
pip install -r requirements.txt
```

## **Usage**  
```bash
python 403-Bypasser.py [-h HELP] [-u URL] [-p PATH] [-z USER_AGENT] [--proxy PROXY_URL] [-k INSECURE] [-v VERBOSE] [-wb WAYBACK_MACHINE] [-o OUTPUT]
```

### **Arguments**
| Flag | Description |
|------|------------|
| `-u, --url` | The URL or domain to bypass. |
| `-p, --path` | The path to bypass. |
| `-z, --user-agent` | Custom or random User-Agent (`-z 'Custom-Agent'` for custom, `-z` for random). |
| `--proxy PROXY_URL` | Proxy to use for requests `[http(s)://host:port]`. |
| `-k, --insecure` | Allow insecure server connections. |
| `-v, --verbose` | Increase verbosity of results. |
| `-wb, --wayback-machine` | Check a domain or URL in the Wayback Machine. |
| `-o, --output` | Save Wayback Machine results to a file. |

## **Examples**
### **Basic 403 Bypass**
```bash
python 403-Bypasser.py -u https://example.com -p admin
```

### **Use a Proxy**
```bash
python 403-Bypasser.py -u https://example.com -p admin --proxy http://127.0.0.1:8080
```

### **Fetch URLs from Wayback Machine**
```bash
python 403-Bypasser.py -wb example.com
```

### **Save Wayback Results**
```bash
python 403-Bypasser.py -wb example.com -o results.txt
```

Here’s a screenshot of 403-Bypasser in action:

![403-Bypasser Screenshot](https://github.com/VictorAzariah/403-Bypasser/blob/main/Screenshot.png)

## **License**
This project is licensed under the **Apache License 2.0**. See the [LICENSE](https://github.com/VictorAzariah/403-Bypasser/blob/main/LICENSE) file for details.  

## **Disclaimer**
🔴 **For educational and security research purposes only.**  
Unauthorized testing on systems **without permission** is illegal. Use responsibly.
