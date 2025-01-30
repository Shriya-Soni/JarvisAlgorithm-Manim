from manim import *

class JarvisAlgorithmVisualization(Scene):
    def construct(self):
        # Reduced points (7 points, 2 inside the hull)
        points = [
            [-4, -1, 0], [2, 3, 0], [1, -3, 0],
            [-2, 1, 0], [0, 0, 0], [3, 1, 0], [-3, 2, 0]
        ]

        # Convert points to Manim Dot objects and display them
        dots = [Dot(point, color=BLUE) for point in points]
        self.play(*[FadeIn(dot, run_time=0.2) for dot in dots])

        self.wait(1)

        # Labels for the points
        labels = [Text(f"{i+1}", font_size=24).next_to(dots[i], UP) for i in range(len(points))]
        self.play(*[Write(label, run_time=0.2) for label in labels])
        self.wait(1)

        # Helper function: Orientation test
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else 2  # Clockwise or Counterclockwise

        # Jarvis March (Gift Wrapping) Algorithm
        hull = []  # To store points in the convex hull

        # Step 1: Find the leftmost point
        leftmost_index = min(range(len(points)), key=lambda i: points[i][0])
        p = leftmost_index
        hull.append(points[p])

        # Visualization for the algorithm
        def animate_orientation(p, q, r, orientation_result):
            p_dot, q_dot, r_dot = [Dot(points[i], color=RED) for i in [p, q, r]]
            edge = Line(points[p], points[q], color=YELLOW)
            triangle = Polygon(points[p], points[q], points[r], color=GREEN, fill_opacity=0.2)

            # Orientation label
            orientation_label = Text(
                "Counterclockwise" if orientation_result == 2 else "Clockwise" if orientation_result == 1 else "Collinear",
                font_size=28,
                color=WHITE
            ).move_to(UP * 3)

            self.play(FadeIn(p_dot, run_time=0.1), FadeIn(q_dot, run_time=0.1), FadeIn(r_dot, run_time=0.1))
            self.play(Create(edge, run_time=0.3), Create(triangle, run_time=0.3))
            self.play(Write(orientation_label, run_time=0.3))
            self.play(FadeOut(orientation_label, run_time=0.2), FadeOut(triangle, run_time=0.2), FadeOut(edge, run_time=0.2))
            self.play(FadeOut(p_dot, run_time=0.1), FadeOut(q_dot, run_time=0.1), FadeOut(r_dot, run_time=0.1))

        # Step 2: Iteratively find hull points
        while True:
            q = (p + 1) % len(points)  # Next candidate point
            for r in range(len(points)):
                if r != p and r != q:
                    # Calculate orientation
                    orient_result = orientation(points[p], points[q], points[r])

                    # Visualize orientation test
                    animate_orientation(p, q, r, orientation_result=orient_result)

                    # Update q if counter-clockwise
                    if orient_result == 2:
                        q = r

            # Add edge to visualization
            line = Line(points[p], points[q], color=WHITE, stroke_width=3)
            self.play(Create(line, run_time=0.3))

            # Add q to the hull
            hull.append(points[q])
            p = q

            # Break if we return to the leftmost point
            if p == leftmost_index:
                break

        # Highlight the final hull
        hull_edges = [Line(hull[i], hull[(i + 1) % len(hull)], color=GREEN, stroke_width=4) for i in range(len(hull))]
        self.play(*[Create(edge, run_time=0.3) for edge in hull_edges])

        # Display final message
        final_message = Text("This is the final convex hull", font_size=36, color=YELLOW).move_to(DOWN * 3)
        self.play(Write(final_message, run_time=1.5))

        # Keep final result displayed
        self.wait(2)
