import re
from pathlib import Path

IN_PATH = Path("dump_sqlite.sql")
OUT_PATH = Path("dump_postgres.sql")

text = IN_PATH.read_text(encoding="utf-8")

# Fix ONLY the boolean in menu_items inserts:
# It is the second-last value: ..., is_available, 'created_at'
# We convert that 0/1 to FALSE/TRUE safely.
def fix_menu_items_bool(match: re.Match) -> str:
    prefix = match.group(1)
    flag = match.group(2)
    suffix = match.group(3)
    return prefix + ("TRUE" if flag == "1" else "FALSE") + suffix

pattern = re.compile(
    r"(INSERT INTO menu_items VALUES\(.+?,)([01])(,'\d{4}-\d{2}-\d{2} [^']+'\);)"
)

text2, n = pattern.subn(fix_menu_items_bool, text)

# Optional sanity check:
if n == 0:
    raise SystemExit("No menu_items boolean values were replaced. Check dump format / file name.")

OUT_PATH.write_text(text2, encoding="utf-8")
print(f"✅ Wrote {OUT_PATH} (fixed {n} menu_items rows)")
