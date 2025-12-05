# This test file was AI-generated to help identify edge cases in the Day 1 solution algorithm.

import unittest
import sys
import os
import subprocess
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDay1SecretEntrance(unittest.TestCase):
    """Unit tests for Day 1 Secret Entrance solution with edge cases"""
    
    def setUp(self):
        """Set up test environment"""
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.solution_path = os.path.join(self.project_root, 'solutions', 'day_1_secret_entrance.py')
        self.inputs_dir = os.path.join(self.project_root, 'inputs')
        
    def run_solution_with_input(self, input_lines, expected_part1=None, expected_part2=None):
        """Helper method to run the solution with given input and check results"""
        # Create temporary input file
        test_input_file = os.path.join(self.inputs_dir, 'day_1_test_input.txt')
        
        try:
            # Write test input
            with open(test_input_file, 'w') as f:
                f.write('\n'.join(input_lines))
            
            # Temporarily backup original input file
            original_input = os.path.join(self.inputs_dir, 'day_1_input.txt')
            backup_input = os.path.join(self.inputs_dir, 'day_1_input.txt.backup')
            
            if os.path.exists(original_input):
                shutil.copy2(original_input, backup_input)
            
            # Replace with test input
            shutil.copy2(test_input_file, original_input)
            
            # Run the solution
            result = subprocess.run(
                [sys.executable, self.solution_path],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            output = result.stdout.strip()
            
            # Parse output
            part1_match = None
            part2_match = None
            for line in output.split('\n'):
                if 'Part 1' in line:
                    part1_match = line
                if 'Part 2' in line:
                    part2_match = line
            
            # Restore original input
            if os.path.exists(backup_input):
                shutil.move(backup_input, original_input)
            
            # Check expectations if provided
            if expected_part1 is not None:
                self.assertIn(f'Part 1 password is: {expected_part1}', output,
                            f"Expected Part 1: {expected_part1}, got: {part1_match}")
            if expected_part2 is not None:
                self.assertIn(f'Part 2 password is: {expected_part2}', output,
                            f"Expected Part 2: {expected_part2}, got: {part2_match}")
            
            return output, part1_match, part2_match
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(backup_input):
                shutil.move(backup_input, original_input)
            raise e
        finally:
            # Clean up test input file
            if os.path.exists(test_input_file):
                os.remove(test_input_file)
    
    def test_edge_case_exact_boundary_left(self):
        """Test: Moving left exactly to position 0 from start (50)"""
        # Start at 50, move left 50 steps -> should end at 0
        input_lines = ['L50']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Should end on zero, so end_on_zero_pos should be 1
        self.assertIn('Part 1 password is: 1', output)
        # Should count as passing through zero
        self.assertIn('Part 2 password is: 1', output)
    
    def test_edge_case_wrap_from_zero_left(self):
        """Test: Starting at 0, moving left (wraps to 99) - EDGE CASE"""
        # Start at 50, move left 50 to get to 0, then move left 1
        # This is the key edge case: when pos=0 and we move left
        input_lines = ['L50', 'L1']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # After first move: pos=0, end_on_zero_pos=1
        # After second move: pos=99 (wrapped), should we count passing through 0?
        # Current algorithm: remaining_steps=1, pos=0, so remaining_steps > pos-min_pos (1 > 0) = True
        # This increments pass_zero_pos, but we're already AT 0, not passing through it
        self.assertIn('Part 1', output)
        self.assertIn('Part 2', output)
        print(f"\n[EDGE CASE] Wrap from 0 left: {part1}, {part2}")
    
    def test_edge_case_wrap_from_max_right(self):
        """Test: Starting at 99, moving right (wraps to 0)"""
        # Start at 50, move right 49 to get to 99, then move right 1
        input_lines = ['R49', 'R1']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Should pass through 0 when wrapping from 99 to 0
        self.assertIn('Part 1', output)
        self.assertIn('Part 2', output)
        print(f"\n[EDGE CASE] Wrap from 99 right: {part1}, {part2}")
    
    def test_edge_case_multiple_full_rotations(self):
        """Test: Steps that cause multiple full rotations"""
        # 200 steps = 2 full rotations (each rotation is 100 positions)
        input_lines = ['R200']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Should count 2 passes through 0 from full rotations
        # Start at 50, 200 steps right = 2 full rotations + 0 remaining
        # Final position: 50 (back to start)
        # Pass through 0: 2 times (once per full rotation)
        self.assertIn('Part 2 password is: 2', output)
        print(f"\n[EDGE CASE] Multiple rotations: {part1}, {part2}")
    
    def test_edge_case_steps_equal_to_range(self):
        """Test: Steps exactly equal to range size (100)"""
        # 100 steps = exactly 1 full rotation
        input_lines = ['R100']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Should count 1 pass through 0, and end at starting position (50)
        # remaining_steps = 0, so no overage
        # Final position: 50 (back to start)
        self.assertIn('Part 2 password is: 1', output)
        self.assertIn('Part 1 password is: 0', output)  # Doesn't end on 0
        print(f"\n[EDGE CASE] Steps equal to range: {part1}, {part2}")
    
    def test_edge_case_very_large_steps(self):
        """Test: Very large step values"""
        input_lines = ['R10000', 'L5000']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # R10000: 100 full rotations, 0 remaining -> pos stays at 50, pass_zero_pos += 100
        # L5000: 50 full rotations, 0 remaining -> pos stays at 50, pass_zero_pos += 50
        # Total: 150 passes through 0
        self.assertIn('Part 2 password is: 150', output)
        print(f"\n[EDGE CASE] Very large steps: {part1}, {part2}")
    
    def test_edge_case_single_step_left(self):
        """Test: Single step left from starting position"""
        input_lines = ['L1']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Start at 50, move to 49, shouldn't pass through 0
        self.assertIn('Part 1 password is: 0', output)
        self.assertIn('Part 2 password is: 0', output)
    
    def test_edge_case_single_step_right(self):
        """Test: Single step right from starting position"""
        input_lines = ['R1']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Start at 50, move to 51, shouldn't pass through 0
        self.assertIn('Part 1 password is: 0', output)
        self.assertIn('Part 2 password is: 0', output)
    
    def test_edge_case_crossing_zero_multiple_times(self):
        """Test: A sequence that crosses zero multiple times"""
        # Move in a way that crosses 0 multiple times
        input_lines = ['L51', 'R1', 'L1', 'R1']  # Go to -1 (99), then back and forth
        output, part1, part2 = self.run_solution_with_input(input_lines)
        self.assertIn('Part 1', output)
        self.assertIn('Part 2', output)
        print(f"\n[EDGE CASE] Multiple crossings: {part1}, {part2}")
    
    def test_edge_case_ending_exactly_at_zero(self):
        """Test: Multiple moves that end exactly at zero"""
        input_lines = ['L25', 'L25']  # 50 - 25 - 25 = 0
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # Should end on zero (end_on_zero_pos should be 1)
        self.assertIn('Part 1 password is: 1', output)
        print(f"\n[EDGE CASE] Ending at zero: {part1}, {part2}")
    
    def test_edge_case_position_99_to_0_wrap(self):
        """Test: Moving right from position 99 wraps to 0"""
        # Start at 50, move right 49 to get to 99, then move right 1
        # Should wrap to 0 and count as passing through 0
        input_lines = ['R49', 'R1']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        # After first: pos=99
        # After second: remaining_steps=1, pos=99, so 1+99=100 > 99, overage=1
        # Should count as passing through 0
        self.assertIn('Part 2 password is: 1', output)
        self.assertIn('Part 1 password is: 1', output)  # Ends on 0
        print(f"\n[EDGE CASE] 99 to 0 wrap: {part1}, {part2}")
    
    def test_edge_case_starting_at_zero_then_left(self):
        """Test: Critical edge case - starting at 0, moving left"""
        # This tests the condition: if pos == 0 and we move left
        # Line 28: remaining_steps > pos - min_pos
        # If pos=0: remaining_steps > 0 - 0 = remaining_steps > 0
        # So ANY left movement from 0 will trigger this, but we're already AT 0
        input_lines = ['L50', 'L1']
        output, part1, part2 = self.run_solution_with_input(input_lines)
        print(f"\n[CRITICAL EDGE CASE] Starting at 0 then left: {part1}, {part2}")
        print("   This may reveal the bug: do we count being AT 0 as passing THROUGH 0?")


if __name__ == '__main__':
    unittest.main(verbosity=2)
