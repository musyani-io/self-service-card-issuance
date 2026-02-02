
class BarcodeNotFoundError(Exception):
    """
    Raised when no barcode is detected
    """

    def __init__(self, message = "No barcode detected."):
        self.message = message
        super().__init__(self.message)
    pass