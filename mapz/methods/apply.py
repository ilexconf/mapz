from .traverse import traverse, TraverseModificatorCallable

from typing import Any, Dict, Hashable, Mapping, Type, Union, cast


def apply(
    data: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    modificator: TraverseModificatorCallable = lambda k, v, **kwargs: (k, v),
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
    **kwargs: Any
) -> Dict[Hashable, Any]:
    d = traverse(data, modificator, mapping_type=mapping_type, **kwargs)

    if isinstance(data, Dict) and inplace:
        data.clear()
        data.update(d)
        d = data

    return cast(Dict[Hashable, Any], d)
