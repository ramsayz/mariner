import re
import pdfplumber

MONTHS = {
    "january","february","march","april","may","june",
    "july","august","september","october","november","december"
}

def extract_nav_mtd_bright_meadow(pdf_path):
    """
    NAV = last value in Ending Equity column (from the performance table)
    MTD = last value in MTD Rate of Return column (from the performance table)

    Logic:
    - Find header containing 'Ending Equity' and 'MTD Rate of Return'
    - Parse subsequent month rows only
    - For each month row: take last comma-number as Ending Equity, and the MTD percent on that line
    """

    # 1) Pull text (line-preserving as much as pdfplumber allows)
    with pdfplumber.open(pdf_path) as pdf:
        lines = []
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                lines.extend(txt.splitlines())

    if not lines:
        return None, None

    # 2) Find start of the performance table by header
    header_idx = None
    for i, line in enumerate(lines):
        l = line.lower()
        if ("ending" in l and "equity" in l) and ("mtd" in l and "rate" in l and "return" in l):
            header_idx = i
            break

    if header_idx is None:
        # Header not found => can't reliably extract
        return None, None

    # 3) Scan rows after header; only accept month rows
    last_nav = None
    last_mtd = None

    # Regex patterns
    comma_number = re.compile(r"\b\d{1,3}(?:,\d{3})+\b")           # 130,170,531
    mtd_percent = re.compile(r"\(?-?\d+(?:\.\d+)?%\)?")           # 0.96% or (1.0%)

    for line in lines[header_idx + 1:]:
        l = line.strip()
        if not l:
            continue

        # Only process real month rows (avoids footers/notes)
        first_word = l.split()[0].lower() if l.split() else ""
        if first_word not in MONTHS:
            # allow year-only lines like "2024" / "2025" to pass without stopping
            # but ignore everything else that isn't a month row
            continue

        # Extract Ending Equity (comma numbers) and MTD% on the same row
        nums = comma_number.findall(l)
        pcts = mtd_percent.findall(l)

        if nums:
            # In these rows, Ending Equity is the last comma-number on the row
            nav_raw = nums[-1]
            last_nav = float(nav_raw.replace(",", ""))

        if pcts:
            # MTD Rate of Return is the first percent that appears after the equity columns.
            # In practice for this table, the first percent on the row is the MTD rate.
            mtd_raw = pcts[0].replace("%", "")
            if mtd_raw.startswith("(") and mtd_raw.endswith(")"):
                last_mtd = -float(mtd_raw.strip("()"))
            else:
                last_mtd = float(mtd_raw)

    return last_nav, last_mtd
