from typing import List, Set


class PackageInput:
    def __init__(self, num_tokens:int, initial_functions:List[object]):
        self.num_tokens = num_tokens
        self.functions = initial_functions
        self.function_names = {f['name'] for f in self.functions}
