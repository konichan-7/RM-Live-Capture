from typing import List, Union, Dict
import asyncio
import shutil

from pydantic import BaseModel
import cachetools.func

import config


class Video(BaseModel):
    title: str
    red: str
    blue: str
    role: str
    round: int
    duration: float
    file_name: str


class VideoFilterProps(BaseModel):
    red: Union[str, None] = None
    blue: Union[str, None] = None
    role: Union[str, None] = None
    current: int
    pageSize: int
    sort: Dict[str, str] = {}


import re

def get_video_info(file_name: str) -> Union[Video, None]:
    title = "Null Vs Null"
    duration = 0.
    with (config.save_dir / file_name).open('r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith("#TITLE:"):
                title = line.replace("#TITLE:", "").strip()
            if line.startswith("#EXTINF:"):
                duration += float(line.split(":")[1].split(",")[0])
    
    match = re.match(r"^(.*?) Vs (.*?) (.*?) R(\d+) (\d+)$", title)
    if not match:
        return None
        
    return Video(
        title=title,
        red=match.group(1),
        blue=match.group(2),
        role=match.group(3),
        round=int(match.group(4)),
        duration=duration,
        file_name=file_name
    )


@cachetools.func.ttl_cache(maxsize=1, ttl=30)
def get_video_list() -> List[Video]:
    res = []
    for it in config.save_dir.glob("*.m3u8"):
        _video = get_video_info(it.name)
        if _video is not None:
            res.append(_video)
    res = sorted(res, key=lambda video: video.file_name.split('_')[-1].split('.')[0], reverse=True)
    return res


def filter_video_list(current: int, pageSize: int, **kwargs):
    res = get_video_list()
    if kwargs.get('red') is not None:
        res = [video for video in res if video.red == kwargs['red']]
    if kwargs.get('blue') is not None:
        res = [video for video in res if video.blue == kwargs['blue']]
    if kwargs.get('role') is not None:
        res = [video for video in res if video.role == kwargs['role']]
    for key, value in kwargs.get('sort', {}).items():
        res = sorted(res, key=lambda video: getattr(video, key), reverse=(value == "descend"))
    total = len(res)
    start = (current - 1) * pageSize
    end = start + pageSize
    return {"data": res[start:end], "total": total}


async def convert_to_mp4(_video: Video):
    config.mp4_dir.mkdir(parents=True, exist_ok=True)

    def run():
        import ffmpeg
        cmd = shutil.which("ffmpeg")
        if cmd is None:
            try:
                import imageio_ffmpeg
                cmd = imageio_ffmpeg.get_ffmpeg_exe()
            except Exception:
                cmd = "ffmpeg"
        ffmpeg.input(str(config.save_dir / _video.file_name)).output(
            str(config.mp4_dir / f"{_video.title}.mp4"),
            acodec="copy", vcodec="copy"
        ).run(cmd=cmd, overwrite_output=True)

    await asyncio.to_thread(run)


async def convert_missing_mp4() -> List[str]:
    errors = []
    for _video in get_video_list():
        mp4 = config.mp4_dir / f"{_video.title}.mp4"
        if mp4.exists():
            continue
        try:
            await convert_to_mp4(_video)
        except Exception as e:
            errors.append(f"{_video.file_name}: {e}")
    return errors


def delete_file(_video: Video):
    mp4 = config.mp4_dir / f"{_video.title}.mp4"
    if mp4.exists():
        mp4.unlink()
    with open(config.save_dir / _video.file_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("#EXTINF"):
                file = config.save_dir / lines[i + 1].strip()
                if file.exists():
                    file.unlink()
    (config.save_dir / _video.file_name).unlink()
    get_video_list.cache_clear()


if __name__ == '__main__':
    async def main():
        errors = await convert_missing_mp4()
        for error in errors:
            print(error)

    asyncio.run(main())
