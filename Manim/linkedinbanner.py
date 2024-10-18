from manim import *
from scipy.stats import norm
config.frame_size = [1584,396] # [WIDTH, HEIGHT]
class LinkedInBanner(Scene):
    def construct(self):
        # Background color
        self.camera.background_color = "#1c1c1c"
        
        name = Text("Kaius de Paula", font_size=38, color=WHITE).shift(RIGHT*3.5 + DOWN * 0.6).set_opacity(0.8)
        job_title = Text("Data Scientist", font_size=24, color=BLUE_D).shift(RIGHT*2).set_opacity(0.8)
        call_to_action = Text("Follow Along for More!", font_size=24, color=WHITE).shift(LEFT * 5.7 + UP * 1.4).set_opacity(0.8).scale(0.5)
        plus_sign = MathTex("+", color=BLUE_D).scale(0.7).next_to(call_to_action, LEFT, buff=0.1)
        small_text = Text("Empowering Decisions through Data & Machine Learning", font_size=28).set_opacity(0.8).shift(DOWN * 0.5 + RIGHT * 3.8).scale(0.4)
        
        # Position the title in the center, with slight upward shift
        name.shift(UP)
        job_title.next_to(name, DOWN * 0.3)
        
        # Create a bell curve (Gaussian function) with opacity
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.4, 0.2],
            tips=False
        ).set_opacity(0.1).scale(0.5)  # Adjust the position and opacity
        
        bell_curve = axes.plot(lambda x: norm.pdf(x,0,1), color=BLUE_C, stroke_width=4)

        area = axes.get_area(
            bell_curve,
            x_range=(-4,4),
            color=(BLUE_E, BLUE_E),
            opacity=0.3,
        )

        # Smaller curved wave lines (using parametric curves)
        wave_line_1 = ParametricFunction(
            lambda t: np.array([t, 0.04 * np.sin(3 * t), 0]), 
            t_range=np.array([-4, 3]),
            fill_opacity=0,
            stroke_width=1
        ).set_color(color=BLUE_E).scale(0.6).next_to(small_text, DOWN * 0.3)

        plane = NumberPlane(
            x_range = (0, 7),
            y_range = (0, 5),
            x_length = 7,
            axis_config={"include_numbers": False},
        ).scale(0.12).next_to(call_to_action, DOWN, buff=0.2)
        line_graph = plane.plot_line_graph(
            x_values = [0, 1.5, 2, 2.8, 4, 6.25],
            y_values = [1, 3, 2.25, 4, 2.5, 4.1],
            line_color=GOLD_E,
            vertex_dot_style=dict(stroke_width=1,  fill_color=PURPLE),
            stroke_width = 2,
            vertex_dot_radius=0.03
        )

        funny_func = MathTex(r"Content_t = f(x) + o(y) + l(z) + l(w) + o(p) + w(q)", font_size=38, color=WHITE).scale(0.4).shift(LEFT*2.9 + UP).set_opacity(0.8)

        edges = []
        partitions = []
        c = 0
        layers = [2, 3, 3, 2]  # the number of neurons in each layer

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1)))
            c += i
        for i, v in enumerate(layers[1:]):
                last = sum(layers[:i+1])
                for j in range(v):
                    for k in range(last - layers[i], last):
                        edges.append((k + 1, j + last + 1))

        vertices = np.arange(1, sum(layers) + 1)

        nn = Graph(
            vertices,
            edges,
            layout='partite',
            partitions=partitions,
            layout_scale=0.8,
            vertex_config={'radius': 0.03, 'fill_color':WHITE},
            edge_config={'stroke_color':BLUE_E},
        ).next_to(funny_func, DOWN, buff=0.3)

        # Add all elements to the scene
        self.add(
            name, 
            job_title, 
            axes, 
            bell_curve, 
            area, 
            call_to_action, 
            plus_sign, 
            small_text, 
            wave_line_1,
            plane, 
            line_graph,
            funny_func,
            nn
        )