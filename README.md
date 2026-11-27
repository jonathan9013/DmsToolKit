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
