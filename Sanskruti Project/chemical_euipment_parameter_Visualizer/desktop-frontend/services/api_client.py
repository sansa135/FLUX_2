import requests
from typing import Dict, List, Optional

API_BASE_URL = 'http://localhost:8000/api'


class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def upload_dataset(self, file_path: str, name: Optional[str] = None) -> Dict:
        """Upload CSV file and return dataset info."""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'name': name} if name else {}
            resp = requests.post(f'{self.base_url}/upload/', files=files, data=data)
            resp.raise_for_status()
            return resp.json()

    def get_datasets(self) -> List[Dict]:
        """Get last 5 uploaded datasets."""
        resp = requests.get(f'{self.base_url}/datasets/')
        resp.raise_for_status()
        return resp.json()

    def get_latest_dataset(self) -> Dict:
        """Get most recently uploaded dataset."""
        resp = requests.get(f'{self.base_url}/datasets/latest/')
        resp.raise_for_status()
        return resp.json()

    def get_dataset_records(self, dataset_id: int, page: int = 1) -> Dict:
        """Get paginated equipment records for a dataset."""
        resp = requests.get(f'{self.base_url}/datasets/{dataset_id}/records/?page={page}')
        resp.raise_for_status()
        return resp.json()

    def get_dataset_summary(self, dataset_id: int) -> Dict:
        """Get summary stats for a dataset."""
        resp = requests.get(f'{self.base_url}/datasets/{dataset_id}/summary/')
        resp.raise_for_status()
        return resp.json()
