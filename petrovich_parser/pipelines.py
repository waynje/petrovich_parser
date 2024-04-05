from openpyxl import Workbook


class PetrovichParserPipeline:

    def open_spider(self, spider):
        self.wb = Workbook()
        self.sheet = self.wb.active
        self.sheet['A1'] = 'Название'
        self.sheet['B1'] = 'Количество'
        self.sheet['C1'] = 'Ссылка'
        self.current_row = 2

    def process_item(self, item, spider):
        self.sheet[f'A{self.current_row}'] = item['product']
        self.sheet[f'B{self.current_row}'] = item['amount']
        self.sheet[f'C{self.current_row}'] = item['link']
        self.current_row += 1
        return item

    def close_spider(self, spider):
        self.wb.save('output.xlsx')
