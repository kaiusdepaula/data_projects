from manim import *
from scipy.stats import norm
config.frame_size = [1584,396] # [WIDTH, HEIGHT]
class LinkedInBanner(Scene):
    def construct(self):
        # Background color
        self.camera.background_color = "#1c1c1c"
        
        phrase1 = Text("I Build AI Applications", font_size=40, color=WHITE).shift(RIGHT*3 + UP*0.2).set_opacity(0.8)
        phrase2 = Text(r"Like There’s Nothing Artificial About It", font_size=25, color=BLUE_D).set_opacity(0.8)
        phrase2.next_to(phrase1, DOWN * 0.3)

        call_to_action = Text("Follow Along for More!", font_size=30, color=WHITE).shift(LEFT * 5.5 + UP * 1.4).set_opacity(0.8).scale(0.5)
        plus_sign = MathTex("-", color=BLUE_D).next_to(call_to_action, LEFT, buff=0.1)
        
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

        funny_func = Text("So you can base your decisions on actual evidence.", font_size=30, color=WHITE).scale(0.5).align_on_border(RIGHT).set_opacity(0.8).shift(DOWN * 1.3)

        # Add all elements to the scene
        self.add(
            phrase1, 
            phrase2, 
            bell_curve.shift(LEFT * 2), 
            area.shift(LEFT * 2), 
            call_to_action, 
            plus_sign,
            funny_func
        )