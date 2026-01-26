import sys
from io import BytesIO

import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.api_client import APIClient


class DataFetchWorker(QThread):
    """Background thread for API calls."""
    
    data_loaded = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, method, *args):
        super().__init__()
        self.method = method
        self.args = args

    def run(self):
        try:
            result = self.method(*self.args)
            self.data_loaded.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_dataset = None
        self.current_page = 1

        self.setWindowTitle('Chemical Equipment Parameter Visualizer')
        self.setGeometry(100, 100, 1200, 800)

        self._init_ui()
        self._load_datasets()

    def _init_ui(self):
        """Initialize UI components."""
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Top control panel
        control_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton('Upload CSV')
        self.upload_btn.clicked.connect(self._on_upload_clicked)
        control_layout.addWidget(self.upload_btn)

        self.dataset_label = QLabel('No dataset loaded')
        control_layout.addWidget(self.dataset_label, 1)

        main_layout.addLayout(control_layout)

        # Tab widget for views
        self.tabs = QTabWidget()
        
        # Records tab
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(5)
        self.records_table.setHorizontalHeaderLabels(
            ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        )
        self.records_table.resizeColumnsToContents()
        
        records_layout = QVBoxLayout()
        records_layout.addWidget(self.records_table)
        
        # Pagination buttons
        pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton('Previous')
        self.prev_btn.clicked.connect(self._on_prev_page)
        self.page_label = QLabel('Page 1')
        self.next_btn = QPushButton('Next')
        self.next_btn.clicked.connect(self._on_next_page)
        
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label, 1)
        pagination_layout.addWidget(self.next_btn)
        records_layout.addLayout(pagination_layout)
        
        records_widget = QWidget()
        records_widget.setLayout(records_layout)
        self.tabs.addTab(records_widget, 'Records')

        # Charts tab
        self.chart_label = QLabel('Load a dataset to view charts')
        self.chart_label.setAlignment(Qt.AlignCenter)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.chart_label)
        scroll_area.setWidgetResizable(True)
        self.tabs.addTab(scroll_area, 'Charts')

        # Summary tab
        self.summary_label = QLabel('Load a dataset to view summary')
        self.summary_label.setAlignment(Qt.AlignCenter)
        
        scroll_area2 = QScrollArea()
        scroll_area2.setWidget(self.summary_label)
        scroll_area2.setWidgetResizable(True)
        self.tabs.addTab(scroll_area2, 'Summary')

        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _load_datasets(self):
        """Load available datasets in background."""
        self.worker = DataFetchWorker(self.api_client.get_datasets)
        self.worker.data_loaded.connect(self._on_datasets_loaded)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def _on_datasets_loaded(self, datasets):
        """Handle loaded datasets."""
        if datasets:
            self.current_dataset = datasets[0]
            self._load_dataset_data(self.current_dataset)
        else:
            self.dataset_label.setText('No datasets found')

    def _load_dataset_data(self, dataset):
        """Load records, charts, and summary for a dataset."""
        self.current_dataset = dataset
        self.current_page = 1
        self.dataset_label.setText(f"Dataset: {dataset['name']} ({dataset['row_count']} rows)")

        # Load records
        self.worker = DataFetchWorker(self.api_client.get_dataset_records, dataset['id'], 1)
        self.worker.data_loaded.connect(self._on_records_loaded)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

        # Load summary and render charts
        self.worker = DataFetchWorker(self.api_client.get_dataset_summary, dataset['id'])
        self.worker.data_loaded.connect(self._on_summary_loaded)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def _on_records_loaded(self, data):
        """Populate records table."""
        records = data.get('results', [])
        self.records_table.setRowCount(len(records))

        for row, record in enumerate(records):
            self.records_table.setItem(row, 0, QTableWidgetItem(record.get('equipment_name', '')))
            self.records_table.setItem(row, 1, QTableWidgetItem(record.get('equipment_type', '')))
            self.records_table.setItem(row, 2, QTableWidgetItem(f"{record.get('flowrate', 'N/A')}"))
            self.records_table.setItem(row, 3, QTableWidgetItem(f"{record.get('pressure', 'N/A')}"))
            self.records_table.setItem(row, 4, QTableWidgetItem(f"{record.get('temperature', 'N/A')}"))

        self.page_label.setText(f"Page {self.current_page}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(data.get('next') is not None)

    def _on_summary_loaded(self, data):
        """Display summary and render charts."""
        summary = data.get('summary', {})
        dataset = data.get('dataset', {})

        # Update summary tab
        summary_text = f"""
        Dataset: {dataset.get('name', 'N/A')}
        Total Records: {dataset.get('row_count', 0)}
        
        Flowrate (min/max/mean/median):
        {summary.get('flowrate', {}).get('min', 'N/A')} / {summary.get('flowrate', {}).get('max', 'N/A')} / {summary.get('flowrate', {}).get('mean', 'N/A')} / {summary.get('flowrate', {}).get('median', 'N/A')}
        
        Pressure (min/max/mean/median):
        {summary.get('pressure', {}).get('min', 'N/A')} / {summary.get('pressure', {}).get('max', 'N/A')} / {summary.get('pressure', {}).get('mean', 'N/A')} / {summary.get('pressure', {}).get('median', 'N/A')}
        
        Temperature (min/max/mean/median):
        {summary.get('temperature', {}).get('min', 'N/A')} / {summary.get('temperature', {}).get('max', 'N/A')} / {summary.get('temperature', {}).get('mean', 'N/A')} / {summary.get('temperature', {}).get('median', 'N/A')}
        
        Equipment Types:
        """
        for type_name, count in summary.get('type_distribution', {}).items():
            summary_text += f"\n  {type_name}: {count}"

        self.summary_label.setText(summary_text)

        # Render charts
        self._render_charts(summary)

    def _render_charts(self, summary):
        """Render matplotlib charts and display in UI."""
        fig, axes = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle('Equipment Parameter Analysis', fontsize=14)

        # Flowrate chart
        flowrate = summary.get('flowrate', {})
        axes[0, 0].bar(
            ['Min', 'Max', 'Mean', 'Median'],
            [flowrate.get(k) for k in ['min', 'max', 'mean', 'median']],
            color='skyblue'
        )
        axes[0, 0].set_title('Flowrate Statistics')
        axes[0, 0].set_ylabel('Value')

        # Pressure chart
        pressure = summary.get('pressure', {})
        axes[0, 1].bar(
            ['Min', 'Max', 'Mean', 'Median'],
            [pressure.get(k) for k in ['min', 'max', 'mean', 'median']],
            color='lightcoral'
        )
        axes[0, 1].set_title('Pressure Statistics')
        axes[0, 1].set_ylabel('Value')

        # Temperature chart
        temperature = summary.get('temperature', {})
        axes[1, 0].bar(
            ['Min', 'Max', 'Mean', 'Median'],
            [temperature.get(k) for k in ['min', 'max', 'mean', 'median']],
            color='lightgreen'
        )
        axes[1, 0].set_title('Temperature Statistics')
        axes[1, 0].set_ylabel('Value')

        # Equipment type distribution
        type_dist = summary.get('type_distribution', {})
        if type_dist:
            axes[1, 1].barh(list(type_dist.keys()), list(type_dist.values()), color='gold')
            axes[1, 1].set_title('Equipment Type Distribution')
            axes[1, 1].set_xlabel('Count')

        plt.tight_layout()

        # Convert matplotlib figure to QPixmap
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        # Display in chart tab
        chart_label = QLabel()
        chart_label.setPixmap(pixmap.scaledToWidth(900, Qt.SmoothTransformation))
        chart_label.setAlignment(Qt.AlignCenter)

        scroll_area = self.tabs.widget(1)
        scroll_area.setWidget(chart_label)

        plt.close(fig)

    def _on_upload_clicked(self):
        """Handle CSV upload."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv);;All Files (*)'
        )
        if file_path:
            self.upload_btn.setEnabled(False)
            self.upload_btn.setText('Uploading...')

            self.worker = DataFetchWorker(self.api_client.upload_dataset, file_path)
            self.worker.data_loaded.connect(self._on_upload_success)
            self.worker.error_occurred.connect(self._on_upload_error)
            self.worker.start()

    def _on_upload_success(self, dataset):
        """Handle successful upload."""
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText('Upload CSV')
        QMessageBox.information(self, 'Success', f"Uploaded: {dataset['name']}")
        self._load_datasets()

    def _on_upload_error(self, error):
        """Handle upload error."""
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText('Upload CSV')
        QMessageBox.critical(self, 'Upload Error', str(error))

    def _on_prev_page(self):
        """Load previous page of records."""
        if self.current_page > 1:
            self.current_page -= 1
            self.worker = DataFetchWorker(
                self.api_client.get_dataset_records,
                self.current_dataset['id'],
                self.current_page
            )
            self.worker.data_loaded.connect(self._on_records_loaded)
            self.worker.error_occurred.connect(self._on_error)
            self.worker.start()

    def _on_next_page(self):
        """Load next page of records."""
        self.current_page += 1
        self.worker = DataFetchWorker(
            self.api_client.get_dataset_records,
            self.current_dataset['id'],
            self.current_page
        )
        self.worker.data_loaded.connect(self._on_records_loaded)
        self.worker.error_occurred.connect(self._on_error)
        self.worker.start()

    def _on_error(self, error):
        """Handle API errors."""
        QMessageBox.critical(self, 'Error', f"API Error: {error}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
