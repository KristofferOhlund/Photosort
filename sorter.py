import os
from datetime import datetime
from exif import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import shutil


class MediaSorter():
    """src, dst --> Str path, 
    Reads jpgs and .mov files creation date.
    Creates folders with years / month and moves the files
    to corresponding folder."""

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def get_photo_vid_md(self):
        """Loops file in src.
        If jpg, jpeg, .mov or mp4, reads the creation date attribute.
        Creates datetime object from attrb.
        Returns dict with full path to file as key, and datetime object as value"""

        # Dictionary for files in src,
        # values == datetime, dst
        media_with_md = {}
        count_images = 0
        count_videos = 0
        unred_photos = 0
        unred_videos = 0

        # Returns successfully files (with datetime attribute)
        photo_success_amnt = count_images - unred_photos
        video_success_amnt = count_videos - unred_videos
        

        # Loops src path for photo or vid.
        # .jpg / Jpegs
        for media in os.listdir(self.src):
            # splits at name and extension
            media_name, media_ext = os.path.splitext(media)
            # Full path file
            media_file = os.path.join(self.src, media)

            # Photos
            if media_ext in [".jpg", ".jpeg", ".JPG", ".JPEG", ".heic", ".HEIC"]:
                count_images += 1
                with open(media_file, "rb") as img:
                    # Image object
                    my_img = Image(img)
                    try:
                        # Datetime attrib --> datetime.datetime object
                        date_obj = datetime.strptime(
                            my_img["datetime"], "%Y:%m:%d %H:%M:%S")
                        # Gets month name from object
                        photo_datetime_obj = datetime.strftime(
                            date_obj, "%d-%B-%Y-%H:%M:%S")

                        # Splits datetime for folder creation. path + year + month
                        # --> day, month, year = key[0], key[1], key[2]
                        photo_datetime = photo_datetime_obj.split("-")

                        # Adds file with creation date to dictionary
                        media_with_md[media_file] = photo_datetime

                    # If missing attrib.
                    except (AttributeError, KeyError) as e:
                        unred_photos += 1
                        continue

            # .MOV and .mp4
            elif media_ext in [".MOV", ".mp4"]:
                count_videos += 1
                parser = createParser(media_file)
                metadata = extractMetadata(parser)
                # Datetime object to string
                datetime_obj = metadata.get("creation_date")

                # Gets month name from object
                mov_datetime_obj = datetime.strftime(
                    datetime_obj, "%d-%B-%Y-%H:%M:%S")

                # Splits datetime for folder creation. path + year + month
                # --> day, month, year = key[0], key[1], key[2]
                mov_datetime = mov_datetime_obj.split("-")

                # Adds to dictionary
                media_with_md[media_file] = mov_datetime

        return media_with_md, count_images, count_videos, photo_success_amnt, video_success_amnt

    def create_dirrs_and_move_files(self, media_dict):
        """Creates new dirr tree as year --> month.
        Renames files from src (keys) as day_month_nr."""

        # Creating directories from list
        dirrs_to_be_created = []
        # media_file destinations
        media_file_dst = []
        # To make media_file names unique, increment from 0
        serial_number = 0

        # Looping through media_dict.
        # Creating new dirr paths and filenames
        for media in media_dict:
            # Splits media for extension
            media_path, media_ext = splitext(media)
            serial_number += 1
            # New dirrs
            dirr_path = os.path.join(
                self.dst, media_dict[media][2], media_dict[media][1])
            # Adds to list
            dirrs_to_be_created.append(dirr_path)

            # New full, filenames Path/day_month_serie_extension
            new_media_name = os.path.join(self.dst, media_dict[media][2], media_dict[media][1],
                                          media_dict[media][0] + "_" + media_dict[media][1] + "_" + f"{serial_number}" + media_ext)
            # Appends new name to list
            media_file_dst.append(new_media_name)

        # Creating dirrs
        for dirr in dirrs_to_be_created:
            os.makedirs(dirr, exist_ok=True)

        # Zips src and dst for files to be moved.
        moves = list(zip(media_dict.keys(), media_file_dst))

        # Moving files
        for media in moves:
            if os.path.exists(media[1]):
                print("File already exists")
            else:
                shutil.move(media[0], media[1])



#if __name__ == "__main__":
#    # Run in Main
#    src = input("Sort media FROM path:    ")
#    dst = input("Sort media TO path:   ")#

#    sorter = MediaSorter(src, dst)
#    data = sorter.get_photo_vid_md()
#    sorter.create_dirrs_and_move_files(data[])
