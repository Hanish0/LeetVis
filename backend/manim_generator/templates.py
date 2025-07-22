"""
Manim script templates for different video types.
"""

from typing import Dict, Any, List

class ManimTemplates:
    """Contains templates for generating different types of Manim scripts"""
    
    def generate_explanation_script(self, problem_title: str, problem_content: str, 
                                  difficulty: str, code_components: Dict[str, Any], 
                                  language: str) -> str:
        """Generate a problem explanation video script"""
        
        # Clean problem content for display
        clean_content = self._clean_html_content(problem_content)
        truncated_content = self._truncate_text(clean_content, 200)
        formatted_code = self._format_code_for_display(code_components["raw_code"], language)
        steps = self._generate_approach_steps(code_components)
        time_complexity = code_components.get('time_complexity', 'O(n)')
        space_complexity = code_components.get('space_complexity', 'O(1)')
        
        # Determine difficulty color
        diff_color = "GREEN" if difficulty == "Easy" else "YELLOW" if difficulty == "Medium" else "RED"
        
        script = f'''from manim import *

class ProblemExplanation(Scene):
    def construct(self):
        # Title slide
        title = Text("{problem_title}", font_size=48, color=BLUE)
        difficulty_text = Text("Difficulty: {difficulty}", font_size=24, color={diff_color})
        difficulty_text.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(difficulty_text))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(difficulty_text))
        
        # Problem statement
        problem_text = Text("Problem Statement", font_size=36, color=BLUE)
        self.play(Write(problem_text))
        self.wait(1)
        
        # Problem description (truncated for readability)
        description = Text(
            "{truncated_content}", 
            font_size=20, 
            color=WHITE
        ).scale(0.8)
        description.next_to(problem_text, DOWN, buff=0.5)
        
        self.play(Write(description))
        self.wait(3)
        self.play(FadeOut(problem_text), FadeOut(description))
        
        # Approach explanation
        approach_title = Text("Approach", font_size=36, color=BLUE)
        self.play(Write(approach_title))
        self.wait(1)
        
        # Show key algorithm steps
        step_group = VGroup()
        
        steps_list = {steps[:4]}  # Limit to 4 steps
        for i, step in enumerate(steps_list):
            step_text = Text(f"{{i+1}}. {{step}}", font_size=18, color=WHITE)
            if i == 0:
                step_text.next_to(approach_title, DOWN, buff=0.5)
            else:
                step_text.next_to(step_group[-1], DOWN, buff=0.3)
            step_group.add(step_text)
            self.play(Write(step_text))
            self.wait(1)
        
        self.wait(2)
        self.play(FadeOut(approach_title), FadeOut(step_group))
        
        # Code solution
        code_title = Text("Solution Code", font_size=36, color=BLUE)
        self.play(Write(code_title))
        self.wait(1)
        
        # Display code (formatted for readability)
        code_text = Code(
            code="""{formatted_code}""",
            language="{language}",
            font_size=14,
            background="window",
            style="monokai"
        )
        code_text.next_to(code_title, DOWN, buff=0.5)
        
        self.play(Create(code_text))
        self.wait(4)
        
        # Complexity analysis
        self.play(FadeOut(code_title), FadeOut(code_text))
        
        complexity_title = Text("Complexity Analysis", font_size=36, color=BLUE)
        self.play(Write(complexity_title))
        
        time_complexity = Text(
            "Time Complexity: {time_complexity}", 
            font_size=24, 
            color=GREEN
        )
        space_complexity = Text(
            "Space Complexity: {space_complexity}", 
            font_size=24, 
            color=GREEN
        )
        
        time_complexity.next_to(complexity_title, DOWN, buff=0.5)
        space_complexity.next_to(time_complexity, DOWN, buff=0.3)
        
        self.play(Write(time_complexity))
        self.play(Write(space_complexity))
        self.wait(3)
        
        # End screen
        self.play(FadeOut(complexity_title), FadeOut(time_complexity), FadeOut(space_complexity))
        
        end_text = Text("Thank you for watching!", font_size=36, color=BLUE)
        self.play(Write(end_text))
        self.wait(2)
'''
        
        return script
    
    def generate_brute_force_script(self, problem_title: str, problem_content: str, 
                                  code_components: Dict[str, Any], language: str) -> str:
        """Generate a brute force solution video script"""
        
        clean_content = self._clean_html_content(problem_content)
        truncated_content = self._truncate_text(clean_content, 150)
        formatted_code = self._format_code_for_display(code_components["raw_code"], language)
        time_complexity = code_components.get('time_complexity', 'O(n²)')
        space_complexity = code_components.get('space_complexity', 'O(1)')
        
        script = f'''from manim import *

class BruteForceSolution(Scene):
    def construct(self):
        # Title slide
        title = Text("{problem_title}", font_size=48, color=BLUE)
        subtitle = Text("Brute Force Approach", font_size=32, color=ORANGE)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Problem recap
        problem_text = Text("Problem Recap", font_size=36, color=BLUE)
        self.play(Write(problem_text))
        
        description = Text(
            "{truncated_content}", 
            font_size=18, 
            color=WHITE
        ).scale(0.8)
        description.next_to(problem_text, DOWN, buff=0.5)
        
        self.play(Write(description))
        self.wait(2)
        self.play(FadeOut(problem_text), FadeOut(description))
        
        # Brute force strategy
        strategy_title = Text("Brute Force Strategy", font_size=36, color=ORANGE)
        self.play(Write(strategy_title))
        
        strategy_text = Text(
            "Try all possible combinations\\nCheck each one systematically\\nReturn first valid solution",
            font_size=20,
            color=WHITE
        )
        strategy_text.next_to(strategy_title, DOWN, buff=0.5)
        
        self.play(Write(strategy_text))
        self.wait(3)
        self.play(FadeOut(strategy_title), FadeOut(strategy_text))
        
        # Algorithm walkthrough
        algo_title = Text("Algorithm Steps", font_size=36, color=ORANGE)
        self.play(Write(algo_title))
        
        # Show nested loops or brute force logic
        steps = [
            "Initialize variables and data structures",
            "Use nested loops to try all combinations",
            "Check each combination against constraints",
            "Return result when valid solution found"
        ]
        
        step_group = VGroup()
        for i, step in enumerate(steps):
            step_text = Text(f"{{i+1}}. {{step}}", font_size=18, color=WHITE)
            if i == 0:
                step_text.next_to(algo_title, DOWN, buff=0.5)
            else:
                step_text.next_to(step_group[-1], DOWN, buff=0.3)
            step_group.add(step_text)
            self.play(Write(step_text))
            self.wait(1.5)
        
        self.wait(2)
        self.play(FadeOut(algo_title), FadeOut(step_group))
        
        # Code implementation
        code_title = Text("Brute Force Implementation", font_size=36, color=ORANGE)
        self.play(Write(code_title))
        
        code_text = Code(
            code="""{formatted_code}""",
            language="{language}",
            font_size=12,
            background="window",
            style="monokai"
        )
        code_text.next_to(code_title, DOWN, buff=0.5)
        
        self.play(Create(code_text))
        self.wait(4)
        
        # Complexity analysis
        self.play(FadeOut(code_title), FadeOut(code_text))
        
        complexity_title = Text("Complexity Analysis", font_size=36, color=ORANGE)
        self.play(Write(complexity_title))
        
        # Brute force typically has higher complexity
        time_complexity = Text(
            "Time Complexity: {time_complexity}", 
            font_size=24, 
            color=RED
        )
        space_complexity = Text(
            "Space Complexity: {space_complexity}", 
            font_size=24, 
            color=GREEN
        )
        
        note = Text(
            "Note: Brute force is simple but not always efficient",
            font_size=18,
            color=YELLOW
        )
        
        time_complexity.next_to(complexity_title, DOWN, buff=0.5)
        space_complexity.next_to(time_complexity, DOWN, buff=0.3)
        note.next_to(space_complexity, DOWN, buff=0.3)
        
        self.play(Write(time_complexity))
        self.play(Write(space_complexity))
        self.play(Write(note))
        self.wait(3)
        
        # End screen
        self.play(FadeOut(complexity_title), FadeOut(time_complexity), 
                 FadeOut(space_complexity), FadeOut(note))
        
        end_text = Text("Next: Optimal Solution!", font_size=36, color=ORANGE)
        self.play(Write(end_text))
        self.wait(2)
'''
        
        return script
    
    def generate_optimal_script(self, problem_title: str, problem_content: str, 
                              code_components: Dict[str, Any], language: str) -> str:
        """Generate an optimal solution video script"""
        
        clean_content = self._clean_html_content(problem_content)
        truncated_content = self._truncate_text(clean_content, 150)
        formatted_code = self._format_code_for_display(code_components["raw_code"], language)
        opt_steps = self._generate_optimal_steps(code_components)
        time_complexity = code_components.get('time_complexity', 'O(n)')
        space_complexity = code_components.get('space_complexity', 'O(1)')
        
        script = f'''from manim import *

class OptimalSolution(Scene):
    def construct(self):
        # Title slide
        title = Text("{problem_title}", font_size=48, color=BLUE)
        subtitle = Text("Optimal Solution", font_size=32, color=GREEN)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Optimization insight
        insight_title = Text("Key Insight", font_size=36, color=GREEN)
        self.play(Write(insight_title))
        
        insight_text = Text(
            "We can optimize by using:\\n• Better data structures\\n• Avoiding redundant work\\n• Mathematical properties",
            font_size=20,
            color=WHITE
        )
        insight_text.next_to(insight_title, DOWN, buff=0.5)
        
        self.play(Write(insight_text))
        self.wait(3)
        self.play(FadeOut(insight_title), FadeOut(insight_text))
        
        # Optimal approach
        approach_title = Text("Optimal Approach", font_size=36, color=GREEN)
        self.play(Write(approach_title))
        
        # Generate optimized steps
        step_group = VGroup()
        
        steps_list = {opt_steps[:4]}
        for i, step in enumerate(steps_list):
            step_text = Text(f"{{i+1}}. {{step}}", font_size=18, color=WHITE)
            if i == 0:
                step_text.next_to(approach_title, DOWN, buff=0.5)
            else:
                step_text.next_to(step_group[-1], DOWN, buff=0.3)
            step_group.add(step_text)
            self.play(Write(step_text))
            self.wait(1.5)
        
        self.wait(2)
        self.play(FadeOut(approach_title), FadeOut(step_group))
        
        # Visual example (if applicable)
        example_title = Text("Example Walkthrough", font_size=36, color=GREEN)
        self.play(Write(example_title))
        
        # Create a simple visual representation
        example_group = self._create_example_visual()
        example_group.next_to(example_title, DOWN, buff=0.5)
        
        self.play(Create(example_group))
        self.wait(3)
        self.play(FadeOut(example_title), FadeOut(example_group))
        
        # Optimal code
        code_title = Text("Optimal Implementation", font_size=36, color=GREEN)
        self.play(Write(code_title))
        
        code_text = Code(
            code="""{formatted_code}""",
            language="{language}",
            font_size=12,
            background="window",
            style="monokai"
        )
        code_text.next_to(code_title, DOWN, buff=0.5)
        
        self.play(Create(code_text))
        self.wait(4)
        
        # Complexity comparison
        self.play(FadeOut(code_title), FadeOut(code_text))
        
        comparison_title = Text("Complexity Comparison", font_size=36, color=GREEN)
        self.play(Write(comparison_title))
        
        # Show improvement
        brute_force = Text("Brute Force: O(n²)", font_size=20, color=RED)
        optimal = Text("Optimal: {time_complexity}", font_size=20, color=GREEN)
        improvement = Text("Significant improvement!", font_size=18, color=YELLOW)
        
        brute_force.next_to(comparison_title, DOWN, buff=0.5)
        optimal.next_to(brute_force, DOWN, buff=0.3)
        improvement.next_to(optimal, DOWN, buff=0.3)
        
        self.play(Write(brute_force))
        self.play(Write(optimal))
        self.play(Write(improvement))
        self.wait(3)
        
        # End screen
        self.play(FadeOut(comparison_title), FadeOut(brute_force), 
                 FadeOut(optimal), FadeOut(improvement))
        
        end_text = Text("Problem Solved Optimally!", font_size=36, color=GREEN)
        self.play(Write(end_text))
        self.wait(2)
'''
        
        return script
    
    def _clean_html_content(self, content: str) -> str:
        """Remove HTML tags and clean content for display"""
        import re
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', content)
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    def _format_code_for_display(self, code: str, language: str) -> str:
        """Format code for better display in Manim"""
        # Remove excessive whitespace and format for readability
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():  # Skip empty lines
                formatted_lines.append(line.rstrip())
        
        # Limit to reasonable number of lines for video
        if len(formatted_lines) > 15:
            formatted_lines = formatted_lines[:15] + ["# ... (truncated)"]
        
        return '\n'.join(formatted_lines)
    
    def _generate_approach_steps(self, code_components: Dict[str, Any]) -> List[str]:
        """Generate approach steps based on code components"""
        steps = []
        
        if code_components.get("variables"):
            steps.append("Initialize necessary variables")
        
        if code_components.get("loops"):
            steps.append("Iterate through the data structure")
        
        if code_components.get("conditions"):
            steps.append("Apply conditional logic")
        
        if code_components.get("return_statement"):
            steps.append("Return the result")
        
        # Default steps if none found
        if not steps:
            steps = [
                "Analyze the problem requirements",
                "Choose appropriate data structures",
                "Implement the core algorithm",
                "Return the solution"
            ]
        
        return steps
    
    def _generate_optimal_steps(self, code_components: Dict[str, Any]) -> List[str]:
        """Generate optimal approach steps"""
        return [
            "Use efficient data structures (HashMap, Set)",
            "Eliminate nested loops where possible",
            "Apply mathematical insights",
            "Optimize space usage"
        ]
    
    def _create_example_visual(self):
        """Create a simple visual example (placeholder)"""
        # Create a simple array visualization
        squares = VGroup()
        for i in range(5):
            square = Square(side_length=0.5, color=BLUE, fill_opacity=0.3)
            number = Text(str(i+1), font_size=20)
            square.add(number)
            if i > 0:
                square.next_to(squares[-1], RIGHT, buff=0.1)
            squares.add(square)
        
        return squares