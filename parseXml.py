import xml.sax
class BiosHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
            self.inTitle = False
    def startElement(self,name, attributes):
            if name == 'HELP_STRING':
                self.inTitle = True
    def characters(self, data):
            if self.inTitle:
                print(data)
    def endElement(self, name):
            if name == 'HELP_STRING':
                self.inTitle = False
                

parser=xml.sax.make_parser()
handler=BiosHandler()
parser.setContentHandler(handler)
parser.parse('biossettings.xml')