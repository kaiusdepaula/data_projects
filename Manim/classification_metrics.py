from manim import *
from random import seed, randint

seed(42)
class Intro(Scene):
    def acting_classifier(self, triangle, n_dots, speed):        
        # Color hash map
        color_map = {0: GREEN, 1: RED, 2: YELLOW, 3: BLUE, 4: ORANGE}
        classes = {0: "Spam", 1: "Not Spam"}
        
        # Generate dots with random colors and labels
        dots = [Dot(color=color_map[randint(0, len(color_map)-1)]).scale(7).shift(LEFT * 5) for _ in range(n_dots)]
        pred_labels = [Tex(classes[randint(0, len(classes)-1)]).next_to(triangle, DOWN, buff=0.3) for _ in range(n_dots)]
        true_labels = [Tex(classes[randint(0, len(classes)-1)]).next_to(triangle, DOWN, buff=0.3) for _ in range(n_dots)]
        
        # Loop through the dots and labels, animating them
        for dot, pred_label, true_label in zip(dots, pred_labels, true_labels):
            self.play(Write(dot), run_time=speed)
            self.play(dot.animate.shift(RIGHT * 5), run_time=speed)
            self.play(FadeIn(pred_label, shift=DOWN), run_time=speed)
            if pred_label.tex_string == true_label.tex_string:
                self.play(Indicate(pred_label, color=GREEN))
            else:
                self.play(Indicate(pred_label, color=RED))
                self.play(Transform(pred_label, true_label))
                

            self.play([dot.animate.shift(RIGHT * 10), FadeOut(pred_label)], run_time=speed)
            self.remove(dot)

    def acting_classifier_with_matrix(self, confusion_matrix, square, triangle, n_dots, speed, accelerator):        
        # Color hash map
        color_map = {0: GREEN, 1: RED, 2: YELLOW, 3: BLUE, 4: ORANGE}
        classes = {0: "Spam", 1: "Not Spam"}
        
        # Generate dots with random colors and labels
        dots = [Dot(color=color_map[randint(0, len(color_map)-1)]).scale(7).next_to(square, LEFT * 2.5) for _ in range(n_dots)]
        pred_labels = [Tex(classes[randint(0, len(classes)-1)]).next_to(triangle, DOWN, buff=0.3) for _ in range(n_dots)]
        true_labels = [Tex(classes[randint(0, len(classes)-1)]).next_to(triangle, DOWN, buff=0.3) for _ in range(n_dots)]
        
        # Add a logic to auto update matrix entries based on matches
        c11 = ValueTracker(0)
        c22 = ValueTracker(0)
        c12 = ValueTracker(0)
        c21 = ValueTracker(0)
        true_positive = always_redraw(lambda: DecimalNumber(c11.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,2)).get_center()))
        true_negative = always_redraw(lambda: DecimalNumber(c22.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,3)).get_center()))
        false_positive = always_redraw(lambda: DecimalNumber(c12.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,3)).get_center()))
        false_negative = always_redraw(lambda: DecimalNumber(c21.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,2)).get_center()))

        # Substitute all cell entries by the correspondent value trackers
        self.play([Write(true_positive), Write(true_negative), Write(false_positive), Write(false_negative)])
        self.remove(*[_ for _ in confusion_matrix.get_entries_without_labels()])

        # Loop through the dots and labels, animating them
        for dot, pred_label, true_label in zip(dots, pred_labels, true_labels):
            self.play(Write(dot), run_time=speed)
            self.play(dot.animate.move_to(square.get_center()), run_time=speed)
            self.play(FadeIn(pred_label, shift=DOWN), run_time=speed)
            if pred_label.tex_string == true_label.tex_string:
                self.play(Indicate(pred_label, color=GREEN), run_time=speed)
                if pred_label.tex_string == "Spam":
                    self.play(c11.animate.set_value(c11.get_value() + 1), run_time=speed)
                elif pred_label.tex_string == "Not Spam":
                    self.play(c22.animate.set_value(c22.get_value() + 1), run_time=speed)
            else:
                self.play(Indicate(pred_label, color=RED), run_time=speed)
                self.play(Transform(pred_label, true_label), run_time=speed)
                if pred_label.tex_string == "Spam" and true_label.tex_string == "Not Spam":
                    self.play(c12.animate.set_value(c12.get_value() + 1), run_time=speed)
                elif pred_label.tex_string == "Not Spam" and true_label.tex_string == "Spam":
                    self.play(c21.animate.set_value(c21.get_value() + 1), run_time=speed)
            self.play([FadeOut(dot), FadeOut(pred_label)], run_time=speed)
            self.remove(dot)
            if speed > 0.15:
                speed -= accelerator
                if speed < 0.15:
                    speed = 0.15
        
    def construct(self):
        def label_updater(obj):
            obj.next_to(square, UP, buff=0.5)

        square = Square()
        square_label = Tex("Classifier").next_to(square, UP, buff=0.5)
        # we want the label to always reside above the square
        square_label.add_updater(label_updater)

        triangle = Triangle(color=DARK_BLUE).set_fill(DARK_BLUE, opacity=1).rotate(PI / 3).scale(0.2).next_to(square, DOWN)

        # Part 1 - Defining how to compute errors
        self.next_section(skip_animations=True)

        self.play(Write(square), run_time=1)
        self.play(FadeIn(square_label, shift=UP * 0.5))
        self.play(Indicate(square_label), run_time=0.8)

        self.wait()
        self.play(Write(triangle))
        self.acting_classifier(triangle, n_dots=3, speed=0.7)
        self.wait()

        classifier = Group(square, square_label, triangle)
        self.play(classifier.animate.shift(LEFT * 4))

        predicted_text = Tex("Predicted")
        actual_text = Tex("Actual")

        # Create a larger backslash
        backslash = Line(start=LEFT * 4, end=RIGHT * 4, stroke_width=0.8).rotate(-PI / 6)

        # Position the texts relative to the backslash
        predicted_text.next_to(backslash.get_center(), DOWN * 4 + LEFT * 2.8).scale(1.8)
        actual_text.next_to(backslash.get_center(), UP * 4 + RIGHT * 2.8).scale(1.8)
        
        # Group the elements together
        pred_actual_group = VGroup(predicted_text, actual_text, backslash)

        confusion_matrix = MathTable(
            [["", ""],
            ["", ""]],
            col_labels=[Text("Spam").rotate(PI / 4), Text("Not Spam").rotate(PI / 4)],
            row_labels=[Text("Spam"), Text("Not Spam")],
            top_left_entry = pred_actual_group.scale(0.5),
            include_outer_lines=False,
            stroke_width=0.8,
        ).scale(0.5).shift(RIGHT)

        self.play(Write(confusion_matrix))
        self.wait()
        self.acting_classifier_with_matrix(confusion_matrix, square, triangle, n_dots=15, speed=0.8, accelerator=0.1)
        self.wait()
        self.play(FadeOut(*classifier))
        self.wait()
        self.play(confusion_matrix.animate.center())
        self.wait()

        # Part 2 - Explaining Accuracy, Precision, Recall and F1
        self.next_section()  
        metric = Text("Accuracy", font_size=50, color=WHITE).to_corner(UP).set_opacity(0.8)

        self.play(confusion_matrix.animate.to_corner(LEFT))
        self.play(Write(metric), run_time=0.8)
        self.wait()

        # Create the LaTeX formula
        accuracy_formula = MathTex(
            r"\text{Accuracy} = \frac{\text{True Positives} + \text{True Negatives}}{\text{Total Samples}}"
        ).shift(RIGHT)
        self.play(Write(accuracy_formula))
        
        
