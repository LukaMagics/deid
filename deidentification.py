class Deidentification:
    
    def __init__(self, string, start_index, end_index, method):
        self.string = string
        self.start_index = start_index
        self.end_index = end_index
        self.method = method
        self._validate_indices()


    def _validate_indices(self):
        if self.start_index < 0 or self.end_index >= len(self.string) or self.start_index > self.end_index:
            raise ValueError("Invalid index range")


    def masking(self, mask_char='*'):

        masked_part = mask_char * (self.end_index - self.start_index)
        new_string = self.string[:self.start_index] + masked_part + self.string[self.end_index:]

        return new_string


    def process(self):
        if self.method == "masking":
            return self.masking()