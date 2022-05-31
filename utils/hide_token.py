def secure_token(token):
    split_token = token.rpartition(':')
    hidden = split_token[0] + split_token[1] + "*" * len(split_token[2])

    return hidden
