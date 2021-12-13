from typing import Union, Iterable, Any


def flatten_to_list(obj: Union[Iterable[Any], Any]) -> Union[list[Any], Any]:
    """
    Flattens iterable to a non-nested list

    Function ignores strings and treats as non-iterable

    :param obj: iterable of nested iterables
    :return: list of non-iterable objects
    """
    if (not isinstance(obj, Iterable)) or isinstance(obj, str):
        return obj
    else:
        out = []
        for item in obj:
            if (not isinstance(item, Iterable)) or isinstance(item, str):
                out.append(item)
            else:
                out += flatten_to_list(item)

        return out


def make_ordinal(num: int) -> str:
    digit = abs(num) % 10

    if 0 < digit < 4:
        if (abs(num) % 100) % 10 == 1:
            return f'{num}th'
        elif digit == 1:
            return f'{num}st'
        elif digit == 2:
            return f'{num}nd'
        else:
            return f'{num}rd'
    else:
        return f'{num}th'
