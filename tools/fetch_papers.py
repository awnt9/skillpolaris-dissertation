import re
import sys
import time

import requests

OPENALEX_URL = "https://api.openalex.org/works"
MAX_RESULTS = 3
MAX_RETRIES = 4
BACKOFF_BASE = 1.0


def reconstruct_abstract(inverted_index):
    if not inverted_index:
        return None
    positions = []
    for word, indices in inverted_index.items():
        for index in indices:
            positions.append((index, word))
    positions.sort()
    return " ".join(word for _, word in positions)


def bibtex_escape(text):
    if not text:
        return ""
    replacements = (
        ("\\", "\\textbackslash{}"),
        ("{", "\\{"),
        ("}", "\\}"),
    )
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def format_authors_display(authorships):
    return ", ".join(
        authorship["author"]["display_name"]
        for authorship in authorships
        if authorship.get("author", {}).get("display_name")
    )


def format_authors_bibtex(authorships):
    names = [
        bibtex_escape(authorship["author"]["display_name"])
        for authorship in authorships
        if authorship.get("author", {}).get("display_name")
    ]
    return " and ".join(names)


def make_cite_key(authorships, year, used_keys):
    first_author = ""
    if authorships:
        display_name = authorships[0].get("author", {}).get("display_name", "")
        parts = display_name.split()
        if parts:
            first_author = re.sub(r"[^a-zA-Z]", "", parts[-1])

    year_str = str(year) if year else "nd"
    base_key = f"{first_author}{year_str}" or "unknown"
    cite_key = base_key
    suffix = ord("a")
    while cite_key in used_keys:
        cite_key = f"{base_key}{chr(suffix)}"
        suffix += 1
    used_keys.add(cite_key)
    return cite_key


def entry_type(work):
    work_type = (work.get("type") or "article").lower()
    if work_type in {"article", "review", "letter", "editorial", "preprint"}:
        return "article"
    if work_type in {"proceedings-article", "paper-conference"}:
        return "inproceedings"
    if work_type == "book":
        return "book"
    return "misc"


def to_bibtex(work, used_keys):
    authorships = work.get("authorships", [])
    year = work.get("publication_year")
    title = bibtex_escape(work.get("title") or "")
    authors = format_authors_bibtex(authorships)
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
    cite_key = make_cite_key(authorships, year, used_keys)
    bib_type = entry_type(work)

    lines = [f"@{bib_type}{{{cite_key},"]
    if title:
        lines.append(f"  title = {{{title}}},")
    if authors:
        lines.append(f"  author = {{{authors}}},")
    if year:
        lines.append(f"  year = {{{year}}},")
    if abstract:
        lines.append(f"  abstract = {{{bibtex_escape(abstract)}}},")
    doi = work.get("doi")
    if doi:
        lines.append(f"  doi = {{{doi.removeprefix('https://doi.org/')}}},")
    lines.append("}")
    return "\n".join(lines)


def fetch_with_retry(url, params):
    last_response = None
    for attempt in range(MAX_RETRIES):
        response = requests.get(url, params=params, timeout=30)
        last_response = response
        if response.status_code == 429:
            time.sleep(BACKOFF_BASE * (2**attempt))
            continue
        response.raise_for_status()
        return response
    last_response.raise_for_status()


def search_papers(query):
    params = {
        "search": query,
        "per_page": MAX_RESULTS,
        "select": "id,title,publication_year,authorships,abstract_inverted_index,doi,type",
    }

    try:
        response = fetch_with_retry(OPENALEX_URL, params)
        data = response.json()
        results = data.get("results", [])

        if not results:
            print("No se encontraron resultados para esta búsqueda.")
            return

        print(f"--- RESULTADOS ACADÉMICOS PARA: '{query}' ---\n")
        used_keys = set()
        for paper in results:
            authors = format_authors_display(paper.get("authorships", []))
            abstract = reconstruct_abstract(paper.get("abstract_inverted_index"))
            print(f"TÍTULO: {paper.get('title')} ({paper.get('publication_year')})")
            print(f"AUTORES: {authors}")
            print(f"ABSTRACT: {abstract}")
            print("BIBTEX:")
            print(to_bibtex(paper, used_keys))
            print("-" * 50)

    except Exception as error:
        print(f"Error al conectar con la API académica: {error}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_papers(sys.argv[1])
    else:
        print("Error: Debes proporcionar un término de búsqueda.")
