import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
import eda_engine as eda
import mobile_canvas as cv

class SiliconCruxMobileApp(App):
    def build(self):
        self.title = "SiliconCrux Mobile Pro v3.5"
        self.blocks = eda.get_initial_blocks()
        self.netlist = eda.get_initial_netlist()

        # Build Main Frame Panel Stack Layout
        master_panel = BoxLayout(orientation='vertical', spacing=0)

        # 1. Persistent Top Dockable Metrics Telemetry Bar
        top_bar = BoxLayout(size_hint_y=0.08, padding=[15, 5], spacing=10)
        with top_bar.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.07, 0.07, 0.07, 1)
            self.top_bg = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self.set_top_bg, pos=self.set_top_bg)

        title_lbl = Label(text="CRUX COCKPIT", color=(0, 0.9, 0.4, 1), bold=True, font_size=15)
        self.hpwl_lbl = Label(text="Total HPWL: 0 um", font_name="Roboto", bold=True, font_size=13)
        self.congest_lbl = Label(text="Congestion: 2.1%", color=(0.9, 0.6, 0, 1), font_size=12)
        
        top_bar.add_widget(title_lbl)
        top_bar.add_widget(self.hpwl_lbl)
        top_bar.add_widget(self.congest_lbl)
        master_panel.add_widget(top_bar)

        # 2. Main CAD Vector Grid Canvas Viewport Workspace
        self.canvas_workspace = cv.SiliconCruxMobileCanvas(self)
        master_panel.add_widget(self.canvas_workspace)

        # 3. Swipe-Up Tcl Terminal Console & Tooling Control Box
        self.control_dock = BoxLayout(orientation='vertical', size_hint_y=0.38, padding=6, spacing=4)
        with self.control_dock.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.dock_bg = Rectangle(size=self.control_dock.size, pos=self.control_dock.pos)
        self.control_dock.bind(size=self.set_dock_bg, pos=self.set_dock_bg)

        # Pre-built quick command button chips toolbar row
        chips_bar = BoxLayout(size_hint_y=0.25, spacing=4)
        btn_snap = ToggleButton(text="Grid Snap: ON", state="down", background_color=(0.2,0.2,0.2,1))
        btn_snap.bind(on_press=self.toggle_magnetic_snapping)
        btn_lock = Button(text="🔒 Lock CPU", background_color=(0.15,0.15,0.15,1))
        btn_lock.bind(on_press=self.toggle_cpu_lock_state)
        btn_nudge = Button(text="➕ Nudge +1um", background_color=(0.15,0.15,0.15,1))
        btn_nudge.bind(on_press=self.nudge_selected_macro)
        
        chips_bar.add_widget(btn_snap)
        chips_bar.add_widget(btn_lock)
        chips_bar.add_widget(btn_nudge)
        self.control_dock.add_widget(chips_bar)

        # Form Generation Field Row 
        form_row = GridLayout(rows=1, cols=4, size_hint_y=0.3, spacing=4)
        self.e_name = TextInput(text="SRAM_3", multiline=False, background_color=(0.2,0.2,0.2,1), foreground_color=(1,1,1,1))
        self.c_type = Spinner(text="Memory", values=("Logic", "Memory", "Analog"), background_color=(0.18,0.18,0.18,1))
        btn_deploy = Button(text="Deploy Macro", background_color=(0.1, 0.45, 0.9, 1), bold=True)
        btn_deploy.bind(on_press=self.deploy_custom_macro)
        
        form_row.add_widget(self.e_name)
        form_row.add_widget(self.c_type)
        form_row.add_widget(btn_deploy)
        self.control_dock.add_widget(form_row)

        # Bottom Command Console Input 
        console_row = BoxLayout(size_hint_y=0.4, spacing=4)
        self.terminal_input = TextInput(text="recalc_hpwl", multiline=False, background_color=(0.05,0.05,0.05,1), foreground_color=(0,1,0,1))
        btn_exe = Button(text="RUN Tcl", size_hint_x=0.25, background_color=(0, 0.6, 0.3, 1), bold=True)
        btn_exe.bind(on_press=self.execute_tcl_command)
        
        console_row.add_widget(self.terminal_input)
        console_row.add_widget(btn_exe)
        self.control_dock.add_widget(console_row)

        master_panel.add_widget(self.control_dock)
        self.canvas_workspace.load_elements()
        return master_panel

    def set_top_bg(self, instance, value): self.top_bg.size = value; self.top_bg.pos = instance.pos
    def set_dock_bg(self, instance, value): self.dock_bg.size = value; self.dock_bg.pos = instance.pos

    # --- ADVANCED SYSTEM ACTION COMMAND IMPLEMENTATIONS ---
    def toggle_magnetic_snapping(self, instance):
        self.canvas_workspace.snap_enabled = (instance.state == "down")
        instance.text = "Grid Snap: ON" if self.canvas_workspace.snap_enabled else "Grid Snap: OFF"

    def toggle_cpu_lock_state(self, instance):
        if "CPU_Core" in self.blocks:
            self.blocks["CPU_Core"].locked = not self.blocks["CPU_Core"].locked
            instance.text = "🔓 Unlock CPU" if self.blocks["CPU_Core"].locked else "🔒 Lock CPU"
            self.canvas_workspace.load_elements()

    def nudge_selected_macro(self, instance):
        """Micro-Nudge Controls: Increments block coordinate physics by exactly 1 micron step."""
        if "SRAM_1" in self.blocks:
            self.blocks["SRAM_1"].x += 1.0
            self.canvas_workspace.load_elements()

    def deploy_custom_macro(self, instance):
        name = self.e_name.text.strip().replace(" ", "_")
        b_type = self.c_type.text
        if not name or name in self.blocks: return
        
        c_map = {"Logic": "#1A73E8", "Memory": "#0F9D58", "Analog": "#E67E22"}
        self.blocks[name] = eda.MacroBlock(name, 300, 250, 100, 120, c_map[b_type], b_type)
        if "CPU_Core" in self.blocks: self.netlist.append(("CPU_Core", name))
        self.canvas_workspace.load_elements()
        self.e_name.text = ""

    def execute_tcl_command(self, instance):
        """Swipe-Up Tcl Terminal command parser simulation logic module."""
        cmd = self.terminal_input.text.strip()
        if cmd == "recalc_hpwl":
            self.canvas_workspace.update_nets()
            self.terminal_input.text = "Tcl Output: HPWL Recalculated cleanly."
        elif cmd == "clear_canvas":
            self.blocks = {"CPU_Core": eda.MacroBlock("CPU_Core", 200, 300, 150, 150, "#1A73E8", "Logic")}
            self.netlist = []
            self.canvas_workspace.load_elements()
            self.terminal_input.text = "Tcl Output: Workspace flushed."
        else:
            self.terminal_input.text = f"Error: unknown command instruction string template '{cmd}'"

if __name__ == "__main__":
    SiliconCruxMobileApp().run()
