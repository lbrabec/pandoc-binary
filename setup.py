import os
import shutil
import subprocess
import sys

from setuptools import setup
from setuptools.command.build import build as _build

try:
    from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        _, _, plat = super().get_tag()
        return "py3", "none", plat


class build(_build):
    def run(self):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        dst = os.path.join(project_dir, "pandoc_rhai", "data", "bin")

        build_pandoc = os.environ.get("BUILD_PANDOC")
        if build_pandoc is None:
            sys.exit("Error: BUILD_PANDOC env var is required (set to 'true' or 'false')")

        if build_pandoc.lower() == "true":
            subprocess.check_call(
                [os.path.join(project_dir, "scripts", "build_pandoc.sh")],
            )
        else:
            pandoc_path = os.environ.get("PANDOC_PATH")
            if pandoc_path is None:
                sys.exit("Error: PANDOC_PATH env var is required when BUILD_PANDOC != 'true'")
            os.makedirs(dst, exist_ok=True)
            shutil.copy2(pandoc_path, os.path.join(dst, "pandoc"))

        super().run()


setup(
    packages=["pandoc_rhai"],
    package_data={"pandoc_rhai": ["data/bin/*"]},
    cmdclass={"build": build, "bdist_wheel": bdist_wheel},
)
