from manim import *
from random import seed, randint

config.frame_size = [1080,1920] # [WIDTH, HEIGHT]
seed(42)
class ShortVideo(Scene):
    # This is a mess, but it functions :) (Sorry for me in the future and for the reader)
    def acting_classifier_with_matrix(self, confusion_matrix, 
        true_positive, true_negative, false_positive, false_negative, 
        c11, c22, c12, c21, square, triangle, n_dots, speed, accelerator):        
        # Color hash map
        color_map = {0: GREEN, 1: RED, 2: YELLOW, 3: BLUE, 4: ORANGE}
        classes = {0: "Spam", 1: "Não Spam"}
        
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
                elif pred_label.tex_string == "Não Spam":
                    self.play(c22.animate.set_value(c22.get_value() + 1), run_time=speed)
            else:
                self.play(Indicate(pred_label, color=RED), run_time=speed)
                self.play(Transform(pred_label, true_label), run_time=speed)
                if pred_label.tex_string == "Spam" and true_label.tex_string == "Não Spam":
                    self.play(c12.animate.set_value(c12.get_value() + 1), run_time=speed)
                elif pred_label.tex_string == "Não Spam" and true_label.tex_string == "Spam":
                    self.play(c21.animate.set_value(c21.get_value() + 1), run_time=speed)
            self.play([FadeOut(dot), FadeOut(pred_label)], run_time=speed)
            self.remove(dot)
            if speed > 0.2:
                speed -= accelerator
                if speed < 0.2:
                    speed = 0.2
        
    def construct(self):
        self.camera.background_color = "#1c1c1c"
        def label_updater(obj):
            obj.next_to(square, UP, buff=0.5)

        square = Square()
        square_label = Tex("Classificador").next_to(square, UP, buff=0.5)
        # we want the label to always reside above the square
        square_label.add_updater(label_updater)

        triangle = Triangle(color=DARK_BLUE).set_fill(DARK_BLUE, opacity=1).rotate(PI / 3).scale(0.2).next_to(square, DOWN)

        # Part 1 - Defining how to compute errors
        self.next_section(skip_animations=True)

        self.play(Write(square), run_time=1)
        self.play(FadeIn(square_label, shift=UP * 0.5))
        self.play(Indicate(square_label), run_time=0.8)

        classifier = Group(square, square_label, triangle)
        self.play(classifier.animate.align_on_border(UP))

        predicted_text = Tex("Previsto")
        actual_text = Tex("Observado")

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
            col_labels=[Text("Spam").rotate(PI / 4), Text("Não Spam").rotate(PI / 4)],
            row_labels=[Text("Spam"), Text("Não Spam")],
            top_left_entry = pred_actual_group.scale(0.5),
            include_outer_lines=False,
            stroke_width=0.8,
        ).scale(0.9)

        self.play(Write(confusion_matrix))
        self.wait()

        # Add a logic to auto update matrix entries based on matches
        c11 = ValueTracker(0)
        c22 = ValueTracker(0)
        c12 = ValueTracker(0)
        c21 = ValueTracker(0)
        true_positive = always_redraw(lambda: DecimalNumber(c11.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,2)).get_center()).scale(1.5))
        true_negative = always_redraw(lambda: DecimalNumber(c22.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,3)).get_center()).scale(1.5))
        false_positive = always_redraw(lambda: DecimalNumber(c12.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,3)).get_center()).scale(1.5))
        false_negative = always_redraw(lambda: DecimalNumber(c21.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,2)).get_center()).scale(1.5))

        self.acting_classifier_with_matrix(confusion_matrix, 
        true_positive, true_negative, false_positive, false_negative, 
        c11, c22, c12, c21, square, triangle, n_dots=15, speed=0.8, accelerator=0.2)
        self.wait()
        self.play(FadeOut(*classifier))
        self.wait()
        self.play(confusion_matrix.animate.center())
        self.wait()

        self.play(confusion_matrix.animate.shift(DOWN * 0.7))
        self.wait()

        # Stop event updaters in values inside confusion matrix
        true_positive = DecimalNumber(c11.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,2)).get_center()).scale(1.5)
        true_negative = DecimalNumber(c22.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,3)).get_center()).scale(1.5)
        false_positive = DecimalNumber(c12.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((2,3)).get_center()).scale(1.5)
        false_negative = DecimalNumber(c21.get_value(), num_decimal_places = 0).move_to(confusion_matrix.get_cell((3,2)).get_center()).scale(1.5)

        # Part 2 - Explaining Accuracy
        self.next_section(skip_animations=False) 

        # Create the LaTeX formula
        accuracy_formula = MathTex(
            r"\text{Accuracy} = \frac{\text{Verdadeiro Positivos} + \text{Verdadeiro Negativos}}{\text{Total de Amostras}}"
        ).next_to(confusion_matrix, UP * 2)
        self.play(Write(accuracy_formula))
        self.wait()
        # self.add(index_labels(accuracy_formula[0]))
        self.play([
            accuracy_formula[0][9:28].animate.set_color(GREEN),
            accuracy_formula[0][29:48].animate.set_color(PURPLE),
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
        equals = Tex(f"= {result:0.2f}").scale(1.4)
        division = Line(start=1.2, end = 3.7)
        total = Group(true_positive.copy(), true_negative.copy(), false_negative.copy(), false_positive.copy()).add_to_back()

        tp = true_positive.set_color(GREEN).copy().add_to_back()
        tn = true_negative.set_color(PURPLE).copy().add_to_back()
        self.add(tp, tn, total)

        self.play([
            tp.animate.next_to(confusion_matrix, DOWN, buff = 1.2).shift(LEFT * 0.6),
            tn.animate.next_to(confusion_matrix, DOWN, buff = 1.2).shift(RIGHT * 0.6)
        ])

        self.play([
            total.animate.arrange(buff=0.7).move_to(Group(tp,tn).get_center() + DOWN * 0.8)
        ])

        self.play([
            Write(plus_numerator.move_to(Group(tp,tn).get_center())), 
            Write(plus_den1.move_to(Group(total[0:2]).get_center())),
            Write(plus_den2.move_to(Group(total[1:3]).get_center())),
            Write(plus_den3.move_to(Group(total[2:4]).get_center())),
            Write(division.set_angle(0).move_to(Group(tp,tn).get_center() + DOWN * 0.4))
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
            r"\text{Precision} = \frac{\text{Verdadeiro Positivos}}{\text{Verdadeiro Positivos} + \text{Falso Positivos}}"
        ).next_to(confusion_matrix, UP * 2)
        self.play(Write(precision_formula))
        # self.add(index_labels(precision_formula[0]))
        self.wait()

        # Highlight Verdadeiro Positivos and Falso Positivos in the formula
        self.play([
            precision_formula[0][10:29].animate.set_color(BLUE),  # Verdadeiro Positivos
            precision_formula[0][30:49].animate.set_color(BLUE),  # Verdadeiro Positivos
            precision_formula[0][50:64].animate.set_color(RED),   # Falso Positivos
            true_positive.animate.set_color(BLUE),
            false_positive.animate.set_color(RED)
        ])
        self.wait()

        # Variables to write equation
        plus_den = Tex("+")
        precision_result = true_positive.get_value() / (true_positive.get_value() + false_positive.get_value())
        equals = Tex(f"= {precision_result:0.2f}").scale(1.4)
        division = Line(start=2.5, end=3.7)

        # Copy true positive and false positive for visual equation
        tp = true_positive.set_color(BLUE).copy()
        fp = false_positive.set_color(RED).copy()
        total = Group(true_positive.copy(), false_positive.copy()).add_to_back()
        self.add(tp, fp, total)

        # Animate moving the true positive and false positive values next to confusion matrix
        self.play([
            tp.animate.next_to(confusion_matrix, DOWN, buff = 1.2)
        ])

        self.play(
            total.animate.arrange(buff=0.7).next_to(tp, DOWN, buff=0.5)
        )
        # Animate equation
        self.play([
            Write(plus_den.move_to(Group(total[0:2]).get_center())),
            Write(division.set_angle(0).move_to(tp.get_center() + DOWN * 0.5))
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
            r"\text{Recall} = \frac{\text{Verdadeiro Positivos}}{\text{Verdadeiro Positivos} + \text{Falso Negativos}}"
        ).next_to(confusion_matrix, UP * 2)
        self.play(Write(recall_formula))
        # self.add(index_labels(recall_formula[0]))
        self.wait()

        # Highlight Verdadeiro Positivos and Falso Negativos in the formula
        self.play([
            recall_formula[0][7:26].animate.set_color(BLUE),   # Verdadeiro Positivos
            recall_formula[0][27:46].animate.set_color(BLUE),  # Verdadeiro Positivos
            recall_formula[0][47:65].animate.set_color(RED),   # Falso Negativos
            true_positive.animate.set_color(BLUE),
            false_negative.animate.set_color(RED)
        ])
        self.wait()

        # Variables to write equation
        plus_den = Tex("+")
        recall_result = true_positive.get_value() / (true_positive.get_value() + false_negative.get_value())
        equals = Tex(f"= {recall_result:0.2f}").scale(1.4)
        division = Line(start=2.5, end=3.7)

        # Copy true positive and false negative for visual equation
        tp = true_positive.set_color(BLUE).copy()
        fn = false_negative.set_color(RED).copy()
        total = Group(true_positive.copy(), false_negative.copy()).add_to_back()
        self.add(tp, fn, total)

        # Animate moving the true positive and false negative values next to confusion matrix
        self.play([
            tp.animate.next_to(confusion_matrix, DOWN, buff = 1.2)
        ])

        self.play(
            total.animate.arrange(buff=0.7).next_to(tp, DOWN, buff=0.5)
        )

        # Animate equation
        self.play([
            Write(plus_den.move_to(Group(total[0:2]).get_center())),
            Write(division.set_angle(0).move_to(tp.get_center() + DOWN * 0.5))
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
        ).next_to(confusion_matrix, UP * 2)
        f1_formula_expanded = MathTex(
            r"{{\text{F1 Score} = 2 \times}} \frac{\frac{\text{Verdadeiro Positivos}}{\text{Verdadeiro Positivos} + \text{Falso Positivos}} \times \frac{\text{Verdadeiro Positivos}}{\text{Verdadeiro Positivos} + \text{Falso Negativos}}}{\frac{\text{Verdadeiro Positivos}}{\text{Verdadeiro Positivos} + \text{Falso Positivos}} + \frac{\text{Verdadeiro Positivos}}{\text{Verdadeiro Positivos} + \text{Falso Negativos}}}"
        ).next_to(confusion_matrix, UP * 2).scale(0.7)
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
            f1_formula_expanded[1][0:19].animate.set_color(BLUE),    
            f1_formula_expanded[1][20:39].animate.set_color(BLUE), 
            f1_formula_expanded[1][40:54].animate.set_color(RED),  
            f1_formula_expanded[1][55:74].animate.set_color(BLUE),    
            f1_formula_expanded[1][75:94].animate.set_color(BLUE),
            f1_formula_expanded[1][95:109].animate.set_color(ORANGE),
            f1_formula_expanded[1][110:129].animate.set_color(BLUE),
            f1_formula_expanded[1][130:149].animate.set_color(BLUE),
            f1_formula_expanded[1][150:164].animate.set_color(RED),
            f1_formula_expanded[1][165:184].animate.set_color(BLUE),
            f1_formula_expanded[1][185:204].animate.set_color(BLUE),
            f1_formula_expanded[1][205:219].animate.set_color(ORANGE),
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
        
        self.play(f1_formula.animate.scale(1.4).next_to(confusion_matrix, DOWN, buff=1.2))
        precision_value = Tex(f"Precision = {precision_result:0.2f}").align_on_border(UP)
        recall_value = Tex(f"Recall = {recall_result:0.2f}").next_to(precision_value, DOWN, buff=0.2)
        self.play(Write(precision_value), Write(recall_value))
        self.wait()

        f1_solved = MathTex(
            fr"{{{{\text{{F1 Score}} = 2 \times}}}} \frac{{\text{precision_result:0.2f} \times \text{recall_result:0.2f}}}{{\text{precision_result:0.2f} + \text{recall_result:0.2f}}}"
        ).next_to(confusion_matrix, DOWN, buff=1.2).scale(1.4)

        # Animate moving Precision and Recall values into the F1 formula
        self.play([
            TransformMatchingTex(f1_formula, f1_solved)
        ])
        
        f1_result = 2 * (precision_result * recall_result) / (precision_result + recall_result)
        f1_final = MathTex(
            fr"{{\text{{F1 Score}} = {f1_result:0.2f}}}"
        ).next_to(confusion_matrix, DOWN, buff=1.2).scale(1.4)

        self.play([
            TransformMatchingShapes(f1_solved, f1_final)
        ])

        # Clean up
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(2)
