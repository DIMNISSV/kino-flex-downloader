from pathlib import Path
from typing import Callable, Sequence


def generate(l: Sequence[str], cmd: str, get_format: Callable[[str], tuple], save_pth: Path):
    save_pth.parent.mkdir(parents=True, exist_ok=True)
    with open(save_pth, 'w') as f:
        for i in l:
            f.write(cmd % get_format(i))
            f.write('\n')
            f.flush()
