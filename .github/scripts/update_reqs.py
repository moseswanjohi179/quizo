import ast, sys, pathlib, re


MAP = {"yaml": "PyYAML", "dotenv": "python-dotenv", "PIL": "Pillow",
       "cv2": "opencv-python", "bs4": "beautifulsoup4", "flask_cors": "flask-cors",
       "socketio": "python-socketio", "sklearn": "scikit-learn"}


root = pathlib.Path(".")
local = {p.name for p in root.iterdir() if p.is_dir()} | {p.stem for p in root.rglob("*.py")}
imports = set()
for f in root.rglob("*.py"):
    try:
        tree = ast.parse(f.read_text())
    except SyntaxError:
        continue
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
            imports.add(n.module.split(".")[0])


third = {i for i in imports if i not in sys.stdlib_module_names and i not in local}


norm = lambda s: re.split(r"[=<>~\[; ]", s.strip())[0].lower().replace("_", "-")
req = pathlib.Path("server/requirements.txt")
lines = req.read_text().splitlines() if req.exists() else []
have = {norm(l) for l in lines if l.strip() and not l.startswith("#")}
for i in sorted(third):
    name = MAP.get(i, i)
    if norm(name) not in have:
        lines.append(name)
req.write_text("\n".join(lines) + "\n")