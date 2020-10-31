from typing import Any, Sequence, Mapping


# [not-sequence-types]
# These python types are not considered to be Sequences in ilexconf,
# even though, technically, they are Sequences in Python.
STR_TYPES = (str, bytes, bytearray)
# [not-sequence-types]


def issequence(arg: Any) -> bool:
    return isinstance(arg, Sequence) and not isinstance(arg, STR_TYPES)


def iskwresult(result: Any) -> bool:
    return (
        result is not None and isinstance(result, tuple) and len(result) == 2
    )


def isinstresult(result: Any) -> bool:
    return result is not None


def traverse(
    arg: Any,
    func=lambda *args, **kwargs: args,
    key_order=lambda k: list(k),
    list_order=lambda l: list(l),
    **kwargs,
) -> Any:

    if "_depth" not in kwargs:
        kwargs["_depth"] = 0
    kwargs["_depth"] += 1

    result = None

    if isinstance(arg, Mapping):
        # This branch always returns ``dic``
        d = dict()

        keys = key_order(arg.keys())
        for k in keys:
            v = arg[k]

            # At this point, ``func``` can transform both ``k`` and ``v``
            # to anything, even to None. Or turn ``v`` into a plain value.
            result = func(k, v, **kwargs)
            if iskwresult(result):
                k, v = result

            if isinstance(v, Mapping) or issequence(v):
                v = traverse(
                    v,
                    func,
                    key_order=key_order,
                    list_order=list_order,
                    **kwargs,
                )

            dict.__setitem__(d, k, v)

        return d

    elif issequence(arg):
        # This branch always returns sequence of the same type as ``arg``.
        l = list()

        items = list_order(arg)
        for i in items:

            result = func(None, i, **kwargs)
            if iskwresult(result):
                k, i = result

            if isinstance(i, Mapping) or issequence(i):
                i = traverse(
                    i, func, key_order=key_order, list_order=list_order, **kwargs
                )

            l.append(i)

        t = type(arg)
        return t(l)

    else:
        # This branch returns whatever results we get from ``func`` or
        # ``arg`` itself if there were no results.
        result = func(None, arg, **kwargs)

        if iskwresult(result):
            k, v = result
            return v
        else:
            return arg

