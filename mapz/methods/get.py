from .getsert import getsert

from typing import Union, MutableMapping, List, Hashable, Any


def get(
    data: Union[MutableMapping, List],
    address: Hashable,
    default: Any = None,
    sep: str = ".",
) -> Any:

    # If key is a string, then try to split it if it contains the separator
    head = address
    tail = None
    if isinstance(address, str) and sep and sep in address:
        # "my.0.key"
        head, tail = address.split(sep, maxsplit=1)

    if isinstance(data, MutableMapping):
        if address in data:
            return dict.__getitem__(data, address)

        v = getsert(data, head, default=default)

        # if tail and isinstance(v, MutableMapping):
        if tail and isinstance(v, (MutableMapping, List)):
            return get(v, tail, sep=sep, default=default)

        # Return whatever got generated by "getsert" otherwise
        return v

    if isinstance(data, List):
        idx = None

        # If key is string
        if isinstance(head, str):
            try:
                idx = int(head)
            except ValueError:
                return None
        elif type(head) == int:
            idx = head
        else:
            return None

        if idx >= len(data) or idx < 0 and abs(idx) > len(data):
            return None

        if tail and isinstance(data[idx], (MutableMapping, List)):
            return get(data[idx], tail, sep=sep, default=default)

        return data[idx]

    return default