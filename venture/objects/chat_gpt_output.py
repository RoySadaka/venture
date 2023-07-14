from dataclasses import dataclass, field
import json

@dataclass
class ChatGPTOutput:
    output: object
    _parsed_args:object = field(default=None)

    @property
    def output_tokens_count(self):
        if 'usage' in self.output and 'completion_tokens' in self.output['usage']:
            return self.output['usage']['completion_tokens']
        return 0

    @property
    def input_tokens_count(self):
        if 'usage' in self.output and 'prompt_tokens' in self.output['usage']:
            return self.output['usage']['prompt_tokens']
        return 0

    @property
    def assistant_message(self):
        return self.output['choices'][0]['message']

    @property
    def assistant_message_content(self):
        return self.assistant_message['content']

    @property
    def assistant_function(self):
        return self.assistant_message['function_call']

    @property
    def assistant_function_name(self):
        return self.assistant_function['name']

    @property
    def assistant_function_arguments(self):
        return self.assistant_function['arguments']

    @property
    def finish_reason(self):
        return self.output['choices'][0]['finish_reason']

    @property
    def assistant_function_parsed_arguments(self):
        if self._parsed_args is None:
            try:
                self._parsed_args = json.loads(self.assistant_function_arguments)
            except:
                pass
        return self._parsed_args

    @property
    def has_function_arguments(self):
        choices_in_output = 'choices' in self.output
        has_function = choices_in_output and 'function_call' in self.assistant_message
        has_function_arguments = has_function and 'arguments' in self.assistant_function
        return has_function_arguments


    @property
    def has_assistant_function_parsed_arguments(self):
        return self.assistant_function_parsed_arguments is not None

    @property
    def has_assistant_message_content(self):
        return 'content' in self.assistant_message and self.assistant_message_content is not None


    @property
    def is_success(self):
        choices_in_output = 'choices' in self.output

        finish_reason_exists = self.finish_reason is not None

        has_message_call = self.assistant_message is not None

        return choices_in_output and \
                finish_reason_exists and \
                has_message_call and \
                (self.has_assistant_message_content or self.has_assistant_function_parsed_arguments)