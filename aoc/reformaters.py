def combine_nonblank_lines(content: list[str], sep: str = " ") -> list[str]:
    content = [item.strip() for item in content]
    i, new_content, clean_content = 0, "", []

    while i < len(content):

        if content[i] == "":
            clean_content.append(new_content.strip())
            new_content = ""
        else:
            new_content += sep + content[i]

        i += 1

    if new_content:
        clean_content.append(new_content.strip())

    return clean_content
