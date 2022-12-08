def snake_case(s: str) -> str:
    return ''.join([f'_{c.lower()}' if c.isupper() else c for c in s]).lstrip(
        '_'
    )


def pluralize(s: str) -> str:
    if s.endswith('y') and not s.endswith('ay') and not s.endswith('ey'):
        return s[:-1] + 'ies'
    if s.endswith('s'):
        return s
    return s + 's'
