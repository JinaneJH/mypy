import re


def parse_signature(sig):
    m = re.match(r'([.a-zA-Z0-9_]+)\(([^)]*)\)', sig)
    if not m:
        return None
    name = m.group(1)
    name = name.split('.')[-1]
    arg_string = m.group(2)
    if not arg_string.strip():
        return (name, [], [])
    args = [arg.strip() for arg in arg_string.split(',')]
    fixed = []
    optional = []
    i = 0
    while i < len(args):
        if args[i].startswith('[') or '=' in args[i]:
            break
        fixed.append(args[i].rstrip('['))
        i += 1
        if args[i - 1].endswith('['):
            break
    while i < len(args):
        arg = args[i]
        arg = arg.strip('[]')
        arg = arg.split('=')[0]
        optional.append(arg)
        i += 1
    return (name, fixed, optional)


def build_signature(fixed, optional):
    args = fixed + ['%s=Undefined' % arg for arg in optional]
    sig = '(%s)' % ', '.join(args)
    # Ad-hoc fixes.
    sig = sig.replace('(self)', '')
    return sig


def parse_all_signatures(lines):
    sigs = []
    for line in lines:
        line = line.strip()
        if re.match(r'\.\. *(function|method) *::', line):
            sig = line.split('::')[1].strip()
            parsed = parse_signature(sig)
            if parsed:
                name, fixed, optional = parsed
                sigs.append((name, build_signature(fixed, optional)))
    return sorted(sigs)


def find_unique_signatures(sigs):
    sig_map = {}
    for name, sig in sigs:
        sig_map.setdefault(name, []).append(sig)
    result = []
    for name, name_sigs in sig_map.items():
        if len(set(name_sigs)) == 1:
            result.append((name, name_sigs[0]))
    return result
