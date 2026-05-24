import sexpdata

def parse_kicad_pcb(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = sexpdata.load(f)
    return data
