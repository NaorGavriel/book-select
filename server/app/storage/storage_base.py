from abc import ABC, abstractmethod


class StorageBase(ABC):
    """
    Interface for image storage classes.
    """

    @abstractmethod
    def save_image(self,*,image_bytes: bytes,filename: str,user_id: int) -> str:
        """
        Save image data and return an identifier.
        The identifier string's format is backend-specific.
        """
        pass
