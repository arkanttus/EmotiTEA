import unicodedata

def normalize_filename(filename):
    titulo_format = ''.join(
        ch
        for ch in unicodedata.normalize('NFKD', filename)
        if not unicodedata.combining(ch)
    )
    return titulo_format