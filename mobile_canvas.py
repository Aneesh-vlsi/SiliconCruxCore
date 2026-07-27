from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse

class MobileBlockWidget(Widget):
    def __init__(self, name, block_data, canvas_view, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.data = block_data
        self.view = canvas_view
        self.size = (block_data.width, block_data.height)
        self.pos = (block_data.x, block_data.y)
        self.draw_block()

    def draw_block(self):
        self.canvas.clear()
        with self.canvas:
            h = self.data.color.lstrip('#')
            rgb = tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))
            Color(*rgb)
            Rectangle(pos=self.pos, size=self.size)
            Color(1, 1, 1, 0.4 if not self.data.locked else 0.8)
            Line(rectangle=(self.pos, self.pos, self.size, self.size), width=1)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.data.locked:
            touch.grab(self)
            self.view.active_drag_block = self
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            nx = self.pos[0] + touch.dx
            ny = self.pos[1] + touch.dy
            if self.view.snap_enabled:
                nx = round(nx / 20.0) * 20.0
                ny = round(ny / 20.0) * 20.0
            self.pos = (nx, ny)
            self.data.x, self.data.y = float(nx), float(ny)
            self.draw_block()
            self.view.update_nets()
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.view.active_drag_block == self:
                self.view.active_drag_block = None
                self.view.update_nets()
            return True
        return super().on_touch_up(touch)


class SiliconCruxMobileCanvas(Widget):
    def __init__(self, app_root, **kwargs):
        super().__init__(**kwargs)
        self.app_root = app_root
        self.visual_blocks = {}
        self.active_drag_block = None
        self.snap_enabled = True
        
        with self.canvas.before:
            Color(0.06, 0.06, 0.06, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def load_elements(self):
        self.clear_widgets()
        self.visual_blocks.clear()
        for name, data in self.app_root.blocks.items():
            b = MobileBlockWidget(name, data, self)
            self.add_widget(b)
            self.visual_blocks[name] = b
        self.update_nets()

    def update_nets(self):
        self.canvas.clear()
        total_hpwl = 0
        with self.canvas:
            Color(0.12, 0.12, 0.12, 1)
            for d in range(0, 2000, 40):
                Line(points=[d, 0, d, 2000], width=0.5)
                Line(points=[0, d, 2000, d], width=0.5)

            Color(0.0, 0.9, 0.4, 0.6)
            for b1_n, b2_n in self.app_root.netlist:
                if b1_n in self.visual_blocks and b2_n in self.visual_blocks:
                    v1, v2 = self.visual_blocks[b1_n], self.visual_blocks[b2_n]
                    c1_x = v1.pos[0] + (v1.size[0] / 2.0)
                    c1_y = v1.pos[1] + (v1.size[1] / 2.0)
                    c2_x = v2.pos[0] + (v2.size[0] / 2.0)
                    c2_y = v2.pos[1] + (v2.size[1] / 2.0)
                    
                    Line(points=[c1_x, c1_y, c2_x, c2_y], width=1.2)
                    total_hpwl += (abs(c1_x - c2_x) + abs(c1_y - c2_y))

            if self.active_drag_block:
                b = self.active_drag_block
                bx = b.pos[0] + (b.size[0] / 2.0)
                by = b.pos[1] + (b.size[1] / 2.0)
                lx, ly = bx, by + 120
                Color(0.15, 0.15, 0.15, 0.9)
                Ellipse(pos=(lx - 50, ly - 50), size=(100, 100))
                Color(0, 0.9, 0.4, 1)
                Line(circle=(lx, ly, 50), width=1.5)
                
                h = b.data.color.lstrip('#')
                rgb = tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))
                Color(*rgb)
                Rectangle(pos=(lx - 25, ly - 25), size=(50, 50))

        self.app_root.hpwl_lbl.text = f"Total HPWL: {int(total_hpwl):,} um"
