import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from downloader import YouTubeDownloader


class DownloadListingTests(unittest.TestCase):
    def test_downloader_lists_audio_files_sorted(self):
        with tempfile.TemporaryDirectory() as directory:
            download_folder = Path(directory)
            (download_folder / "z-song.mp3").touch()
            (download_folder / "a-song.mp3").touch()
            (download_folder / "notes.txt").touch()

            downloader = YouTubeDownloader.__new__(YouTubeDownloader)
            downloader.download_folder = download_folder

            self.assertEqual(
                [path.name for path in downloader.list_downloaded_files()],
                ["a-song.mp3", "z-song.mp3"],
            )

    def test_main_listing_separates_file_rows(self):
        with patch("bootstrap.ensure_runtime_environment"):
            from main import YouTubeAudioDedupSystem

        with tempfile.TemporaryDirectory() as directory:
            first_file = Path(directory) / "a-song.mp3"
            second_file = Path(directory) / "b-song.mp3"
            first_file.write_bytes(b"a")
            second_file.write_bytes(b"bb")

            app = YouTubeAudioDedupSystem.__new__(YouTubeAudioDedupSystem)
            app.downloader = Mock()
            app.downloader.list_downloaded_files.return_value = [first_file, second_file]

            output = StringIO()
            with redirect_stdout(output):
                app.list_downloaded_files()

            self.assertIn("a-song.mp3", output.getvalue())
            self.assertIn("a-song.mp3  (0.00 MB)\n\n  b-song.mp3", output.getvalue())


if __name__ == "__main__":
    unittest.main()
