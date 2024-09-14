from manim import *

class ExampleTable(Scene):
    def construct(self):
        table_origin = Table(
            [["200", "Setor A", "Produto X", "Região Norte", "..."],
            ["200", "Setor B", "Produto Y", "Região Sul", "..."],
            ["201", "Setor A", "Produto Z", "Região Norte", "..."],
            ["201", "Setor A", "Produto Z", "Região Norte", "..."],
            ["...", "...", "...", "...", "..."],
            ["202", "Setor C", "Produto W", "Região Oeste", "..."]],
            col_labels=[Text("Departamento"), Text("Setor"), Text("Produto"), Text("Região"), Text("...")],
            include_outer_lines=True
        ).scale(0.5)

        table_transformed = Table(
            [["200SetorAProdutoXRegiãoNorte", "..."],
            ["200SetorBProdutoYRegiãoSul", "..."],
            ["201SetorAProdutoZRegiãoNorte", "..."],
            ["201SetorAProdutoZRegiãoNorte", "..."],
            ["...", "..."],
            ["202SetorCProdutoWRegiãoOeste", "..."]],
            col_labels=[Text("ID"), Text("...")],
            include_outer_lines=True
        ).scale(0.5).shift(LEFT * 2)

        table_transformed_legible =  Table(
            [["ID1", "..."],
            ["ID2", "..."],
            ["ID3", "..."],
            ["ID3", "..."],
            ["...", "..."],
            ["IDn", "..."]],
            col_labels=[Text("ID"), Text("...")],
            include_outer_lines=True
        ).scale(0.5)

        table_final = Table(
            [["ID1", "Roupas", "1.0"],
            ["ID2", "Alimentos", "1.0"],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["...", "...", "..."],
            ["IDn", "Eletrônicos", "1.0"]],
            col_labels=[Text("ID"), Text("Classe"), Text("Percentual da Classe")],
            include_outer_lines=True
        ).scale(0.5)

        # Animation loop
        self.play(Write(table_origin), run_time=4)
        self.wait()
        self.play(AnimationGroup(*[
            Indicate(cell, scale_factor=1.6, color=RED)
            for cell in table_origin.get_rows()[1][0:-1]
        ], lag_ratio=0.4))
        self.play(ReplacementTransform(table_origin, table_transformed), run_time=3)
        self.wait()
        self.play(ReplacementTransform(table_transformed, table_transformed_legible), run_time=3)
        self.wait()
        self.play(table_transformed_legible.animate.shift(LEFT * 1.5))
        self.play(ReplacementTransform(table_transformed_legible, table_final), run_time=3)
        self.wait()
        temp = table_final.add_highlighted_cell((4,3), color=GREEN).add_highlighted_cell((5,3), color=GREEN)
        self.play([ReplacementTransform(table_final, temp), Circumscribe(Group(table_final.get_cell((4,3)), table_final.get_cell((5,3))), color=RED, fade_out= True)], run_time=2)
        self.wait()
        self.play(FadeOut(table_final), run_time=2)

class Classifier(Scene):
    def construct(self):
        def label_updater(obj):
            """An updater which continually move an object above the square.
            The first parameter (obj) is always the object that is being updated."""
            obj.next_to(square, UP, buff=0.5)

        square = Square()
        square_label = Tex("Classificador").next_to(square, UP, buff=0.5)
        # we want the label to always reside above the square
        square_label.add_updater(label_updater)

        dot = Dot(color=BLUE).scale(7)
        dot_label = Tex("Linha da Tabela (ID)").next_to(dot, UP, buff=0.5)

        triangle = Triangle(color=WHITE).set_fill(WHITE, opacity=1).rotate(PI / 3).scale(0.2).next_to(square, DOWN)
        triangle_label = Tex("Roupas").next_to(triangle, DOWN, buff=0.5)

        dots = [
            Dot(color=GREEN).scale(7), 
            Dot(color=RED).scale(7), 
            Arc(angle=-PI, color=GREEN).set_fill(GREEN, opacity=1).scale(0.5).shift(UP * 0.2)
        ]
        labels = [
            Tex("Móveis").next_to(triangle, DOWN, buff=0.5), 
            Tex("Alimentos").next_to(triangle, DOWN, buff=0.5), 
            Tex("?").next_to(triangle, DOWN, buff=0.5),
        ]

        # Animation loop
        self.play(Write(square), run_time=1)
        self.play(FadeIn(square_label, shift=UP * 0.5))
        self.play(Indicate(square_label))
        self.play(square.animate.shift(RIGHT * 5))

        self.play(Write(dot), run_time=2)
        self.play(FadeIn(dot_label, shift=UP * 0.5))
        self.play(FadeOut(dot_label))

        self.play([square.animate.shift(LEFT * 5), dot.animate.shift(LEFT * 5)])
        self.wait()
        self.play(Write(triangle)) # Aponta para a resposta do classificador

        self.play(dot.animate.shift(RIGHT * 5))
        self.play(FadeIn(triangle_label, shift=DOWN))
        self.play([dot.animate.shift(RIGHT * 10), FadeOut(triangle_label)])
        self.remove(dot)

        contador = 0
        for dot, label in zip(dots, labels):
            self.play(Write(dot.shift(LEFT * 5)), run_time=0.5)
            self.wait(0.5)
            self.play(dot.animate.shift(RIGHT * 5), run_time=1)
            self.play(FadeIn(label, shift=DOWN))
            if contador < 2:
                self.play([dot.animate.shift(RIGHT * 10), FadeOut(label)])
                self.remove(dot)
                contador += 1
        self.wait()
        self.play(FadeOut(square, square_label, triangle, dot, label), run_time=1)

class Solutions(Scene):
    def construct(self):
        first_arrow = Arrow(start=LEFT * 1.2, end=LEFT * 0.1, color=GOLD).scale(1.5)

        table = Table(
            [["ID1", "Roupas", "1.0"],
            ["ID2", "Alimentos", "1.0"],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["ID4", "Bebidas", "1.0"],
            ["ID5", "Móveis", "0.8"],
            ["ID5", "Eletrônicos", "0.2"],
            ["ID6", "Vestuário", "1.0"],
            ["ID7", "Alimentos", "0.7"],
            ["ID7", "Bebidas", "0.3"],
            ["ID8", "Eletrônicos", "1.0"],
            ["ID9", "Roupas", "1.0"],
            ["ID10", "Automóveis", "0.6"],
            ["ID10", "Peças", "0.4"]],
            col_labels=[Text("ID"), Text("Classe"), Text("Percentual da Classe")],
            include_outer_lines=True
        ).scale(0.3)

        table_expanded = Table(
            [["...", "...", "..."],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Eletrônicos", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["ID3", "Móveis", "0.5"],
            ["...", "...", "..."]],
            col_labels=[Text("ID"), Text("Classe"), Text("Percentual da Classe")],
            include_outer_lines=True
        ).scale(0.3)

        filtered_table = Table(
            [["ID1", "Roupas", "1.0"],
            ["ID2", "Alimentos", "1.0"],
            ["ID4", "Bebidas", "1.0"],
            ["ID5", "Móveis", "0.8"],
            ["ID6", "Vestuário", "1.0"],
            ["ID7", "Alimentos", "0.7"],
            ["ID8", "Eletrônicos", "1.0"],
            ["ID9", "Roupas", "1.0"],
            ["ID10", "Automóveis", "0.6"]],
            col_labels=[Text("ID"), Text("Classe"), Text("Percentual da Classe")],
            include_outer_lines=True
        ).scale(0.3)

        # Dados da tabela original
        table_final = Table(
            [["ID1", "Roupas", "1.0", "Roupas:0.7;Eletrônicos:0.1; ..."],
            ["ID2", "Alimentos", "1.0", "Alimentos:0.8;Bebidas:0.1;..."],
            ["ID3", "Eletrônicos", "0.5", "Eletrônicos:0.6;Móveis:0.2;..."],
            ["ID3", "Móveis", "0.5", "Eletrônicos:0.6;Móveis:0.2;..."],
            ["ID4", "Bebidas", "1.0", "Bebidas:0.9;Alimentos:0.1;..."],
            ["ID5", "Móveis", "0.8", "Móveis:0.6;Eletrônicos:0.2;..."],
            ["ID5", "Eletrônicos", "0.2", "Móveis:0.6;Eletrônicos:0.2;..."],
            ["ID6", "Vestuário", "1.0", "Vestuário:0.9;Roupas:0.1;..."],
            ["ID7", "Alimentos", "0.7", "Alimentos:0.8;Bebidas:0.2;..."],
            ["ID7", "Bebidas", "0.3", "Alimentos:0.8;Bebidas:0.2;..."],
            ["ID8", "Eletrônicos", "1.0", "Eletrônicos:0.85;Móveis:0.15;..."],
            ["ID9", "Roupas", "1.0", "Roupas:0.9;Eletrônicos:0.07;..."],
            ["ID10", "Automóveis", "0.6", "Automóveis:0.7;Peças:0.3;..."],
            ["ID10", "Peças", "0.4", "Automóveis:0.7;Peças:0.3;..."]],
            col_labels=[Text("ID"), Text("Classe"), Text("Percentual da Classe"), Text("Recomendações")],
            include_outer_lines=True
        ).scale(0.3)

        self.play(Write(table), run_time=5)
        self.wait()
        self.play(table.animate.shift(LEFT * 3.2), run_time=3)
        self.play(Write(first_arrow.next_to(table, RIGHT)), run_time=1)
        self.wait()
        self.play(first_arrow.animate.shift(RIGHT * 0.2), run_time = 0.6)
        self.play(first_arrow.animate.shift(LEFT * 0.2), run_time = 0.6)
        self.play(DrawBorderThenFill(table_expanded.next_to(first_arrow, RIGHT)), run_time=3)
        self.wait()
        self.play(Circumscribe(Group(table.get_cell((5, 1)), table.get_cell((4, 1))), color=BLUE, fade_out=True), run_time=2)
        cells = [
            table_expanded.get_entries((3, 2)),
            table_expanded.get_entries((4, 2)),
            table_expanded.get_entries((5, 2)),
            table_expanded.get_entries((6, 2)),
            table_expanded.get_entries((7, 2)),
            table_expanded.get_entries((8, 2)),
            table_expanded.get_entries((9, 2)),
            table_expanded.get_entries((10, 2)),
            table_expanded.get_entries((11, 2)),
            table_expanded.get_entries((12,2))
        ]
        self.play(AnimationGroup([
            Indicate(cell, color=RED, scale_factor=1.8)
            for cell in cells
        ], lag_ratio=0.6), run_time=4)
        self.wait()
        self.play(Uncreate(table_expanded), run_time=3)
        self.wait()
        self.play(first_arrow.animate.shift(RIGHT * 0.2), run_time = 0.6)
        self.play(first_arrow.animate.shift(LEFT * 0.2), run_time = 0.6)
        self.play(DrawBorderThenFill(filtered_table.next_to(first_arrow, RIGHT)), run_time=3)
        self.wait()
        cells = [
            table.get_entries((2, 3)),
            table.get_entries((3, 3)),
            table.get_entries((6, 3)),
            table.get_entries((7, 3)),
            table.get_entries((9, 3)),
            table.get_entries((10, 3)),
            table.get_entries((12, 3)),
            table.get_entries((13, 3)),
            table.get_entries((14,3))
        ]
        self.play(AnimationGroup([
            Indicate(cell, color=RED, scale_factor=1.8)
            for cell in cells
        ], lag_ratio=0.6), run_time=4)
        self.wait()
        self.play([Unwrite(filtered_table), Unwrite(first_arrow)], run_time=3)
        self.wait()
        self.play(table.animate.shift(RIGHT * 3.7), run_time=3)
        self.wait()
        self.play(ReplacementTransform(table, table_final), run_time=4)
        self.wait()
        grupo_header = table_final.get_rows()[0].copy()
        grupo = table_final.get_rows()[3:5].copy()
        self.add(grupo, grupo_header)
        self.play(Unwrite(table_final, reverse=False), run_time=1)
        self.play([grupo.animate.scale(1.5).center(), grupo_header.animate.scale(1.5).shift(0.5* DOWN)], run_time=2)
        self.wait()
        self.play([Unwrite(grupo_header), Unwrite(grupo[1])], run_time=2)
        grupo = grupo[0]
        self.play(grupo.animate.center(), run_time=1)
        self.wait()
        self.play([Circumscribe(grupo[1], color=BLUE), Circumscribe(grupo[3], color=BLUE)])
        self.wait()
        self.play(FadeOut(grupo), run_time=2)

class Final(Scene):
    def construct(self):
        square = Square()
        triangle = Triangle(color=WHITE).set_fill(WHITE, opacity=1).rotate(PI / 3).scale(0.2).next_to(square, DOWN)
        def label_updater(obj):
            obj.next_to(square, DOWN, buff=0.2)

        triangle.add_updater(label_updater)
        dots = [
            Dot(color=GREEN).scale(5).shift(DOWN), 
            Dot(color=RED).scale(5).shift(DOWN), 
            Dot(color=DARK_BROWN).scale(5).shift(DOWN),
            Dot(color=PINK).scale(5).shift(DOWN), 
            Dot(color=BLUE).scale(5).shift(DOWN), 
            Dot(color=GRAY).scale(5).shift(DOWN)
        ]

        self.play(Write(square), Write(triangle), run_time=2)
        self.wait()
        self.play(Rotate(triangle, PI/3, rate_func=linear), run_time=1)
        self.wait()

        self.play(square.animate.shift(UP * 2))

        first = True
        for dot in dots:
            if first:
                self.play(Write(dot.shift(LEFT * 2.6)), run_time=0.5)
                first = False
            else:
                self.play(Write(dot.next_to(last_dot, RIGHT)), run_time=0.5)
            last_dot = dot

        for dot in dots:
            self.play(dot.animate.move_to(square.get_center()), run_time=0.7)
            self.play(FadeOut(dot), run_time=0.4)

        self.play(square.animate.center())
        self.play(Rotate(triangle, -PI/3, rate_func=linear), run_time=1)

        last_dot = Arc(angle=-PI, color=GREEN).set_fill(GREEN, opacity=1).scale(0.5).shift(UP * 0.5)
        last_label = Tex("Eletrônicos:0.6;Móveis:0.2;...").next_to(triangle, DOWN, buff=0.5)
        self.play(Write(last_dot.shift(LEFT * 5)), run_time=1)
        self.wait()
        self.play(last_dot.animate.move_to(square), run_time=1)
        self.wait()
        self.play(FadeIn(last_label, shift=DOWN), run_time=1)
        self.wait()
        self.play([last_dot.animate.shift(RIGHT * 10), FadeOut(last_label)], run_time=1)

        self.wait()
        self.play(FadeOut(square, triangle), run_time=1)