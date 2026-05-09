import sys

import internetarchive as ia


def _ensure_utf8_stdout() -> None:
    if getattr(sys.stdout, "reconfigure", None):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def _title_from_hit(hit: dict) -> str:
    raw = hit.get("title") or hit.get("titleSorter")
    if raw is None:
        return "タイトルなし"
    if isinstance(raw, list):
        raw = raw[0] if raw else None
    if raw is None:
        return "タイトルなし"
    return str(raw)


def get_keaton_pd_list():
    # 検索クエリ: 作成者がバスター・キートン、メディアタイプが動画
    query = 'creator:"Buster Keaton" AND mediatype:movies'

    print("Internet Archive — 作成者「Buster Keaton」の動画一覧", flush=True)
    print(f"{'タイトル':<50} | {'識別子':<20}", flush=True)
    print("-" * 75, flush=True)

    # identifier / title を Solr から直接取得（1件ごとの get_item より高速）
    search = ia.search_items(query, fields=["identifier", "title", "titleSorter"])

    for result in search:
        item_id = result["identifier"]
        title = _title_from_hit(result)
        safe = title[:48] + ("..." if len(title) > 48 else "")
        print(f"{safe:<50} | {item_id:<20}", flush=True)


if __name__ == "__main__":
    _ensure_utf8_stdout()
    get_keaton_pd_list()
