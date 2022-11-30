class BlankSolutionPartMixin:
    """
    Add this when you want to satisfy the ABC requirements of
    the solution class but don't care about the actual part functions
    """

    def _part_one(self) -> int:
        return 1

    def _part_two(self) -> int:
        return 1
