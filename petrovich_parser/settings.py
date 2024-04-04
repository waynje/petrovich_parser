from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
RESULTS = 'results'

BOT_NAME = 'petrovich_parser'


NEWSPIDER_MODULE = 'petrovich_parser.spiders'
SPIDER_MODULES = [NEWSPIDER_MODULE]
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'petrovich_parser.pipelines.PetrovichParserPipeline': 300,
}
