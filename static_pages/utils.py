


def parse_error(error):
	message = ''
	for e in error:
		if type(e) is tuple:
			message = e[1][0]
			break
		message = e
		break
	return message