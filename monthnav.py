MONTHS = {
    "january","february","march","april","may","june",
    "july","august","september","october","november","december"
}

last_month_key = None

for k in line_keys:
    if k <= latest_year_key:
        continue

    row_words = get_line_words(k)
    if not row_words:
        continue

    first_word = row_words[0]['text'].lower()

    if first_word in MONTHS:
        last_month_key = k  # keep updating → last one wins

if last_month_key is None:
    print(f"  ⚠ No month row found in: {os.path.basename(pdf_path)}")
    return None

dec_words = get_line_words(last_month_key)
