class CardNotFoundError(Exception):
    """
    Raised when no card is detected in the image
    """

    def __init__(self, message="No ID card detected in image."):
        self.message = message
        super().__init__(self.message)


class CardDetectionAmbiguousError(Exception):
    """
    Raised when multiple cards are detected in the image
    """

    def __init__(self, message="Multiple cards detected in image."):
        self.message = message
        super().__init__(self.message)


class OCRExtractionError(Exception):
    """
    Raised when OCR fails to extract student ID
    """

    def __init__(self, message="Failed to extract student ID from card."):
        self.message = message
        super().__init__(self.message)


class PerspectiveCorrectionError(Exception):
    """
    Raised when perspective correction fails or produces invalid output
    """

    def __init__(self, message="Failed to correct card perspective."):
        self.message = message
        super().__init__(self.message)


class InvalidStudentIDError(Exception):
    """
    Raised when extracted student ID fails validation
    """

    def __init__(self, message="Extracted student ID is invalid."):
        self.message = message
        super().__init__(self.message)
