import os
import ffmpeg
import pyheif
from PIL import Image
import shutil
import pyexiv2


def convert_to_heic(jpeg_image_path, heic_image_path):
    """将JPEG图片转换为HEIC格式"""
    image = Image.open(jpeg_image_path)
    heif_file = pyheif.PyHEIFWriter(heic_image_path)
    heif_file.write(image)
    print(f"Converted {jpeg_image_path} to {heic_image_path}")


def convert_video_to_mov(mp4_video_path, mov_video_path):
    """将MP4视频转换为MOV格式"""
    ffmpeg.input(mp4_video_path).output(mov_video_path).run()
    print(f"Converted {mp4_video_path} to {mov_video_path}")


def copy_exif_data(image_path, heic_image_path):
    """复制原始图片的EXIF元数据到HEIC文件"""
    metadata = pyexiv2.ImageMetadata(image_path)
    metadata.read()

    heic_metadata = pyexiv2.ImageMetadata(heic_image_path)
    heic_metadata.read()

    for key in metadata.exif_keys:
        heic_metadata[key] = metadata[key]

    heic_metadata.write()
    print(f"Copied EXIF metadata from {image_path} to {heic_image_path}")


def create_live_photo(motion_photo_folder, output_folder):
    """将小米动态照片转换为苹果实况照片"""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 假设Motion Photo文件夹中有图片和视频
    static_image_path = os.path.join(motion_photo_folder, 'image.jpg')
    video_path = os.path.join(motion_photo_folder, 'video.mp4')

    if not os.path.exists(static_image_path) or not os.path.exists(video_path):
        raise FileNotFoundError("Motion photo folder must contain 'image.jpg' and 'video.mp4'")

    # 1. 将静态图片转换为HEIC格式
    heic_image_path = os.path.join(output_folder, 'image.heic')
    convert_to_heic(static_image_path, heic_image_path)

    # 2. 将视频转换为MOV格式
    mov_video_path = os.path.join(output_folder, 'video.mov')
    convert_video_to_mov(video_path, mov_video_path)

    # 3. 复制EXIF元数据
    copy_exif_data(static_image_path, heic_image_path)

    # 4. 输出Live Photo文件结构
    print(f"Live Photo created in {output_folder}:")
    print(f"- {heic_image_path}")
    print(f"- {mov_video_path}")


# 使用示例
if __name__ == "__main__":
    motion_photo_folder = 'path_to_motion_photo_folder'  # 输入小米动态照片文件夹路径
    output_folder = 'output_live_photo_folder'  # 输出苹果实况照片的文件夹路径
    create_live_photo(motion_photo_folder, output_folder)
