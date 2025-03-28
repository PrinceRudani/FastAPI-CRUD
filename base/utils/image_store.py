import os

from base.config.logger_config import get_logger
from base.utils.custom_exception import AppServices

logger = get_logger()

UPLOAD_DIR = "static/product_image/"


class ProductImageUploader:
    @staticmethod
    async def save_image(images):
        """Save uploaded image(s) and return its name and path."""
        try:
            file_paths = []
            file_names = []

            # Ensure images is a list
            if not isinstance(images, list):
                images = [images]

            if images:
                os.makedirs(UPLOAD_DIR, exist_ok=True)

                for image in images:
                    image_path = os.path.join(UPLOAD_DIR, image.filename)
                    print("image path>>>>>>>>>.", image_path)

                    with open(image_path, "wb") as buffer:
                        buffer.write(await image.read())
                        file_paths.append(image_path)
                        file_names.append(image.filename)

                return file_names, file_paths

            return None, None

        except Exception as exception:
            logger.exception("Error saving image")
            return AppServices.handle_exception(exception, is_raise=True)
