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
