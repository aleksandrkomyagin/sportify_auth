from dataclasses import dataclass, fields


@dataclass
class ValidatedDataClass:
    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if not isinstance(value, f.type):
                raise TypeError(
                    f"{f.name} must be {f.type.__name__}, got {type(value).__name__}"
                )
