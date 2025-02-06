from prefect import flow, task


class BooleanWithProvenance:
    def __init__(self, value, provenance):
        self.value = value
        self.provenance = provenance

    def __bool__(self):
        return bool(self.value)

    def __repr__(self):
        return f"BooleanWithProvenance({self.value}, {self.provenance})"

    def __eq__(self, other):
        if isinstance(other, BoolWithProvenance):
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


@flow
def main():
    argument = BooleanWithProvenance(True, [])
    result = bool_task(argument)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
