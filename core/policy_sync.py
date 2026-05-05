import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

import requests


POLICY_KEYWORDS = [
    "15分钟",
    "生活圈",
    "公共服务",
    "社区",
    "养老",
    "老年人",
    "医疗",
    "医院",
    "无障碍",
    "慢行",
    "绿地",
    "公园",
    "学校",
    "儿童",
    "教育",
    "交通",
    "旅游",
    "民宿",
    "短租",
    "免税",
    "三亚",
    "海南",
    "自由贸易港",
    "城市更新",
]

DEFAULT_UNKNOWN = "原文信息待补充"


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(value):
    text = unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_policy_sources(config_path):
    path = Path(config_path)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def load_policy_cache(cache_path):
    path = Path(cache_path)
    if not path.exists() or path.stat().st_size == 0:
        return {
            "updated_at": "",
            "records": [],
            "sources": [],
            "last_error": "",
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "updated_at": "",
            "records": [],
            "sources": [],
            "last_error": f"政策缓存读取失败：{exc}",
        }
    if not isinstance(data, dict):
        return {
            "updated_at": "",
            "records": [],
            "sources": [],
            "last_error": "政策缓存格式异常。",
        }
    data.setdefault("updated_at", "")
    data.setdefault("records", [])
    data.setdefault("sources", [])
    data.setdefault("last_error", "")
    return data


def find_keywords(text):
    return [keyword for keyword in POLICY_KEYWORDS if keyword in text]


def find_nearby_date(text):
    patterns = [
        r"20\d{2}[-/.年]\d{1,2}[-/.月]\d{1,2}日?",
        r"20\d{2}年\d{1,2}月",
        r"20\d{2}-\d{1,2}",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return DEFAULT_UNKNOWN


def build_snippet(page_text, title, max_length=180):
    cleaned_page = clean_text(page_text)
    if not cleaned_page:
        return DEFAULT_UNKNOWN
    position = cleaned_page.find(clean_text(title))
    if position < 0:
        return cleaned_page[:max_length]
    start = max(0, position - 40)
    end = min(len(cleaned_page), position + max_length)
    snippet = cleaned_page[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(cleaned_page):
        snippet += "..."
    return snippet


def is_probable_policy_title(title):
    if len(title) < 8 or len(title) > 90:
        return False
    skip_words = ["首页", "搜索", "登录", "注册", "联系我们", "网站地图", "无障碍", "手机版"]
    if any(word == title or title.endswith(word) for word in skip_words):
        return False
    return bool(find_keywords(title)) or any(mark in title for mark in ["政策", "规划", "办法", "通知", "方案", "意见", "条例", "解读"])


def extract_policy_items_from_html(html_text, source, max_items=12):
    page_text = re.sub(r"<script[\s\S]*?</script>", " ", html_text, flags=re.IGNORECASE)
    page_text = re.sub(r"<style[\s\S]*?</style>", " ", page_text, flags=re.IGNORECASE)
    plain_text = clean_text(page_text)
    link_pattern = re.compile(
        r"<a\b[^>]*href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<title>[\s\S]*?)</a>",
        flags=re.IGNORECASE,
    )
    records = []
    seen = set()
    for match in link_pattern.finditer(page_text):
        title = clean_text(match.group("title"))
        if not is_probable_policy_title(title):
            continue
        url = urljoin(source.get("url", ""), match.group("href"))
        identity = (title, url)
        if identity in seen:
            continue
        seen.add(identity)

        nearby = page_text[max(0, match.start() - 260): min(len(page_text), match.end() + 260)]
        publish_date = find_nearby_date(clean_text(nearby))
        snippet = build_snippet(plain_text, title)
        keyword_text = f"{title} {snippet}"
        records.append(
            {
                "title": title or DEFAULT_UNKNOWN,
                "url": url or DEFAULT_UNKNOWN,
                "source_org": source.get("source_org") or DEFAULT_UNKNOWN,
                "source_level": source.get("source_level") or DEFAULT_UNKNOWN,
                "publish_date": publish_date,
                "snippet": snippet or DEFAULT_UNKNOWN,
                "fetched_at": now_text(),
                "keywords": find_keywords(keyword_text),
                "source_name": source.get("name") or DEFAULT_UNKNOWN,
            }
        )
        if len(records) >= max_items:
            break
    return records


def fetch_policy_source(source, timeout=10):
    headers = {
        "User-Agent": "Mozilla/5.0 Qiongdao-Zhihua policy evidence demo",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    response = requests.get(source["url"], headers=headers, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding or "utf-8"
    html_text = response.text
    return extract_policy_items_from_html(html_text, source)


def sync_policy_sources(config_path, cache_path, timeout=10):
    sources = load_policy_sources(config_path)
    enabled_sources = [source for source in sources if source.get("enabled", True)]
    records = []
    errors = []

    for source in enabled_sources:
        if not source.get("url"):
            errors.append(f"{source.get('name', DEFAULT_UNKNOWN)}：缺少 URL")
            continue
        try:
            records.extend(fetch_policy_source(source, timeout=timeout))
        except Exception as exc:
            errors.append(f"{source.get('name', DEFAULT_UNKNOWN)}：{exc}")

    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if records:
        payload = {
            "updated_at": now_text(),
            "sources": sources,
            "records": records,
            "last_error": "；".join(errors),
        }
        cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "ok": True,
            "updated": True,
            "record_count": len(records),
            "updated_at": payload["updated_at"],
            "errors": errors,
            "cache": payload,
        }

    cache = load_policy_cache(cache_path)
    return {
        "ok": False,
        "updated": False,
        "record_count": len(cache.get("records", [])),
        "updated_at": cache.get("updated_at", ""),
        "errors": errors or ["未能从已启用政策源抽取到有效政策条目。"],
        "cache": cache,
    }
