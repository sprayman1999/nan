def is_hex_char(text):
	HEX_TABLE = "0123456789ABCDEFabcdef"
	if len(text) < 3 or len(text) > 4:
		return False
	if text[0] != "\\" or text[1] != 'x':
		return False
	if len(text) == 3:
		if text[2] in HEX_TABLE:
			return True
	if len(text) == 4:
		if text[2] in HEX_TABLE and text[3] in HEX_TABLE:
			return True
	return False
