
from pathlib import Path
import re
import traceback

from class_measures_result import Results
from plots import *


CSV_WITH_TRAILING_NUMBER_RE = re.compile(r"^(?P<prefix>.+?)(?P<number>\d+)\.csv$")


def find_unique_prefixes(directory: Path) -> list[str]:
    """Zwraca unikalne początki nazw plików CSV, tj. nazwę bez końcowego {liczba}.csv."""
    prefixes = set()

    for path in directory.glob("*.csv"):
        match = CSV_WITH_TRAILING_NUMBER_RE.match(path.name)
        if match:
            prefixes.add(match.group("prefix"))

    return sorted(prefixes)


def run_step(step_name, func, *args, **kwargs):
    print(f"    [STEP] {step_name}")
    try:
        result = func(*args, **kwargs)
        print(f"    [OK]   {step_name}")
        return result
    except Exception as exc:
        print(f"    [FAIL] {step_name}: {exc}")
        traceback.print_exc()
        raise


def process_prefix(prefix: str) -> None:
    print(f"[START] Prefix: {prefix}")
    dumpfile = f"{prefix}.pkl"
    results_instance = Results(dumpfile=dumpfile, resultfilename=prefix)
    
    results_instance.dump_class_to_file(dumpfile)
    print(f"[OK] Zapisano dump: {dumpfile}")
    print("plotting pow in pos::")
    #plot_power_in_position(dumpfile)
    print("plotting pow in pos teams::")
    #plot_pow_in_pos_teams(dumpfile)
    print("plotting pow in pos merge::")
    #plot_pow_in_pos_merge(dumpfile)
    print("plotting pat char::")
    plot_pattern_characteristics(dumpfile)
    print("plotting hamming::")
    #plot_hamming(dumpfile)

    print(f"[DONE] Zakończono przetwarzanie: {prefix}\n")



def main() -> None:
    base_dir = Path(__file__).resolve().parent
    prefixes = find_unique_prefixes(base_dir)

    if not prefixes:
        print("Nie znaleziono żadnych plików CSV w formacie <prefix><liczba>.csv")
        return

    print("Znalezione początki nazw plików:")
    for prefix in prefixes:
        print(f" - {prefix}")
    print()

    for prefix in prefixes:
        #try:
            process_prefix(prefix)
        #except Exception as exc:
        #    print(f"[ERROR] Prefix '{prefix}' nie został przetworzony: {exc}\n")


if __name__ == "__main__":
    main()
