class MacroBlock:
    def __init__(self, name, x, y, w, h, color, b_type="Logic"):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.width = int(w)
        self.height = int(h)
        self.color = color
        self.block_type = b_type
        self.locked = False

    def get_center(self):
        return (self.x + self.width / 2.0, self.y + self.height / 2.0)

def get_initial_blocks():
    return {
        "CPU_Core": MacroBlock("CPU_Core", 200, 300, 150, 150, "#1A73E8", "Logic"),
        "SRAM_1": MacroBlock("SRAM_1", 450, 450, 100, 150, "#0F9D58", "Memory"),
        "SRAM_2": MacroBlock("SRAM_2", 450, 150, 100, 150, "#0F9D58", "Memory"),
        "IO_Peri": MacroBlock("IO_Peri", 650, 320, 90, 90, "#E67E22", "Analog")
    }

def get_initial_netlist():
    return [
        ("CPU_Core", "SRAM_1"), ("CPU_Core", "SRAM_2"),
        ("SRAM_1", "IO_Peri"), ("SRAM_2", "IO_Peri")
    ]
