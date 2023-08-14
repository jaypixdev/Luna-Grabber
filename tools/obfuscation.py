import argparse
import base64
import codecs
import os
import random
import sys
from lzma import compress
from marshal import dumps
from textwrap import wrap


class CodeObfuscator:
    def __init__(self, code, output_path):
        self.code = code.encode()
        self.output_path = output_path
        self.var_length = 3
        self.variables = {}

        self.marshal()
        self.obfuscate_code()

    def generate_variable(self, name):
        new_variable = self.variables.get(name)
        if new_variable is None:
            new_variable = "_" + "".join(["_" for _ in range(self.var_length)])
            self.var_length += 1
            self.variables[name] = new_variable
        return new_variable

    def obfuscate_string(self, string, config={}, is_function=False):
        # ... (same as before)

    def compress_code(self):
        self.code = compress(self.code)

    def marshal(self):
        self.code = dumps(compile(self.code, "<string>", "exec"))

    def obfuscate_code(self):
        self.compress_code()
        # ... (rest of the obfuscation process, same as before)

    def finalize(self):
        if os.path.dirname(self.output_path).strip() != "":
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w") as obfuscated_file:
            obfuscated_file.write(self.code.decode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=sys.argv[0], description="Obfuscates Python code to make it harder to read")
    parser.add_argument("input_file", help="Path to the file containing the Python code")
    parser.add_argument("-o", type=str, help='Output file path [Default: "Obfuscated_<input_file>.py"]', dest="output_path")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f'No such file: "{args.input_file}"', file=sys.stderr)
        sys.exit(1)
    elif not args.input_file.endswith((".py", ".pyw")):
        print('The file does not have a valid Python script extension!', file=sys.stderr)
        sys.exit(1)

    if args.output_path is None:
        args.output_path = "Obfuscated_" + os.path.basename(args.input_file)

    with open(args.input_file, encoding="utf-8") as source_file:
        code_content = source_file.read()

    obfuscator = CodeObfuscator(code_content, args.output_path)
    obfuscator.finalize()
