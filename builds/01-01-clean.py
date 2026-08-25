raw_og = "\n\t  the QUICK   brown fox    jumped over    the LAZY dog.  \n"

raw = raw_og.strip()
raw = raw.lower()
raw = " ".join(raw.split())
raw = raw.capitalize()

word_count = len(raw.split())

print(f"{raw_og} is the uncleaned string. {raw} is the cleaned string.")
print(f"Word count: {word_count}")