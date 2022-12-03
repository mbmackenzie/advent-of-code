import glob
import os


def main() -> int:

    # dirs = glob.glob("20*/")
    # for d in dirs:
    #     files = glob.glob(f"{d}/day*.*")
    #     for f in files:

    #         old_path = os.path.split(f)
    #         day_num = old_path[-1][3:5]

    #         new_folder = os.path.join(d, day_num)
    #         if not os.path.exists(new_folder):
    #             print(f"mkdir {new_folder}")
    #             os.mkdir(new_folder)

    #         new_path = os.path.join(new_folder, "sol.py")
    #         print(f"cp {f} {new_path}")
    #         os.rename(f, new_path)

    files = glob.glob("20*/*/sol.py")

    for f in files:
        path = os.path.normpath(f)
        year, day, _ = path.split(os.sep)
        new_name = os.path.join(year, day, f"aoc_{day}_{year}.py")

        print(f"mv {f} {new_name}")
        os.rename(f, new_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
