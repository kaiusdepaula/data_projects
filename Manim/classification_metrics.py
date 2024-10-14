from manim import *
from random import seed, randint

class Hello(Scene):
    def construct(self):
        # Title text
        title = Text("Hi there!", font_size=70, color=WHITE, weight=BOLD)
        title.shift(UP*2)

        # Subtitle text
        subtitle = Text("Lets review Accuracy, Precision, Recall, F1 Score", font_size=40, color=WHITE)
        subtitle.shift(UP*0.5)

        # Add elements to scene with animations
        self.play(Write(subtitle), Write(title))
        self.wait()
        self.play(Unwrite(subtitle), Unwrite(title))

class Bye(Scene):
    def construct(self):
        # Title text
        title = Text("Thank you for watching!", font_size=70, color=WHITE, weight=BOLD)
        title.shift(UP*2)

        # Subtitle text
        subtitle = Text("Like and share!", font_size=40, color=WHITE)
        subtitle.shift(UP*0.5)

        # Add elements to scene with animations
        self.play(Write(subtitle), Write(title))
        self.wait()
        self.play(Unwrite(subtitle), Unwrite(title))


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

    # This is a mess, but it functions :) (Sorry for me in the future and for the reader)
    def acting_classifier_with_matrix(self, confusion_matrix, 
        true_positive, true_negative, false_positive, false_negative, 
        c11, c22, c12, c21, square, triangle, n_dots, speed, accelerator):        
        # Color hash map
        color_map = {0: GREEN, 1: RED, 2: YELLOW, 3: BLUE, 4: ORANGE}
        classes = {0: "Spam", 1: "Not Spam"}
        
        # Generate dots with random colors and labels
        dots = [Dot(color=color_map[randint(0, len(color_map)-1)]).scale(7).next_to(square, LEFT * 2.5) for _ in range(n_dots)]
        pred_labels = [Tex(classes[randint(0, len(classes)-1)]).next_to(triangle, DOWN, buff=0.3) for _ in range(n_dots)]
        true_labels = [Tex(classes[randint(0, len(classes)-1)]).next_to(triangle, DOWN, buff=0.3) for _ in range(n_dots)]

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
        self.next_section(skip_animations=False)

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

        # Add a logic to auto update matrix entries based on matches
        c11 = ValueTracker(0)
        c22 = ValueTracker(0)
        c12 = ValueTracker(0)
        c21 = ValueTracker(0)
        true_positive = always_redraw(lambda: DecimalNumber(c11.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,2)).get_center()))
        true_negative = always_redraw(lambda: DecimalNumber(c22.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,3)).get_center()))
        false_positive = always_redraw(lambda: DecimalNumber(c12.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,3)).get_center()))
        false_negative = always_redraw(lambda: DecimalNumber(c21.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,2)).get_center()))

        self.acting_classifier_with_matrix(confusion_matrix, 
        true_positive, true_negative, false_positive, false_negative, 
        c11, c22, c12, c21, square, triangle, n_dots=15, speed=0.8, accelerator=0.1)
        self.wait()
        self.play(FadeOut(*classifier))
        self.wait()
        self.play(confusion_matrix.animate.center())
        self.wait()

        self.play(confusion_matrix.animate.to_corner(LEFT))
        self.wait()

        # Stop event updaters in values inside confusion matrix
        true_positive = DecimalNumber(c11.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,2)).get_center())
        true_negative = DecimalNumber(c22.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,3)).get_center())
        false_positive = DecimalNumber(c12.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,3)).get_center())
        false_negative = DecimalNumber(c21.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,2)).get_center())

        # Part 2 - Explaining Accuracy
        self.next_section(skip_animations=False) 

        # Create the LaTeX formula
        accuracy_formula = MathTex(
            r"\text{Accuracy} = \frac{\text{True Positives} + \text{True Negatives}}{\text{Total Samples}}"
        ).to_corner(UP)
        self.play(Write(accuracy_formula))
        self.wait()
        # self.add(index_labels(accuracy_formula[0]))
        self.play([
            accuracy_formula[0][9:22].animate.set_color(GREEN),
            accuracy_formula[0][23:36].animate.set_color(PURPLE),
            true_positive.animate.set_color(GREEN),
            true_negative.animate.set_color(PURPLE)
        ])
        self.wait()

        # Variables to write equation
        plus_numerator = Tex("+")
        plus_den1 = Tex("+")
        plus_den2 = Tex("+")
        plus_den3 = Tex("+")
        result = (true_positive.get_value() + true_negative.get_value()) / \
            (true_positive.get_value() + true_negative.get_value() + \
            false_negative.get_value() + false_positive.get_value())
        equals = Tex(f"= {result:0.2f}")
        division = Line(start=1.5, end = 3.7)
        total = Group(true_positive.copy(), true_negative.copy(), false_negative.copy(), false_positive.copy()).add_to_back()

        tp = true_positive.set_color(GREEN).copy()
        tn = true_negative.set_color(PURPLE).copy()
        self.add(tp, tn, total)

        self.play([
            tp.animate.next_to(confusion_matrix, RIGHT, buff=2.5),
            tn.animate.next_to(confusion_matrix, RIGHT, buff=3.5)
        ])

        self.play([
            total.animate.arrange(buff=0.7).move_to(RIGHT * 2.15 + DOWN * 0.6)
        ])

        self.play([
            Write(plus_numerator.move_to(Group(tp,tn).get_center())), 
            Write(plus_den1.move_to(Group(total[0:2]).get_center())),
            Write(plus_den2.move_to(Group(total[1:3]).get_center())),
            Write(plus_den3.move_to(Group(total[2:4]).get_center())),
            Write(division.set_angle(0).move_to(Group(tp,tn).get_center() + DOWN * 0.3))
        ])

        self.play(Write(equals.next_to(division, RIGHT, buff=0.4)))
        self.wait()

        self.play([
            Unwrite(mobject) for mobject in [plus_numerator, plus_den1, plus_den2, plus_den3, division, *total, tp, tn, accuracy_formula, equals]
        ] + [
            true_positive.animate.set_color(WHITE),
            true_negative.animate.set_color(WHITE)  
        ])
        self.wait()
        
        self.next_section(skip_animations=False)

        # Part 3 - Explaining Precision

        # Create the LaTeX formula for Precision
        precision_formula = MathTex(
            r"\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}"
        ).to_corner(UP)
        self.play(Write(precision_formula))
        # self.add(index_labels(precision_formula[0]))
        self.wait()

        # Highlight True Positives and False Positives in the formula
        self.play([
            precision_formula[0][10:23].animate.set_color(BLUE),  # True Positives
            precision_formula[0][24:37].animate.set_color(BLUE),  # True Positives
            precision_formula[0][38:52].animate.set_color(RED),   # False Positives
            true_positive.animate.set_color(BLUE),
            false_positive.animate.set_color(RED)
        ])
        self.wait()

        # Variables to write equation
        plus_den = Tex("+")
        precision_result = true_positive.get_value() / (true_positive.get_value() + false_positive.get_value())
        equals = Tex(f"= {precision_result:0.2f}")
        division = Line(start=2.5, end=3.7)

        # Copy true positive and false positive for visual equation
        tp = true_positive.set_color(BLUE).copy()
        fp = false_positive.set_color(RED).copy()
        total = Group(true_positive.copy(), false_positive.copy()).add_to_back()
        self.add(tp, fp, total)

        # Animate moving the true positive and false positive values next to confusion matrix
        self.play([
            tp.animate.next_to(confusion_matrix, RIGHT, buff=3),
            total.animate.arrange(buff=0.7).move_to(RIGHT * 2.15 + DOWN * 0.6)
        ])
        # Animate equation
        self.play([
            Write(plus_den.move_to(Group(total[0:2]).get_center())),
            Write(division.set_angle(0).move_to(tp.get_center() + DOWN * 0.3))
        ])

        # Show the result of Precision
        self.play(Write(equals.next_to(division, RIGHT, buff=0.4)))
        self.wait()

        # Clean up
        self.play([
            Unwrite(mobject) for mobject in [plus_den, division, tp, fp, precision_formula, equals, *total]
            ] + [
            true_positive.animate.set_color(WHITE),
            false_positive.animate.set_color(WHITE)
            ])
        self.wait()
        
        self.next_section(skip_animations=False) 

        # Part 4 - Explaining Recall

        # Create the LaTeX formula for Recall
        recall_formula = MathTex(
            r"\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}"
        ).to_corner(UP)
        self.play(Write(recall_formula))
        # self.add(index_labels(recall_formula[0]))
        self.wait()

        # Highlight True Positives and False Negatives in the formula
        self.play([
            recall_formula[0][7:20].animate.set_color(BLUE),   # True Positives
            recall_formula[0][21:34].animate.set_color(BLUE),  # True Positives
            recall_formula[0][35:49].animate.set_color(RED),   # False Negatives
            true_positive.animate.set_color(BLUE),
            false_negative.animate.set_color(RED)
        ])
        self.wait()

        # Variables to write equation
        plus_den = Tex("+")
        recall_result = true_positive.get_value() / (true_positive.get_value() + false_negative.get_value())
        equals = Tex(f"= {recall_result:0.2f}")
        division = Line(start=2.5, end=3.7)

        # Copy true positive and false negative for visual equation
        tp = true_positive.set_color(BLUE).copy()
        fn = false_negative.set_color(RED).copy()
        total = Group(true_positive.copy(), false_negative.copy()).add_to_back()
        self.add(tp, fn, total)

        # Animate moving the true positive and false negative values next to confusion matrix
        self.play([
            tp.animate.next_to(confusion_matrix, RIGHT, buff=3),
            total.animate.arrange(buff=0.7).move_to(RIGHT * 2.15 + DOWN * 0.6)
        ])

        # Animate equation
        self.play([
            Write(plus_den.move_to(Group(total[0:2]).get_center())),
            Write(division.set_angle(0).move_to(tp.get_center() + DOWN * 0.3))
        ])

        # Show the result of Recall
        self.play(Write(equals.next_to(division, RIGHT, buff=0.4)))
        self.wait()

        # Clean up
        self.play([
            Unwrite(mobject) for mobject in [plus_den, division, tp, fn, recall_formula, equals, *total]
            ] + [
            true_positive.animate.set_color(WHITE),
            false_negative.animate.set_color(WHITE)
        ])
        self.wait()

        self.next_section(skip_animations=False)
        # Part 5 - Explaining F1 Score

        # Create the LaTeX formula for F1 Score
        f1_formula = MathTex(
            r"{{\text{F1 Score} = 2 \times}} \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}"
        ).to_corner(UP)
        f1_formula_expanded = MathTex(
            r"{{\text{F1 Score} = 2 \times}} \frac{\frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}} \times \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}}{\frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}} + \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}}"
        ).to_corner(UP).scale(0.7)
        self.play(Write(f1_formula))
        self.wait()
        self.play(
            TransformMatchingTex(
                f1_formula, 
                f1_formula_expanded
            ), run_time=2
        )
        # Highlight cells in formula and in matrix
        self.play([
            f1_formula_expanded[1][0:13].animate.set_color(BLUE),    
            f1_formula_expanded[1][14:27].animate.set_color(BLUE), 
            f1_formula_expanded[1][28:42].animate.set_color(RED),  
            f1_formula_expanded[1][43:56].animate.set_color(BLUE),    
            f1_formula_expanded[1][57:70].animate.set_color(BLUE),
            f1_formula_expanded[1][71:85].animate.set_color(ORANGE),
            f1_formula_expanded[1][86:99].animate.set_color(BLUE),
            f1_formula_expanded[1][100:113].animate.set_color(BLUE),
            f1_formula_expanded[1][114:128].animate.set_color(RED),
            f1_formula_expanded[1][129:142].animate.set_color(BLUE),
            f1_formula_expanded[1][143:156].animate.set_color(BLUE),
            f1_formula_expanded[1][157:171].animate.set_color(ORANGE),
            true_positive.animate.set_color(BLUE),
            false_positive.animate.set_color(RED),
            false_negative.animate.set_color(ORANGE)
        ])
        self.wait(2)

        self.play(
            TransformMatchingTex(
                f1_formula_expanded,
                f1_formula
            ), run_time=2
        )

        # Show the previous results for Precision and Recall
        
        self.play(f1_formula.animate.scale(0.8).next_to(confusion_matrix, RIGHT * 2))
        precision_value = Tex(f"Precision = {precision_result:0.2f}").align_on_border(UP)
        recall_value = Tex(f"Recall = {recall_result:0.2f}").next_to(precision_value, DOWN, buff=0.2)
        self.play(Write(precision_value), Write(recall_value))
        self.wait()

        f1_solved = MathTex(
            fr"{{{{\text{{F1 Score}} = 2 \times}}}} \frac{{\text{precision_result:0.2f} \times \text{recall_result:0.2f}}}{{\text{precision_result:0.2f} + \text{recall_result:0.2f}}}"
        ).next_to(confusion_matrix, RIGHT * 2)

        # Animate moving Precision and Recall values into the F1 formula
        self.play([
            TransformMatchingTex(f1_formula, f1_solved)
        ])
        
        f1_result = 2 * (precision_result * recall_result) / (precision_result + recall_result)
        f1_final = MathTex(
            fr"{{\text{{F1 Score}} = {f1_result:0.2f}}}"
        ).next_to(confusion_matrix, RIGHT * 2)

        self.play([
            TransformMatchingShapes(f1_solved, f1_final)
        ])

        # Clean up
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(2)
