# DmsToolKit

Generate a dungeon map and save it as an Excel workbook in your Downloads folder.

Open the settings form with:

```text
dmstoolkit --gui
```

The form lets you set the target size, hall/room chances, and chances for each room size. Click **Generate dungeon** to create the workbook. Tkinter is part of Python's standard library and does not need a separate `pip` install.

Run `dmstoolkit` with no options to use the defaults: 500 occupied cells, a 70% hall / 30% room split, and room-size chances of 20% for size 9, 60% for size 7, and 20% for size 5.

The generation settings can be adjusted when launching the command:

```text
dmstoolkit --target-size 300 --hall-percentage 60 --room-percentage 40 --room-9-percentage 10 --room-7-percentage 50 --room-5-percentage 40
```

The hall and room percentages must add up to 100, as must the three room-size percentages. `--target-size` must be a positive number of occupied cells.

## Windows executable

To download a standalone Windows executable, open the repository's [Releases page](https://github.com/jonathan9013/DmsToolKit/releases) and download `DmsToolKit.exe` from a release. The executable opens the settings form and does not require Python to be installed.

To build it locally from a clone, install [uv](https://docs.astral.sh/uv/), then run:

```powershell
uv sync --locked
uv run pyinstaller --noconfirm --clean --onefile --windowed --name DmsToolKit --paths src src\dmstoolkit\__main__.py
```

The executable is written to `dist\DmsToolKit.exe`. Publishing a GitHub Release builds the Windows executable automatically and attaches it to that release. Running the build workflow manually makes the executable available as a workflow artifact.
