def parse_version(version_str):
    """Convert a version string into a list of integers."""
    # Split the string and filter out empty strings before converting to int
    parts = [part for part in version_str.split(".") if part]
    return list(map(int, parts))


def is_version_in_range(version_str, ver_range_str):
    """Check if the given version falls within the specified range."""
    # Ensure the range is in the expected format
    if "," not in ver_range_str:
        print(f"Invalid version range format: {ver_range_str}")
        return False

    # Split the version range into lower and upper bounds
    lower_bound, upper_bound = ver_range_str.split(",")

    # Extract the comparison operator and version for lower bound
    if lower_bound.startswith(">="):
        lower_op = "="
        lower_version_str = lower_bound[2:]
    elif lower_bound.startswith(">"):
        lower_op = ">"
        lower_version_str = lower_bound[1:]
    else:
        print(f"Invalid lower bound operator: {lower_bound}")
        return False

    # Extract the comparison operator and version for upper bound
    if upper_bound.startswith("<="):
        upper_op = "="
        upper_version_str = upper_bound[2:]
    elif upper_bound.startswith("<"):
        upper_op = "<"
        upper_version_str = upper_bound[1:]
    else:
        print(f"Invalid upper bound operator: {upper_bound}")
        return False

    # Parse versions
    try:
        lower_version = parse_version(lower_version_str)
        upper_version = parse_version(upper_version_str)
        version = parse_version(version_str)
    except ValueError as e:
        print(f"Invalid version format: {e}")
        return False

    # Perform the comparisons
    if lower_op == ">":
        is_lower_satisfied = version > lower_version
    else:  # lower_op == "="
        is_lower_satisfied = version >= lower_version

    if upper_op == "<":
        is_upper_satisfied = version < upper_version
    else:  # upper_op == "="
        is_upper_satisfied = version <= upper_version

    return is_lower_satisfied and is_upper_satisfied


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python version_check.py <version> <ver_range>")
        sys.exit(1)

    version = sys.argv[1]
    ver_range = sys.argv[2]
    result = is_version_in_range(version, ver_range)
    print(result)
