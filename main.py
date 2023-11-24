from manim import *
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

import os

class Title(Scene):
    def construct(self):
        title = Text("Ramanujan and Pi", font_size=30)
        subtitle = Text("Ref: PI - The next generation. Chapter 10", font_size=24).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(subtitle))

class Ramanujan(Scene):
    def construct(self):
        # Cargar la imagen de contorno en Manim
        img_mobject = ImageMobject("Ramanujan.jpg").scale(0.5)

        # Añadir un texto encima de la imagen
        text = Text("Ramanujan").scale(2)
        self.play(Write(text))
        self.wait(2)
        self.play(text.animate.scale(0.5).to_edge(UP))

        self.play(FadeIn(img_mobject))
        self.wait(6)
        # Fade out everything from the previous scene
        self.play(FadeOut(Group(*self.mobjects)))

        # Title
        title = Text("Métodos de Ramanujan\npara calcular Pi", line_spacing=1.5).scale(1.5)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.scale(0.5).to_edge(UP))

        # Explanation
        explanation = Text("""
            Ramanujan desarrolló algoritmos que usaban ecuaciones
            modulares y que convergían muy rápidamente a Pi.
        """).scale(0.75).next_to(title, DOWN)
        self.play(Write(explanation))

        # Show the formula
        formula = MathTex(r"1 / \pi = 2\sqrt{2} / 9801 \sum_{n=0}^{\infty} \frac{(4n)!(1103+26390n)}{(n!)^4 396^{4n}}").next_to(explanation, DOWN)
        self.play(Write(formula))

        # Calculate the middle point between the explanation and the bottom edge of the screen
        middle_point = (explanation.get_bottom() + config.frame_y_radius * DOWN) / 2

        # Show a number line with the value of Pi
        number_line = NumberLine(x_range=[3, 3.2, 0.05], length=10, include_numbers=True, include_tip=True).move_to(middle_point)
        self.play(Create(number_line))

        # Show how the terms of the series add up to Pi
        dots = VGroup()
        pi_sequence = [3, 3.1, 3.14, 3.141, 3.1415, 3.14159]
        for i in range(len(pi_sequence)):
            dot = Dot().move_to(number_line.n2p(pi_sequence[i])).set_color(RED)
            dots.add(dot)
            self.play(FadeIn(dot), run_time=0.5)
            self.wait(0.5)
        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))


class ArchimedesMethod(Scene):
    def construct(self):
        # Explicación de la fórmula p_c
        title = Text("ARCHIMEDES' METHOD", font_size=30).shift(UP)
        subtitle = VGroup(
            MathTex(r"\text{Este método sirve para estimar } \pi \text{. Se basó en polígonos regulares}"),
            MathTex(r"\text{inscritos y circunscritos en un círculo de diámetro unitario. Los perímetros}"),
            MathTex(r"\text{de estos polígonos proporcionaron límites para } \pi \text{. Aunque hoy en día}"),
            MathTex(r"\text{podríamos usar funciones trigonométricas para calcular estos perímetros,}"),
            MathTex(r"\text{Arquímedes desarrolló relaciones equivalentes usando solo construcciones geométricas.}"),
            MathTex(r"\text{Con polígonos de 96 lados, determinó que } 3^{10/71} < \pi < 3^{1/2} \text{.}"),
        ).arrange(DOWN).scale(0.75).shift(DOWN)
        formula_text = MathTex(r"p_c = n \cdot \tan\left(\frac{180}{n}\right)", font_size=30).shift(UP)
        formula_explanation = MathTex(r"\text{Donde }","p_c", r"\text{ es el perímetro del polígono circunscrito, n es el número de lados del polígono}", font_size=30).shift(DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(10)
        self.play(FadeOut(title), FadeOut(subtitle))

        self.play(Write(formula_text), Write(formula_explanation))
        self.wait(5)
        self.play(FadeOut(formula_text), FadeOut(formula_explanation))

        # Crear un círculo de radio 2
        circle = Circle(radius=2)
        self.play(Create(circle))
        circle2= circle.copy()

        # Crear una lista de colores
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        # Crear un texto para mostrar el valor de p_c
        pc_text = MathTex("p_c = ", font_size=24)
        pc_value = DecimalNumber(0, num_decimal_places=5, font_size=24)  # Ajustado a 10 decimales
        pc_group = VGroup(pc_text, pc_value).arrange(RIGHT)
        pc_group.to_corner(UL)
        self.add(pc_group)

        # Crear un texto para mostrar el valor de n
        n_text = MathTex("n = ", font_size=24)
        n_value = DecimalNumber(0, num_decimal_places=0, font_size=24)  # Ajustado a 0 decimales
        n_group = VGroup(n_text, n_value).arrange(RIGHT)
        n_group.to_edge(UP)
        self.add(n_group)

        for n in range(3, 5):  # De 3 a 4
            # Actualizar el valor de n
            self.play(n_value.animate.set_value(n), run_time=1)  # Muestra n sin decimales

            polygon = self.create_polygon(n, colors[n % len(colors)])
            self.play(Transform(circle2, polygon), run_time=1)

            # Calcular el valor de p_c y actualizar el texto
            pc = n * np.tan(np.pi / n)
            self.play(pc_value.animate.set_value(pc), run_time=1)  # Muestra pc con 10 decimales

        for n in range(5, 300, 4):  # De 5 a 49, de dos en dos
            # Actualizar el valor de n
            self.play(n_value.animate.set_value(n), run_time=2/n)  # Muestra n sin decimales

            polygon = self.create_polygon(n, colors[n % len(colors)])
            self.play(Transform(circle2, polygon), run_time=2/n)

            # Calcular el valor de p_c y actualizar el texto
            pc = n * np.tan(np.pi / n)
            self.play(pc_value.animate.set_value(pc), run_time=2/n)  # Muestra pc con 10 decimales


        # Mostrar que el perímetro se acerca a pi
        pi_text = MathTex(r"\pi", font_size=30)
        self.play(Write(pi_text))

        # Añadir una flecha al final para indicar que p_c se acerca a pi cuando n tiende a infinito
        arrow = Arrow(pc_group.get_right(), pi_text.get_left(), buff=0.1)
        arrow_text = MathTex(r"\text{Cuando n tiende a infinito, }" , "p_c" , r"\text{ se aproxima a pi}", font_size=18).next_to(arrow.get_center(), RIGHT)
        self.play(Create(arrow), Write(arrow_text))
        self.wait(5)

        # Hacer un fadeout de la escena anterior
        self.play(FadeOut(arrow), FadeOut(arrow_text), FadeOut(pc_group), FadeOut(n_group), FadeOut(circle), FadeOut(circle2), FadeOut(pi_text))

        # Crear un texto para mostrar la fórmula del perímetro inscrito
        formula_text = MathTex(r"p_i = n \cdot \sin\left(\frac{180}{n}\right)", font_size=30).shift(UP)
        formula_explanation = MathTex(r"\text{Donde }","p_i", r"\text{ es el perímetro del polígono inscrito, n es el número de lados del polígono}", font_size=30).shift(DOWN)
        self.play(Write(formula_text), Write(formula_explanation))
        self.wait(5)
        self.play(FadeOut(formula_text), FadeOut(formula_explanation))

        # Crear un círculo de radio 2
        circle = Circle(radius=2)
        self.play(Create(circle))
        circle2 = circle.copy()

        # Crear un texto para mostrar el valor de p_i
        pi_text = MathTex("p_i = ", font_size=24)
        pi_value = DecimalNumber(0, num_decimal_places=5, font_size=24)  # Ajustado a 10 decimales
        pi_group = VGroup(pi_text, pi_value).arrange(RIGHT)
        pi_group.to_corner(UL)
        self.add(pi_group)

        # Crear un texto para mostrar el valor de n
        n_text = MathTex("n = ", font_size=24)
        n_value = DecimalNumber(0, num_decimal_places=0, font_size=24)  # Ajustado a 0 decimales
        n_group = VGroup(n_text, n_value).arrange(RIGHT)
        n_group.to_edge(UP)
        self.add(n_group)

        for n in range(3, 5):  # De 3 a 4
            # Actualizar el valor de n
            self.play(n_value.animate.set_value(n), run_time=1)  # Muestra n sin decimales

            polygon = self.create_polygon(n, colors[n % len(colors)], inscribed=True)
            self.play(Transform(circle2, polygon), run_time=1)

            # Calcular el valor de p_i y actualizar el texto
            pi = n * np.sin(np.pi / n)
            self.play(pi_value.animate.set_value(pi), run_time=1)  # Muestra pi con 10 decimales

        for n in range(5, 300, 4):  # De 5 a 49, de dos en dos
            # Actualizar el valor de n
            self.play(n_value.animate.set_value(n), run_time=1/n)  # Muestra n sin decimales

            polygon = self.create_polygon(n, colors[n % len(colors)], inscribed=True)
            self.play(Transform(circle2, polygon), run_time=1/n)

            # Calcular el valor de p_i y actualizar el texto
            pi = n * np.sin(np.pi / n)
            self.play(pi_value.animate.set_value(pi), run_time=1/n)  # Muestra pi con 10 decimales


        # Mostrar que el perímetro se acerca a pi
        pi_text = MathTex(r"\pi", font_size=30)
        self.play(Write(pi_text))

        # Añadir una flecha al final para indicar que p_i se acerca a pi cuando n tiende a infinito
        arrow = Arrow(pi_group.get_right(), pi_text.get_left(), buff=0.1)
        arrow_text = MathTex(r"\text{Cuando n tiende a infinito, }" , "p_i" , r"\text{ se aproxima a pi}", font_size=18).next_to(arrow.get_center(), RIGHT)
        self.play(Create(arrow), Write(arrow_text))
        self.wait(5)

        # Hacer un fadeout de la escena final
        self.play(FadeOut(arrow), FadeOut(arrow_text), FadeOut(pi_group), FadeOut(n_group), FadeOut(circle), FadeOut(circle2), FadeOut(pi_text))

    def create_polygon(self, n, color, inscribed=False):
            # Crear un polígono regular con n lados
            angles = np.linspace(0, 2*np.pi, n+1)[:-1]
            if inscribed:
                points = np.array([np.cos(angles), np.sin(angles), np.zeros_like(angles)]).T
            else:
                points = np.array([np.cos(angles)/np.cos(np.pi/n), np.sin(angles)/np.cos(np.pi/n), np.zeros_like(angles)]).T
            polygon = Polygon(*points, color=color)
            polygon.scale(2)
            return polygon


class PiScene(Scene):
    def construct(self):
        # Crear el símbolo de Pi y un signo de interrogación
        pi_symbol = MathTex("\\pi", color=BLUE).scale(3)
        question_mark = Text("?", color=RED).scale(3).next_to(pi_symbol, RIGHT)

        # Mostrar el símbolo de Pi y el signo de interrogación
        self.play(Write(pi_symbol), Write(question_mark))
        self.wait(2)

        # Reducir el tamaño del símbolo de Pi y moverlo a la esquina superior izquierda
        self.play(
            pi_symbol.animate.scale(1/3).to_corner(UP + LEFT),
            FadeOut(question_mark)
        )

        # Crear un círculo y un diámetro
        circle = Circle().move_to(ORIGIN)
        diameter = Line(circle.get_left(), circle.get_right())
        self.play(Create(circle), Create(diameter))

        # Etiquetar el círculo y el diámetro
        circle_label = MathTex("C").next_to(circle, UP)
        diameter_label = MathTex("D").next_to(diameter, UP)
        self.play(Write(circle_label), Write(diameter_label))

# Desdoblar el círculo en una línea
        unfolded_circle = Line(circle.get_bottom(), circle.get_bottom() + 2*PI*RIGHT).move_to(ORIGIN + DOWN)
        self.play(Transform(circle, unfolded_circle))

        # Mover el diámetro para alinearlo con la línea desdoblada
        self.play(diameter.animate.next_to(unfolded_circle, UP, aligned_edge=LEFT).shift(UP*0.5))

        # Duplicar el diámetro 3 veces y luego agregar una 0.14 parte del diámetro
        diameters = [diameter]
        for i in range(2):
            new_diameter = diameter.copy().next_to(diameters[-1], RIGHT, buff=0)
            new_diameter.set_color(random_bright_color())
            self.play(Create(new_diameter))
            diameters.append(new_diameter)

        # Agregar una 0.14 parte del diámetro
        partial_diameter = diameter.copy().scale(0.14).next_to(diameters[-1], RIGHT, buff=0)
        partial_diameter.set_color(random_bright_color())
        self.play(Create(partial_diameter))
        # Mover las etiquetas para evitar la superposición
        self.play(
            circle_label.animate.next_to(unfolded_circle, UP),
            diameter_label.animate.next_to(diameter, UP)
        )

        # Agregar una etiqueta que muestra que D es 3.14 veces C
        pi_relation_label = MathTex("\\pi \\text{ veces el diametro es el perimetro de el circulo}").next_to(unfolded_circle, DOWN)
        self.play(Write(pi_relation_label))
        self.wait(2)

        self.play(FadeOut(Group(*self.mobjects)))

class PiApproximation(Scene):
    def construct(self):
        title = Text("Métodos Antiguos").scale(2)
        self.play(Write(title))
        self.play(title.animate.scale(0.5).to_edge(UP))
        
        limitations_title = Text("Limitaciones:").next_to(title, DOWN).scale(0.75)
        self.play(Write(limitations_title))
        
        limitations = BulletedList(
            "Eran lentos",
            "Requerían cálculos difíciles",
            "Solo proporcionaban una aproximación de Pi con una precisión limitada"
        ).next_to(limitations_title, DOWN).scale(0.5)
        self.play(Write(limitations))
        
        circle = Circle().move_to(DOWN*2)
        pi_value = DecimalNumber(3, num_decimal_places=1).next_to(circle, DOWN)
        pi_text = Text("Pi = ").next_to(pi_value, LEFT)
        pi_group = VGroup(pi_text, pi_value)
        
        self.play(Create(circle), Write(pi_group))
        
        complexity_arrow = Arrow(DOWN, UP, color=GREEN).next_to(circle, LEFT)
        complexity_text = Text("Complejidad del cálculo").next_to(complexity_arrow, LEFT).scale(0.4)
        speed_arrow = Arrow(UP, DOWN, color=RED).next_to(circle, RIGHT)
        speed_text = Text("Velocidad del cálculo").next_to(speed_arrow, RIGHT).scale(0.4)
        
        self.play(Create(complexity_arrow), Write(complexity_text), Create(speed_arrow), Write(speed_text))
        
        pi_sequence = [3, 3.1, 3.14, 3.141, 3.1415, 3.14159, 3.141592, 3.1415926, 3.14159265]
        time_sequence = [0.5, 0.5, 0.5, 1, 1, 1, 1.5, 1.5, 1.5]
        for i in range(1, len(pi_sequence)):
            pi_value.set_value(pi_sequence[i])
            pi_value.set_num_decimal_places(i+1)
            self.wait(time_sequence[i])

        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))

class ModularFunctionsAndPi(Scene):
    def construct(self):
        self.intro()
        self.example1()
        self.example2()
        self.conclusion()

    def intro(self):
        intro_text = VGroup(
            Text("Introducción a las funciones"),
            Text("modulares y las aproximaciones a pi")
        ).arrange(DOWN).scale(0.75)
        self.play(Write(intro_text))
        self.wait()
        self.play(FadeOut(intro_text))

    def example1(self):
        example1_text = VGroup(
            Text("Ejemplo 1: Serie infinita para pi"),
            Text("a partir de una ecuación modular"),
            Text("de segundo orden")
        ).arrange(DOWN).scale(0.75)
        self.play(Write(example1_text))
        self.wait(2)
        self.play(example1_text.animate.shift(UP*2))
        self.wait()
        equation = MathTex(r"f(q) = 2\sqrt{2} \sum_{n=0}^{\infty} \frac{q^{(2n+1)^2}}{1-q^{(2n+1)^2}}").scale(0.9)
        self.play(Write(equation))
        self.wait()
        series = MathTex(r"\frac{1}{\pi} = \frac{2\sqrt{2}}{9801} \sum_{n=0}^{\infty} \frac{(4n)!(1103+26390n)}{(n!)4396^{4n}}").scale(0.9)
        self.play(Transform(equation, series))
        self.wait()
        self.play(FadeOut(equation))
        self.play(FadeOut(example1_text))

    def example2(self):
        example2_text = VGroup(
            Text("Ejemplo 2: Algoritmo iterativo para pi"),
            Text("a partir de una ecuación modular"),
            Text("de cuarto orden")
        ).arrange(DOWN).scale(0.75)
        self.play(Write(example2_text))
        self.wait(2)
        self.play(example2_text.animate.shift(UP*2))
        self.wait()
        equation = MathTex(r"f(q) = \frac{1}{\sqrt{2}} \sum_{n=0}^{\infty} \frac{q^{n^2}}{1+q^{n^2}}").scale(0.9)
        self.play(Write(equation))
        self.wait()
        algorithm =VGroup(
            MathTex(r"a_0 = 6-4\sqrt{2}, a_{n+1} = (1+y_{n+1})^4 a_n - 2^{2n+3} y_{n+1} (1+y_{n+1}+y_{n+1}^2)"),
            MathTex(r"y_0 = \sqrt{2}-1, y_{n+1} = \frac{1-\sqrt{1-y_n^2}}{1+\sqrt{1-y_n^2}}"),
        ).arrange(DOWN).scale(0.75)
        self.play(Transform(equation, algorithm))
        self.wait()
        self.play(FadeOut(equation))
        self.play(FadeOut(example2_text))

    def conclusion(self):
        conclusion_text = VGroup(
            Text("Las funciones modulares y las aproximaciones a pi"),
            Text("son dos temas fascinantes de la teoría de números que "),
            Text("nos muestran la riqueza y la complejidad de las matemáticas. "),
            Text("Ramanujan fue un pionero en este campo, "),
            Text("y sus descubrimientos siguen inspirando a los matemáticos y a los aficionados.")
        ).arrange(DOWN).scale(0.5)
        self.play(Write(conclusion_text))
        self.wait(2)
        self.wait()
        self.play(FadeOut(conclusion_text))


class ModernMethodsForPi(Scene):
    def construct(self):
        self.intro()
        self.machin_formula()

    def intro(self):
        intro_text = VGroup(
            Text("Con el desarrollo del cálculo, se encontraron"),
            Text("series para funciones trigonométricas inversas"),
            Text("que convergían a Pi.")
        ).arrange(DOWN).scale(0.75)
        self.play(Write(intro_text))
        self.wait(2)
        self.play(FadeOut(intro_text))

    def machin_formula(self):
        machin_text = VGroup(
            Text("La fórmula de Machin fue la más usada por dos siglos para calcular Pi."),
            Text("Se basa en la expansión en serie de Taylor de la función arco tangente."),
            Text("Al sustituir x = 1/5 y x = 1/239 en la serie de Taylor"),
            Text("multiplicar por los coeficientes adecuados,"),
            Text("obtenemos una serie que converge a pi mucho más rápido que la serie de arco tangente original.")
        ).arrange(DOWN).scale(0.5)
        self.play(Write(machin_text))
        self.wait(2)
        self.play(machin_text.animate.scale(0.5).to_edge(UP))
        machin_formula = MathTex(r"\pi = 16 \arctan \left(\frac{1}{5}\right) - 4 \arctan \left(\frac{1}{239}\right)").scale(0.75)
        self.play(Write(machin_formula))
        self.wait(2)
        self.play(machin_formula.animate.next_to(machin_text, DOWN))
        computer_text = VGroup(
            Text("Con las computadoras, se lograron"),
            Text("calcular millones de dígitos de Pi.")
        ).arrange(DOWN).scale(0.6)
        self.play(Write(computer_text))
        self.wait(3)
        # Definir la función arctan
        def arctan(x, n):
            return sum(((-1)**k * x**(2*k+1)) / (2*k+1) for k in range(n))

        # Calcular pi usando la fórmula de Machin
        def machin_pi(n):
            return 16*arctan(1/5, n) - 4*arctan(1/239, n)

        # Animar el cálculo de pi
        results = VGroup()  # Grupo para almacenar los resultados
        row = VGroup()  # Grupo para almacenar una fila de resultados
        for i in range(1, 11):
            pi_approx = DecimalNumber(machin_pi(i), num_decimal_places=i)  # Aumentar el número de decimales
            pi_approx.next_to(machin_formula, DOWN)  # Colocar el resultado debajo de "computer_text"
            self.play(Write(pi_approx), run_time=0.5)
            if i <= 5:  # Para las primeras 5 aproximaciones
                pi_approx.target = row[-1].get_right() + RIGHT if row else config.frame_width / 5 * LEFT + DOWN
                row.add(pi_approx)
            elif i <= 8:  # Para las siguientes 3 aproximaciones
                if i == 6:  # Si es la primera de las siguientes 3 aproximaciones, crear una nueva fila
                    results.add(row)
                    row = VGroup()
                pi_approx.target = row[-1].get_right() + RIGHT * 1.5 if row else config.frame_width / 5.5 * LEFT + DOWN * 2
                row.add(pi_approx)
            else:  # Para las últimas 2 aproximaciones
                if i == 9:  # Si es la primera de las últimas 2 aproximaciones, crear una nueva fila
                    results.add(row)
                    row = VGroup()
                pi_approx.target = row[-1].get_right() + RIGHT * 2 if row else config.frame_width / 6 * LEFT + DOWN * 3
                row.add(pi_approx)
            self.play(ApplyMethod(pi_approx.move_to, pi_approx.target), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(Group(*self.mobjects)))

class PiHistory(Scene):
    def construct(self):
        title = Text("Historia del cálculo de Pi")
        self.play(Write(title))
        self.wait(3)
        self.play(title.animate.scale(0.7).to_edge(UP))

        # Añade los puntos importantes en la línea de tiempo
        points = [-1.9, -1.65, -0.25, 0.429, 1.914]
        descriptions = [
        VGroup(
            Text("Aproximación de Pi a 3.125"),
            Text("Babilonios (1900 a.C.)")
        ).arrange(DOWN),
        VGroup(
            Text("Aproximación de Pi a 3.1605"),
            Text("Egipcios (1650 a.C.)")
        ).arrange(UP),
        VGroup(
            Text("Aproximación de Pi entre 3^1/7 y 3^10/71"),
            Text("Arquímedes (250 a.C.)")
        ).arrange(DOWN),
        VGroup(
            Text("Aproximación de Pi a 355/113"),
            Text("Zu Chongzhi (429 d.C.)")
        ).arrange(UP),
        VGroup(
            Text("Desarrollo de la serie infinita para calcular Pi"),
            Text("Ramanujan (1914 d.C.)")
        ).arrange(DOWN)
        ]

        # Crea una línea de tiempo
        start = -5 # punto inicial de la línea de tiempo
        end = 5 # punto final de la línea de tiempo
        timeline = NumberLine(x_range=[start, end, 1], include_numbers=False, include_ticks=False)
        timeline.arrange(LEFT, center=False)
        self.play(Write(timeline))
        i= 1
        for point, description in zip(points, descriptions):
            dot = Dot(color=RED, stroke_width=1).move_to(timeline.number_to_point(point*2.5))
            if i % 2 == 0:
                label = description.next_to(dot, DOWN).scale(0.35)
            else:
                label = description.next_to(dot, UP).scale(0.35)
            self.play(GrowFromCenter(dot), Write(label), run_time=2)
            self.wait(2)
            i += 1

        self.wait()
        self.play(FadeOut(Group(*self.mobjects)))

        image = ImageMobject("pi.jpeg").scale_to_fit_height(7)
        self.add(image)
        conclusion = Text("Conclusión").to_edge(UP)
        self.play(FadeIn(conclusion))
        self.wait(10)
        self.play(FadeOut(Group(*self.mobjects)))

# Para ejecutar la animación
if __name__ == "__main__":
    script_name = f"{os.path.basename(__file__)}"
    os.system(f"manim -p --disable_caching -qh {script_name} PiHistory")
