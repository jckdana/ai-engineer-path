# Creates a small folder of sample documents for lesson 01-05. Safe to run twice.
from pathlib import Path

DOCS = Path(__file__).resolve().parent / "01-05-docs"

files = {
    "meeting-notes.txt": "Weekly sync at Café Luna\nShip the ticket filter by Friday.\nBudget approved for the team offsite.\n",
    "clients/acme.txt": "Acme Corp\nWants a weekly report of urgent tickets.\nBudget is 500 dollars a month.\n",
    "clients/zeta.txt": "Zeta Ltd\nInterested in a document Q&A bot.\n",
    "empty.txt": "",
    "README.md": "# Not a .txt file\nThe index should skip this one.\n",
}

for name, text in files.items():
    path = DOCS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(DOCS))