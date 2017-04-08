from paths import *

def run():
    print_('Extractor will be ran.')
    os.system('""')
    os.system('"' + extractorExe + ' "' + joinPath(first_outputs, '07. Absolution.mp3') + '" "' + joinPath(first_outputs, '07. Absolution.json') + '"')