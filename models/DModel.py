from dataclasses import dataclass, field
@dataclass()
class Result:
    name: str = ""
    found: str = ""
    score: float = 0.0
    line: int = 0
    def __str__(self):
        return self.name
@dataclass()
class File:
    name: str = ""
    type: str = ""
    size: int = 0
    path: str = ""
    parent: str = ""
    children: list = field(default_factory=list)
    content: str = ""
    results: list[Result] = field(default_factory=list)

    def __str__(self):
        return self.name

@dataclass()
class Directory:
    name: str = ""
    files: list[File] = field(default_factory=list)

    def __str__(self):
        return self.name


@dataclass()
class DModel:
    directory: list[Directory]

