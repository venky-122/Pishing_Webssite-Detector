# feature_extraction.py
import re
from urllib.parse import urlparse

SHORTENER_DOMAINS = {
    "bit.ly","tinyurl.com","goo.gl","t.co","ow.ly","buff.ly","adf.ly","bit.do",
    "is.gd","cutt.ly","tiny.cc"
}

IP_REGEX = re.compile(
    r"^(?:http[s]?://)?(?:(?:\d{1,3}\.){3}\d{1,3})(?:[:/]|$)"
)

def has_ip(url: str) -> int:
    return 1 if IP_REGEX.search(url) else 0

def has_at_symbol(url: str) -> int:
    return 1 if "@" in url else 0

def has_https_token_in_domain(url: str) -> int:
    # Checks if 'https' appears in the domain part to trick users
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        return 1 if "https" in parsed.netloc.lower() else 0
    except:
        return 0

def is_using_shortener(url: str) -> int:
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        domain = parsed.netloc.lower().replace("www.", "")
        return 1 if domain in SHORTENER_DOMAINS else 0
    except:
        return 0

def count_dots(url: str) -> int:
    return url.count(".")

def url_length(url: str) -> int:
    return len(url)

def has_dash_in_domain(url: str) -> int:
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        domain = parsed.netloc.lower()
        return 1 if "-" in domain else 0
    except:
        return 0

def has_port(url: str) -> int:
    # looks for :port in netloc
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        return 1 if ":" in parsed.netloc and not parsed.netloc.endswith(":") else 0
    except:
        return 0

def num_subdomains(url: str) -> int:
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        domain = parsed.netloc.lower().replace("www.", "")
        parts = domain.split(".")
        # If domain like sub.test.co.in -> more than 2 indicates subdomains
        return max(0, len(parts) - 2)
    except:
        return 0

def has_https_scheme(url: str) -> int:
    if url.startswith("https://"):
        return 1
    # if user omitted scheme, check after parse
    try:
        parsed = urlparse(url if url.startswith("http") else "http://" + url)
        return 1 if parsed.scheme == "https" else 0
    except:
        return 0

def extract_features_from_url(url: str) -> dict:
    """Return a dict of features in a deterministic order/names."""
    return {
        "url_length": url_length(url),
        "num_dots": count_dots(url),
        "has_at": has_at_symbol(url),
        "has_https_scheme": has_https_scheme(url),
        "has_https_token_in_domain": has_https_token_in_domain(url),
        "is_shortened": is_using_shortener(url),
        "has_ip": has_ip(url),
        "has_dash": has_dash_in_domain(url),
        "has_port": has_port(url),
        "subdomain_count": num_subdomains(url)
    }

# the exact ordered list of features (important for DataFrame columns)
FEATURE_COLUMNS = [
    "url_length",
    "num_dots",
    "has_at",
    "has_https_scheme",
    "has_https_token_in_domain",
    "is_shortened",
    "has_ip",
    "has_dash",
    "has_port",
    "subdomain_count"
]
