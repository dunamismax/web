import os
import uuid
import logging
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from fastapi import HTTPException, UploadFile
from typing import Dict, Optional

# ✅ Configure logging
logger = logging.getLogger("file-converter")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class FileConverterService:
    def __init__(self):
        """Initialize the file converter service."""
        self.tasks: Dict[str, dict] = {}
        self.upload_dir = Path("/home/sawyer/github/web/converter_service/uploads")
        self.output_dir = Path("/home/sawyer/github/web/converter_service/converted")
        self._create_dirs()

        # ✅ Allowed file formats
        self.allowed_formats = {
            "audio": ["mp3", "wav", "ogg", "flac", "aac", "m4a"],
            "video": ["mp4", "mov", "avi", "mkv", "webm"],
            "special": ["voicemail_wav"],
        }

        # ✅ FFmpeg conversion settings
        self.conversion_profiles = {
            "voicemail_wav": {
                "extension": "wav",
                "ffmpeg_args": [
                    "-acodec",
                    "pcm_mulaw",
                    "-ar",
                    "8000",
                    "-ac",
                    "1",
                    "-vn",
                    "-y",
                ],
            }
        }

    def _create_dirs(self):
        """Ensure upload and output directories exist."""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def handle_conversion(
        self, file: UploadFile, output_format: str = "mp3"
    ) -> dict:
        file_ext = self._get_file_extension(file.filename)
        task_id = str(uuid.uuid4())

        if not self._is_valid_extension(file_ext):
            raise HTTPException(400, "Unsupported file format.")

        upload_path = self.upload_dir / f"{task_id}_original.{file_ext}"
        await self._save_file(file, upload_path)

        self.tasks[task_id] = {
            "status": "queued",
            "original_name": file.filename,
            "upload_path": str(upload_path),
            "output_path": None,
            "start_time": datetime.now(),
            "error": None,
        }

        logger.info(
            f"🚀 Task Created: {task_id} - {self.tasks[task_id]}"
        )  # ✅ Debugging log

        asyncio.create_task(self._process_file(task_id, output_format))
        return {"task_id": task_id}

    async def _process_file(self, task_id: str, output_format: str):
        """Processes file conversion in the background."""
        try:
            task = self.tasks[task_id]
            task["status"] = "processing"

            # ✅ Determine output format
            output_ext = self.conversion_profiles.get(output_format, {}).get(
                "extension", output_format
            )
            output_filename = f"{task_id}_converted.{output_ext}"
            output_path = self.output_dir / output_filename

            # ✅ Build FFmpeg command
            ffmpeg_args = self.conversion_profiles.get(output_format, {}).get(
                "ffmpeg_args", []
            )
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                task["upload_path"],
                *ffmpeg_args,
                str(output_path),
            ]

            # ✅ Run FFmpeg conversion
            logger.info(f"Starting conversion: {task['upload_path']} -> {output_path}")
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            # ✅ Handle timeout
            timeout = 300  # 5 minutes
            try:
                await asyncio.wait_for(proc.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                proc.kill()
                raise RuntimeError("Conversion timed out.")

            # ✅ Check for FFmpeg success
            if proc.returncode != 0:
                raise RuntimeError(f"FFmpeg error: {proc.stderr.decode()}")

            # ✅ Mark task as completed
            task["output_path"] = str(output_path)
            task["status"] = "completed"
            logger.info(f"Conversion successful: {output_path}")

        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            task["status"] = "failed"
            task["error"] = str(e)

        finally:
            # ✅ Cleanup original file
            try:
                os.remove(task["upload_path"])
            except Exception as e:
                logger.error(f"Cleanup error: {e}")

    async def get_status(self, task_id: str) -> dict:
        task = self.tasks.get(task_id)

        if not task:
            logger.error(f"❌ Task Not Found: {task_id}")  # ✅ Debugging log
            raise HTTPException(404, "Task not found.")

        return {
            "status": task["status"],
            "download_url": (
                f"/download/{Path(task['output_path']).name}"
                if task["output_path"]
                else None
            ),
            "error": task.get("error"),
        }

    async def serve_file(self, filename: str):
        """Serves converted files with security checks."""
        file_path = self.output_dir / filename

        # ✅ Security checks
        if not file_path.exists() or ".." in filename:
            raise HTTPException(404, "File not found.")

        return FileResponse(
            file_path,
            headers={
                "Content-Disposition": f"attachment; filename={filename.split('_', 2)[-1]}"
            },
        )

    # ✅ Helper Methods
    def _get_file_extension(self, filename: str) -> str:
        """Extracts the file extension from a filename."""
        return Path(filename).suffix[1:].lower()

    def _is_valid_extension(self, ext: str) -> bool:
        """Checks if a file extension is valid for conversion."""
        return any(ext in formats for formats in self.allowed_formats.values())

    async def _save_file(self, file: UploadFile, path: Path):
        """Saves an uploaded file asynchronously."""
        try:
            with open(path, "wb") as buffer:
                while content := await file.read(1024 * 1024):  # 1MB chunks
                    buffer.write(content)
        except Exception as e:
            logger.error(f"File save failed: {e}")
            raise HTTPException(500, "Failed to save uploaded file.")
