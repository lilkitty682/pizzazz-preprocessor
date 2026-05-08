import os

RECURSIVE = True  # set False if you only want top-level src scanning


def find_project_root(start_dir):
    current = start_dir
    while True:
        if os.path.exists(os.path.join(current, "gleam.toml")):
            return current

        parent = os.path.dirname(current)
        if parent == current:  # reached filesystem root
            raise FileNotFoundError("Could not find gleam.toml in any parent directory")

        current = parent


def translate(text):
    semicolons = False
    inComment = False
    inMlComment = False
    exitingMlComment = False
    inString = False
    returnCode = ""
    n = 0

    for i in text:
        exitingMlComment = False

        if n == 0 and i == ";":
            semicolons = True
        elif i == "\n":
            inComment = False
        elif i == "/" and text[n - 1] == "*":
            inMlComment = False
            exitingMlComment = True
        elif i == "/" and text[n - 1] == "/" and not inString:
            inComment = True
            returnCode = returnCode[:-1]
        elif i == "*" and text[n - 1] == "/" and not inString:
            inMlComment = True
            returnCode = returnCode[:-1]
        elif i == "\"" and not inComment and not inMlComment:
            inString = not inString

        if not inString and not inComment and not inMlComment and not exitingMlComment:
            if i == "{":
                returnCode += "{\n"
            elif semicolons:
                if i == "\n":
                    returnCode += " "
                elif i == ";":
                    returnCode += "\n"
                else:
                    returnCode += i
            else:
                returnCode += i

        if inString:
            returnCode += i

        n += 1

    return returnCode


def process_file(path):
    output_path = path.replace(".pizzazz", ".gleam")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    translated = translate(content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated)

    print(f"Converted: {path} -> {output_path}")


# --- AUTO PROJECT DETECTION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = find_project_root(script_dir)

src_dir = os.path.join(project_root, "src")

if not os.path.exists(src_dir):
    raise FileNotFoundError(f"No src/ folder found in project root: {project_root}")

print("Project root:", project_root)
print("Scanning src:", src_dir)


# --- FILE WALK ---
if RECURSIVE:
    for root, dirs, files in os.walk(src_dir):
        for filename in files:
            if filename.lower().endswith(".pizzazz"):
                process_file(os.path.join(root, filename))
else:
    for filename in os.listdir(src_dir):
        full_path = os.path.join(src_dir, filename)
        if os.path.isfile(full_path) and filename.lower().endswith(".pizzazz"):
            process_file(full_path)
