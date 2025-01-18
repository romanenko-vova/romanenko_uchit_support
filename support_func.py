def escape_text(text):
    symbols = '.,-()!?='
    for symbol in symbols:
        text = text.replace(symbol, f'\\{symbol}')
    return text