import re
from typing import Any, Callable


def _smart_type(value: Any) -> Any:
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            pass
        cleaned = re.sub(r'[^\d.-]', '', value.replace(',', '.'))
        try:
            return float(cleaned)
        except ValueError:
            pass
        return value

    return str(value)


def sorted_dict_by_value(dict_: dict, key_func: Callable[[Any], Any] = _smart_type, reverse=False) -> dict:
    return dict(sorted(dict_.items(), key=lambda item: key_func(item[1]), reverse=reverse))