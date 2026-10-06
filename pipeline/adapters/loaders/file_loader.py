from pipeline.ports.loader import LoaderPort
import pandas as pd
from pathlib import Path
class FileLoader(LoaderPort):
    """
    Adapter for saving a DataFrame to CSV file.
    """

    def __init__(self,output_path:Path)->None:
        """
        Initialize the FileLoader.

        Args:
            output_path: the file path to save the DataFrame.
        """
        self.output_path = output_path

    def load(self,df:pd.DataFrame) -> None:
        """
        Creates the target directory if needed and saves the DataFrame.

        Args:
            df:DataFrame to save.
        """
        # Ensure the target directory exists (e.g. `reports/`).
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(self.output_path,index=False)