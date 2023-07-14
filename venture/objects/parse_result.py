class ParseResult:
    ERROR = 'Error, try again'
    SUCCESS_ADD = 'Successfully added'
    SUCCESS_DELETE = 'Successfully deleted'
    ALREADY_EXISTS = 'Skipped, already exists'
    TOO_SHORT = 'Skipped, too short'
    TOO_LONG = 'Skipped, too long'

    @staticmethod
    def symbol(value):
        if value == ParseResult.ERROR:
            return '🟥'
        if value in {ParseResult.SUCCESS_ADD, ParseResult.SUCCESS_DELETE}:
            return '🟩'
        if value in {ParseResult.ALREADY_EXISTS, ParseResult.TOO_SHORT, ParseResult.TOO_LONG}:
            return '🟧'
        return ''
