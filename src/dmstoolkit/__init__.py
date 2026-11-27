import argparse

from dmstoolkit import dungeon_generator as dg


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a dungeon map.")
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open the settings form instead of generating from the command line.",
    )
    parser.add_argument(
        "--target-size",
        type=int,
        default=500,
        help="Stop after at least this many occupied cells (default: %(default)s).",
    )
    parser.add_argument(
        "--hall-percentage",
        type=int,
        default=70,
        help="Percentage chance of generating a hall (default: %(default)s).",
    )
    parser.add_argument(
        "--room-percentage",
        type=int,
        default=30,
        help="Percentage chance of generating a room (default: %(default)s).",
    )
    parser.add_argument(
        "--room-9-percentage",
        type=int,
        default=20,
        help="Percentage chance of a 9-cell room (default: %(default)s).",
    )
    parser.add_argument(
        "--room-7-percentage",
        type=int,
        default=60,
        help="Percentage chance of a 7-cell room (default: %(default)s).",
    )
    parser.add_argument(
        "--room-5-percentage",
        type=int,
        default=20,
        help="Percentage chance of a 5-cell room (default: %(default)s).",
    )
    args = parser.parse_args()

    if args.gui:
        from dmstoolkit.gui import launch_gui

        launch_gui()
        return

    try:
        dg.generate_dungeon(
            target_size=args.target_size,
            hall_percentage=args.hall_percentage,
            room_percentage=args.room_percentage,
            room_9_percentage=args.room_9_percentage,
            room_7_percentage=args.room_7_percentage,
            room_5_percentage=args.room_5_percentage,
        )
    except ValueError as error:
        parser.error(str(error))
