#!/usr/bin/env python3
"""
Java JUnit to Python pytest converter
Converts Java JUnit test files to Python pytest format
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case"""
    # Handle special cases like 'testXML' -> 'test_xml'
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

class JavaToPytestConverter:
    def __init__(self):
        # Mapping of Java to Python method names
        self.method_mappings = {
            'assertEquals': 'assert {} == {}',
            'assertNotEquals': 'assert {} != {}',
            'assertTrue': 'assert {}',
            'assertFalse': 'assert not {}',
            'assertNull': 'assert {} is None',
            'assertNotNull': 'assert {} is not None',
            'assertSame': 'assert {} is {}',
            'assertNotSame': 'assert {} is not {}',
            'assertArrayEquals': 'assert {} == {}',
            'assertThrows': 'with pytest.raises({}):\n    {}',
        }
        
        # Java to Python type mappings
        self.type_mappings = {
            'boolean': 'bool',
            'int': 'int',
            'double': 'float',
            'float': 'float',
            'String': 'str',
            'List': 'List',
            'ArrayList': 'List',
            'HashMap': 'Dict',
            'Map': 'Dict',
        }
        
        # Import mappings for common Java classes
        self.import_mappings = {
            'Math': 'math',
            'List': 'typing.List',
            'ArrayList': 'typing.List',
            'HashMap': 'typing.Dict',
            'Map': 'typing.Dict',
        }

    def camel_to_snake(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        # Handle special cases like 'testXML' -> 'test_xml'
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    def convert_class_name(self, java_class: str) -> str:
        """Convert Java class name to Python test class name"""
        # Remove 'Test' suffix if present, then add 'Test' prefix
        class_name = java_class.replace('Test', '')
        return f"Test{class_name}"

    def convert_constants(self, content: str) -> str:
        """Convert Java constants to Python constants"""
        # Convert static final constants
        content = re.sub(
            r'private static final\s+(\w+)\s+(\w+)\s*=\s*([^;]+);',
            r'\2 = \3',
            content
        )
        
        # Convert constant names to UPPER_CASE
        def convert_constant_name(match):
            const_name = match.group(2)
            return match.group(0).replace(const_name, const_name.upper())
        
        content = re.sub(
            r'(\w+)\s*=\s*([^;]+);',
            convert_constant_name,
            content
        )
        
        return content

    def convert_imports(self, content: str) -> str:
        """Convert Java imports to Python imports"""
        lines = content.split('\n')
        python_imports = set()
        converted_lines = []
        
        for line in lines:
            # Skip Java imports and add Python equivalents
            if line.strip().startswith('import '):
                if 'junit' in line:
                    python_imports.add('import pytest')
                elif 'Math' in line:
                    python_imports.add('import math')
                elif 'List' in line:
                    python_imports.add('from typing import List')
                elif 'ArrayList' in line:
                    python_imports.add('from typing import List')
                # Skip other Java imports - they'll need manual handling
                continue
            elif line.strip().startswith('package '):
                # Skip package declarations
                continue
            else:
                converted_lines.append(line)
        
        # Add Python imports at the top
        python_import_lines = sorted(list(python_imports))
        if python_import_lines:
            python_import_lines.append('')  # Add blank line after imports
        
        return '\n'.join(python_import_lines + converted_lines)

    def convert_method_signature(self, method_signature: str) -> str:
        """Convert Java method signature to Python"""
        # Extract method name and convert to snake_case
        method_match = re.search(r'(\w+)\s*\(([^)]*)\)', method_signature)
        if not method_match:
            return method_signature
        
        method_name = method_match.group(1)
        params = method_match.group(2)
        
        # Convert method name
        python_method_name = self.camel_to_snake(method_name)
        
        # Convert parameters (simplified - just remove types)
        python_params = []
        if params.strip():
            for param in params.split(','):
                param = param.strip()
                if param:
                    # Extract parameter name (last word)
                    param_name = param.split()[-1]
                    python_params.append(param_name)
        
        params_str = ', '.join(python_params)
        if params_str:
            return f"def {python_method_name}(self, {params_str}):"
        else:
            return f"def {python_method_name}(self):"

    def convert_assertions(self, content: str) -> str:
        """Convert Java assertions to Python assertions"""
        # Handle assertAll - convert to multiple assert statements
        def convert_assert_all(match):
            full_match = match.group(0)
            # Extract the lambda expressions inside assertAll
            lambda_content = re.findall(r'\(\)\s*->\s*([^,)]+)', full_match)
            python_asserts = []
            for assertion in lambda_content:
                assertion = assertion.strip()
                # Remove any trailing commas or parentheses
                assertion = re.sub(r'[,)]+$', '', assertion)
                converted = self.convert_single_assertion(assertion)
                if converted:
                    python_asserts.append(f"        {converted}")
            return '\n'.join(python_asserts)
        
        # Convert assertAll blocks
        # content = re.sub(
        #     r'assertAll\s*\(([^}]+)\}\s*\)',
        #     convert_assert_all,
        #     content,
        #     flags=re.DOTALL
        # )
        
        # Convert individual assertions
        for java_assert, python_template in self.method_mappings.items():
            if '{}' in python_template:
                # Handle assertions with parameters
                pattern = rf'{java_assert}\s*\((.*)\)'
                def replace_assertion(match):
                    params = [p.strip() for p in match.group(1).split(',')]
                    # print("----", match)
                    # print(len(params), params)
                    if java_assert == "assertEquals":
                        if len(params) == 3:
                            output = f"assert {params[1]} == pytest.approx({params[0]}, abs={params[2]})"
                            # output = "a == y"
                            return output
                        if len(params) == 2:
                            output = f"assert {params[1]} == {params[0]}"
                            # output = "a == y"
                            return output
                        print("^^missed", match)
                    if java_assert in ['assertEquals', 'assertNotEquals', 'assertSame', 'assertNotSame']:
                        if len(params) >= 2:
                            return python_template.format(params[1], params[0])
                    elif java_assert in ['assertTrue', 'assertFalse', 'assertNull', 'assertNotNull']:
                        if len(params) >= 1:
                            return python_template.format(", ".join(params))
                        # return match.group(0).replace("assertTrue", "assert").replace("assertFalse", "assert not")
                    return match.group(0)
                
                content = re.sub(pattern, replace_assertion, content)
        
        return content

    def convert_single_assertion(self, assertion: str) -> str:
        """Convert a single assertion statement"""
        assertion = assertion.strip()
        
        # Handle assertEquals with epsilon
        if assertion.startswith('assertEquals('):
            # Extract parameters
            params_match = re.search(r'assertEquals\(([^)]+)\)', assertion)
            if params_match:
                params = [p.strip() for p in params_match.group(1).split(',')]
                if len(params) == 3:  # expected, actual, epsilon
                    return f"assert abs({params[1]} - {params[0]}) < {params[2]}"
                elif len(params) == 2:  # expected, actual
                    return f"assert {params[1]} == {params[0]}"
            else:
                print(f"No equals for {assertion}")
        else:
            print("----", assertion)
        
        # Handle other assertions
        for java_assert, python_template in self.method_mappings.items():
            if assertion.startswith(java_assert + '('):
                pattern = rf'{java_assert}\s*\(([^)]+)\)'
                match = re.search(pattern, assertion)
                if match:
                    params = [p.strip() for p in match.group(1).split(',')]
                    if java_assert in ['assertEquals', 'assertNotEquals']:
                        if len(params) >= 2:
                            return python_template.format(params[1], params[0])
                    elif java_assert in ['assertTrue', 'assertFalse']:
                        if len(params) >= 1:
                            return python_template.format(params[0])
        
        return assertion

    def convert_java_syntax(self, content: str) -> str:
        """Convert various Java syntax elements to Python"""
        # Convert variable declarations
        content = re.sub(r'var\s+(\w+)\s*=', r'\1 =', content)
        content = re.sub(r'final\s+var\s+(\w+)\s*=', r'\1 =', content)
        content = re.sub(r'(\w+)\s+(\w+)\s*=', r'\2 =', content)
        
        # Convert method calls
        content = re.sub(r'Units\.degreesToRadians\(([^)]+)\)', r'math.radians(\1)', content)
        content = re.sub(r'Math\.([a-zA-Z]+)', r'math.\1', content)
        
        # Convert List.of() to Python list
        content = re.sub(r'List\.of\(([^)]+)\)', r'[\1]', content)
        
        # Convert new ArrayList<>() to list
        content = re.sub(r'new ArrayList<[^>]*>\(\)', r'[]', content)
        
        # Convert enhanced for loops
        content = re.sub(
            r'for\s*\(\s*(\w+)\s+(\w+)\s*:\s*([^)]+)\s*\)\s*{',
            r'for \2 in \3:',
            content
        )
        
        # Convert traditional for loops
        content = re.sub(
            r'for\s*\(\s*int\s+(\w+)\s*=\s*(\d+);\s*\1\s*<\s*([^;]+);\s*\1\+\+\s*\)\s*{',
            r'for \1 in range(\2, \3):',
            content
        )
        
        # Convert .length to len()
        content = re.sub(r'(\w+)\.length', r'len(\1)', content)
        content = re.sub(r'(\w+)\.size\(\)', r'len(\1)', content)
        
        # Convert .get() method calls
        content = re.sub(r'(\w+)\.get\(([^)]+)\)', r'\1[\2]', content)
        
        # Convert Java boolean literals
        content = re.sub(r'\btrue\b', 'True', content)
        content = re.sub(r'\bfalse\b', 'False', content)
        
        # Convert null to None
        content = re.sub(r'\bnull\b', 'None', content)
        
        # Convert Double.isNaN() to math.isnan()
        content = re.sub(r'\(\(Double\)\s*([^)]+)\)\.isNaN\(\)', r'math.isnan(\1)', content)
        
        return content

    def convert_class_structure(self, content: str) -> str:
        """Convert Java class structure to Python class structure"""
        lines = content.split('\n')
        converted_lines = []
        indent_level = 0
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            # Convert class declaration
            if line.startswith('class ') and line.endswith('{'):
                class_name = line.split()[1].replace('{', '')
                python_class_name = self.convert_class_name(class_name)
                converted_lines.append(f"class {python_class_name}:")
                indent_level = 1
                continue
            
            # Convert method declarations
            if line.startswith('@Test'):
                converted_lines.append('    @pytest.mark.parametrize' if 'parametrize' in line else '')
                continue
            
            # Convert method signatures
            if re.match(r'(public|private|protected)?\s*(static)?\s*void\s+\w+\s*\([^)]*\)\s*{', line):
                method_signature = self.convert_method_signature(line)
                converted_lines.append(f"    {method_signature}")
                indent_level += 1
                continue
            elif line.endswith("{"):
                converted_lines.append("    " * indent_level + line[:-1])
                indent_level += 1
                continue
            
            
            # Skip closing braces of class
            if line == '}':
                indent_level -= 1
                continue
            
            # Convert method body
            if line and not line.startswith('//') and not line.startswith('/*'):
                # Add appropriate indentation
                if indent_level > 0:
                    converted_lines.append(f"        {line}")
                else:
                    converted_lines.append("    " * indent_level + line)
        
        return '\n'.join(converted_lines)

    def convert_file(self, java_file_path: str, output_path: str = None) -> str:
        """Convert a Java test file to Python pytest format"""
        with open(java_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply conversions in order
        content = self.convert_imports(content)
        # content = self.convert_constants(content)
        content = self.convert_java_syntax(content)
        content = self.convert_assertions(content)
        content = self.convert_class_structure(content)

        content = content.replace(" new ", " ")
        content = content.replace(";", "")
        content = content.replace(".getX(", ".X(")
        content = content.replace(".getY(", ".Y(")
        content = content.replace(".getZ(", ".Z(")
        content = content.replace(".getW()", ".W()")
        content = content.replace(".getDegrees()", ".degrees()")
        content = content.replace(".getRotation()", ".rotation()")
        content = content.replace(".getDistance(", ".distance(")
        content = content.replace(".getFocalPoints(", ".focalPoints(")
        content = re.sub(r"\.plus\((.*)\)", r" + \1", content)
        content = re.sub(r"\.minus\((.*)\)", r" - \1", content)
        content = re.sub(r"\.times\((.*)\)", r" * \1", content)
        content = re.sub(r"\.div\((.*)\)", r" / \1", content)
        content = re.sub(r"\.divide\((.*)\)", r" / \1", content)
        content = re.sub(r"VecBuilder.fill\((.*)\)", r"np.array([\1])", content)
        # content = content.replace("Rotation2d.fromDegrees", "math.degrees")
        content = content.replace("Rotation2d.kCW_Pi_2", "Rotation2d.fromDegrees(-90)")
        content = content.replace("Rotation2d.kCCW_Pi_2", "Rotation2d.fromDegrees(90.0)")
        content = content.replace("Rotation2d.kPi", "Rotation2d.fromDegrees(180)")
        content = content.replace("Rotation2d.kZero", "Rotation2d.fromDegrees(0)")
        content = content.replace("Rotation3d.kZero", "Rotation3d()")
        content = content.replace("Pose2d.kZero", "Pose2d(0, 0, 0)")
        content = content.replace("Pose3d.kZero", "Pose3d(0, 0, 0)")
        content = content.replace("Translation2d.kZero", "Translation2d(0, 0)")
        content = content.replace("Translation3d.kZero", "Translation3d(0, 0, 0)")
        content = content.replace("math.toRadians", "math.radians")
        content = content.replace("getTotalTime()", "totalTime()")
        content = content.replace("getTranslation()", "translation()")
        content = content.replace("getRotation()", "rotation()")
        content = content.replace("getRadians()", "radians()")

        
        content = content.replace("new Translation2d(", "Translation2d(")
        content = content.replace("new Translation3d(", "Translation3d(")
        content = content.replace("new Quaternion(", "Quaternion(")
        content = content.replace("new Pose2d(", "Pose2d(")
        content = content.replace("new Pose3d(", "Pose3d(")
        content = content.replace("new Rectangle2d(", "Rectangle2d(")
        content = content.replace("new Rotation2d(", "Rotation2d(")
        content = content.replace("new Rotation3d(", "Rotation3d(")
        content = content.replace("Math.PI", "math.pi")
        content = content.replace("math.PI", "math.pi")
        content = content.replace("SwerveModulePosition[] {fl, fr, bl, br}", "[fl, fr, bl, br]")
        content = content.replace("SwerveModulePosition[] {zero, zero, zero, zero}", "[zero, zero, zero, zero]")


# for \(i = 0 i < (.*) \+\+i\)
# for i in range($1):
        

        content = re.sub(r"\(\) -> (.*),\n", r"\1\n", content)
        content = re.sub(r"\(\) -> (.*)\)\n", r"\1\n", content)
        # content = re.sub(r"\(\) -> (.*)\),", r"\1", content)
        
        # Add pytest imports and docstring
        python_content = '''"""
Converted from Java JUnit test to Python pytest
"""

import math
import pytest
from typing import List, Dict, Optional

''' + content
        
        # Write to output file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(python_content)
            print(f"Converted test written to: {output_path}")
        
        return python_content

def xxxx(input_file, output):

    
    # Determine output path
    if output:
        output_path = output
    else:
        # Generate output filename
        stem = Path(input_file).stem
        print()
        if stem.endswith('Test'):
            stem = stem[:-4]  # Remove 'Test' suffix
        output_path = f"test_{camel_to_snake(stem)}.py"
    
    # Convert the file
    converter = JavaToPytestConverter()
    
    try:
        result = converter.convert_file(input_file, output_path)
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Convert Java JUnit tests to Python pytest')
    parser.add_argument('input_file', help='Input Java test file')
    parser.add_argument('-o', '--output', help='Output Python test file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)

    if input_path.is_dir():
        for root, _, files in os.walk(input_path):
            print(root, files)
            for f in files:
                stem = Path(f).stem
                print()
                if stem.endswith('Test'):
                    stem = stem[:-4]  # Remove 'Test' suffix
                # output_path = os.path.join(root.replace("src/test/java/edu/wpi/first/math", "src/test/python"), f"test_{camel_to_snake(stem)}.py")
                output_path = os.path.join(root.replace("src/test/native/cpp", "src/test/python"), f"test_{camel_to_snake(stem)}.py")
                import pathlib
                pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as of:
                    of.write("""def test_dummy():
                    pass
                    """)
                # Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                # xxxx(os.path.join(root, f), output_path)
    else:
        xxxx(input_path, args.output)
        
if __name__ == "__main__":
    main()