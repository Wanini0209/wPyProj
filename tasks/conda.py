"""Tasks for Conda Develop Environments.

Methods
-------
update:
    Update local Conda information.
create:
    Create Conda develop environment.
remove:
    Remove Conda develop environment.
activate:
    Activate Conda develop environment.

"""

import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

from invoke import Context, task

CONDA_INFO_FILE: str = ".conda"
PROJ_INFO_FILE: str = ".info"
MAX_64BYTE_INT: int = 0xFFFFFFFFFFFFFFFF


def get_cmd_output(cmd: str, encoding: str = "utf-8") -> str:
    """Execute command and return output."""
    recv = subprocess.check_output(cmd, shell=True)
    ret = recv.decode(encoding)
    return ret.strip()


def get_random_env_name(prefix: str) -> str:
    """Generate random environment name."""
    now = datetime.datetime.now()
    suffix = hex(hash(now) & MAX_64BYTE_INT)

    if not suffix.startswith("0x"):
        raise ValueError(f"Invalid hex format: {suffix}")

    ret = f"{prefix}_{suffix[2:]}"
    return ret


class CondaInfo(NamedTuple):
    """Conda Environment Information."""

    python_version: str
    env_name: str
    conda_path: str | None = None
    conda_cmd: str | None = None
    activate_cmd: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Convert to dictionary."""
        ret = {
            "condaCmd": self.conda_cmd,
            "activateCmd": self.activate_cmd,
            "envName": self.env_name,
            "condaRoot": self.conda_path,
            "pyVer": self.python_version,
        }
        return ret

    def dump_to_json(self, file: str) -> None:
        """Dump to JSON file."""
        with open(file, "w", encoding="utf-8") as fout:
            json.dump(self.to_dict(), fout)

    @classmethod
    def from_dict(cls, recv: dict[str, str]) -> "CondaInfo":
        """Create CondaInfo from dictionary."""
        # 這裡放寬檢查，因為如果環境改變，路徑可能失效，但在載入時我們暫時接受
        return cls(
            python_version=recv.get("pyVer", "3.9"),
            env_name=recv.get("envName", ""),
            conda_path=recv.get("condaRoot"),
            conda_cmd=recv.get("condaCmd"),
            activate_cmd=recv.get("activateCmd"),
        )

    @classmethod
    def load_from_json(cls, file: str) -> "CondaInfo":
        """Load from JSON file."""
        with open(file, encoding="utf-8") as fin:
            recv = json.load(fin)
        return cls.from_dict(recv)

    @classmethod
    def make(cls, project_name: str, python_version: str) -> "CondaInfo":
        """Create new CondaInfo for project.

        Parameters
        ----------
        project_name : str
            Name of the project.
        python_version : str
            Python version to use.

        Returns
        -------
        CondaInfo
            New CondaInfo instance.
        """
        # 1. 尋找 Conda 執行檔
        conda_cmd = shutil.which("conda")
        if not conda_cmd:
            # 嘗試一些常見的預設路徑 (Windows)
            user_profile = os.environ.get("USERPROFILE", "")
            candidates = [
                os.path.join(user_profile, "anaconda3", "Scripts", "conda.exe"),
                os.path.join(user_profile, "miniconda3", "Scripts", "conda.exe"),
            ]
            for cand in candidates:
                if os.path.exists(cand):
                    conda_cmd = cand
                    break

        if not conda_cmd:
            raise FileNotFoundError("Conda executable not found in PATH")

        conda_cmd_path = Path(conda_cmd)

        # 2. 尋找 Activate 腳本
        # 在 Windows 上通常是 Scripts/activate.bat
        # 在 Linux/Mac 上通常是 bin/activate
        activate_cmd = None

        if sys.platform == "win32":
            # Windows: 通常在 Scripts 資料夾
            scripts_dir = conda_cmd_path.parent
            activate_candidate = scripts_dir / "activate.bat"
            if activate_candidate.exists():
                activate_cmd = str(activate_candidate)
        else:
            # Linux/Mac: conda 可能是個 shell script 封裝，真正的 bin 在上一層或同一層
            # 嘗試從 conda 路徑推導
            bin_dir = conda_cmd_path.parent
            activate_candidate = bin_dir / "activate"
            if activate_candidate.exists():
                activate_cmd = str(activate_candidate)

        # 3. 尋找 Conda Root
        # 通常是 Scripts 或 bin 的上一層
        conda_root = conda_cmd_path.parent.parent

        env_name = get_random_env_name(project_name)

        ret = cls(
            conda_path=str(conda_root),
            conda_cmd=str(conda_cmd),
            activate_cmd=str(activate_cmd) if activate_cmd else None,
            env_name=env_name,
            python_version=python_version,
        )
        return ret


def _get_conda_info() -> CondaInfo | None:
    """Get conda information from local file."""
    if os.path.exists(CONDA_INFO_FILE):
        ret = CondaInfo.load_from_json(CONDA_INFO_FILE)
        return ret
    return None


def _update_conda_info(info: CondaInfo) -> None:
    """Update conda information to local file."""
    info.dump_to_json(CONDA_INFO_FILE)


def get_proj_info() -> dict[str, str]:
    """Get project information."""
    if not os.path.exists(PROJ_INFO_FILE):
        # Fallback if .info doesn't exist (e.g. manually created project)
        return {"name": "wPyProj", "version": "3.12"}

    with open(PROJ_INFO_FILE, encoding="utf-8") as f:
        ret = json.load(f)
    return ret


@task
def update(ctx: Context) -> None:
    """Update local Conda information."""
    proj_info = get_proj_info()
    info = CondaInfo.make(proj_info["name"], proj_info["version"])
    _update_conda_info(info)
    print(f"Conda info updated. Env Name: {info.env_name}")


@task(pre=[update])
def create(ctx: Context) -> None:
    """Create Conda develop environment."""
    info = _get_conda_info()
    if info is None:
        raise RuntimeError("Please run `update` before `create`")

    ctx.run(
        f"{info.conda_cmd} "
        f"create --name {info.env_name} "
        f"python={info.python_version} -y"
    )


@task
def remove(ctx: Context) -> None:
    """Remove Conda develop environment."""
    info = _get_conda_info()
    if info is None:
        raise RuntimeError("Please run `create` before `remove`")

    ctx.run(f"{info.conda_cmd} " f"remove --name {info.env_name} --all -y")


@task
def activate(ctx: Context) -> None:
    """Activate Conda develop environment."""
    info = _get_conda_info()
    if info is None:
        raise RuntimeError("Please run `create` before `activate`")

    if not info.activate_cmd:
        print(
            "Activate command not found automatically. "
            f"Please try: conda activate {info.env_name}"
        )
        return

    if sys.platform == "win32":
        os.system(
            f'start "Conda Activate" cmd /s /k "{info.activate_cmd}" {info.env_name}'
        )
    else:
        print(f"To activate, run: source {info.activate_cmd} {info.env_name}")
