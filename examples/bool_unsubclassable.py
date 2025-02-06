from typing import Any

from prefect import flow, task


class BoolWithProvenance(int):
    # NOTE(PG): Subclass from int to avoid TypeError when subclassing from bool. Bools are just
    #           a special case of integers, so this should be fine.
    def __new__(cls, value, provenance):
        return super().__new__(cls, value)

    def __init__(self, value: Any, provenance: list):
        self.value = value
        self._provenance = provenance

    @property
    def provenance(self) -> list:
        return self._provenance

    @provenance.setter
    def provenance(self, value: list):
        self._provenance = value

    def __bool__(self) -> bool:
        return bool(self.value)

    def __repr__(self) -> str:
        return f"BoolWithProvenance({self.value}, {self.provenance})"

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.value == other.value

        return self.value == other

    def __hash__(self):
        return hash(self.value)

    # FIXME(PG): This is a very bad hack...
    @property
    def __class__(self):
        return bool


@task
def bool_task(x: bool) -> bool:
    return x


@task
def check_if_bool(x: Any) -> bool:
    return isinstance(x, bool)


@flow
def main():
    argument = BoolWithProvenance(True, [])
    result = bool_task(argument)
    print(f"Result: {result}")
    is_bool = check_if_bool(result)
    print(f"Result is boolean-ish? {is_bool}")


if __name__ == "__main__":
    main()
