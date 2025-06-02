from PyQt5.QtWidgets import QTableWidgetItem
from data_viewer_Layout import DataViewerLayout
from PyQt5.QtCore import pyqtSignal, QThread
import pandas as pd
from util import checkFileFormat, show_message


class DataLoader(QThread):

    MainData = pyqtSignal(pd.DataFrame)

    def __init__(self, format, path):
        super().__init__()

        self.format = format
        self.path = path

        self.Main_data = None

        self.file_reader = {
            ".csv": lambda file_path: pd.read_csv(file_path),
            ".xlsx": lambda file_path: pd.read_excel(file_path),
            ".json": lambda file_path: pd.read_json(file_path)
        }

    def run(self):
        self.Main_data = self.file_reader[self.format](self.path)
        self.Main_data.dropna(axis=1, inplace=True)
        self.MainData.emit(self.Main_data)



class DataViewer(DataViewerLayout):

    dataSelected = pyqtSignal(bool)
    passData = pyqtSignal(pd.DataFrame)
    passColumns = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.Data = None # user Selected Data
        self.sample_data = None # sliced sample of selected data
        self.chunck = None # Chunck number


        self.table_place_holder.DropSignal.connect(self.HandleDrop)
        self.backward_btn.clicked.connect(self.prev_btn)
        self.forward_btn.clicked.connect(self.next_btn)
        


    def HandleDrop(self, path):
        format = checkFileFormat(path)
        self.chunck = 0
       

        if format in [".csv", ".xlsx"]:

            if hasattr(self, "Data_Loader"):
                self.Data_Loader.quit()
                self.Data_Loader.wait()
            
            self.data_loading_screen.screen.start()
            self.table_stack.setCurrentIndex(2)

            self.Data_Loader = DataLoader(format, path)
            self.Data_Loader.MainData.connect(self.capture_data)
            self.Data_Loader.start()
        else:
            show_message(self, "Invalid file format...")
            self.dataSelected.emit(False)
            return


    
    def displaySample(self):

        for i in range(self.sample_data.shape[0]):
            for j in range(self.sample_data.shape[1]):
                item = QTableWidgetItem(str(self.sample_data.iat[i,j]))

                self.table.setItem(i,j,item)


    def getChunck(self, size, current_Chunck):
        if len(self.Data) <= 200:
            return self.Data

        start = current_Chunck * size
        end = start + size

        if start >= len(self.Data):
            return self.sample_data

        if start < len(self.Data):
            row_lable = [str(i) for i in range(start+1, end + 2)]
            self.table.setVerticalHeaderLabels(row_lable)
        
        return self.Data.iloc[start:end]
        
        
    def updateColumnsItem(self, columns):

        columns_ref = {"numeric":[], "char":[]}
        
        for column in columns:
            if pd.api.types.is_numeric_dtype(self.Data[column]):
                self.numeric_column_list.addItem(column)
                columns_ref["numeric"].append(column)
            else:
                self.categorical_columns_list.addItem(column)
                columns_ref["char"].append(column)

        self.info.setText(f"Rows:- {self.Data.shape[0]} | Columns:- {self.Data.shape[1]} | Numeric datatype:- {self.numeric_column_list.count()} | Categorical datatype:- {self.categorical_columns_list.count()}")
        self.passColumns.emit(columns_ref)


    def prev_btn(self):
        if self.Data is not None and len(self.Data) > 200:
            if self.chunck > 0:
                self.chunck -= 1
                self.sample_data = self.getChunck(100, self.chunck)
                self.displaySample()

    def next_btn(self):
        if self.Data is not None:
            total_rows = len(self.Data)
            max_chunks = (total_rows // 100) + (1 if total_rows % 100 else 0)

            if self.chunck + 1 >= max_chunks:
                return

            self.chunck += 1
            self.sample_data = self.getChunck(100, self.chunck)
            self.displaySample()

    
    def capture_data(self, data):
        self.Data = data

        if len(self.Data) <= 200:
            self.table.setRowCount(len(self.Data))
            row_lable = [str(i) for i in range(1, len(self.Data) + 1)]
            self.table.setVerticalHeaderLabels(row_lable)
        else:
            self.table.setRowCount(100)

        self.table.setColumnCount(self.Data.shape[1])
        self.table.setHorizontalHeaderLabels(self.Data.columns)

        self.sample_data = self.getChunck(100,self.chunck)
        self.displaySample()

        self.data_loading_screen.screen.stop()
        self.table_stack.setCurrentIndex(1)
        self.numeric_column_list.clear()
        self.categorical_columns_list.clear()

        self.dataSelected.emit(True)
        self.passData.emit(self.Data)

        self.updateColumnsItem(self.Data.columns)



