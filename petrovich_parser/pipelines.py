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
        data = [
            (item['name'], item['amount'], item['link'])
        ]

        for product, amount, link in data:
            self.sheet[f'A{self.current_row}'] = product
            self.sheet[f'B{self.current_row}'] = amount
            self.sheet[f'C{self.current_row}'] = link
            self.current_row += 1
            return item

    def close_spider(self, spider):
        self.wb.save('output.xlsx')
