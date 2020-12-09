from typing import Dict, Any, Hashable, Mapping, Type, Union
from types import MappingProxyType


def to_flat(
    data: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    prefix: str = "",
    sep: str = ".",
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Flatten the mapping so that there is no hierarchy."""

    d = mapping_type()

    p = f"{prefix}" if prefix else ""
    for key in data:
        v = MappingProxyType(data).__getitem__(key)
        if isinstance(v, Mapping):
            flattened = to_flat(
                v,
                prefix=f"{p}{key}{sep}",
                sep=sep,
                mapping_type=mapping_type,
            )
            d.update(flattened)
        else:
            dict.__setitem__(d, f"{p}{key}", v)

    if isinstance(data, Dict) and inplace:
        data.clear()
        data.update(d)
        d = data

    return d
