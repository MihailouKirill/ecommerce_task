import argparse
import io
import json
import os
import random
import zipfile
from datetime import date, datetime, timedelta
from typing import Any


class EventDataGenerator:
    """
    Generates nested zip archives of mock e-commerce event data.

    The structure is:
    - Master Zip (per week)
      - Daily Zip
        - Part-JSON-files
          - [List of event objects]
    """

    CUSTOMER_IDS: list[str] = [f"c{i:03d}" for i in range(1, 101)]
    PRODUCT_IDS: list[str] = [f"p{i:03d}" for i in range(1, 51)]
    EVENT_TYPES: list[str] = ["view_product", "add_to_cart", "purchase"]
    EVENT_WEIGHTS: list[float] = [0.70, 0.25, 0.05]

    def __init__(
        self,
        start_date: date,
        output_dir: str = "data",
        days_per_week: int = 7,
        parts_per_day: int = 5,
        events_per_part: int = 100,
    ) -> None:
        """
        Initializes the data generator.

        :param start_date: The start date for the first week.
        :type start_date: datetime.date
        :param output_dir: The directory to save the master zip files.
        :type output_dir: str
        :param days_per_week: Number of daily zips per master zip.
        :type days_per_week: int
        :param parts_per_day: Number of JSON parts per daily zip.
        :type parts_per_day: int
        :param events_per_part: Number of events per JSON part file.
        :type events_per_part: int
        """
        self.start_date: date = start_date
        self.output_dir: str = output_dir
        self.days_per_week: int = days_per_week
        self.parts_per_day: int = parts_per_day
        self.events_per_part: int = events_per_part

        os.makedirs(self.output_dir, exist_ok=True)

    def _create_random_event(self, current_time: datetime) -> dict[str, Any]:
        """
        Generates a single random event dictionary.

        :param current_time: The timestamp for the event.
        :type current_time: datetime.datetime
        :return: A dictionary representing a single event.
        :rtype: Dict[str, Any]
        """
        event_type: str = random.choices(
            self.EVENT_TYPES, weights=self.EVENT_WEIGHTS, k=1
        )[0]

        event: dict[str, Any] = {
            "timestamp": current_time.isoformat(),
            "customer_id": random.choice(self.CUSTOMER_IDS),
            "event_type": event_type,
            "product_id": random.choice(self.PRODUCT_IDS),
        }

        if event_type == "purchase":
            event["quantity"] = random.randint(1, 3)

        return event

    def _generate_day_data(self, date_val: date) -> bytes:
        """
        Generates all event data for a single day and returns it as the
        in-memory bytes of a daily zip file.

        :param date_val: The specific date to generate data for.
        :type date_val: datetime.date
        :return: The binary content of the in-memory daily zip file.
        :rtype: bytes
        """
        print(f"    Generating data for {date_val}...")

        daily_zip_buffer: io.BytesIO = io.BytesIO()

        with zipfile.ZipFile(
            daily_zip_buffer, "w", compression=zipfile.ZIP_DEFLATED
        ) as daily_zip:
            current_time: datetime = datetime.combine(date_val, datetime.min.time())

            for i in range(self.parts_per_day):
                part_name: str = f"part-{i + 1:03d}.json"
                events_list: list[dict[str, Any]] = []

                for _ in range(self.events_per_part):
                    current_time += timedelta(seconds=random.randint(1, 60))
                    event = self._create_random_event(current_time)
                    events_list.append(event)

                json_data: str = json.dumps(events_list, indent=2)
                daily_zip.writestr(part_name, json_data)

        return daily_zip_buffer.getvalue()

    def _generate_week_zip(self, week_start_date: date) -> None:
        """
        Generates one complete master zip file for a given week.

        :param week_start_date: The start date of the week to generate.
        :type week_start_date: datetime.date
        """
        week_number: int = week_start_date.isocalendar()[1]
        master_zip_name: str = f"events_week_{week_number}.zip"
        master_zip_path: str = os.path.join(self.output_dir, master_zip_name)

        print(f"\nGenerating master zip: '{master_zip_name}'...")

        with zipfile.ZipFile(
            master_zip_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as master_zip:
            for i in range(self.days_per_week):
                current_date: date = week_start_date + timedelta(days=i)
                daily_zip_name: str = f"events_{current_date}.zip"

                daily_zip_bytes: bytes = self._generate_day_data(current_date)

                master_zip.writestr(daily_zip_name, daily_zip_bytes)

        print(f"Successfully generated {master_zip_path}")
        print(f"Total size: {os.path.getsize(master_zip_path) / 1024:.2f} KB")

    def run(self, num_weeks: int) -> None:
        """
        The main public method to run the data generation.

        :param num_weeks: The total number of master (weekly) zips to create.
        :type num_weeks: int
        """
        print("=" * 40)
        print(f"Starting data generation for {num_weeks} week(s)...")
        print(f"Output directory: {self.output_dir}")
        print("=" * 40)

        for i in range(num_weeks):
            current_week_start: date = self.start_date + timedelta(weeks=i)
            self._generate_week_zip(current_week_start)

        print("\n" + "=" * 40)
        print("All data generation complete.")
        print("=" * 40)


def main() -> None:
    """
    Main entry point for the script.
    Parses command-line arguments and runs the generator.
    """
    parser = argparse.ArgumentParser(
        description="Generate mock e-commerce event data in nested zip archives.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        required=True,
        help="The number of weeks (master zip files) to generate.",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="data",
        help="The directory to save the generated zip files (default: 'data').",
    )

    parser.add_argument(
        "-s",
        "--start-date",
        type=str,
        default="2023-10-23",
        help="The start date for the first week in YYYY-MM-DD format (default: '2023-10-23').",
    )

    args = parser.parse_args()

    try:
        start_date: date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    generator: EventDataGenerator = EventDataGenerator(
        start_date=start_date, output_dir=args.output_dir
    )
    generator.run(num_weeks=args.count)


if __name__ == "__main__":
    main()
